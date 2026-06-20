import json
from parser import AuditParser
from field_registry import FIELD_CATEGORIES
from event_reconstructor import EventReconstructor

#function called process record with self and record as inputs

#check if serial has none value
#get serial using record.get
#if not note then check if it exists in logical events, if no create empty list
#if yes append it to the logical event

class EventAssembler:

#a constructor creating a dictionary called logical_Events
    def __init__(self):
        self.logical_events={}

    def process_record(self, record):

        serial = record.get("serial")

        if serial is None:
            return

        if serial not in self.logical_events:
            self.logical_events[serial] = []

        self.logical_events[serial].append(record)


    def categorize_fields(self,records):
        categorized = {

        "identity":{},
        "process":{},
        "session":{},
        "filesystem":{}
        }

        for record in records:
            fields = record.get("fields",{})

            for key,value in fields.items():
                for category,known_fields in FIELD_CATEGORIES.items():
                    if key in known_fields:
                        if category == "filesystem" and key == "name":
                            if "paths" not in categorized["filesystem"]:
                                categorized["filesystem"]["paths"] = []
                            categorized["filesystem"]["paths"].append(value)

                        else:
                            categorized[category][key] = value

        return categorized



  #main function

if __name__=="__main__":

    assembler=EventAssembler()
    parser = AuditParser()
    reconstructor=EventReconstructor()

    with open("samples/output.txt","r") as file:

        for line in file:

            if not line.strip():
                continue

            record = parser.parse_line(line)

            assembler.process_record(record)
    
    for serial, records in assembler.logical_events.items():

        print(f"\n===== EVENT {serial} =====")

        categorized = assembler.categorize_fields(records)
        timestamp = records[0]["timestamp"]
        logical_event = reconstructor.reconstruct(serial,timestamp,categorized)

        print(
            json.dumps(
            logical_event,
            indent=4
            )
        )

        break