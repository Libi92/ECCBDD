log_enabled = False


class Logger:
    @staticmethod
    def log(*args, display=False):
        if log_enabled:
            print(*args)

        if not log_enabled and display:
            print(*args)
