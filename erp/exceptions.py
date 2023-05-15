class NotFound(Exception):
    def __init__(self, *args, **errors):
        self.message = "Resource Not Found "
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class UnauthorizedAccess(Exception):
    def __init__(self, *args, **errors):
        self.message = "Unauthorized Access "
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class AlreadyExist(Exception):
    def __init__(self, *args, **errors):
        self.message = "Already Exist "
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)
