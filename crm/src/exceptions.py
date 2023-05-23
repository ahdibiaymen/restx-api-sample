class NotFound(Exception):
    def __init__(self, *args, **errors):
        self.message = "Resource Not Found "
        self.errors = errors
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class UnauthorizedAccess(Exception):
    def __init__(self, *args, **errors):
        self.message = "Unauthorized Access "
        self.errors = errors
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class AlreadyExist(Exception):
    def __init__(self, *args, **errors):
        self.message = "Already Exist "
        self.errors = errors
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class OrderAborted(Exception):
    def __init__(self, *args, **errors):
        self.message = "OrderAborted "
        self.errors = errors
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class BadJWTSignature(Exception):
    def __init__(self, **errors):
        self.message = "JWT signature is invalid"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class NoOperation(Exception):
    def __init__(self, reason=False):
        self.message = "No operation needed"
        if reason:
            self.message += f": {reason}"
        super().__init__(self.message)


class ParameterError(Exception):
    def __init__(self, **errors):
        self.message = "Arguments passed are invalid"
        self.errors = errors
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class DBError(Exception):
    def __init__(self, *args, **errors):
        self.message = "Database error "
        self.errors = errors
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)
