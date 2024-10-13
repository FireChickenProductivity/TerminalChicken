from talon import Module, Context, actions

context = Context()
context.matches = """
app: Code
app: Visual Studio Code
title: /.terminalchicken/
"""

module = Module()
module.tag('terminal_chicken', 'Enables terminal chicken commands')

context.tags = ['user.terminal_chicken']