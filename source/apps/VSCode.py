from talon import Context, actions

context = Context()
context.matches = """
app: Code
app: Visual Studio Code
title: /.terminalchicken/
"""

@context.action_class('user')
class Actions:
    def terminal_chicken_next_terminal():
        """Advances to the next terminal"""
        actions.user.vscode("workbench.action.terminal.focusNext")
    
    def terminal_chicken_last_terminal():
        """Advances to the previous terminal"""
        actions.user.vscode("workbench.action.terminal.focusPrevious")

    def terminal_chicken_return():
        """Returns to the controlling program"""
        actions.user.vscode("workbench.action.focusActiveEditorGroup")
