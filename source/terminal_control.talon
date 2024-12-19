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

terminal (set|update) {user.terminal_chicken_terminal}:
    user.terminal_chicken_update_terminal(terminal_chicken_terminal)