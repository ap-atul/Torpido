"""
Main logger class to print to console based on the modes selected or passed. Utility modes support ASCII color formats.

Android style logging system!
"""


class Log:
    """
    Contains four variety of function each with different color

    Attributes
    ----------
    Log.modes : dict
    storing mode string and color

    {"mode" : "color"}

    Examples
    ---------
    >>> Log.e("The input file does not exists")
    >>> Log.d("Loading the input data")
    >>> Log.w("Parsing with deprecated LParser")
    >>> Log.i("Parsing was successful")
    """
    modes = dict()
    modes['DEBUG'] = '\033[92m'
    modes['ERROR'] = '\033[91m'
    modes['INFO'] = '\033[94m'
    modes['WARN'] = '\033[93m'

    @staticmethod
    def log(message, mode='INFO'):
        """
        Logs input message with color defined by the mode and a tag of that mode.

        Parameters
        ----------
        message : any
        input message to print
        mode : str
        mode to print. Available options:

        'DEBUG' : green color text with tag of [DEBUG]
        'ERROR' : red color text with tag of [ERROR]
        'INFO' : blue color text with tag of [INFO]
        'WARN' : yellow color text with tag of [WARN]
        """
        print(f"{Log.modes[mode]}[{mode}] {message}")

    @staticmethod
    def d(message):
        """
        Logs in debug mode, internally calls main log function which
        prints the message in `DEBUG` mode

        Parameters
        ----------
        message : str
        normal string to print function any fstring or
        format strings can be possible
        """
        Log.log(message, mode='DEBUG')

    @staticmethod
    def i(message):
        """
        Logs in info mode, internally calls main log function which
        prints the message in `INFO` mode

        Parameters
        ----------
        message : str
        normal string to print function any fstring or
        format strings can be possible
        """
        Log.log(message, mode='INFO')

    @staticmethod
    def e(message):
        """
        Logs in error mode, internally calls main log function which
        prints the message in `ERROR` mode

        Parameters
        ----------
        message : str
        normal string to print function any fstring
        or format strings can be possible
        """
        Log.log(message, mode='ERROR')

    @staticmethod
    def w(message):
        """
        Logs in warning mode, internally calls main log function which
        prints the message in `WARN` mode

        Parameters
        ----------
        message : str
        normal string to print function any fstring or
        format strings can be possible
        """
        Log.log(message, mode='WARN')
