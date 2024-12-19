tag: user.terminal_chicken
-

send:
    user.terminal_chicken_send_command_on_current_line_to_terminal("focus Terminal")
    edit.line_insert_down()

consume:
    user.terminal_chicken_send_command_on_current_line_to_terminal("focus Terminal")
    edit.delete()

run <user.cursorless_target>:
    user.terminal_chicken_send_command_on_line_with_cursorless_target_to_terminal(cursorless_target, "focus Terminal")
    edit.file_end()

complete: user.terminal_chicken_complete_current_line("focus Terminal")