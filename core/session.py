import os
import json


class SessionTracker:
    def __init__(self):
        self.active_sessions = {}

    def process_event(self,record):
        if "ses" not in record:
            return None

        ses_id = str(record["ses"])
        current_uid = record.get("uid")

        if ses_id not in self.active_sessions:
            self.active_sessions[ses_id]={
                "session owner": current_uid,
                "events":[],
                "user_activity": {}
            }
        session = self.active_sessions[ses_id]
        session["events"].append(record)

        if current_uid not in session["user_activity"]:
            session["user_activity"][current_uid]=[]
        session["user_activity"][current_uid].append(record)


if __name__ == "__main__":
    tracker = SessionTracker()
    json_file = "../parsed.json"

    with open(json_file,"r") as file:
        records=json.load(file)
        for record in records:
            tracker.process_event(record)
    print(json.dumps(tracker.active_sessions,indent=4))