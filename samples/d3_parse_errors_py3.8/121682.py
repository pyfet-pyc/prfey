# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pyaudio.py
"""
PyAudio provides Python bindings for PortAudio, the cross-platform
audio I/O library. With PyAudio, you can easily use Python to play and
record audio on a variety of platforms.  PyAudio is inspired by:

* pyPortAudio/fastaudio: Python bindings for PortAudio v18 API.
* tkSnack: cross-platform sound toolkit for Tcl/Tk and Python.

.. include:: ../sphinx/examples.rst

Overview
--------

**Classes**
  :py:class:`PyAudio`, :py:class:`Stream`

.. only:: pamac

   **Host Specific Classes**
     :py:class:`PaMacCoreStreamInfo`

**Stream Conversion Convenience Functions**
  :py:func:`get_sample_size`, :py:func:`get_format_from_width`

**PortAudio version**
  :py:func:`get_portaudio_version`, :py:func:`get_portaudio_version_text`

.. |PaSampleFormat| replace:: :ref:`PortAudio Sample Format <PaSampleFormat>`
.. _PaSampleFormat:

**Portaudio Sample Formats**
  :py:data:`paFloat32`, :py:data:`paInt32`, :py:data:`paInt24`,
  :py:data:`paInt16`, :py:data:`paInt8`, :py:data:`paUInt8`,
  :py:data:`paCustomFormat`

.. |PaHostAPI| replace:: :ref:`PortAudio Host API <PaHostAPI>`
.. _PaHostAPI:

**PortAudio Host APIs**
  :py:data:`paInDevelopment`, :py:data:`paDirectSound`, :py:data:`paMME`,
  :py:data:`paASIO`, :py:data:`paSoundManager`, :py:data:`paCoreAudio`,
  :py:data:`paOSS`, :py:data:`paALSA`, :py:data:`paAL`, :py:data:`paBeOS`,
  :py:data:`paWDMKS`, :py:data:`paJACK`, :py:data:`paWASAPI`,
  :py:data:`paNoDevice`

.. |PaErrorCode| replace:: :ref:`PortAudio Error Code <PaErrorCode>`
.. _PaErrorCode:

**PortAudio Error Codes**
  :py:data:`paNoError`, :py:data:`paNotInitialized`,
  :py:data:`paUnanticipatedHostError`, :py:data:`paInvalidChannelCount`,
  :py:data:`paInvalidSampleRate`, :py:data:`paInvalidDevice`,
  :py:data:`paInvalidFlag`, :py:data:`paSampleFormatNotSupported`,
  :py:data:`paBadIODeviceCombination`, :py:data:`paInsufficientMemory`,
  :py:data:`paBufferTooBig`, :py:data:`paBufferTooSmall`,
  :py:data:`paNullCallback`, :py:data:`paBadStreamPtr`,
  :py:data:`paTimedOut`, :py:data:`paInternalError`,
  :py:data:`paDeviceUnavailable`,
  :py:data:`paIncompatibleHostApiSpecificStreamInfo`,
  :py:data:`paStreamIsStopped`, :py:data:`paStreamIsNotStopped`,
  :py:data:`paInputOverflowed`, :py:data:`paOutputUnderflowed`,
  :py:data:`paHostApiNotFound`, :py:data:`paInvalidHostApi`,
  :py:data:`paCanNotReadFromACallbackStream`,
  :py:data:`paCanNotWriteToACallbackStream`,
  :py:data:`paCanNotReadFromAnOutputOnlyStream`,
  :py:data:`paCanNotWriteToAnInputOnlyStream`,
  :py:data:`paIncompatibleStreamHostApi`

.. |PaCallbackReturnCodes| replace:: :ref:`PortAudio Callback Return Code <PaCallbackReturnCodes>`
.. _PaCallbackReturnCodes:

**PortAudio Callback Return Codes**
  :py:data:`paContinue`, :py:data:`paComplete`, :py:data:`paAbort`

.. |PaCallbackFlags| replace:: :ref:`PortAutio Callback Flag <PaCallbackFlags>`
.. _PaCallbackFlags:

**PortAudio Callback Flags**
  :py:data:`paInputUnderflow`, :py:data:`paInputOverflow`,
  :py:data:`paOutputUnderflow`, :py:data:`paOutputOverflow`,
  :py:data:`paPrimingOutput`
"""
__author__ = 'Hubert Pham'
__version__ = '0.2.11'
__docformat__ = 'restructuredtext en'
import sys
try:
    import _portaudio as pa
