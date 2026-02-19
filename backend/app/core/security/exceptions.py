class SecurityException(Exception):
    pass


class RateLimitExceeded(SecurityException):
    pass


class ValidationError(SecurityException):
    pass

