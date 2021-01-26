from threading import Thread


class Threader:
    @staticmethod
    def rip(function_to_rip, args):
        Thread(target=function_to_rip, args=args).start()
