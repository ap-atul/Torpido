"""
Class to print normal prints with strings
but with colors
"""


class Log:
    modes = dict()
    modes['DEBUG'] = '\033[92m'
    modes['ERROR'] = '\033[91m'
    modes['INFO'] = '\033[94m'
    modes['WARN'] = '\033[93m'
    printing = True
    onlyInfo = False

    def log(self, mode='INFO'):
        """
        read the message and printing color
        based on the mode from the dict
        :param mode: str
        :return: None
        """
        if Log.onlyInfo:
            if mode is "INFO":
                print(f"{Log.modes[mode]}[{mode}] {self}", flush=True)
                return

        print(f"{Log.modes[mode]}[{mode}] {self}", flush=True)

    @staticmethod
    def setOnlyInfo(which):
        Log.onlyInfo = which

    @staticmethod
    def setPrint(mode=True):
        Log.printing = mode

    @staticmethod
    def d(message):
        Log.log(message, mode='DEBUG')

    @staticmethod
    def i(message):
        Log.log(message, mode='INFO')

    @staticmethod
    def e(message):
        Log.log(message, mode='ERROR')

    @staticmethod
    def w(message):
        Log.log(message, mode='WARN')
