class SessionManager:
    def __init__(self):
        self.sessions = {}

    def add_session(self, session):
        self.sessions[session.id] = session

    def remove_session(self, session):
        self.sessions.pop(session.id)

    def get_session(self, session_id):
        return self.sessions.get(session_id)