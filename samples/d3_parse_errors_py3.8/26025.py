# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\package_index.py
"""PyPI and direct package downloading"""
import sys, os, re, shutil, socket, base64, hashlib, itertools, warnings
from functools import wraps
from setuptools.extern import six
from setuptools.extern.six.moves import urllib, http_client, configparser, map
import setuptools
from pkg_resources import CHECKOUT_DIST, Distribution, BINARY_DIST, normalize_path, SOURCE_DIST, Environment, find_distributions, safe_name, safe_version, to_filename, Requirement, DEVELOP_DIST, EGG_DIST
from setuptools import ssl_support
from distutils import log
from distutils.errors import DistutilsError
from fnmatch import translate
from setuptools.py27compat import get_all_headers
from setuptools.py33compat import unescape
from setuptools.wheel import Wheel
__metaclass__ = type
EGG_FRAGMENT = re.compile('^egg=([-A-Za-z0-9_.+!]+)$')
HREF = re.compile('href\\s*=\\s*[\'"]?([^\'"> ]+)', re.I)
PYPI_MD5 = re.compile('<a href="([^"#]+)">([^<]+)</a>\\n\\s+\\(<a (?:title="MD5 hash"\\n\\s+)href="[^?]+\\?:action=show_md5&amp;digest=([0-9a-f]{32})">md5</a>\\)')
URL_SCHEME = re.compile('([-+.a-z0-9]{2,}):', re.I).match
EXTENSIONS = '.tar.gz .tar.bz2 .tar .zip .tgz'.split()
__all__ = [
 'PackageIndex', 'distros_for_url', 'parse_bdist_wininst',
 'interpret_distro_name']
_SOCKET_TIMEOUT = 15
_tmpl = 'setuptools/{setuptools.__version__} Python-urllib/{py_major}'
user_agent = _tmpl.format(py_major=('{}.{}'.format)(*sys.version_info),
  setuptools=setuptools)

def parse_requirement_arg(spec):
    try:
        return Requirement.parse(spec)
    except ValueError:
        raise DistutilsError('Not a URL, existing file, or requirement spec: %r' % (spec,))


def parse_bdist_wininst(name):
    """Return (base,pyversion) or (None,None) for possible .exe name"""
    lower = name.lower()
    base, py_ver, plat = (None, None, None)
    if lower.endswith('.exe'):
        if lower.endswith('.win32.exe'):
            base = name[:-10]
            plat = 'win32'
        elif lower.startswith('.win32-py', -16):
            py_ver = name[-7:-4]
            base = name[:-16]
            plat = 'win32'
        elif lower.endswith('.win-amd64.exe'):
            base = name[:-14]
            plat = 'win-amd64'
        elif lower.startswith('.win-amd64-py', -20):
            py_ver = name[-7:-4]
            base = name[:-20]
            plat = 'win-amd64'
    return (
     base, py_ver, plat)


def egg_info_for_url(url):
    parts = urllib.parse.urlparse(url)
    scheme, server, path, parameters, query, fragment = parts
    base = urllib.parse.unquote(path.split('/')[(-1)])
    if server == 'sourceforge.net':
        if base == 'download':
            base = urllib.parse.unquote(path.split('/')[(-2)])
    if '#' in base:
        base, fragment = base.split('#', 1)
    return (base, fragment)


def distros_for_url(url, metadata=None):
    """Yield egg or source distribution objects that might be found at a URL"""
    base, fragment = egg_info_for_url(url)
    for dist in distros_for_location(url, base, metadata):
        yield dist
    else:
        if fragment:
            match = EGG_FRAGMENT.match(fragment)
            if match:
                for dist in interpret_distro_name(url,
                  (match.group(1)), metadata, precedence=CHECKOUT_DIST):
                    yield dist


def distros_for_location(location, basename, metadata=None):
    """Yield egg or source distribution objects based on basename"""
    if basename.endswith('.egg.zip'):
        basename = basename[:-4]
    if basename.endswith('.egg'):
        if '-' in basename:
            return [
             Distribution.from_location(location, basename, metadata)]
    if basename.endswith('.whl'):
        if '-' in basename:
            wheel = Wheel(basename)
            if not wheel.is_compatible():
                return []
            return [
             Distribution(location=location,
               project_name=(wheel.project_name),
               version=(wheel.version),
               precedence=(EGG_DIST + 1))]
    if basename.endswith('.exe'):
        win_base, py_ver, platform = parse_bdist_wininst(basename)
        if win_base is not None:
            return interpret_distro_name(location, win_base, metadata, py_ver, BINARY_DIST, platform)
    for ext in EXTENSIONS:
        if basename.endswith(ext):
            basename = basename[:-len(ext)]
            return interpret_distro_name(location, basename, metadata)
    else:
        return []


def distros_for_filename(filename, metadata=None):
    """Yield possible egg or source distribution objects based on a filename"""
    return distros_for_location(normalize_path(filename), os.path.basename(filename), metadata)


def interpret_distro_name(location, basename, metadata, py_version=None, precedence=SOURCE_DIST, platform=None):
    """Generate alternative interpretations of a source distro name

    Note: if `location` is a filesystem filename, you should call
    ``pkg_resources.normalize_path()`` on it before passing it to this
    routine!
    """
    parts = basename.split('-')
    if not py_version:
        if any((re.match('py\\d\\.\\d$', p) for p in parts[2:])):
            return
    for p in range(1, len(parts) + 1):
        yield Distribution(location,
          metadata, ('-'.join(parts[:p])), ('-'.join(parts[p:])), py_version=py_version,
          precedence=precedence,
          platform=platform)