except ImportError:
    print("Could not import the PyAudio C module '_portaudio'.")
    raise
else:
    paFloat32 = pa.paFloat32
    paInt32 = pa.paInt32
    paInt24 = pa.paInt24
    paInt16 = pa.paInt16
    paInt8 = pa.paInt8
    paUInt8 = pa.paUInt8
    paCustomFormat = pa.paCustomFormat
    paInDevelopment = pa.paInDevelopment
    paDirectSound = pa.paDirectSound
    paMME = pa.paMME
    paASIO = pa.paASIO
    paSoundManager = pa.paSoundManager
    paCoreAudio = pa.paCoreAudio
    paOSS = pa.paOSS
    paALSA = pa.paALSA
    paAL = pa.paAL
    paBeOS = pa.paBeOS
    paWDMKS = pa.paWDMKS
    paJACK = pa.paJACK
    paWASAPI = pa.paWASAPI
    paNoDevice = pa.paNoDevice
    paNoError = pa.paNoError
    paNotInitialized = pa.paNotInitialized
    paUnanticipatedHostError = pa.paUnanticipatedHostError
    paInvalidChannelCount = pa.paInvalidChannelCount
    paInvalidSampleRate = pa.paInvalidSampleRate
    paInvalidDevice = pa.paInvalidDevice
    paInvalidFlag = pa.paInvalidFlag
    paSampleFormatNotSupported = pa.paSampleFormatNotSupported
    paBadIODeviceCombination = pa.paBadIODeviceCombination
    paInsufficientMemory = pa.paInsufficientMemory
    paBufferTooBig = pa.paBufferTooBig
    paBufferTooSmall = pa.paBufferTooSmall
    paNullCallback = pa.paNullCallback
    paBadStreamPtr = pa.paBadStreamPtr
    paTimedOut = pa.paTimedOut
    paInternalError = pa.paInternalError
    paDeviceUnavailable = pa.paDeviceUnavailable
    paIncompatibleHostApiSpecificStreamInfo = pa.paIncompatibleHostApiSpecificStreamInfo
    paStreamIsStopped = pa.paStreamIsStopped
    paStreamIsNotStopped = pa.paStreamIsNotStopped
    paInputOverflowed = pa.paInputOverflowed
    paOutputUnderflowed = pa.paOutputUnderflowed
    paHostApiNotFound = pa.paHostApiNotFound
    paInvalidHostApi = pa.paInvalidHostApi
    paCanNotReadFromACallbackStream = pa.paCanNotReadFromACallbackStream
    paCanNotWriteToACallbackStream = pa.paCanNotWriteToACallbackStream
    paCanNotReadFromAnOutputOnlyStream = pa.paCanNotReadFromAnOutputOnlyStream
    paCanNotWriteToAnInputOnlyStream = pa.paCanNotWriteToAnInputOnlyStream
    paIncompatibleStreamHostApi = pa.paIncompatibleStreamHostApi
    paContinue = pa.paContinue
    paComplete = pa.paComplete
    paAbort = pa.paAbort
    paInputUnderflow = pa.paInputUnderflow
    paInputOverflow = pa.paInputOverflow
    paOutputUnderflow = pa.paOutputUnderflow
    paOutputOverflow = pa.paOutputOverflow
    paPrimingOutput = pa.paPrimingOutput

    def get_sample_size(format):
        """
    Returns the size (in bytes) for the specified
    sample *format*.

    :param format: A |PaSampleFormat| constant.
    :raises ValueError: on invalid specified `format`.
    :rtype: integer
    """
        return pa.get_sample_size(format)


    def get_format_from_width(width, unsigned=True):
        """
    Returns a PortAudio format constant for the specified *width*.

    :param width: The desired sample width in bytes (1, 2, 3, or 4)
    :param unsigned: For 1 byte width, specifies signed or unsigned format.

    :raises ValueError: when invalid *width*
    :rtype: A |PaSampleFormat| constant
    """
        if width == 1:
            if unsigned:
                return paUInt8
            return paInt8
        else:
            if width == 2:
                return paInt16
            if width == 3:
                return paInt24
            if width == 4:
                return paFloat32
            raise ValueError('Invalid width: %d' % width)


    def get_portaudio_version():
        """
    Returns portaudio version.

    :rtype: string
    """
        return pa.get_version()


    def get_portaudio_version_text():
        """
    Returns PortAudio version as a text string.

    :rtype: string
    """
        return pa.get_version_text()


    class Stream:
        __doc__ = '\n    PortAudio Stream Wrapper. Use :py:func:`PyAudio.open` to make a new\n    :py:class:`Stream`.\n\n    **Opening and Closing**\n      :py:func:`__init__`, :py:func:`close`\n\n    **Stream Info**\n      :py:func:`get_input_latency`, :py:func:`get_output_latency`,\n      :py:func:`get_time`, :py:func:`get_cpu_load`\n\n    **Stream Management**\n      :py:func:`start_stream`, :py:func:`stop_stream`, :py:func:`is_active`,\n      :py:func:`is_stopped`\n\n    **Input Output**\n      :py:func:`write`, :py:func:`read`, :py:func:`get_read_available`,\n      :py:func:`get_write_available`\n    '

        def __init__(self, PA_manager, rate, channels, format, input=False, output=False, input_device_index=None, output_device_index=None, frames_per_buffer=1024, start=True, input_host_api_specific_stream_info=None, output_host_api_specific_stream_info=None, stream_callback=None):
            """
        Initialize a stream; this should be called by
        :py:func:`PyAudio.open`. A stream can either be input, output,
        or both.

        :param PA_manager: A reference to the managing :py:class:`PyAudio`
            instance
        :param rate: Sampling rate
        :param channels: Number of channels
        :param format: Sampling size and format. See |PaSampleFormat|.
        :param input: Specifies whether this is an input stream.
            Defaults to ``False``.
        :param output: Specifies whether this is an output stream.
            Defaults to ``False``.
        :param input_device_index: Index of Input Device to use.
            Unspecified (or ``None``) uses default device.
            Ignored if `input` is ``False``.
        :param output_device_index:
            Index of Output Device to use.
            Unspecified (or ``None``) uses the default device.
            Ignored if `output` is ``False``.
        :param frames_per_buffer: Specifies the number of frames per buffer.
        :param start: Start the stream running immediately.
            Defaults to ``True``. In general, there is no reason to set
            this to ``False``.
        :param input_host_api_specific_stream_info: Specifies a host API
            specific stream information data structure for input.

            .. only:: pamac

               See :py:class:`PaMacCoreStreamInfo`.

        :param output_host_api_specific_stream_info: Specifies a host API
            specific stream information data structure for output.

            .. only:: pamac

               See :py:class:`PaMacCoreStreamInfo`.

        :param stream_callback: Specifies a callback function for
            *non-blocking* (callback) operation.  Default is
            ``None``, which indicates *blocking* operation (i.e.,
            :py:func:`Stream.read` and :py:func:`Stream.write`).  To use
            non-blocking operation, specify a callback that conforms
            to the following signature:

            .. code-block:: python

               callback(in_data,      # recorded data if input=True; else None
                        frame_count,  # number of frames
                        time_info,    # dictionary
                        status_flags) # PaCallbackFlags

            ``time_info`` is a dictionary with the following keys:
            ``input_buffer_adc_time``, ``current_time``, and
            ``output_buffer_dac_time``; see the PortAudio
            documentation for their meanings.  ``status_flags`` is one
            of |PaCallbackFlags|.

            The callback must return a tuple:

            .. code-block:: python

                (out_data, flag)

            ``out_data`` is a byte array whose length should be the
            (``frame_count * channels * bytes-per-channel``) if
            ``output=True`` or ``None`` if ``output=False``.  ``flag``
            must be either :py:data:`paContinue`, :py:data:`paComplete` or
            :py:data:`paAbort` (one of |PaCallbackReturnCodes|).
            When ``output=True`` and ``out_data`` does not contain at
            least ``frame_count`` frames, :py:data:`paComplete` is
            assumed for ``flag``.

            **Note:** ``stream_callback`` is called in a separate
            thread (from the main thread).  Exceptions that occur in
            the ``stream_callback`` will:

            1. print a traceback on standard error to aid debugging,
            2. queue the exception to be thrown (at some point) in
               the main thread, and
            3. return `paAbort` to PortAudio to stop the stream.

            **Note:** Do not call :py:func:`Stream.read` or
            :py:func:`Stream.write` if using non-blocking operation.

            **See:** PortAudio's callback signature for additional
            details: http://portaudio.com/docs/v19-doxydocs/portaudio_8h.html#a8a60fb2a5ec9cbade3f54a9c978e2710

        :raise ValueError: Neither input nor output are set True.
        """
            if not input:
                if not output:
                    raise ValueError('Must specify an input or output stream.')
            self._parent = PA_manager
            self._is_input = input
            self._is_output = output
            self._is_running = start
            self._rate = rate
            self._channels = channels
            self._format = format
            self._frames_per_buffer = frames_per_buffer
            arguments = {'rate':rate, 
             'channels':channels, 
             'format':format, 
             'input':input, 
             'output':output, 
             'input_device_index':input_device_index, 
             'output_device_index':output_device_index, 
             'frames_per_buffer':frames_per_buffer}
            if input_host_api_specific_stream_info:
                _l = input_host_api_specific_stream_info
                arguments['input_host_api_specific_stream_info'] = _l._get_host_api_stream_object()
            if output_host_api_specific_stream_info:
                _l = output_host_api_specific_stream_info
                arguments['output_host_api_specific_stream_info'] = _l._get_host_api_stream_object()
            if stream_callback:
                arguments['stream_callback'] = stream_callback
            self._stream = (pa.open)(**arguments)
            self._input_latency = self._stream.inputLatency
            self._output_latency = self._stream.outputLatency
            if self._is_running:
                pa.start_stream(self._stream)

        def close(self):
            """ Close the stream """
            pa.close(self._stream)
            self._is_running = False
            self._parent._remove_stream(self)

        def get_input_latency(self):
            """
        Return the input latency.

        :rtype: float
        """
            return self._stream.inputLatency

        def get_output_latency(self):
            """
        Return the output latency.

        :rtype: float
        """
            return self._stream.outputLatency

        def get_time(self):
            """
        Return stream time.

        :rtype: float
        """
            return pa.get_stream_time(self._stream)

        def get_cpu_load(self):
            """
        Return the CPU load.  This is always 0.0 for the
        blocking API.

        :rtype: float
        """
            return pa.get_stream_cpu_load(self._stream)

        def start_stream(self):
            """ Start the stream. """
            if self._is_running:
                return
            pa.start_stream(self._stream)
            self._is_running = True

        def stop_stream(self):
            """
        Stop the stream. Once the stream is stopped, one may not call
        write or read.  Call :py:func:`start_stream` to resume the
        stream.
        """
            if not self._is_running:
                return
            pa.stop_stream(self._stream)
            self._is_running = False

        def is_active(self):
            """
        Returns whether the stream is active.

        :rtype: bool
        """
            return pa.is_stream_active(self._stream)

        def is_stopped(self):
            """
        Returns whether the stream is stopped.

        :rtype: bool
        """
            return pa.is_stream_stopped(self._stream)

        def write(self, frames, num_frames=None, exception_on_underflow=False):
            """
        Write samples to the stream.  Do not call when using
        *non-blocking* mode.

        :param frames:
           The frames of data.
        :param num_frames:
           The number of frames to write.
           Defaults to None, in which this value will be
           automatically computed.
        :param exception_on_underflow:
           Specifies whether an IOError exception should be thrown
           (or silently ignored) on buffer underflow. Defaults
           to False for improved performance, especially on
           slower platforms.

        :raises IOError: if the stream is not an output stream
           or if the write operation was unsuccessful.

        :rtype: `None`
        """
            if not self._is_output:
                raise IOError('Not output stream', paCanNotWriteToAnInputOnlyStream)
            if num_frames == None:
                width = get_sample_size(self._format)
                num_frames = int(len(frames) / (self._channels * width))
            pa.write_stream(self._stream, frames, num_frames, exception_on_underflow)

        def read(self, num_frames, exception_on_overflow=True):
            """
        Read samples from the stream.  Do not call when using
        *non-blocking* mode.

        :param num_frames: The number of frames to read.
        :param exception_on_overflow:
           Specifies whether an IOError exception should be thrown
           (or silently ignored) on input buffer overflow. Defaults
           to True.
        :raises IOError: if stream is not an input stream
          or if the read operation was unsuccessful.
        :rtype: string
        """
            if not self._is_input:
                raise IOError('Not input stream', paCanNotReadFromAnOutputOnlyStream)
            return pa.read_stream(self._stream, num_frames, exception_on_overflow)

        def get_read_available(self):
            """
        Return the number of frames that can be read without waiting.

        :rtype: integer
        """
            return pa.get_stream_read_available(self._stream)

        def get_write_available(self):
            """
        Return the number of frames that can be written without
        waiting.

        :rtype: integer

        """
            return pa.get_stream_write_available(self._stream)


    class PyAudio:
        __doc__ = '\n    Python interface to PortAudio. Provides methods to:\n     - initialize and terminate PortAudio\n     - open and close streams\n     - query and inspect the available PortAudio Host APIs\n     - query and inspect the available PortAudio audio\n       devices\n\n    Use this class to open and close streams.\n\n    **Stream Management**\n      :py:func:`open`, :py:func:`close`\n\n    **Host API**\n      :py:func:`get_host_api_count`, :py:func:`get_default_host_api_info`,\n      :py:func:`get_host_api_info_by_type`,\n      :py:func:`get_host_api_info_by_index`,\n      :py:func:`get_device_info_by_host_api_device_index`\n\n    **Device API**\n      :py:func:`get_device_count`, :py:func:`is_format_supported`,\n      :py:func:`get_default_input_device_info`,\n      :py:func:`get_default_output_device_info`,\n      :py:func:`get_device_info_by_index`\n\n    **Stream Format Conversion**\n      :py:func:`get_sample_size`, :py:func:`get_format_from_width`\n\n    **Details**\n    '

        def __init__(self):
            """Initialize PortAudio."""
            pa.initialize()
            self._streams = set()

        def terminate(self):
            """
        Terminate PortAudio.

        :attention: Be sure to call this method for every instance of
          this object to release PortAudio resources.
        """
            for stream in self._streams.copy():
                stream.close()
            else:
                self._streams = set()
                pa.terminate()

        def get_sample_size(self, format):
            """
        Returns the size (in bytes) for the specified
        sample `format` (a |PaSampleFormat| constant).

        :param format: A |PaSampleFormat| constant.
        :raises ValueError: Invalid specified `format`.
        :rtype: integer
        """
            return pa.get_sample_size(format)

        def get_format_from_width(self, width, unsigned=True):
            """
        Returns a PortAudio format constant for the specified `width`.

        :param width: The desired sample width in bytes (1, 2, 3, or 4)
        :param unsigned: For 1 byte width, specifies signed or unsigned format.

        :raises ValueError: for invalid `width`
        :rtype: A |PaSampleFormat| constant.
        """
            if width == 1:
                if unsigned:
                    return paUInt8
                return paInt8
            else:
                if width == 2:
                    return paInt16
                if width == 3:
                    return paInt24
                if width == 4:
                    return paFloat32
                raise ValueError('Invalid width: %d' % width)

        def open(self, *args, **kwargs):
            """
        Open a new stream. See constructor for
        :py:func:`Stream.__init__` for parameter details.

        :returns: A new :py:class:`Stream`
        """
            stream = Stream(self, *args, **kwargs)
            self._streams.add(stream)
            return stream

        def close(self, stream):
            """
        Close a stream. Typically use :py:func:`Stream.close` instead.

        :param stream: An instance of the :py:class:`Stream` object.
        :raises ValueError: if stream does not exist.
        """
            if stream not in self._streams:
                raise ValueError("Stream `%s' not found" % str(stream))
            stream.close()

        def _remove_stream(self, stream):
            """
        Internal method. Removes a stream.

        :param stream: An instance of the :py:class:`Stream` object.
        """
            if stream in self._streams:
                self._streams.remove(stream)

        def get_host_api_count(self):
            """
        Return the number of available PortAudio Host APIs.

        :rtype: integer
        """
            return pa.get_host_api_count()

        def get_default_host_api_info(self):
            """
        Return a dictionary containing the default Host API
        parameters. The keys of the dictionary mirror the data fields
        of PortAudio's ``PaHostApiInfo`` structure.

        :raises IOError: if no default input device is available
        :rtype: dict
        """
            defaultHostApiIndex = pa.get_default_host_api()
            return self.get_host_api_info_by_index(defaultHostApiIndex)

        def get_host_api_info_by_type(self, host_api_type):
            """
        Return a dictionary containing the Host API parameters for the
        host API specified by the `host_api_type`. The keys of the
        dictionary mirror the data fields of PortAudio's ``PaHostApiInfo``
        structure.

        :param host_api_type: The desired |PaHostAPI|
        :raises IOError: for invalid `host_api_type`
        :rtype: dict
        """
            index = pa.host_api_type_id_to_host_api_index(host_api_type)
            return self.get_host_api_info_by_index(index)

        def get_host_api_info_by_index(self, host_api_index):
            """
        Return a dictionary containing the Host API parameters for the
        host API specified by the `host_api_index`. The keys of the
        dictionary mirror the data fields of PortAudio's ``PaHostApiInfo``
        structure.

        :param host_api_index: The host api index
        :raises IOError: for invalid `host_api_index`
        :rtype: dict
        """
            return self._make_host_api_dictionary(host_api_index, pa.get_host_api_info(host_api_index))

        def get_device_info_by_host_api_device_index(self, host_api_index, host_api_device_index):
            """
        Return a dictionary containing the Device parameters for a
        given Host API's n'th device. The keys of the dictionary
        mirror the data fields of PortAudio's ``PaDeviceInfo`` structure.

        :param host_api_index: The Host API index number
        :param host_api_device_index: The n'th device of the host API
        :raises IOError: for invalid indices
        :rtype: dict
        """
            long_method_name = pa.host_api_device_index_to_device_index
            device_index = long_method_name(host_api_index, host_api_device_index)
            return self.get_device_info_by_index(device_index)

        def _make_host_api_dictionary(self, index, host_api_struct):
            """
        Internal method to create Host API dictionary that mirrors
        PortAudio's ``PaHostApiInfo`` structure.

        :rtype: dict
        """
            return {'index':index, 
             'structVersion':host_api_struct.structVersion, 
             'type':host_api_struct.type, 
             'name':host_api_struct.name, 
             'deviceCount':host_api_struct.deviceCount, 
             'defaultInputDevice':host_api_struct.defaultInputDevice, 
             'defaultOutputDevice':host_api_struct.defaultOutputDevice}

        def get_device_count(self):
            """
        Return the number of PortAudio Host APIs.

        :rtype: integer
        """
            return pa.get_device_count()

        def is_format_supported(self, rate, input_device=None, input_channels=None, input_format=None, output_device=None, output_channels=None, output_format=None):
            """
        Check to see if specified device configuration
        is supported. Returns True if the configuration
        is supported; throws a ValueError exception otherwise.

        :param rate:
           Specifies the desired rate (in Hz)
        :param input_device:
           The input device index. Specify ``None`` (default) for
           half-duplex output-only streams.
        :param input_channels:
           The desired number of input channels. Ignored if
           `input_device` is not specified (or ``None``).
        :param input_format:
           PortAudio sample format constant defined
           in this module
        :param output_device:
           The output device index. Specify ``None`` (default) for
           half-duplex input-only streams.
        :param output_channels:
           The desired number of output channels. Ignored if
           `input_device` is not specified (or ``None``).
        :param output_format:
           |PaSampleFormat| constant.

        :rtype: bool
        :raises ValueError: tuple containing (error string, |PaErrorCode|).
        """
            if input_device == None:
                if output_device == None:
                    raise ValueError('must specify stream format for input, output, or both', paInvalidDevice)
            kwargs = {}
            if input_device != None:
                kwargs['input_device'] = input_device
                kwargs['input_channels'] = input_channels
                kwargs['input_format'] = input_format
            if output_device != None:
                kwargs['output_device'] = output_device
                kwargs['output_channels'] = output_channels
                kwargs['output_format'] = output_format
            return (pa.is_format_supported)(rate, **kwargs)

        def get_default_input_device_info(self):
            """
        Return the default input Device parameters as a
        dictionary. The keys of the dictionary mirror the data fields
        of PortAudio's ``PaDeviceInfo`` structure.

        :raises IOError: No default input device available.
        :rtype: dict
        """
            device_index = pa.get_default_input_device()
            return self.get_device_info_by_index(device_index)

        def get_default_output_device_info(self):
            """
        Return the default output Device parameters as a
        dictionary. The keys of the dictionary mirror the data fields
        of PortAudio's ``PaDeviceInfo`` structure.

        :raises IOError: No default output device available.
        :rtype: dict
        """
            device_index = pa.get_default_output_device()
            return self.get_device_info_by_index(device_index)

        def get_device_info_by_index(self, device_index):
            """
        Return the Device parameters for device specified in
        `device_index` as a dictionary. The keys of the dictionary
        mirror the data fields of PortAudio's ``PaDeviceInfo``
        structure.

        :param device_index: The device index
        :raises IOError: Invalid `device_index`.
        :rtype: dict
        """
            return self._make_device_info_dictionary(device_index, pa.get_device_info(device_index))

        def _make_device_info_dictionary--- This code section failed: ---

 L. 991         0  LOAD_FAST                'device_info'
                2  LOAD_ATTR                name
                4  STORE_FAST               'device_name'

 L. 994         6  LOAD_CONST               ('utf-8', 'cp1252')
                8  GET_ITER         
             10_0  COME_FROM            48  '48'
             10_1  COME_FROM            44  '44'
             10_2  COME_FROM            34  '34'
               10  FOR_ITER             50  'to 50'
               12  STORE_FAST               'codec'

 L. 995        14  SETUP_FINALLY        36  'to 36'

 L. 996        16  LOAD_FAST                'device_name'
               18  LOAD_METHOD              decode
               20  LOAD_FAST                'codec'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'device_name'

 L. 997        26  POP_BLOCK        
               28  POP_TOP          
               30  JUMP_FORWARD         50  'to 50'
               32  POP_BLOCK        
               34  JUMP_BACK            10  'to 10'
             36_0  COME_FROM_FINALLY    14  '14'

 L. 998        36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 999        42  POP_EXCEPT       
               44  JUMP_BACK            10  'to 10'
               46  END_FINALLY      
               48  JUMP_BACK            10  'to 10'
             50_0  COME_FROM            30  '30'
             50_1  COME_FROM            10  '10'

 L.1003        50  LOAD_FAST                'index'

 L.1004        52  LOAD_FAST                'device_info'
               54  LOAD_ATTR                structVersion

 L.1005        56  LOAD_FAST                'device_name'

 L.1006        58  LOAD_FAST                'device_info'
               60  LOAD_ATTR                hostApi

 L.1007        62  LOAD_FAST                'device_info'
               64  LOAD_ATTR                maxInputChannels

 L.1008        66  LOAD_FAST                'device_info'
               68  LOAD_ATTR                maxOutputChannels

 L.1010        70  LOAD_FAST                'device_info'
               72  LOAD_ATTR                defaultLowInputLatency

 L.1012        74  LOAD_FAST                'device_info'
               76  LOAD_ATTR                defaultLowOutputLatency

 L.1014        78  LOAD_FAST                'device_info'
               80  LOAD_ATTR                defaultHighInputLatency

 L.1016        82  LOAD_FAST                'device_info'
               84  LOAD_ATTR                defaultHighOutputLatency

 L.1018        86  LOAD_FAST                'device_info'
               88  LOAD_ATTR                defaultSampleRate

 L.1003        90  LOAD_CONST               ('index', 'structVersion', 'name', 'hostApi', 'maxInputChannels', 'maxOutputChannels', 'defaultLowInputLatency', 'defaultLowOutputLatency', 'defaultHighInputLatency', 'defaultHighOutputLatency', 'defaultSampleRate')
               92  BUILD_CONST_KEY_MAP_11    11 
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 44


    try:
        paMacCoreStreamInfo = pa.paMacCoreStreamInfo
    except AttributeError:
        pass
    else:

        class PaMacCoreStreamInfo:
            __doc__ = '\n        Mac OS X-only: PaMacCoreStreamInfo is a PortAudio Host API\n        Specific Stream Info data structure for specifying Mac OS\n        X-only settings. Instantiate this class (if desired) and pass\n        the instance as the argument in :py:func:`PyAudio.open` to parameters\n        ``input_host_api_specific_stream_info`` or\n        ``output_host_api_specific_stream_info``.\n        (See :py:func:`Stream.__init__`.)\n\n        :note: Mac OS X only.\n\n        .. |PaMacCoreFlags| replace:: :ref:`PortAudio Mac Core Flags <PaMacCoreFlags>`\n        .. _PaMacCoreFlags:\n\n        **PortAudio Mac Core Flags**\n          :py:data:`paMacCoreChangeDeviceParameters`,\n          :py:data:`paMacCoreFailIfConversionRequired`,\n          :py:data:`paMacCoreConversionQualityMin`,\n          :py:data:`paMacCoreConversionQualityMedium`,\n          :py:data:`paMacCoreConversionQualityLow`,\n          :py:data:`paMacCoreConversionQualityHigh`,\n          :py:data:`paMacCoreConversionQualityMax`,\n          :py:data:`paMacCorePlayNice`,\n          :py:data:`paMacCorePro`,\n          :py:data:`paMacCoreMinimizeCPUButPlayNice`,\n          :py:data:`paMacCoreMinimizeCPU`\n\n        **Settings**\n          :py:func:`get_flags`, :py:func:`get_channel_map`\n        '
            paMacCoreChangeDeviceParameters = pa.paMacCoreChangeDeviceParameters
            paMacCoreFailIfConversionRequired = pa.paMacCoreFailIfConversionRequired
            paMacCoreConversionQualityMin = pa.paMacCoreConversionQualityMin
            paMacCoreConversionQualityMedium = pa.paMacCoreConversionQualityMedium
            paMacCoreConversionQualityLow = pa.paMacCoreConversionQualityLow
            paMacCoreConversionQualityHigh = pa.paMacCoreConversionQualityHigh
            paMacCoreConversionQualityMax = pa.paMacCoreConversionQualityMax
            paMacCorePlayNice = pa.paMacCorePlayNice
            paMacCorePro = pa.paMacCorePro
            paMacCoreMinimizeCPUButPlayNice = pa.paMacCoreMinimizeCPUButPlayNice
            paMacCoreMinimizeCPU = pa.paMacCoreMinimizeCPU

            def __init__(self, flags=None, channel_map=None):
                """
            Initialize with flags and channel_map. See PortAudio
            documentation for more details on these parameters; they are
            passed almost verbatim to the PortAudio library.

            :param flags: |PaMacCoreFlags| OR'ed together.
                See :py:class:`PaMacCoreStreamInfo`.
            :param channel_map: An array describing the channel mapping.
                See PortAudio documentation for usage.
            """
                kwargs = {'flags':flags, 
                 'channel_map':channel_map}
                if flags == None:
                    del kwargs['flags']
                if channel_map == None:
                    del kwargs['channel_map']
                self._paMacCoreStreamInfo = paMacCoreStreamInfo(**kwargs)

            def get_flags(self):
                """
            Return the flags set at instantiation.

            :rtype: integer
            """
                return self._paMacCoreStreamInfo.flags

            def get_channel_map(self):
                """
            Return the channel map set at instantiation.

            :rtype: tuple or None
            """
                return self._paMacCoreStreamInfo.channel_map

            def _get_host_api_stream_object(self):
                """Private method."""
                return self._paMacCoreStreamInfo