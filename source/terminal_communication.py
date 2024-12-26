from talon import Module, actions, app, settings, imgui
from typing import Any, Callable

FOCUS_ACTION_NAMES = ['focus', 'key', 'act']
DEFAULT_TERMINAL_STRING = 'act user.vscode workbench.action.terminal.focus;act user.vscode workbench.action.terminal.focusNext;act user.vscode workbench.action.terminal.focusPrevious;act user.vscode workbench.action.focusActiveEditorGroup'

current_terminal_focus_action = ""
current_terminal_return_action = ""
current_terminal_next_action = ""
current_terminal_previous_action = ""
completion_options = []
text_to_complete_with_options = ""

def extract_action_and_text(terminal_text: str):
    for action_name in FOCUS_ACTION_NAMES:
        if terminal_text.startswith(action_name + " "):
            return action_name, terminal_text[len(action_name) + 1:]

def find_biggest_leading_suffix(suffix: str, target: str):
    for i in range(len(suffix)):
        candidate = suffix[i:]
        if target.startswith(candidate):
            return candidate
    return ""

def find_text_after_suffix(suffix: str, target: str):
    if target.startswith(suffix):
        return target[len(suffix):]
    return target

def compute_terminal_options(text: str):
    options = []
    current_option = ""
    is_inside_string = False
    string_characters = ['"', "'"]
    consecutive_backslash_count = 0
    for character in text:
        if character == "\\":
            consecutive_backslash_count += 1
            if consecutive_backslash_count == 2:
                current_option += "\\"
                consecutive_backslash_count = 0
        else:
            if character == " " and not is_inside_string and consecutive_backslash_count == 0:
                if current_option:
                    options.append(current_option)
                current_option = ""
            elif character in string_characters and not is_inside_string and consecutive_backslash_count == 0:
                is_inside_string = True
                current_option += character
            elif character in string_characters and is_inside_string and consecutive_backslash_count == 0 and current_option[0] == character:
                is_inside_string = False
                current_option += character
            elif character == " " and not is_inside_string and consecutive_backslash_count == 1:
                current_option += "\\" + character
            else:
                current_option += character
            consecutive_backslash_count = 0
    if current_option:
        options.append(current_option)
    return options

def update_terminal(text: str):
    global current_terminal_focus_action
    global current_terminal_return_action
    global current_terminal_next_action
    global current_terminal_previous_action
    current_terminal_focus_action, current_terminal_next_action, current_terminal_previous_action, current_terminal_return_action = compute_split_values_with_defaults(
        text,
        ["", "act app.window_next", "act app.window_previous", "focus Code"]
    )

module = Module()
module.setting(
    'terminal_chicken_default_terminal',
    type = str,
    default = None,
    desc = 'The default terminal for terminal chicken'
)

module.setting(
    'terminal_chicken_switch_delay',
    type = float,
    default = 0.2,
    desc = "How long to sweep after switching application or windows in certain contexts"
)

module.setting(
    'terminal_chicken_copy_delay',
    type = float,
    default = 0.5, 
    desc = "How long to wait in between selecting terminal text and copying it"
)

module.list("terminal_chicken_terminal", desc="List of definitions for terminal chicken terminals")

@imgui.open(y=0)
def gui(gui: imgui.GUI):
    global completion_options
    gui.text("Completion Options")
    gui.line()
    for index, option in enumerate(completion_options):
        gui.text(f"completion {index + 1}: {option}")    
    if gui.button("completion close"):
        actions.user.terminal_chicken_hide_completion_options()

def compute_split_values_with_defaults(text: str, default_values):
    values = text.split(";")
    results = []
    for i in range(len(default_values)):
        if i < len(values) and values[i] != "":
            results.append(values[i])
        else:
            results.append(default_values[i])
    return results

def sleep_delay_setting(name: str):
    actions.sleep(settings.get(name))

def sleep_for_switch_delay():
    sleep_delay_setting("user.terminal_chicken_switch_delay")

def sleep_for_copy_delay():
    sleep_delay_setting("user.terminal_chicken_copy_delay")