def unique_everseen(iterable, key=None):
    """List unique elements, preserving order. Remember all elements ever seen."""
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in six.moves.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element

    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def unique_values(func):
    """
    Wrap a function returning an iterable such that the resulting iterable
    only ever yields unique items.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return unique_everseen(func(*args, **kwargs))

    return wrapper


REL = re.compile('<([^>]*\\srel\\s*=\\s*[\'"]?([^\'">]+)[^>]*)>', re.I)

@unique_values
def find_external_links(url, page):
    """Find rel="homepage" and rel="download" links in `page`, yielding URLs"""
    for match in REL.finditer(page):
        tag, rel = match.groups()
        rels = set(map(str.strip, rel.lower().split(',')))
        if not 'homepage' in rels:
            if 'download' in rels:
                for match in HREF.finditer(tag):
                    yield urllib.parse.urljoin(url, htmldecode(match.group(1)))

    else:
        for tag in ('<th>Home Page', '<th>Download URL'):
            pos = page.find(tag)
            if pos != -1:
                match = HREF.search(page, pos)
                if match:
                    yield urllib.parse.urljoin(url, htmldecode(match.group(1)))


class ContentChecker:
    __doc__ = '\n    A null content checker that defines the interface for checking content\n    '

    def feed(self, block):
        """
        Feed a block of data to the hash.
        """
        pass

    def is_valid(self):
        """
        Check the hash. Return False if validation fails.
        """
        return True

    def report(self, reporter, template):
        """
        Call reporter with information about the checker (hash name)
        substituted into the template.
        """
        pass


class HashChecker(ContentChecker):
    pattern = re.compile('(?P<hash_name>sha1|sha224|sha384|sha256|sha512|md5)=(?P<expected>[a-f0-9]+)')

    def __init__(self, hash_name, expected):
        self.hash_name = hash_name
        self.hash = hashlib.new(hash_name)
        self.expected = expected

    @classmethod
    def from_url(cls, url):
        """Construct a (possibly null) ContentChecker from a URL"""
        fragment = urllib.parse.urlparse(url)[(-1)]
        if not fragment:
            return ContentChecker()
        match = cls.pattern.search(fragment)
        if not match:
            return ContentChecker()
        return cls(**match.groupdict())

    def feed(self, block):
        self.hash.update(block)

    def is_valid(self):
        return self.hash.hexdigest() == self.expected

    def report(self, reporter, template):
        msg = template % self.hash_name
        return reporter(msg)


class PackageIndex(Environment):
    __doc__ = 'A distribution index that scans web pages for download URLs'

    def __init__(self, index_url='https://pypi.org/simple/', hosts=('*',), ca_bundle=None, verify_ssl=True, *args, **kw):
        (Environment.__init__)(self, *args, **kw)
        self.index_url = index_url + '/'[:not index_url.endswith('/')]
        self.scanned_urls = {}
        self.fetched_urls = {}
        self.package_pages = {}
        self.allows = re.compile('|'.join(map(translate, hosts))).match
        self.to_scan = []
        use_ssl = verify_ssl and ((ssl_support.is_available and ca_bundle) or (ssl_support.find_ca_bundle()))
        if use_ssl:
            self.opener = ssl_support.opener_for(ca_bundle)
        else:
            self.opener = urllib.request.urlopen

    def process_url(self, url, retrieve=False):
        """Evaluate a URL as a possible download, and maybe retrieve it"""
        if url in self.scanned_urls:
            if not retrieve:
                return
            self.scanned_urls[url] = True
            if not URL_SCHEME(url):
                self.process_filename(url)
                return
            dists = list(distros_for_url(url))
            if dists:
                if not self.url_ok(url):
                    return
                self.debug('Found link: %s', url)
            if dists or (retrieve and url in self.fetched_urls):
                list(map(self.add, dists))
                return
            if not self.url_ok(url):
                self.fetched_urls[url] = True
                return
            self.info('Reading %s', url)
            self.fetched_urls[url] = True
            tmpl = 'Download error on %s: %%s -- Some packages may not be found!'
            f = self.open_url(url, tmpl % url)
            if f is None:
                return
            if isinstance(f, urllib.error.HTTPError):
                if f.code == 401:
                    self.info('Authentication error: %s' % f.msg)
            self.fetched_urls[f.url] = True
            if 'html' not in f.headers.get('content-type', '').lower():
                f.close()
                return
            base = f.url
            page = f.read()
            if not isinstance(page, str):
                if isinstance(f, urllib.error.HTTPError):
                    charset = 'latin-1'
                else:
                    charset = f.headers.get_param('charset') or 'latin-1'
                page = page.decode(charset, 'ignore')
            f.close()
            for match in HREF.finditer(page):
                link = urllib.parse.urljoin(base, htmldecode(match.group(1)))
                self.process_url(link)
            else:
                if url.startswith(self.index_url):
                    if getattr(f, 'code', None) != 404:
                        page = self.process_index(url, page)

    def process_filename(self, fn, nested=False):
        if not os.path.exists(fn):
            self.warn('Not found: %s', fn)
            return
        if os.path.isdir(fn):
            path = (nested or os.path.realpath)(fn)
            for item in os.listdir(path):
                self.process_filename(os.path.join(path, item), True)
            else:
                dists = distros_for_filename(fn)
                if dists:
                    self.debug('Found: %s', fn)
                    list(map(self.add, dists))

    def url_ok(self, url, fatal=False):
        s = URL_SCHEME(url)
        is_file = s and s.group(1).lower() == 'file'
        if is_file or (self.allows(urllib.parse.urlparse(url)[1])):
            return True
        msg = '\nNote: Bypassing %s (disallowed host; see http://bit.ly/2hrImnY for details).\n'
        if fatal:
            raise DistutilsError(msg % url)
        else:
            self.warn(msg, url)

    def scan_egg_links(self, search_path):
        dirs = filter(os.path.isdir, search_path)
        egg_links = ((
         path, entry) for path in dirs for entry in os.listdir(path))
        list(itertools.starmap(self.scan_egg_link, egg_links))

    def scan_egg_link(self, path, entry):
        with open(os.path.join(path, entry)) as raw_lines:
            lines = list(filter(None, map(str.strip, raw_lines)))
        if len(lines) != 2:
            return
        egg_path, setup_path = lines
        for dist in find_distributions(os.path.join(path, egg_path)):
            dist.location = (os.path.join)(path, *lines)
            dist.precedence = SOURCE_DIST
            self.add(dist)

    def process_index(self, url, page):
        """Process the contents of a PyPI page"""

        def scan(link):
            if link.startswith(self.index_url):
                parts = list(map(urllib.parse.unquote, link[len(self.index_url):].split('/')))
                if len(parts) == 2:
                    if '#' not in parts[1]:
                        pkg = safe_name(parts[0])
                        ver = safe_version(parts[1])
                        self.package_pages.setdefault(pkg.lower(), {})[link] = True
                        return (
                         to_filename(pkg), to_filename(ver))
            return (None, None)

        for match in HREF.finditer(page):
            try:
                scan(urllib.parse.urljoin(url, htmldecode(match.group(1))))
            except ValueError:
                pass

        else:
            pkg, ver = scan(url)
            if pkg:
                for new_url in find_external_links(url, page):
                    base, frag = egg_info_for_url(new_url)
                    if base.endswith('.py') and not frag:
                        if ver:
                            new_url += '#egg=%s-%s' % (pkg, ver)
                    else:
                        self.need_version_info(url)
                    self.scan_url(new_url)
                else:
                    return PYPI_MD5.sub(lambda m: '<a href="%s#md5=%s">%s</a>' % m.group(1, 3, 2), page)

            return ''

    def need_version_info(self, url):
        self.scan_all('Page at %s links to .py file(s) without version info; an index scan is required.', url)

    def scan_all(self, msg=None, *args):
        if self.index_url not in self.fetched_urls:
            if msg:
                (self.warn)(msg, *args)
            self.info('Scanning index of all packages (this may take a while)')
        self.scan_url(self.index_url)

    def find_packages(self, requirement):
        self.scan_url(self.index_url + requirement.unsafe_name + '/')
        if not self.package_pages.get(requirement.key):
            self.scan_url(self.index_url + requirement.project_name + '/')
        if not self.package_pages.get(requirement.key):
            self.not_found_in_index(requirement)
        for url in list(self.package_pages.get(requirement.key, ())):
            self.scan_url(url)

    def obtain(self, requirement, installer=None):
        self.prescan()
        self.find_packages(requirement)
        for dist in self[requirement.key]:
            if dist in requirement:
                return dist
            else:
                self.debug('%s does not match %s', requirement, dist)
        else:
            return super(PackageIndex, self).obtain(requirement, installer)

    def check_hash(self, checker, filename, tfp):
        """
        checker is a ContentChecker
        """
        checker.report(self.debug, 'Validating %%s checksum for %s' % filename)
        if not checker.is_valid():
            tfp.close()
            os.unlink(filename)
            raise DistutilsError('%s validation failed for %s; possible download problem?' % (
             checker.hash.name, os.path.basename(filename)))

    def add_find_links(self, urls):
        """Add `urls` to the list that will be prescanned for searches"""
        for url in urls:
            if not self.to_scan is None or URL_SCHEME(url) or url.startswith('file:') or list(distros_for_url(url)):
                self.scan_url(url)
            else:
                self.to_scan.append(url)

    def prescan(self):
        """Scan urls scheduled for prescanning (e.g. --find-links)"""
        if self.to_scan:
            list(map(self.scan_url, self.to_scan))
        self.to_scan = None

    def not_found_in_index(self, requirement):
        if self[requirement.key]:
            meth, msg = self.info, "Couldn't retrieve index page for %r"
        else:
            meth, msg = self.warn, "Couldn't find index page for %r (maybe misspelled?)"
        meth(msg, requirement.unsafe_name)
        self.scan_all()

    def download(self, spec, tmpdir):
        """Locate and/or download `spec` to `tmpdir`, returning a local path

        `spec` may be a ``Requirement`` object, or a string containing a URL,
        an existing local filename, or a project/version requirement spec
        (i.e. the string form of a ``Requirement`` object).  If it is the URL
        of a .py file with an unambiguous ``#egg=name-version`` tag (i.e., one
        that escapes ``-`` as ``_`` throughout), a trivial ``setup.py`` is
        automatically created alongside the downloaded file.

        If `spec` is a ``Requirement`` object or a string containing a
        project/version requirement spec, this method returns the location of
        a matching distribution (possibly after downloading it to `tmpdir`).
        If `spec` is a locally existing file or directory name, it is simply
        returned unchanged.  If `spec` is a URL, it is downloaded to a subpath
        of `tmpdir`, and the local filename is returned.  Various errors may be
        raised if a problem occurs during downloading.
        """
        if not isinstance(spec, Requirement):
            scheme = URL_SCHEME(spec)
            if scheme:
                found = self._download_url(scheme.group(1), spec, tmpdir)
                base, fragment = egg_info_for_url(spec)
                if base.endswith('.py'):
                    found = self.gen_setup(found, fragment, tmpdir)
                return found
            if os.path.exists(spec):
                return spec
            spec = parse_requirement_arg(spec)
        return getattr(self.fetch_distribution(spec, tmpdir), 'location', None)

    def fetch_distribution(self, requirement, tmpdir, force_scan=False, source=False, develop_ok=False, local_index=None):
        """Obtain a distribution suitable for fulfilling `requirement`

        `requirement` must be a ``pkg_resources.Requirement`` instance.
        If necessary, or if the `force_scan` flag is set, the requirement is
        searched for in the (online) package index as well as the locally
        installed packages.  If a distribution matching `requirement` is found,
        the returned distribution's ``location`` is the value you would have
        gotten from calling the ``download()`` method with the matching
        distribution's URL or filename.  If no matching distribution is found,
        ``None`` is returned.

        If the `source` flag is set, only source distributions and source
        checkout links will be considered.  Unless the `develop_ok` flag is
        set, development and system eggs (i.e., those using the ``.egg-info``
        format) will be ignored.
        """
        self.info('Searching for %s', requirement)
        skipped = {}
        dist = None

        def find(req, env=None):
            if env is None:
                env = self
            for dist in env[req.key]:
                if dist.precedence == DEVELOP_DIST and not develop_ok:
                    if dist not in skipped:
                        self.warn('Skipping development or system egg: %s', dist)
                        skipped[dist] = 1
                else:
                    test = (dist in req) and ((dist.precedence <= SOURCE_DIST) or (not source))
                    if test:
                        loc = self.download(dist.location, tmpdir)
                        dist.download_location = loc
                        if os.path.exists(dist.download_location):
                            return dist

        if force_scan:
            self.prescan()
            self.find_packages(requirement)
            dist = find(requirement)
        if not dist:
            if local_index is not None:
                dist = find(requirement, local_index)
        if dist is None:
            if self.to_scan is not None:
                self.prescan()
            dist = find(requirement)
        if dist is None:
            if not force_scan:
                self.find_packages(requirement)
                dist = find(requirement)
        if dist is None:
            self.warn('No local packages or working download links found for %s%s', source and 'a source distribution of ' or '', requirement)
        else:
            self.info('Best match: %s', dist)
            return dist.clone(location=(dist.download_location))

    def fetch(self, requirement, tmpdir, force_scan=False, source=False):
        """Obtain a file suitable for fulfilling `requirement`

        DEPRECATED; use the ``fetch_distribution()`` method now instead.  For
        backward compatibility, this routine is identical but returns the
        ``location`` of the downloaded distribution instead of a distribution
        object.
        """
        dist = self.fetch_distribution(requirement, tmpdir, force_scan, source)
        if dist is not None:
            return dist.location

    def gen_setup(self, filename, fragment, tmpdir):
        match = EGG_FRAGMENT.match(fragment)
        dists = match and ([d for d in interpret_distro_name(filename, match.group(1), None) if d.version]) or ([])
        if len(dists) == 1:
            basename = os.path.basename(filename)
            if os.path.dirname(filename) != tmpdir:
                dst = os.path.join(tmpdir, basename)
                from setuptools.command.easy_install import samefile
                if not samefile(filename, dst):
                    shutil.copy2(filename, dst)
                    filename = dst
                with open(os.path.join(tmpdir, 'setup.py'), 'w') as file:
                    file.write('from setuptools import setup\nsetup(name=%r, version=%r, py_modules=[%r])\n' % (
                     dists[0].project_name, dists[0].version,
                     os.path.splitext(basename)[0]))
                return filename
        if match:
            raise DistutilsError("Can't unambiguously interpret project/version identifier %r; any dashes in the name or version should be escaped using underscores. %r" % (
             fragment, dists))
        else:
            raise DistutilsError("Can't process plain .py files without an '#egg=name-version' suffix to enable automatic setup script generation.")

    dl_blocksize = 8192

    def _download_to--- This code section failed: ---

 L. 727         0  LOAD_FAST                'self'
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Downloading %s'
                6  LOAD_FAST                'url'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 729        12  LOAD_CONST               None
               14  STORE_FAST               'fp'

 L. 730        16  SETUP_FINALLY       256  'to 256'

 L. 731        18  LOAD_GLOBAL              HashChecker
               20  LOAD_METHOD              from_url
               22  LOAD_FAST                'url'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'checker'

 L. 732        28  LOAD_FAST                'self'
               30  LOAD_METHOD              open_url
               32  LOAD_FAST                'url'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'fp'

 L. 733        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'fp'
               42  LOAD_GLOBAL              urllib
               44  LOAD_ATTR                error
               46  LOAD_ATTR                HTTPError
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE    74  'to 74'

 L. 734        52  LOAD_GLOBAL              DistutilsError

 L. 735        54  LOAD_STR                 "Can't download %s: %s %s"
               56  LOAD_FAST                'url'
               58  LOAD_FAST                'fp'
               60  LOAD_ATTR                code
               62  LOAD_FAST                'fp'
               64  LOAD_ATTR                msg
               66  BUILD_TUPLE_3         3 
               68  BINARY_MODULO    

 L. 734        70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            50  '50'

 L. 737        74  LOAD_FAST                'fp'
               76  LOAD_METHOD              info
               78  CALL_METHOD_0         0  ''
               80  STORE_FAST               'headers'

 L. 738        82  LOAD_CONST               0
               84  STORE_FAST               'blocknum'

 L. 739        86  LOAD_FAST                'self'
               88  LOAD_ATTR                dl_blocksize
               90  STORE_FAST               'bs'

 L. 740        92  LOAD_CONST               -1
               94  STORE_FAST               'size'

 L. 741        96  LOAD_STR                 'content-length'
               98  LOAD_FAST                'headers'
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   146  'to 146'

 L. 743       104  LOAD_GLOBAL              get_all_headers
              106  LOAD_FAST                'headers'
              108  LOAD_STR                 'Content-Length'
              110  CALL_FUNCTION_2       2  ''
              112  STORE_FAST               'sizes'

 L. 744       114  LOAD_GLOBAL              max
              116  LOAD_GLOBAL              map
              118  LOAD_GLOBAL              int
              120  LOAD_FAST                'sizes'
              122  CALL_FUNCTION_2       2  ''
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'size'

 L. 745       128  LOAD_FAST                'self'
              130  LOAD_METHOD              reporthook
              132  LOAD_FAST                'url'
              134  LOAD_FAST                'filename'
              136  LOAD_FAST                'blocknum'
              138  LOAD_FAST                'bs'
              140  LOAD_FAST                'size'
              142  CALL_METHOD_5         5  ''
              144  POP_TOP          
            146_0  COME_FROM           102  '102'

 L. 746       146  LOAD_GLOBAL              open
              148  LOAD_FAST                'filename'
              150  LOAD_STR                 'wb'
              152  CALL_FUNCTION_2       2  ''
              154  SETUP_WITH          242  'to 242'
              156  STORE_FAST               'tfp'
            158_0  COME_FROM           222  '222'
            158_1  COME_FROM           218  '218'

 L. 748       158  LOAD_FAST                'fp'
              160  LOAD_METHOD              read
              162  LOAD_FAST                'bs'
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'block'

 L. 749       168  LOAD_FAST                'block'
              170  POP_JUMP_IF_FALSE   224  'to 224'

 L. 750       172  LOAD_FAST                'checker'
              174  LOAD_METHOD              feed
              176  LOAD_FAST                'block'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L. 751       182  LOAD_FAST                'tfp'
              184  LOAD_METHOD              write
              186  LOAD_FAST                'block'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 752       192  LOAD_FAST                'blocknum'
              194  LOAD_CONST               1
              196  INPLACE_ADD      
              198  STORE_FAST               'blocknum'

 L. 753       200  LOAD_FAST                'self'
              202  LOAD_METHOD              reporthook
              204  LOAD_FAST                'url'
              206  LOAD_FAST                'filename'
              208  LOAD_FAST                'blocknum'
              210  LOAD_FAST                'bs'
              212  LOAD_FAST                'size'
              214  CALL_METHOD_5         5  ''
              216  POP_TOP          
              218  JUMP_BACK           158  'to 158'

 L. 755       220  JUMP_FORWARD        224  'to 224'
              222  JUMP_BACK           158  'to 158'
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           170  '170'

 L. 756       224  LOAD_FAST                'self'
              226  LOAD_METHOD              check_hash
              228  LOAD_FAST                'checker'
              230  LOAD_FAST                'filename'
              232  LOAD_FAST                'tfp'
              234  CALL_METHOD_3         3  ''
              236  POP_TOP          
              238  POP_BLOCK        
              240  BEGIN_FINALLY    
            242_0  COME_FROM_WITH      154  '154'
              242  WITH_CLEANUP_START
              244  WITH_CLEANUP_FINISH
              246  END_FINALLY      

 L. 757       248  LOAD_FAST                'headers'
              250  POP_BLOCK        
              252  CALL_FINALLY        256  'to 256'
              254  RETURN_VALUE     
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM_FINALLY    16  '16'

 L. 759       256  LOAD_FAST                'fp'
          258_260  POP_JUMP_IF_FALSE   270  'to 270'

 L. 760       262  LOAD_FAST                'fp'
              264  LOAD_METHOD              close
              266  CALL_METHOD_0         0  ''
              268  POP_TOP          
            270_0  COME_FROM           258  '258'
              270  END_FINALLY      

Parse error at or near `JUMP_FORWARD' instruction at offset 220

    def reporthook(self, url, filename, blocknum, blksize, size):
        pass

    def open_url--- This code section failed: ---

 L. 766         0  LOAD_FAST                'url'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 'file:'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 767        10  LOAD_GLOBAL              local_open
               12  LOAD_FAST                'url'
               14  CALL_FUNCTION_1       1  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             8  '8'

 L. 768        18  SETUP_FINALLY        34  'to 34'

 L. 769        20  LOAD_GLOBAL              open_with_auth
               22  LOAD_FAST                'url'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                opener
               28  CALL_FUNCTION_2       2  ''
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    18  '18'

 L. 770        34  DUP_TOP          
               36  LOAD_GLOBAL              ValueError
               38  LOAD_GLOBAL              http_client
               40  LOAD_ATTR                InvalidURL
               42  BUILD_TUPLE_2         2 
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE   130  'to 130'
               48  POP_TOP          
               50  STORE_FAST               'v'
               52  POP_TOP          
               54  SETUP_FINALLY       116  'to 116'

 L. 771        56  LOAD_STR                 ' '
               58  LOAD_METHOD              join
               60  LOAD_LISTCOMP            '<code_object <listcomp>>'
               62  LOAD_STR                 'PackageIndex.open_url.<locals>.<listcomp>'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  LOAD_FAST                'v'
               68  LOAD_ATTR                args
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'msg'

 L. 772        78  LOAD_FAST                'warning'
               80  POP_JUMP_IF_FALSE    96  'to 96'

 L. 773        82  LOAD_FAST                'self'
               84  LOAD_METHOD              warn
               86  LOAD_FAST                'warning'
               88  LOAD_FAST                'msg'
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          
               94  JUMP_FORWARD        112  'to 112'
             96_0  COME_FROM            80  '80'

 L. 775        96  LOAD_GLOBAL              DistutilsError
               98  LOAD_STR                 '%s %s'
              100  LOAD_FAST                'url'
              102  LOAD_FAST                'msg'
              104  BUILD_TUPLE_2         2 
              106  BINARY_MODULO    
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            94  '94'
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_FINALLY    54  '54'
              116  LOAD_CONST               None
              118  STORE_FAST               'v'
              120  DELETE_FAST              'v'
              122  END_FINALLY      
              124  POP_EXCEPT       
          126_128  JUMP_FORWARD        406  'to 406'
            130_0  COME_FROM            46  '46'

 L. 776       130  DUP_TOP          
              132  LOAD_GLOBAL              urllib
              134  LOAD_ATTR                error
              136  LOAD_ATTR                HTTPError
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   174  'to 174'
              142  POP_TOP          
              144  STORE_FAST               'v'
              146  POP_TOP          
              148  SETUP_FINALLY       162  'to 162'

 L. 777       150  LOAD_FAST                'v'
              152  ROT_FOUR         
              154  POP_BLOCK        
              156  POP_EXCEPT       
              158  CALL_FINALLY        162  'to 162'
              160  RETURN_VALUE     
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM_FINALLY   148  '148'
              162  LOAD_CONST               None
              164  STORE_FAST               'v'
              166  DELETE_FAST              'v'
              168  END_FINALLY      
              170  POP_EXCEPT       
              172  JUMP_FORWARD        406  'to 406'
            174_0  COME_FROM           140  '140'

 L. 778       174  DUP_TOP          
              176  LOAD_GLOBAL              urllib
              178  LOAD_ATTR                error
              180  LOAD_ATTR                URLError
              182  COMPARE_OP               exception-match
          184_186  POP_JUMP_IF_FALSE   250  'to 250'
              188  POP_TOP          
              190  STORE_FAST               'v'
              192  POP_TOP          
              194  SETUP_FINALLY       238  'to 238'

 L. 779       196  LOAD_FAST                'warning'
              198  POP_JUMP_IF_FALSE   216  'to 216'

 L. 780       200  LOAD_FAST                'self'
              202  LOAD_METHOD              warn
              204  LOAD_FAST                'warning'
              206  LOAD_FAST                'v'
              208  LOAD_ATTR                reason
              210  CALL_METHOD_2         2  ''
              212  POP_TOP          
              214  JUMP_FORWARD        234  'to 234'
            216_0  COME_FROM           198  '198'

 L. 782       216  LOAD_GLOBAL              DistutilsError
              218  LOAD_STR                 'Download error for %s: %s'

 L. 783       220  LOAD_FAST                'url'
              222  LOAD_FAST                'v'
              224  LOAD_ATTR                reason
              226  BUILD_TUPLE_2         2 

 L. 782       228  BINARY_MODULO    
              230  CALL_FUNCTION_1       1  ''
              232  RAISE_VARARGS_1       1  'exception instance'
            234_0  COME_FROM           214  '214'
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_FINALLY   194  '194'
              238  LOAD_CONST               None
              240  STORE_FAST               'v'
              242  DELETE_FAST              'v'
              244  END_FINALLY      
              246  POP_EXCEPT       
              248  JUMP_FORWARD        406  'to 406'
            250_0  COME_FROM           184  '184'

 L. 784       250  DUP_TOP          
              252  LOAD_GLOBAL              http_client
              254  LOAD_ATTR                BadStatusLine
              256  COMPARE_OP               exception-match
          258_260  POP_JUMP_IF_FALSE   326  'to 326'
              262  POP_TOP          
              264  STORE_FAST               'v'
              266  POP_TOP          
              268  SETUP_FINALLY       314  'to 314'

 L. 785       270  LOAD_FAST                'warning'
          272_274  POP_JUMP_IF_FALSE   292  'to 292'

 L. 786       276  LOAD_FAST                'self'
              278  LOAD_METHOD              warn
              280  LOAD_FAST                'warning'
              282  LOAD_FAST                'v'
              284  LOAD_ATTR                line
              286  CALL_METHOD_2         2  ''
              288  POP_TOP          
              290  JUMP_FORWARD        310  'to 310'
            292_0  COME_FROM           272  '272'

 L. 788       292  LOAD_GLOBAL              DistutilsError

 L. 789       294  LOAD_STR                 '%s returned a bad status line. The server might be down, %s'

 L. 791       296  LOAD_FAST                'url'
              298  LOAD_FAST                'v'
              300  LOAD_ATTR                line
              302  BUILD_TUPLE_2         2 

 L. 789       304  BINARY_MODULO    

 L. 788       306  CALL_FUNCTION_1       1  ''
              308  RAISE_VARARGS_1       1  'exception instance'
            310_0  COME_FROM           290  '290'
              310  POP_BLOCK        
              312  BEGIN_FINALLY    
            314_0  COME_FROM_FINALLY   268  '268'
              314  LOAD_CONST               None
              316  STORE_FAST               'v'
              318  DELETE_FAST              'v'
              320  END_FINALLY      
              322  POP_EXCEPT       
              324  JUMP_FORWARD        406  'to 406'
            326_0  COME_FROM           258  '258'

 L. 793       326  DUP_TOP          
              328  LOAD_GLOBAL              http_client
              330  LOAD_ATTR                HTTPException
              332  LOAD_GLOBAL              socket
              334  LOAD_ATTR                error
              336  BUILD_TUPLE_2         2 
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   404  'to 404'
              344  POP_TOP          
              346  STORE_FAST               'v'
              348  POP_TOP          
              350  SETUP_FINALLY       392  'to 392'

 L. 794       352  LOAD_FAST                'warning'
          354_356  POP_JUMP_IF_FALSE   372  'to 372'

 L. 795       358  LOAD_FAST                'self'
              360  LOAD_METHOD              warn
              362  LOAD_FAST                'warning'
              364  LOAD_FAST                'v'
              366  CALL_METHOD_2         2  ''
              368  POP_TOP          
              370  JUMP_FORWARD        388  'to 388'
            372_0  COME_FROM           354  '354'

 L. 797       372  LOAD_GLOBAL              DistutilsError
              374  LOAD_STR                 'Download error for %s: %s'

 L. 798       376  LOAD_FAST                'url'
              378  LOAD_FAST                'v'
              380  BUILD_TUPLE_2         2 

 L. 797       382  BINARY_MODULO    
              384  CALL_FUNCTION_1       1  ''
              386  RAISE_VARARGS_1       1  'exception instance'
            388_0  COME_FROM           370  '370'
              388  POP_BLOCK        
              390  BEGIN_FINALLY    
            392_0  COME_FROM_FINALLY   350  '350'
              392  LOAD_CONST               None
              394  STORE_FAST               'v'
              396  DELETE_FAST              'v'
              398  END_FINALLY      
              400  POP_EXCEPT       
              402  JUMP_FORWARD        406  'to 406'
            404_0  COME_FROM           340  '340'
              404  END_FINALLY      
            406_0  COME_FROM           402  '402'
            406_1  COME_FROM           324  '324'
            406_2  COME_FROM           248  '248'
            406_3  COME_FROM           172  '172'
            406_4  COME_FROM           126  '126'

Parse error at or near `DUP_TOP' instruction at offset 130

    def _download_url(self, scheme, url, tmpdir):
        name, fragment = egg_info_for_url(url)
        if name:
            while True:
                if '..' in name:
                    name = name.replace('..', '.').replace('\\', '_')

        else:
            name = '__downloaded__'
        if name.endswith('.egg.zip'):
            name = name[:-4]
        filename = os.path.join(tmpdir, name)
        if scheme == 'svn' or (scheme.startswith('svn+')):
            return self._download_svn(url, filename)
        if scheme == 'git' or (scheme.startswith('git+')):
            return self._download_git(url, filename)
        if scheme.startswith('hg+'):
            return self._download_hg(url, filename)
        if scheme == 'file':
            return urllib.request.url2pathname(urllib.parse.urlparse(url)[2])
        self.url_ok(url, True)
        return self._attempt_download(url, filename)

    def scan_url(self, url):
        self.process_url(url, True)

    def _attempt_download(self, url, filename):
        headers = self._download_to(url, filename)
        if 'html' in headers.get('content-type', '').lower():
            return self._download_html(url, headers, filename)
        return filename

    def _download_html(self, url, headers, filename):
        file = open(filename)
        for line in file:
            if line.strip():
                if re.search('<title>([^- ]+ - )?Revision \\d+:', line):
                    file.close()
                    os.unlink(filename)
                    return self._download_svn(url, filename)
                else:
                    break
        else:
            file.close()
            os.unlink(filename)
            raise DistutilsError('Unexpected HTML page found at ' + url)

    def _download_svn(self, url, filename):
        warnings.warn('SVN download support is deprecated', UserWarning)
        url = url.split('#', 1)[0]
        creds = ''
        if not url.lower().startswith('svn:') or '@' in url:
            scheme, netloc, path, p, q, f = urllib.parse.urlparse(url)
            if not netloc:
                if path.startswith('//'):
                    if '/' in path[2:]:
                        netloc, path = path[2:].split('/', 1)
                        auth, host = _splituser(netloc)
                        if auth:
                            if ':' in auth:
                                user, pw = auth.split(':', 1)
                                creds = ' --username=%s --password=%s' % (user, pw)
                            else:
                                creds = ' --username=' + auth
                            netloc = host
                            parts = (scheme, netloc, url, p, q, f)
                            url = urllib.parse.urlunparse(parts)
            self.info('Doing subversion checkout from %s to %s', url, filename)
            os.system('svn checkout%s -q %s %s' % (creds, url, filename))
            return filename

    @staticmethod
    def _vcs_split_rev_from_url(url, pop_prefix=False):
        scheme, netloc, path, query, frag = urllib.parse.urlsplit(url)
        scheme = scheme.split('+', 1)[(-1)]
        path = path.split('#', 1)[0]
        rev = None
        if '@' in path:
            path, rev = path.rsplit('@', 1)
        url = urllib.parse.urlunsplit((scheme, netloc, path, query, ''))
        return (
         url, rev)

    def _download_git(self, url, filename):
        filename = filename.split('#', 1)[0]
        url, rev = self._vcs_split_rev_from_url(url, pop_prefix=True)
        self.info('Doing git clone from %s to %s', url, filename)
        os.system('git clone --quiet %s %s' % (url, filename))
        if rev is not None:
            self.info('Checking out %s', rev)
            os.system('git -C %s checkout --quiet %s' % (
             filename,
             rev))
        return filename

    def _download_hg(self, url, filename):
        filename = filename.split('#', 1)[0]
        url, rev = self._vcs_split_rev_from_url(url, pop_prefix=True)
        self.info('Doing hg clone from %s to %s', url, filename)
        os.system('hg clone --quiet %s %s' % (url, filename))
        if rev is not None:
            self.info('Updating to %s', rev)
            os.system('hg --cwd %s up -C -r %s -q' % (
             filename,
             rev))
        return filename

    def debug(self, msg, *args):
        (log.debug)(msg, *args)

    def info(self, msg, *args):
        (log.info)(msg, *args)

    def warn(self, msg, *args):
        (log.warn)(msg, *args)


entity_sub = re.compile('&(#(\\d+|x[\\da-fA-F]+)|[\\w.:-]+);?').sub

def decode_entity(match):
    what = match.group(0)
    return unescape(what)


def htmldecode(text):
    """
    Decode HTML entities in the given text.

    >>> htmldecode(
    ...     'https://../package_name-0.1.2.tar.gz'
    ...     '?tokena=A&amp;tokenb=B">package_name-0.1.2.tar.gz')
    'https://../package_name-0.1.2.tar.gz?tokena=A&tokenb=B">package_name-0.1.2.tar.gz'
    """
    return entity_sub(decode_entity, text)


def socket_timeout(timeout=15):

    def _socket_timeout(func):

        def _socket_timeout(*args, **kwargs):
            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)
            try:
                return func(*args, **kwargs)
            finally:
                socket.setdefaulttimeout(old_timeout)

        return _socket_timeout

    return _socket_timeout


def _encode_auth(auth):
    """
    A function compatible with Python 2.3-3.3 that will encode
    auth from a URL suitable for an HTTP header.
    >>> str(_encode_auth('username%3Apassword'))
    'dXNlcm5hbWU6cGFzc3dvcmQ='

    Long auth strings should not cause a newline to be inserted.
    >>> long_auth = 'username:' + 'password'*10
    >>> chr(10) in str(_encode_auth(long_auth))
    False
    """
    auth_s = urllib.parse.unquote(auth)
    auth_bytes = auth_s.encode()
    encoded_bytes = base64.b64encode(auth_bytes)
    encoded = encoded_bytes.decode()
    return encoded.replace('\n', '')


class Credential:
    __doc__ = '\n    A username/password pair. Use like a namedtuple.\n    '

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __iter__(self):
        yield self.username
        yield self.password

    def __str__(self):
        return '%(username)s:%(password)s' % vars(self)


class PyPIConfig(configparser.RawConfigParser):

    def __init__(self):
        """
        Load from ~/.pypirc
        """
        defaults = dict.fromkeys(['username', 'password', 'repository'], '')
        configparser.RawConfigParser.__init__(self, defaults)
        rc = os.path.join(os.path.expanduser('~'), '.pypirc')
        if os.path.exists(rc):
            self.read(rc)

    @property
    def creds_by_repository(self):
        sections_with_repositories = [section for section in self.sections() if self.get(section, 'repository').strip()]
        return dict(map(self._get_repo_cred, sections_with_repositories))

    def _get_repo_cred(self, section):
        repo = self.get(section, 'repository').strip()
        return (
         repo,
         Credential(self.get(section, 'username').strip(), self.get(section, 'password').strip()))

    def find_credential(self, url):
        """
        If the URL indicated appears to be a repository defined in this
        config, return the credential for that repository.
        """
        for repository, cred in self.creds_by_repository.items():
            if url.startswith(repository):
                return cred


def open_with_auth(url, opener=urllib.request.urlopen):
    """Open a urllib2 request, handling HTTP authentication"""
    parsed = urllib.parse.urlparse(url)
    scheme, netloc, path, params, query, frag = parsed
    if netloc.endswith(':'):
        raise http_client.InvalidURL("nonnumeric port: ''")
    if scheme in ('http', 'https'):
        auth, address = _splituser(netloc)
    else:
        auth = None
    if not auth:
        cred = PyPIConfig().find_credential(url)
        if cred:
            auth = str(cred)
            info = (cred.username, url)
            (log.info)(*('Authenticating as %s for %s (from .pypirc)', ), *info)
    if auth:
        auth = 'Basic ' + _encode_auth(auth)
        parts = (scheme, address, path, params, query, frag)
        new_url = urllib.parse.urlunparse(parts)
        request = urllib.request.Request(new_url)
        request.add_header('Authorization', auth)
    else:
        request = urllib.request.Request(url)
    request.add_header('User-Agent', user_agent)
    fp = opener(request)
    if auth:
        s2, h2, path2, param2, query2, frag2 = urllib.parse.urlparse(fp.url)
        if s2 == scheme:
            if h2 == address:
                parts = (
                 s2, netloc, path2, param2, query2, frag2)
                fp.url = urllib.parse.urlunparse(parts)
    return fp


def _splituser(host):
    """splituser('user[:passwd]@host[:port]')
    --> 'user[:passwd]', 'host[:port]'."""
    user, delim, host = host.rpartition('@')
    return (
     user if delim else None, host)


open_with_auth = socket_timeout(_SOCKET_TIMEOUT)(open_with_auth)

def fix_sf_url(url):
    return url


def local_open--- This code section failed: ---

 L.1114         0  LOAD_GLOBAL              urllib
                2  LOAD_ATTR                parse
                4  LOAD_METHOD              urlparse
                6  LOAD_FAST                'url'
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_6     6 
               12  STORE_FAST               'scheme'
               14  STORE_FAST               'server'
               16  STORE_FAST               'path'
               18  STORE_FAST               'param'
               20  STORE_FAST               'query'
               22  STORE_FAST               'frag'

 L.1115        24  LOAD_GLOBAL              urllib
               26  LOAD_ATTR                request
               28  LOAD_METHOD              url2pathname
               30  LOAD_FAST                'path'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'filename'

 L.1116        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              isfile
               42  LOAD_FAST                'filename'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.1117        48  LOAD_GLOBAL              urllib
               50  LOAD_ATTR                request
               52  LOAD_METHOD              urlopen
               54  LOAD_FAST                'url'
               56  CALL_METHOD_1         1  ''
               58  RETURN_VALUE     
             60_0  COME_FROM            46  '46'

 L.1118        60  LOAD_FAST                'path'
               62  LOAD_METHOD              endswith
               64  LOAD_STR                 '/'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE   232  'to 232'
               70  LOAD_GLOBAL              os
               72  LOAD_ATTR                path
               74  LOAD_METHOD              isdir
               76  LOAD_FAST                'filename'
               78  CALL_METHOD_1         1  ''
               80  POP_JUMP_IF_FALSE   232  'to 232'

 L.1119        82  BUILD_LIST_0          0 
               84  STORE_FAST               'files'

 L.1120        86  LOAD_GLOBAL              os
               88  LOAD_METHOD              listdir
               90  LOAD_FAST                'filename'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
             96_0  COME_FROM           196  '196'
               96  FOR_ITER            198  'to 198'
               98  STORE_FAST               'f'

 L.1121       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              join
              106  LOAD_FAST                'filename'
              108  LOAD_FAST                'f'
              110  CALL_METHOD_2         2  ''
              112  STORE_FAST               'filepath'

 L.1122       114  LOAD_FAST                'f'
              116  LOAD_STR                 'index.html'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   158  'to 158'

 L.1123       122  LOAD_GLOBAL              open
              124  LOAD_FAST                'filepath'
              126  LOAD_STR                 'r'
              128  CALL_FUNCTION_2       2  ''
              130  SETUP_WITH          146  'to 146'
              132  STORE_FAST               'fp'

 L.1124       134  LOAD_FAST                'fp'
              136  LOAD_METHOD              read
              138  CALL_METHOD_0         0  ''
              140  STORE_FAST               'body'
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM_WITH      130  '130'
              146  WITH_CLEANUP_START
              148  WITH_CLEANUP_FINISH
              150  END_FINALLY      

 L.1125       152  POP_TOP          
              154  BREAK_LOOP          222  'to 222'
              156  JUMP_FORWARD        178  'to 178'
            158_0  COME_FROM           120  '120'

 L.1126       158  LOAD_GLOBAL              os
              160  LOAD_ATTR                path
              162  LOAD_METHOD              isdir
              164  LOAD_FAST                'filepath'
              166  CALL_METHOD_1         1  ''
              168  POP_JUMP_IF_FALSE   178  'to 178'

 L.1127       170  LOAD_FAST                'f'
              172  LOAD_STR                 '/'
              174  INPLACE_ADD      
              176  STORE_FAST               'f'
            178_0  COME_FROM           168  '168'
            178_1  COME_FROM           156  '156'

 L.1128       178  LOAD_FAST                'files'
              180  LOAD_METHOD              append
              182  LOAD_STR                 '<a href="{name}">{name}</a>'
              184  LOAD_ATTR                format
              186  LOAD_FAST                'f'
              188  LOAD_CONST               ('name',)
              190  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  JUMP_BACK            96  'to 96'
            198_0  COME_FROM            96  '96'

 L.1131       198  LOAD_STR                 '<html><head><title>{url}</title></head><body>{files}</body></html>'

 L.1130       200  STORE_FAST               'tmpl'

 L.1133       202  LOAD_FAST                'tmpl'
              204  LOAD_ATTR                format
              206  LOAD_FAST                'url'
              208  LOAD_STR                 '\n'
              210  LOAD_METHOD              join
              212  LOAD_FAST                'files'
              214  CALL_METHOD_1         1  ''
              216  LOAD_CONST               ('url', 'files')
              218  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              220  STORE_FAST               'body'
            222_0  COME_FROM           154  '154'

 L.1134       222  LOAD_CONST               (200, 'OK')
              224  UNPACK_SEQUENCE_2     2 
              226  STORE_FAST               'status'
              228  STORE_FAST               'message'
              230  JUMP_FORWARD        242  'to 242'
            232_0  COME_FROM            80  '80'
            232_1  COME_FROM            68  '68'

 L.1136       232  LOAD_CONST               (404, 'Path not found', 'Not found')
              234  UNPACK_SEQUENCE_3     3 
              236  STORE_FAST               'status'
              238  STORE_FAST               'message'
              240  STORE_FAST               'body'
            242_0  COME_FROM           230  '230'

 L.1138       242  LOAD_STR                 'content-type'
              244  LOAD_STR                 'text/html'
              246  BUILD_MAP_1           1 
              248  STORE_FAST               'headers'

 L.1139       250  LOAD_GLOBAL              six
              252  LOAD_METHOD              StringIO
              254  LOAD_FAST                'body'
              256  CALL_METHOD_1         1  ''
              258  STORE_FAST               'body_stream'

 L.1140       260  LOAD_GLOBAL              urllib
              262  LOAD_ATTR                error
              264  LOAD_METHOD              HTTPError
              266  LOAD_FAST                'url'
              268  LOAD_FAST                'status'
              270  LOAD_FAST                'message'
              272  LOAD_FAST                'headers'
              274  LOAD_FAST                'body_stream'
              276  CALL_METHOD_5         5  ''
              278  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 230