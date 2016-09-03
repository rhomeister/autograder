from colorama import Fore, Style, init

class ConsoleLogger(object):
    def __init__(self):
        init() # initialize colorama

    def error(self, message):
        self.print_message('     ERROR: ' + message, Fore.RED)

    def warn(self, message):
        self.print_message('     WARN: ' + message, Fore.YELLOW)

    def info(self, message):
        self.print_message('     INFO: ' + message, Fore.GREEN)

    def print_message(self, message, color):
        print color + message + Style.RESET_ALL
