import unittest

from torpido.pmpi import Communication


class PmpiTest(unittest.TestCase):
    def test_communication(self):
        sent = {"mydata", 200}

        def my_function(data):
            self.assertEqual(data, sent)

        comm = Communication()
        comm.register("ID", my_function)
        sender = comm.sender()

        sender.send("ID", sent)
        comm.end()

    def test_dtype(self):
        sent = {"mydata", 200}

        def my_function(data):
            self.assertEqual(dict, type(data))

        comm = Communication()
        comm.register("ID", my_function)
        comm.unregister("ID")
        sender = comm.sender()

        sender.send("ID", sent)
        comm.end()

    def test_multiple_id(self):
        sent = {"mydata", 200}

        def my_function(data):
            self.assertEqual(dict, type(data))

        comm = Communication()
        comm.register("ID", my_function)
        comm.register("IDE", my_function)
        sender = comm.sender()

        from time import sleep
        sleep(0.1)

        sender.send("ID", sent)
        sender.send("IDE", sent)
        comm.end()


if __name__ == '__main__':
    unittest.main()
