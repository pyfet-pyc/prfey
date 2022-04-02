# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImageChops.py
from . import Image

def constant(image, value):
    """Fill a channel with a given grey level.

    :rtype: :py:class:`~PIL.Image.Image`
    """
    return Image.new('L', image.size, value)


def duplicate(image):
    """Copy a channel. Alias for :py:meth:`PIL.Image.Image.copy`.

    :rtype: :py:class:`~PIL.Image.Image`
    """
    return image.copy()


def invert(image):
    """
    Invert an image (channel).

    .. code-block:: python

        out = MAX - image

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image.load()
    return image._new(image.im.chop_invert())


def lighter(image1, image2):
    """
    Compares the two images, pixel by pixel, and returns a new image containing
    the lighter values.

    .. code-block:: python

        out = max(image1, image2)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_lighter(image2.im))


def darker(image1, image2):
    """
    Compares the two images, pixel by pixel, and returns a new image containing
    the darker values.

    .. code-block:: python

        out = min(image1, image2)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_darker(image2.im))


def difference(image1, image2):
    """
    Returns the absolute value of the pixel-by-pixel difference between the two
    images.

    .. code-block:: python

        out = abs(image1 - image2)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_difference(image2.im))


def multiply(image1, image2):
    """
    Superimposes two images on top of each other.

    If you multiply an image with a solid black image, the result is black. If
    you multiply with a solid white image, the image is unaffected.

    .. code-block:: python

        out = image1 * image2 / MAX

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_multiply(image2.im))


def screen(image1, image2):
    """
    Superimposes two inverted images on top of each other.

    .. code-block:: python

        out = MAX - ((MAX - image1) * (MAX - image2) / MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_screen(image2.im))


def soft_light(image1, image2):
    """
    Superimposes two images on top of each other using the Soft Light algorithm

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_soft_light(image2.im))


def hard_light(image1, image2):
    """
    Superimposes two images on top of each other using the Hard Light algorithm

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_hard_light(image2.im))


def overlay(image1, image2):
    """
    Superimposes two images on top of each other using the Overlay algorithm

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_overlay(image2.im))


def add(image1, image2, scale=1.0, offset=0):
    """
    Adds two images, dividing the result by scale and adding the
    offset. If omitted, scale defaults to 1.0, and offset to 0.0.

    .. code-block:: python

        out = ((image1 + image2) / scale + offset)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_add(image2.im, scale, offset))


def subtract(image1, image2, scale=1.0, offset=0):
    """
    Subtracts two images, dividing the result by scale and adding the offset.
    If omitted, scale defaults to 1.0, and offset to 0.0.

    .. code-block:: python

        out = ((image1 - image2) / scale + offset)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_subtract(image2.im, scale, offset))


def add_modulo(image1, image2):
    """Add two images, without clipping the result.

    .. code-block:: python

        out = ((image1 + image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_add_modulo(image2.im))


def subtract_modulo(image1, image2):
    """Subtract two images, without clipping the result.

    .. code-block:: python

        out = ((image1 - image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_subtract_modulo(image2.im))


def logical_and(image1, image2):
    """Logical AND between two images.

    Both of the images must have mode "1". If you would like to perform a
    logical AND on an image with a mode other than "1", try
    :py:meth:`~PIL.ImageChops.multiply` instead, using a black-and-white mask
    as the second image.

    .. code-block:: python

        out = ((image1 and image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_and(image2.im))


def logical_or(image1, image2):
    """Logical OR between two images.

    Both of the images must have mode "1".

    .. code-block:: python

        out = ((image1 or image2) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_or(image2.im))


def logical_xor(image1, image2):
    """Logical XOR between two images.

    Both of the images must have mode "1".

    .. code-block:: python

        out = ((bool(image1) != bool(image2)) % MAX)

    :rtype: :py:class:`~PIL.Image.Image`
    """
    image1.load()
    image2.load()
    return image1._new(image1.im.chop_xor(image2.im))


def blend(image1, image2, alpha):
    """Blend images using constant transparency weight. Alias for
    :py:func:`PIL.Image.blend`.

    :rtype: :py:class:`~PIL.Image.Image`
    """
    return Image.blend(image1, image2, alpha)


def composite(image1, image2, mask):
    """Create composite using transparency mask. Alias for
    :py:func:`PIL.Image.composite`.

    :rtype: :py:class:`~PIL.Image.Image`
    """
    return Image.composite(image1, image2, mask)


def offset--- This code section failed: ---

 L. 325         0  LOAD_FAST                'yoffset'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 326         8  LOAD_FAST                'xoffset'
               10  STORE_FAST               'yoffset'
             12_0  COME_FROM             6  '6'

 L. 327        12  LOAD_FAST                'image'
               14  LOAD_METHOD              load
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 328        20  LOAD_FAST                'image'
               22  LOAD_METHOD              _new
               24  LOAD_FAST                'image'
               26  LOAD_ATTR                im
               28  LOAD_METHOD              offset
               30  LOAD_FAST                'xoffset'
               32  LOAD_FAST                'yoffset'
               34  CALL_METHOD_2         2  ''
               36  CALL_METHOD_1         1  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1