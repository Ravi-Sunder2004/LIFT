import json

class SessionTracker:

    def __init__(self):
        self.sessions={}

    def add_event(self,logical_event):

        auid=logical_event["who"].get("auid")
        ses = logical_event["context"].get("ses")

        session_key=f"{auid}:{ses}"

        if session_key not in self.sessions:
            self.sessions[session_key]=[]

        self.sessions[session_key].append(logical_event)

    def get_sessions(self):
        return self.sessions