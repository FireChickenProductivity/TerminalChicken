from talon import Module, Context, actions

context = Context()
context.matches = """
app: Code
title: /.terminalchicken/
"""

module = Module()
module.tag('terminal_chicken', 'Enables terminal chicken commands')

context.tags = ['user.terminal_chicken']