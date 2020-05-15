
class InsertError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InsertError, {0}'.format(self.message)
        else:
            return 'InsertError has been raised.'

class UpdateError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'UpdateError, {0}'.format(self.message)
        else:
            return 'UpdateError has been raised.'

class DeleteError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'DeleteError, {0}'.format(self.message)
        else:
            return 'DeleteError has been raised.'

class FetchError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'FetchError, {0}'.format(self.message)
        else:
            return 'FetchError has been raised.'

class InputError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'InputError, {0}'.format(self.message)
        else:
            return 'InputError has been raised.'