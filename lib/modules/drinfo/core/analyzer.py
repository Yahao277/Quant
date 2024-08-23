
class Analyzer:
    def __init__(self):
        self.sessions_count = 0
        self.reset()
        return

    def analyze(self, session_data: dict, context):
        self.sessions_count += 1

    def report(self):
        return {
            'sessions_count': self.sessions_count,
        }

    def reset(self):
        self.sessions_count = 0
