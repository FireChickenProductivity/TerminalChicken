import os

GRANDPARENT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
TERMINAL_FILES_DIRECTORY_PATH = os.path.join(GRANDPARENT_DIRECTORY, 'terminal_files')
os.makedirs(TERMINAL_FILES_DIRECTORY_PATH, exist_ok=True)
MAIN_TERMINAL_FILE_PATH = os.path.join(TERMINAL_FILES_DIRECTORY_PATH, 'terminal.terminalchicken')
if not os.path.exists(MAIN_TERMINAL_FILE_PATH):
    with open(MAIN_TERMINAL_FILE_PATH, 'w') as _:
        pass

from talon import actions, Module, Context

module = Module()
@module.action_class
class Actions:
    def terminal_chicken_open_vscode_workbench():
        """Opens the vscode workbench"""
        actions.key("ctrl-p")

    def terminal_chicken_open_main_file():
        '''Opens the main terminal chicken file'''
        actions.user.terminal_chicken_open_vscode_workbench()
        actions.insert(MAIN_TERMINAL_FILE_PATH)
        actions.sleep(1)
        actions.key('enter')

mac_context = Context()
mac_context.matches = r"""
os: mac
"""
@mac_context.action_class('user')
class MacActions:
    def terminal_chicken_open_vscode_workbench():
        """Opens the vscode workbench"""
        actions.key('cmd-p')