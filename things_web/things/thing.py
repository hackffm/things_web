

class Thing(object):
    """docstring for Thing."""

    def __init__(self, id, debug=False):
        self.debug = debug
        self.id = id

    def handle_message(self, message):
        print(message)
