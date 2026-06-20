
class EventReconstructor:

    def reconstruct(self,serial,timestamp,categorized_event):
        identity = categorized_event.get("identity", {})
        process = categorized_event.get("process", {})
        session = categorized_event.get("session", {})
        filesystem = categorized_event.get("filesystem", {})

        who=identity.copy()

        action = {}

        for field in ["syscall","success","exit"]:
            if field in process:
                action[field]=process[field]

        process_info = {}

        for field in ["pid","ppid","exe","comm"]:
            if field in process:
                process_info[field]=process[field]
            
        target = {}

        if "paths" in filesystem:
            target["paths"]=filesystem["paths"]

        context={}

        for field in ["cwd","ses","tty"]:
            if field in session:
                context[field]=session[field]

            if field in filesystem:
                context[field]=filesystem[field]

        return {
            "serial":serial,
            "timestamp":timestamp,
            "who": who,

            "action": action,

            "process_info":process_info,

            "target": target,

            "context": context,
            "raw_categories":categorized_event
        }

if __name__ == "__main__":

    sample_event = {

        "identity": {
            "uid": "kali",
            "auid": "kali"
        },

        "process": {
            "pid": "1217",
            "ppid": "996",
            "exe": "/usr/bin/xfdesktop",
            "comm": "xfdesktop",
            "syscall": "unlink"
        },

        "session": {
            "ses": "2",
            "tty": "(none)"
        },

        "filesystem": {
            "cwd": "/home/kali",
            "name": "/tmp/test.txt"
        }
    }

    reconstructor = EventReconstructor()

    result = reconstructor.reconstruct(sample_event)

    import json

    print(json.dumps(result, indent=4))