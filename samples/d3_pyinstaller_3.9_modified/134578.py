# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: dhooks\file.py
from typing import BinaryIO, Union

class File:
    __doc__ = "\n    Data class that represents a file that can be sent to discord.\n\n    Parameters\n    ----------\n    fp : str or :class:`io.BytesIO`\n        A file path or a binary stream that is the file. If a file path\n        is provided, this class will open and close the file for you.\n\n    name : str, optional\n        The name of the file that discord will use, if not provided,\n        defaults to the file name or the binary stream's name.\n\n    "

    def __init__(self, fp: Union[(BinaryIO, str)], name: str=''):
        if isinstance(fp, str):
            self.fp = open(fp, 'rb')
            self._manual_opened = True
            self.name = name if name else fp
        else:
            self.fp = fp
            self._manual_opened = False
            self.name = name if name else getattr(fp, 'name', 'filename')
        self._close = self.fp.close
        self.fp.close = lambda: None

    def seek--- This code section failed: ---

 L.  38         0  LOAD_FAST                'self'
                2  LOAD_ATTR                fp
                4  LOAD_ATTR                seek
                6  LOAD_FAST                'offset'
                8  BUILD_LIST_1          1 
               10  LOAD_FAST                'args'
               12  CALL_FINALLY         15  'to 15'
               14  WITH_CLEANUP_FINISH
               16  BUILD_MAP_0           0 
               18  LOAD_FAST                'kwargs'
               20  <164>                 1  ''
               22  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def close(self, force=False) -> None:
        """
        Closes the file if the file was opened by :class:`File`,
        if not, this does nothing.

        Parameters
        ----------
        force: bool
            If set to :class:`True`, force close every file.

        """
        self.fp.close = self._close
        if self._manual_opened or (force):
            self.fp.close()