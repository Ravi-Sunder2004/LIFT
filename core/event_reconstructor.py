class EventReconstructor:

    def reconstruct(self, serial, timestamp, categorized_event):

        identity = categorized_event.get("identity", {})
        process = categorized_event.get("process", {})
        session = categorized_event.get("session", {})
        filesystem = categorized_event.get("filesystem", {})

        who = identity.copy()

        action = {}

        for field in ["syscall", "success", "exit"]:
            if field in process:
                action[field] = process[field]

        process_info = {}

        for field in ["pid", "ppid", "exe", "comm"]:
            if field in process:
                process_info[field] = process[field]

        target = {}

        if "paths" in filesystem:
            target["paths"] = filesystem["paths"]

        context = {}

        for field in ["cwd", "ses", "tty"]:

            if field in session:
                context[field] = session[field]

            if field in filesystem:
                context[field] = filesystem[field]

        return {

            "serial": serial,

            "timestamp": timestamp,

            "who": who,

            "action": action,

            "process_info": process_info,

            "target": target,

            "context": context,

            "raw_categories": categorized_event
        }