class EcommerceException(Exception):
    pass


class NotFoundException(EcommerceException):
    pass


class ValidationException(EcommerceException):
    pass


class AuthenticationException(EcommerceException):
    pass


class AuthorizationException(EcommerceException):
    pass


class StockException(EcommerceException):
    pass


class PaymentException(EcommerceException):
    pass
