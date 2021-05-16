#! etc/bin/python3

from colorama import init, Fore, Style



class TerminalColor:

    init()
    colors = {
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
        "cyan": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "reset": Style.RESET_ALL
    }


    def green(self, string):
        print(self.colors["green"] + str(string))


    def yellow(self, string):
        print(self.colors["yellow"] + str(string))


    def red(self, string):
        print(self.colors["red"] + str(string))


    def cyan(self, string):
        print(self.colors["cyan"] + str(string))


    def magenta(self, string):
        print(self.colors["magenta"] + str(string))


    def reset(self, string):
        print(self.colors["reset"] + str(string))

