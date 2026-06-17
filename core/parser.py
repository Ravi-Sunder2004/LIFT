import re
import json
from typing import Dict,Any

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

        field_pattern=re.compile(r'(\w+)=(".*?"|\'.*?\'|\S+)')

        for key, value in field_pattern.findall(line):
            if key in("type","msg"):
                continue
            audit_record["fields"][key]=self.__strip_quotes(value)

        nested_match = re.search(r"msg='([^']*)'",line)
        if nested_match:
            for key,value in field_pattern.findall(nested_match.group(1)):
                audit_record["fields"][key]=self.__strip_quotes(value)
        return audit_record

    @staticmethod

    def __strip_quotes(value:str)->str:
        if len(value)>=2 and value[0] == value[-1] and value[0] in ('"',"'"):
            return value[1:-1]
        return value


if __name__ == "__main__":

    parser = AuditParser()

    with open("samples/output.txt") as f:
        for line in f:
            if line.strip():
                record = parser.parse_line(line)
                print(json.dumps(record,indent=4))

