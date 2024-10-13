tag: user.terminal_chicken
-

send:
    user.terminal_chicken_send_command_on_current_line_to_terminal("Terminal")
    edit.line_insert_down()

run <user.cursorless_target>:
    user.terminal_chicken_send_command_on_line_with_cursorless_target_to_terminal(cursorless_target, "Terminal")
    edit.file_end()