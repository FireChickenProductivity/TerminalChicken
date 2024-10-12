#testing: user.terminal_chicken_send_command_to_terminal("ls", "Terminal")

#term send:
    #user.terminal_chicken_send_command_on_current_line_to_terminal("Terminal")
    #edit.line_insert_down()

#send <user.cursorless_target>:
    #user.terminal_chicken_send_command_on_line_with_cursorless_target_to_terminal(cursorless_target, "Terminal")
    #edit.file_end()