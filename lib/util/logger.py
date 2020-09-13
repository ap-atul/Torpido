"""
Logger to print the content to the command line or the
UI, for printing in the command line it uses various 
colors to make it highly readable
Diff functions can be used to call diff color modes
"""


class Log:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    printing = True

    @staticmethod
    def setPrint(mode=True):
        """
        to print the logs or not
        :param mode: bool
        :return: none
        """
        Log.printing = mode

    @staticmethod
    def log(message, mode='INFO'):
        """
        string is printed using mode (color)
        :param message: str, msg to print
        :param mode: str, mode color
        :return: none
        """
        if Log.printing:
            if mode == 'INFO':
                color = Log.BLUE
            elif mode == 'DEBUG':
                color = Log.GREEN
            elif mode == 'WARN':
                color = Log.YELLOW
            else:
                color = Log.RED

            print(f"{color}[{mode}] {message}")

    @staticmethod
    def d(message):
        """
        debug log function
        :param message: str
        :return: none
        """
        Log.log(message, mode='DEBUG')

    @staticmethod
    def i(message):
        """
        info log function
        :param message: str
        :return: none
        """
        Log.log(message, mode='INFO')

    @staticmethod
    def e(message):
        """
        error log function
        :param message: str
        :return: none
        """
        Log.log(message, mode='ERROR')

    @staticmethod
    def w(message):
        """
        warning log function
        :param message: str
        :return: none
        """
        Log.log(message, mode='WARN')
