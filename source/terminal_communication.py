from talon import Module, Context, actions

module = Module()
@module.action_class
class Actions:
    def terminal_chicken_focus_vscode():
        """Focuses visual studio code"""
        actions.user.switcher_focus("Code")

    def terminal_chicken_focus_terminal(name: str):
        """Focuses the terminal with the specified name"""
        actions.user.switcher_focus(name)
    
    def terminal_chicken_send_command_to_terminal(command: str, terminal_name: str):
        """Sends the specified command to the specified terminal program"""
        actions.user.terminal_chicken_focus_terminal(terminal_name)
        actions.insert(command)
        actions.key('enter')
        actions.user.terminal_chicken_focus_vscode()
    
    def terminal_chicken_send_command_on_current_line_to_terminal(terminal_name: str):
        """Sends the text on the current line to the specified terminal program and advances to the next line"""
        actions.edit.line_start()
        actions.edit.extend_line_end()
        text = actions.edit.selected_text()
        actions.user.terminal_chicken_send_command_to_terminal(text, terminal_name)
        actions.edit.line_insert_down()