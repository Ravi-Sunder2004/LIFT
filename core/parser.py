import re
import json
import os
from typing import Dict,Any,Optional

class AuditParser:

    def parse_line(self,line:str)->Dict[str,Any]:

        audit_record={
            "record_type":None,
            "serial":None,
            "timestamp":None,
            "fields":{}
        }

        record_match = re.search(r"type=(\w+)",line)

        if record_match:
            audit_record["record_type"]=record_match.group(1)

        audit_match=re.search(r"msg=audit\((.*):(\d+)\)",line)
        if audit_match:

            audit_record["timestamp"] = audit_match.group(1)
            audit_record["serial"] = audit_match.group(2)

        tokens = line.split()

        for token in tokens:
            if"=" not in token:
                continue
            key,value = token.split("=",1)

            if key in ["type","msg"]:
                continue

            audit_record["fields"][key]=value
        return audit_record


parser = AuditParser()

with open("samples/output.txt") as f:
    for line in f:
        if line.strip():
            record = parser.parse_line(line)
            print(json.dumps(record,indent=4))
