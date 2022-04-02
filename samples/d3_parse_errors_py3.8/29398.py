# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\common\actions\action_builder.py
from selenium.webdriver.remote.command import Command
from . import interaction
from .key_actions import KeyActions
from .key_input import KeyInput
from .pointer_actions import PointerActions
from .pointer_input import PointerInput

class ActionBuilder(object):

    def __init__(self, driver, mouse=None, keyboard=None):
        if mouse is None:
            mouse = PointerInput(interaction.POINTER_MOUSE, 'mouse')
        if keyboard is None:
            keyboard = KeyInput(interaction.KEY)
        self.devices = [
         mouse, keyboard]
        self._key_action = KeyActions(keyboard)
        self._pointer_action = PointerActions(mouse)
        self.driver = driver

    def get_device_with--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        26  'to 26'

 L.  39         2  LOAD_FAST                'self'
                4  LOAD_ATTR                devices
                6  LOAD_METHOD              index
                8  LOAD_FAST                'name'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'idx'

 L.  40        14  LOAD_FAST                'self'
               16  LOAD_ATTR                devices
               18  LOAD_FAST                'idx'
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     0  '0'

 L.  41        26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  42        32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
               36  END_FINALLY      
             38_0  COME_FROM            34  '34'

Parse error at or near `POP_EXCEPT' instruction at offset 32

    @property
    def pointer_inputs(self):
        return [device for device in self.devices if device.type == interaction.POINTER]

    @property
    def key_inputs(self):
        return [device for device in self.devices if device.type == interaction.KEY]

    @property
    def key_action(self):
        return self._key_action

    @property
    def pointer_action(self):
        return self._pointer_action

    def add_key_input(self, name):
        new_input = KeyInput(name)
        self._add_inputnew_input
        return new_input

    def add_pointer_input(self, kind, name):
        new_input = PointerInput(kind, name)
        self._add_inputnew_input
        return new_input

    def perform(self):
        enc = {'actions': []}
        for device in self.devices:
            encoded = device.encode()
            if encoded['actions']:
                enc['actions'].appendencoded
        else:
            self.driver.execute(Command.W3C_ACTIONS, enc)

    def clear_actions(self):
        """
            Clears actions that are already stored on the remote end
        """
        self.driver.executeCommand.W3C_CLEAR_ACTIONS

    def _add_input(self, input):
        self.devices.appendinput