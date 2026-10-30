class AppError(Exception):
    """Базовое исключение приложения."""
    pass

class UsernameTakenError(AppError):
    pass

class UserNotFoundError(AppError):
    pass