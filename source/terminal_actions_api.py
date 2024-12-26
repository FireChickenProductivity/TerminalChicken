from talon import Module, actions

module = Module()
@module.action_class
class Actions:
    def terminal_chicken_next_terminal():
        """Advances to the next terminal"""
        actions.app.window_next()
    
    def terminal_chicken_last_terminal():
        """Advances to the previous terminal"""
        actions.app.window_previous()

    def terminal_chicken_return():
        """Returns to the controlling program"""
        actions.user.switcher_focus("Code")

    