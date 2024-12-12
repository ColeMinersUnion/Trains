from PyQt6.QtCore import QTimer, QObject
import functools

class DelayedExecutor(QObject):
    def __init__(self):
        super().__init__()
        self.delayed = 0

    def delay(self):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                def execute():
                    func(*args, **kwargs)

                timer = QTimer()
                timer.setSingleShot(True)
                timer.timeout.connect(execute)
                timer.start(int(self.delayed * 1000))  # Convert seconds to milliseconds

                # Keep a reference to the timer to prevent it from being garbage collected
                wrapper.timers.append(timer)

            wrapper.timers = []  # Hold references to timers
            return wrapper
        return decorator