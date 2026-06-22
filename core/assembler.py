from core.parser import AuditParser
from core.field_registry import FIELD_CATEGORIES
from core.event_reconstructor import EventReconstructor
from core.session import SessionTracker



#check if serial has none value
#get serial using record.get
#if not note then check if it exists in logical events, if no create empty list
#if yes append it to the logical event

class EventAssembler:

#a constructor creating a dictionary called logical_Events
    def __init__(self):
        self.logical_events={}
#function called process record with self and record as inputs
    def process_record(self, record):
    #extracting the serial number from the audit record
        serial = record.get("serial")
    #if there is no serial number associated with the record just return none
        if serial is None:
            return
    #if the particular serial number is not present in the logical events list, then we are adding it
        if serial not in self.logical_events:
            self.logical_events[serial] = []

        self.logical_events[serial].append(record)

# a reconstructing method that categorizes the parsed records based on identity,process,session and filesystem artifacts
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

