from colorama import Fore, Style

class BaseCheck(object):
    def __init__(self, context):
        self.context = context
        self.error_count = 0
        self.warning_count = 0

    def error(self, message):
        self.error_count += 1
        self.print_message('     ERROR: ' + message, Fore.RED)

    def warn(self, message):
        self.warning_count += 1
        self.print_message('     WARN: ' + message, Fore.YELLOW)

    def info(self, message):
        self.print_message('     INFO: ' +  message, Fore.GREEN)

    def print_message(self, message, color):
        print color + message + Style.RESET_ALL
