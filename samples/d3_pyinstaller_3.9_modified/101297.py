# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImageSequence.py


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
               26  <121>                62  ''
               28  POP_TOP          
               30  STORE_FAST               'e'
               32  POP_TOP          
               34  SETUP_FINALLY        54  'to 54'

 L.  42        36  LOAD_GLOBAL              IndexError
               38  LOAD_FAST                'e'
               40  RAISE_VARARGS_2       2  'exception instance with __cause__'
               42  POP_BLOCK        
               44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  STORE_FAST               'e'
               50  DELETE_FAST              'e'
               52  JUMP_FORWARD         64  'to 64'
             54_0  COME_FROM_FINALLY    34  '34'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  <48>             
               62  <48>             
             64_0  COME_FROM            52  '52'

Parse error at or near `<121>' instruction at offset 26

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
               42  <121>                78  ''
               44  POP_TOP          
               46  STORE_FAST               'e'
               48  POP_TOP          
               50  SETUP_FINALLY        70  'to 70'

 L.  53        52  LOAD_GLOBAL              StopIteration
               54  LOAD_FAST                'e'
               56  RAISE_VARARGS_2       2  'exception instance with __cause__'
               58  POP_BLOCK        
               60  POP_EXCEPT       
               62  LOAD_CONST               None
               64  STORE_FAST               'e'
               66  DELETE_FAST              'e'
               68  JUMP_FORWARD         80  'to 80'
             70_0  COME_FROM_FINALLY    50  '50'
               70  LOAD_CONST               None
               72  STORE_FAST               'e'
               74  DELETE_FAST              'e'
               76  <48>             
               78  <48>             
             80_0  COME_FROM            68  '68'

Parse error at or near `<121>' instruction at offset 42


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