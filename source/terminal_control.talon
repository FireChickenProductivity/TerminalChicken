tag: user.terminal_chicken
-

send:
    user.terminal_chicken_send_command_on_current_line_to_terminal()
    edit.line_insert_down()

consume:
    user.terminal_chicken_send_command_on_current_line_to_terminal()
    edit.delete()

run <user.cursorless_target>:
    user.terminal_chicken_send_command_on_line_with_cursorless_target_to_terminal(cursorless_target)
    edit.file_end()

complete: user.terminal_chicken_complete_current_line()

term (set|update) {user.terminal_chicken_terminal}:
    user.terminal_chicken_update_terminal(terminal_chicken_terminal)

term next [<number_small>]:
    user.terminal_chicken_switch_to_next_terminal_instance(number_small or 1)

term last [<number_small>]:
    user.terminal_chicken_switch_to_previous_terminal_instance(number_small or 1)