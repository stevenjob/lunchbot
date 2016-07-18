from Rating import Rating
import time

class Destination():
    def __init__(self):
        self.rating = Rating()
        self.history = []

    def add_visit(self, when = None):
        when_resolved = when
        if when_resolved is None:
            # int() as we get a fraction from time.time()
            when_resolved = int(time.time())
        self.history.append(when_resolved)

    def latest_visit(self):
        if len(self.history) == 0:
            return 0
        return max(self.history)
