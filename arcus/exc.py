class InvalidAuth(Exception):

    def __init__(self, value):
        self.value = value
