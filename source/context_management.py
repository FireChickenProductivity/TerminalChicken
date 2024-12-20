from talon import Module, Context, actions

context = Context()
context.matches = """
app: Code
app: Visual Studio Code
title: /.terminalchicken/
"""

module = Module()
module.tag('terminal_chicken', 'Enables terminal chicken commands')
module.tag('terminal_chicken_completion', 'Enables terminal chicken completion commands')

context.tags = ['user.terminal_chicken']

completion_tag_context = Context()

@module.action_class
class Actions:
    def terminal_chicken_deactivate_completion_options_context():
        """Deactivates the terminal chicken completion options context"""
        global completion_tag_context
        completion_tag_context.tags = []

    def terminal_chicken_activate_completion_options_context():
        """Activates the terminal chicken completion options context"""
        global completion_tag_context
        completion_tag_context.tags = ['user.terminal_chicken_completion']