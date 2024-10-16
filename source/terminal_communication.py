from talon import Module, Context, actions
from typing import Any

FOCUS_ACTION_NAMES = ['focus', 'key', 'act']

def extract_action_and_text(terminal_text: str):
    for action_name in FOCUS_ACTION_NAMES:
        if terminal_text.startswith(action_name + " "):
            return action_name, terminal_text[len(action_name) + 1:]

module = Module()
@module.action_class
class Actions:
    def terminal_chicken_focus_vscode():
        """Focuses visual studio code"""
        actions.user.switcher_focus("Code")

    def terminal_chicken_focus_terminal(name: str):
        """Focuses the terminal with the specified name"""
        action, text = extract_action_and_text(name)
        if action == 'focus':
            actions.user.switcher_focus(text)
        elif action == 'key':
            actions.key(text)
        elif action == 'act':
            action_name = text
            value = None
            if " " in text:
                action_name, value = text.split(" ", 1)
            action = getattr(actions, action_name)
            if value:
                action(value)
            else:
                action()
        else:
            raise ValueError(f"TerminalChicken: Received invalid terminal focusing action {action}!")
    
    def terminal_chicken_send_command_to_terminal(command: str, terminal_name: str):
        """Sends the specified command to the specified terminal program"""
        actions.user.terminal_chicken_focus_terminal(terminal_name)
        actions.insert(command)
        actions.key('enter')
        actions.user.terminal_chicken_focus_vscode()
    
    def terminal_chicken_send_command_on_current_line_to_terminal(terminal_name: str):
        """Sends the text on the current line to the specified terminal program"""
        actions.edit.line_start()
        actions.edit.extend_line_end()
        text = actions.edit.selected_text()
        actions.user.terminal_chicken_send_command_to_terminal(text, terminal_name)

    def terminal_chicken_send_command_on_line_with_cursorless_target_to_terminal(target: Any, terminal_name: str):
        """Sends the text on the line with the specified cursorless target with the specified terminal program"""
        actions.user.cursorless_command("setSelection", target)
        actions.user.terminal_chicken_send_command_on_current_line_to_terminal(terminal_name)

    def terminal_chicken_obtain_terminal_text_after_completion(terminal_name: str, text_to_complete: str):
        """Gets the text in the terminal with specified name"""
        actions.user.terminal_chicken_focus_terminal(terminal_name)
        actions.insert(text_to_complete)
        actions.key('tab')
        actions.edit.select_all()
        actions.sleep(0.5)
        text = actions.edit.selected_text()
        actions.edit.right()
        actions.key('ctrl-c')
        actions.user.terminal_chicken_focus_vscode()
        return text

    def terminal_chicken_compute_completion_text(line_start: str, terminal_text: str):
        """Computes the completion text given the line start and the terminal text"""
        start_index = terminal_text.rfind(line_start)
        if start_index == -1:
            return ""
        ending_index = terminal_text.find('\n', start_index)
        if ending_index == -1:
            ending_index = len(terminal_text) - 1
        result = terminal_text[start_index + len(line_start):ending_index]
        return result

    def terminal_chicken_complete_current_line(terminal_name: str):
        """Performs terminal completion on the current line"""
        actions.edit.extend_line_start()
        text_to_complete = actions.edit.selected_text()
        terminal_text = actions.user.terminal_chicken_obtain_terminal_text_after_completion(terminal_name, text_to_complete)
        completion_text = actions.user.terminal_chicken_compute_completion_text(text_to_complete, terminal_text)
        actions.edit.right()
        actions.insert(completion_text)