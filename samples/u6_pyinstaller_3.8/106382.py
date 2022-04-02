# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\ImageSequence.py


class Iterator:
    __doc__ = '\n    This class implements an iterator object that can be used to loop\n    over an image sequence.\n\n    You can use the ``[]`` operator to access elements by index. This operator\n    will raise an :py:exc:`IndexError` if you try to access a nonexistent\n    frame.\n\n    :param im: An image object.\n    '

    def __init__(self, im):
        if not hasattr(im, 'seek'):
            raise AttributeError('im must have seek method')
        self.im = im
        self.position = getattr(self.im, '_min_frame', 0)

    def __getitem__--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        22  'to 22'

 L.  39         2  LOAD_FAST                'self'
                4  LOAD_ATTR                im
                6  LOAD_METHOD              seek
                8  LOAD_FAST                'ix'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L.  40        14  LOAD_FAST                'self'
               16  LOAD_ATTR                im
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.  41        22  DUP_TOP          
               24  LOAD_GLOBAL              EOFError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    44  'to 44'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  42        36  LOAD_GLOBAL              IndexError
               38  RAISE_VARARGS_1       1  'exception instance'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            28  '28'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

Parse error at or near `POP_TOP' instruction at offset 32

    def __iter__(self):
        return self

    def __next__--- This code section failed: ---

 L.  48         0  SETUP_FINALLY        38  'to 38'

 L.  49         2  LOAD_FAST                'self'
                4  LOAD_ATTR                im
                6  LOAD_METHOD              seek
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                position
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L.  50        16  LOAD_FAST                'self'
               18  DUP_TOP          
               20  LOAD_ATTR                position
               22  LOAD_CONST               1
               24  INPLACE_ADD      
               26  ROT_TWO          
               28  STORE_ATTR               position

 L.  51        30  LOAD_FAST                'self'
               32  LOAD_ATTR                im
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     0  '0'

 L.  52        38  DUP_TOP          
               40  LOAD_GLOBAL              EOFError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    60  'to 60'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  53        52  LOAD_GLOBAL              StopIteration
               54  RAISE_VARARGS_1       1  'exception instance'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            44  '44'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'

Parse error at or near `POP_TOP' instruction at offset 48


def all_frames(im, func=None):
    """
    Applies a given function to all frames in an image or a list of images.
    The frames are returned as a list of separate images.

    :param im: An image, or a list of images.
    :param func: The function to apply to all of the image frames.
    :returns: A list of images.
    """
    if not isinstance(im, list):
        im = [
         im]
    ims = []
    for imSequence in im:
        current = imSequence.tell()
        ims += [im_frame.copy() for im_frame in Iterator(imSequence)]
        imSequence.seekcurrent
    else:
        if func:
            return [func(im) for im in ims]
        return ims