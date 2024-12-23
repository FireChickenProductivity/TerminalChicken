# Overview
Terminal Chicken allows writing terminal commands in VSCode and then sending them to a terminal. This allows benefiting from cursorless editing for terminal commands. Terminal Chicken supports text completion by sending the text over to the terminal, attempting to use its builtin completion mechanism, and then copying the text in the terminal so that it can be brought back into VSCode.

# Commands
Terminal chicken commands are available in VSCode if the current file is a .terminalchicken file. The command "terminal chicken" is available in VSCode to open a default .terminalchicken file using the command palette.

send: sends the current line to the terminal and starts a new line in VSCode.

consume: sends the current line to the terminal and deletes it. This can be useful for commands you would not want to accidentally repeat.

run (user.cursorless_target): sends the line containing the target to the terminal and puts the cursor at the bottom of the file.

complete: attempts to complete the current line using the terminal's completion feature. This may not handle all corner cases. If only a single completion option is detected, it gets brought back to VSCode. Otherwise, all options are shown through a completion menu and you choose the desired one with "completion (option number)". 

completion (option number): puts the chosen completion option from the terminal into VSCode.

completion (close or hide): closes the completion menu.

term set (terminal name from terminal_chicken_terminal.talon-list): sets the terminal program to interact with.

term next (optional number_small): attempts to switch the terminal to the next window. If the optional number_small is provided, it will attempt to advance to the next window that many times.

terminal last (optional number_small): attempts to switch the terminal to the previous window. If the optional number is provided, it attempts to switch back that many windows.

# terminal_chicken_terminal.talon-list
This maps names of terminal programs to information on how to interact with them. Terminal Chicken expects information in the form of a semicolon separated list. The first entry describes how to focus the terminal, the second describes the action for returning to VSCode, the third describes the action for focusing the next terminal window, and the fourth describes the action for focusing the previous terminal window. 

Action descriptions obey the following rules. "focus (Name)" means using the user.switcher_focus action with the name, such as "focus Terminal" for mac. "act (action_name) (optional string argument)" means using the specified talon action with the optional argument if present. Example: "act user.vscode workbench.action.terminal.focus" for focusing the terminal in VSCode itself. 

The default action for returning to VSCode if none is provided is "focus Code". The default action for focusing the next terminal window is "act app.window_next", and the default action for focusing the previous terminal window is "act app.window_previous". The default is used if the action is omitted or is empty.

# Dependencies
The current setup depends on the following community actions::

user.switcher_focus

user.vscode

This setup is partly dependent on cursorless. 

# Tag
The tag user.terminal_chicken is active in a .terminalchicken file in VSCode, which could be used to activate your terminal commands.

# Settings
user.terminal_chicken_default_terminal can be used to provide the description for the default terminal. 

# Issues
The completion action may not handle all corner cases.

This setup was mostly tested on mac and tested a little on windows. There has been no testing yet on other operating systems. 