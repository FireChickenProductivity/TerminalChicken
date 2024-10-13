import os

GRANDPARENT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TERMINAL_FILES_DIRECTORY_PATH = os.path.join(GRANDPARENT_DIRECTORY, 'terminal_files')
os.makedirs(TERMINAL_FILES_DIRECTORY_PATH, exist_ok=True)
MAIN_TERMINAL_FILE_PATH = os.path.join(TERMINAL_FILES_DIRECTORY_PATH, 'terminal.terminalchicken')
if not os.path.exists(MAIN_TERMINAL_FILE_PATH):
    with open(MAIN_TERMINAL_FILE_PATH, 'w') as _:
        pass

from talon import actions, Module

module = Module()
@module.action_class
class Actions:
    def terminal_chicken_open_main_file():
        '''Opens the main terminal chicken file'''
        actions.key('cmd-p')
        actions.insert(MAIN_TERMINAL_FILE_PATH)
        actions.sleep(1)
        actions.key('enter')