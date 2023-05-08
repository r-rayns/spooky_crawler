class Dictionary():
    def __init__(self, value):
        self.value = value
        self.error = None

    # safely retrieve value from dictionary else set value to None
    def safeGet(self, *keys):
      error_occurred = False
      for index, key in enumerate(keys):
        if self.value is None:
          # value is none we won't be able to access any properties on it, error
          error_occurred = True
          break

        try:
          self.value = self.value[key]
        except KeyError:
          if(index == len(keys) - 1):
            # no key worked, error
            error_occurred = True
            break

      if error_occurred:
        self.error = KeyError
        self.value = None
        return self

      return self


    # sets value to the result of a function if
    # original value could not be retrieved from the dictionary
    def onError(self, fn):
        if self.error:
            self.value = fn()
        return self
