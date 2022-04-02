# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\env.py
"""
    env.py

    Simplified access to environment variables in Python.

    @copyright: 2018 by Mike Miller
    @license: LGPL
"""
import sys, os
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping
else:
    __version__ = '0.91'

    class EnvironmentVariable(str):
        __doc__ = ' Represents a variable entry in the environment.  Base class.\n\n        Contains the functionality of strings plus a number of convenience\n        properties for type conversion.\n    '

        def __init__(self, *args):
            raise NotImplementedError('Use Entry() or NullEntry() instead.')


    class Entry(EnvironmentVariable):
        __doc__ = ' Represents an existing entry in the environment. '

        def __new__(cls, name, value):
            return str.__new__(cls, value)

        def __init__(self, name, value, sep=os.pathsep):
            self.name = name
            self.value = value
            self._pathsep = sep

        @property
        def truthy(self):
            """ Convert a Boolean-like string value to a Boolean or None.
            Note: the rules are different than string type "truthiness."

            ''              --> False
            '0'             --> False
            '1'             --> True
            ('no', 'false') --> False       #\xa0case-insensitive
            ('yes', 'true') --> True        #\xa0case-insensitive
            else            --> None
        """
            lower = self.lower()
            if lower.isdigit():
                return bool(int(lower))
            if lower in ('yes', 'true'):
                return True
            if lower in ('no', 'false'):
                return False
            if self == '':
                return False
            return

        bool = truthy

        @property
        def float(self):
            """ Return a float. """
            return float(self)

        @property
        def int(self):
            """ Return an int. """
            return int(self)

        @property
        def list(self):
            """ Split a path string (defaults to os.pathsep) and return list.

            Use str.split instead when a custom delimiter is needed.
        """
            return self.split(self._pathsep)

        @property
        def path(self):
            """ Return a path string as a Path object. """
            from pathlib import Path
            return Path(self)

        @property
        def path_list(self):
            """ Return list of Path objects. """
            from pathlib import Path
            return [Path(pathstr) for pathstr in self.split(self._pathsep)]

        @property
        def from_json(self):
            """ Parse a JSON string. """
            from json import loads
            return loads(self)

        def __repr__(self):
            return '%s(%r, %r)' % (self.__class__.__name__, self.name, self.value)


    class NullEntry(EnvironmentVariable):
        __doc__ = ' Represents an non-existent entry in the environment.\n\n        This is a None-like convenience object that won\'t throw AttributeError\n        on attribute lookups.  Attributes are instead returned as "falsey"\n        numeric zero or empty string/containers.\n    '

        def __new__(cls, name):
            return str.__new__(cls, '')

        def __init__(self, name):
            self.name = name
            self.value = None

        def __bool__(self):
            return False

        @property
        def truthy(self):
            if self.value is None:
                return
            return False

        @property
        def float(self):
            return 0.0

        @property
        def int(self):
            return 0

        @property
        def list(self):
            return []

        @property
        def path(self):
            pass

        @property
        def path_list(self):
            return []

        @property
        def from_json(self):
            return {}

        def __repr__(self):
            return '%s(%r)' % (self.__class__.__name__, self.name)


    class Environment(MutableMapping):
        __doc__ = ' A mapping object that presents a simplified view of the OS Environment.\n    '
        _Entry_class = Entry
        _NullEntry_class = NullEntry

        def __init__(self, environ=os.environ, sensitive=False if os.name == 'nt' else True, writable=False):
            setobj = object.__setattr__
            (setobj(self, '_original_env', environ),)
            (setobj(self, '_sensitive', sensitive),)
            (setobj(self, '_writable', writable),)
            if sensitive:
                setobj(self, '_envars', environ)
            else:
                setobj(self, '_envars', {value:name.lower() for name, value in environ.items()})

        def __contains__(self, name):
            return name in self._envars

        def __getattr__--- This code section failed: ---

 L. 189         0  LOAD_FAST                'name'
                2  LOAD_STR                 'Environment'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 190         8  LOAD_GLOBAL              Environment
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 191        12  LOAD_FAST                'name'
               14  LOAD_STR                 'Entry'
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    30  'to 30'

 L. 192        20  LOAD_GLOBAL              Entry
               22  JUMP_IF_TRUE_OR_POP    28  'to 28'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _Entry_class
             28_0  COME_FROM            22  '22'
               28  RETURN_VALUE     
             30_0  COME_FROM            18  '18'

 L. 194        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _sensitive
               34  POP_JUMP_IF_TRUE     44  'to 44'

 L. 195        36  LOAD_FAST                'name'
               38  LOAD_METHOD              lower
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'name'
             44_0  COME_FROM            34  '34'

 L. 197        44  SETUP_FINALLY        66  'to 66'

 L. 198        46  LOAD_FAST                'self'
               48  LOAD_METHOD              _Entry_class
               50  LOAD_FAST                'name'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _envars
               56  LOAD_FAST                'name'
               58  BINARY_SUBSCR    
               60  CALL_METHOD_2         2  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    44  '44'

 L. 199        66  DUP_TOP          
               68  LOAD_GLOBAL              KeyError
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE    94  'to 94'
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L. 200        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _NullEntry_class
               84  LOAD_FAST                'name'
               86  CALL_METHOD_1         1  ''
               88  ROT_FOUR         
               90  POP_EXCEPT       
               92  RETURN_VALUE     
             94_0  COME_FROM            72  '72'
               94  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 76

        def __setattr__(self, name, value):
            if self._writable:
                self._envars[name] = value
                if self._original_env is os.environ:
                    os.environ[name] = value
            else:
                raise AttributeError('This Environment is read-only.')

        def __delattr__(self, name):
            del self._envars[name]

        def __len__(self):
            return len(self._envars)

        def __delitem__(self, key):
            del self._envars[key]

        def __getitem__(self, key):
            return self._envars[key]

        def __setitem__(self, key, item):
            self.data[key] = item

        def __iter__(self):
            return iter(self._envars)

        def __repr__(self):
            entry_list = ', '.join(['%s=%r' % (k, v) for k, v in self.items()])
            return '%s(%s)' % (self.__class__.__name__, entry_list)

        def from_prefix(self, prefix, lowercase=True, strip=True):
            """ Returns a dictionary of keys with the same prefix.
            Compat with kr/env, lowercased.

            > xdg = env.from_prefix('XDG_')

            > for key, value in xdg.items():
                 print('%-20s' % key, value[:6], '…')
            config_dirs      /etc/x…
            current_desktop  MATE
            data_dirs        /usr/s…
            …
        """
            env_subset = {}
            for key in self._envars.keys():
                if key.startswith(prefix):
                    if strip:
                        new_key = key[len(prefix):]
                    new_key = new_key.lower() if lowercase else new_key
                    env_subset[new_key] = self._envars[key]
                return Environment(environ=env_subset,
                  sensitive=(self._sensitive),
                  writable=(self._writable))

        prefix = from_prefix

        def map--- This code section failed: ---

 L. 260         0  LOAD_CLOSURE             'kwargs'
                2  LOAD_CLOSURE             'self'
                4  BUILD_TUPLE_2         2 
                6  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                8  LOAD_STR                 'Environment.map.<locals>.<dictcomp>'
               10  MAKE_FUNCTION_8          'closure'

 L. 261        12  LOAD_DEREF               'kwargs'

 L. 260        14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


    if __name__ == '__main__':
        testenv = dict(EMPTY='',
          JSON_DATA='{"one":1, "two":2, "three":3}',
          PI='3.1416',
          READY='no',
          PORT='5150',
          QT_ACCESSIBILITY='1',
          SSH_AUTH_SOCK='/run/user/1000/keyring/ssh',
          TERM='xterm-256color',
          USER='fred',
          XDG_DATA_DIRS='/usr/local/share:/usr/share',
          XDG_SESSION_ID='c1',
          XDG_SESSION_TYPE='x11')
        __doc__ += "\n\n        Default::\n\n            >>> env = Environment(testenv, sensitive=True, writable=True)\n\n            >>> env.USER                                # exists, repr\n            Entry('USER', 'fred')\n\n            >>> str(env.USER)                           # exists, str\n            'fred'\n\n            >>> env.USER + '_suffix'                    # str ops\n            'fred_suffix'\n\n            >>> env.USER.title()                        # str ops II\n            'Fred'\n\n            >>> bool(env.USER)                          # check exists/not empty\n            True\n\n            >>> print(f'term: {env.TERM}')              # via interpolation\n            term: xterm-256color\n\n            >>> 'NO_EXISTO' in env                      # check existence, DNE\n            False\n\n            >>> env.NO_EXISTO or 'default'              #\xa0DNE\xa0with default\n            'default'\n\n            >>> env.NO_EXISTO                           #\xa0var DNE repr\n            NullEntry('NO_EXISTO')\n\n            >>> env.NO_EXISTO.value is None             #\xa0check existence II\n            True\n\n            >>> bool(env.NO_EXISTO)                     # check when DNE: False\n            False\n\n            >>> 'EMPTY' in env                          # check existence\n            True\n\n            >>> env.EMPTY                               #\xa0exists but empty\n            Entry('EMPTY', '')\n\n            >>> env.EMPTY.value is None                 #\xa0check existence II\n            False\n\n            >>> bool(env.EMPTY)                         # check when empty: False\n            False\n\n            >>> env.EMPTY or 'default'                  #\xa0exists, blank\xa0w/ def.\n            'default'\n\n            >>> key_name = 'PI'\n            >>> env[key_name]                           # getitem syntax\n            '3.1416'\n\n            >>> env.PI.float                            # type conversion\n            3.1416\n\n            >>> env.PORT.int or 9000                    #\xa0type conv. w/ default\n            5150\n\n            >>> env.QT_ACCESSIBILITY.truthy             # 0/1/yes/no/true/false\n            True\n\n            >>> sorted(env.JSON_DATA.from_json.keys())  # sorted: compat < 3.6\n            ['one', 'three', 'two']\n\n            >>> env.XDG_DATA_DIRS.list\n            ['/usr/local/share', '/usr/share']\n\n            >>> env.XDG_DATA_DIRZ.list                  # DNE fallback\n            []\n\n            # using isinstance to avoid Platform errs:\n            >>> from pathlib import Path\n            >>> isinstance(env.SSH_AUTH_SOCK.path, Path)\n            True\n\n            >>> all(map(lambda p: isinstance(p, Path), env.XDG_DATA_DIRS.path_list))\n            True\n\n        KR/env compatibility::\n\n            >>> sorted(env.prefix('XDG_', False).keys())\n            ['DATA_DIRS', 'SESSION_ID', 'SESSION_TYPE']\n\n            >>> sorted(env.prefix('XDG_', False).values())\n            ['/usr/local/share:/usr/share', 'c1', 'x11']\n\n            >>> env.map(username='USER')\n            {'username': 'fred'}\n\n        Writing is possible when writable is set to True (see above),\n        though not exceedingly useful::\n\n            >>> env.READY\n            Entry('READY', 'no')\n\n            >>> env.READY = 'yes'\n\n            >>> env.READY\n            Entry('READY', 'yes')\n\n        Unicode test::\n\n            >>> env.MÖTLEY = 'Crüe'\n            >>> env.MÖTLEY\n            Entry('MÖTLEY', 'Crüe')\n\n        Sensitive False::\n\n            >>> env = Environment(testenv, sensitive=False)\n            >>> str(env.USER)                           #\xa0interactive repr\n            'fred'\n            >>> str(env.user)                           #\xa0interactive repr\n            'fred'\n    "
        import doctest
        sys.exit(doctest.testmod(verbose=(True if '-v' in sys.argv else False))[0])
    else:
        Environment._module = sys.modules[__name__]
        sys.modules[__name__] = Environment()