@module.action_class
class Actions:
    def terminal_chicken_update_terminal(text: str):
        """Updates the terminal chicken with the specified text"""
        update_terminal(text)
            
    def terminal_chicken_return():
        """Returns to terminal control"""
        actions.user.terminal_chicken_focus(current_terminal_return_action)

    def terminal_chicken_focus(name: str):
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

    def terminal_chicken_focus_terminal():
        """Focuses the terminal chicken terminal"""
        actions.user.terminal_chicken_focus(current_terminal_focus_action)

    def terminal_chicken_switch_to_next_terminal():
        """Switches the currently active terminal chicken terminal to the next one"""
        actions.user.terminal_chicken_focus(current_terminal_next_action)

    def terminal_chicken_switch_to_previous_terminal():
        """Switches the currently active terminal chicken terminal to the previous one"""
        actions.user.terminal_chicken_focus(current_terminal_previous_action)

    def terminal_chicken_switch_terminal_instance(action: Callable, times: int = 1):
        """Switches the terminal instance with the specified action"""
        actions.user.terminal_chicken_focus_terminal()
        sleep_for_switch_delay()
        for _ in range(times):
            action()
            sleep_for_switch_delay()
        actions.user.terminal_chicken_return()

    def terminal_chicken_switch_to_next_terminal_instance(times: int = 1):
        """Switches the terminal chicken terminal instance to the next one from cursorless  and returns to the application"""
        actions.user.terminal_chicken_switch_terminal_instance(actions.user.terminal_chicken_switch_to_next_terminal, times)

    def terminal_chicken_switch_to_previous_terminal_instance(times: int = 1):
        """Switches the terminal chicken terminal instance to the previous one from cursorless and returns to the application"""
        actions.user.terminal_chicken_switch_terminal_instance(actions.user.terminal_chicken_switch_to_previous_terminal, times)
    
    def terminal_chicken_send_command_to_terminal(command: str):
        """Sends the specified command to the specified terminal program"""
        actions.user.terminal_chicken_focus_terminal()
        actions.insert(command)
        actions.key('enter')
        actions.user.terminal_chicken_return()
    
    def terminal_chicken_send_command_on_current_line_to_terminal():
        """Sends the text on the current line to the specified terminal program"""
        actions.edit.line_start()
        actions.edit.extend_line_end()
        text = actions.edit.selected_text()
        actions.user.terminal_chicken_send_command_to_terminal(text)

    def terminal_chicken_send_command_on_line_with_cursorless_target_to_terminal(target: Any):
        """Sends the text on the line with the specified cursorless target with the terminal program"""
        actions.user.cursorless_command("setSelection", target)
        actions.user.terminal_chicken_send_command_on_current_line_to_terminal()

    def terminal_chicken_obtain_terminal_text_after_completion(text_to_complete: str):
        """Gets the text in the terminal with specified name"""
        actions.user.terminal_chicken_focus_terminal()
        actions.insert(text_to_complete)
        actions.key('tab')
        actions.edit.select_all()
        sleep_for_copy_delay()
        text = actions.edit.selected_text()
        actions.edit.right()
        actions.key('ctrl-c')
        actions.user.terminal_chicken_return()
        return text

    def terminal_chicken_compute_completion_text(line_start: str, terminal_text: str, last_argument: str):
        """Computes the completion text given the line start, last_argument, and the terminal text"""
        start_index = terminal_text.rfind(line_start)
        if start_index == -1:
            terminal_text_arguments = compute_terminal_options(terminal_text)
            if terminal_text_arguments:
                return terminal_text_arguments[-1]
            return last_argument
        ending_index = terminal_text.find('\n', start_index)
        if ending_index == -1:
            ending_index = len(terminal_text)
        result = terminal_text[start_index + len(line_start):ending_index]
        return last_argument + result

    def terminal_chicken_complete_current_line():
        """Performs terminal completion on the current line"""
        actions.edit.extend_line_start()
        text_to_complete = actions.edit.selected_text()
        terminal_text = actions.user.terminal_chicken_obtain_terminal_text_after_completion(text_to_complete)
        command_arguments = compute_terminal_options(text_to_complete)
        last_argument = command_arguments[-1]
        completion_text = actions.user.terminal_chicken_compute_completion_text(text_to_complete, terminal_text, last_argument)
        actions.edit.right()
        if completion_text != last_argument:
            actions.user.terminal_chicken_perform_completion(last_argument, completion_text)
        else:
            last_completion_text_instance = terminal_text.rfind(text_to_complete)
            remaining_text = terminal_text[last_completion_text_instance + len(text_to_complete):]
            if remaining_text:
                options = compute_terminal_options(remaining_text.strip())
                if len(options) == 1 and options[0] != last_argument:
                   actions.user.terminal_chicken_perform_completion(last_argument, options[0])
                elif options:
                    global completion_options, text_to_complete_with_options
                    text_to_complete_with_options = last_argument
                    completion_options = []
                    for option in options:
                        completion_options.append(option)
                    actions.user.terminal_chicken_show_completion_options()
    
    def terminal_chicken_show_completion_options():
        """Shows terminal chicken completion options"""
        gui.show()
        actions.user.terminal_chicken_activate_completion_options_context()
    
    def terminal_chicken_hide_completion_options():
        """Hides terminal chicken completion options"""
        gui.hide()
        actions.user.terminal_chicken_deactivate_completion_options_context()
        global completion_options
        completion_options = None
    
    def terminal_chicken_perform_completion(text_to_complete: str, completion: str):
        """Completes the text inside the editor"""
        already_present_suffix = find_biggest_leading_suffix(text_to_complete, completion)
        if already_present_suffix:
            completion = find_text_after_suffix(already_present_suffix, completion)
        for _ in range(len(text_to_complete) - len(already_present_suffix)):
            actions.edit.delete()
        actions.insert(completion)
        
    def terminal_chicken_select_completion_option(option: int):
        """Selects the specified completion option"""
        if completion_options:
            completion = completion_options[option - 1]
            actions.user.terminal_chicken_perform_completion(text_to_complete_with_options, completion)
            actions.user.terminal_chicken_hide_completion_options()
    
def on_ready():
    current_setting_value = settings.get("user.terminal_chicken_default_terminal")
    if not current_setting_value:
        current_setting_value = DEFAULT_TERMINAL_STRING
    update_terminal(current_setting_value)
app.register("ready", on_ready)