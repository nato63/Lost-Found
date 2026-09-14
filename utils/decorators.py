from functools import wraps


def login_required(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            print("Please login first.")
            return None
        return function(self, *args, **kwargs)

    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            print("Please login first.")
            return None

        if self.current_user.role != "admin":
            print("Admin access required.")
            return None

        return function(self, *args, **kwargs)

    return wrapper
