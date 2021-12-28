class Dictionary():
    def __init__(self, value):
        self.value = value
        self.error = None

    # safely retrieve value from dictonary else set value to None
    def safeGet(self, *keys):
        for index, key in enumerate(keys):
            try:
                self.value = self.value[key]
            except KeyError:
                if(index == len(keys) - 1):
                    # no key worked, error
                    self.error = KeyError
                    self.value = None
                    return self
        return self

    # sets value to the result of a function if
    # original value could not be retrieved from the dictonary
    def onError(self, fn):
        if self.error:
            self.value = fn()
        return self
