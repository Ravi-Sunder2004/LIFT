import sys
import json

from core.parser import AuditParser
from core.assembler import EventAssembler
from core.event_reconstructor import EventReconstructor
from core.session import SessionTracker


def export_sessions(source_file, destination_file):

    parser = AuditParser()
    assembler = EventAssembler()
    reconstructor = EventReconstructor()
    session_tracker = SessionTracker()

    with open(source_file, "r") as file:

        for line in file:

            if not line.strip():
                continue

            record = parser.parse_line(line)

            assembler.process_record(record)

    for serial, records in assembler.logical_events.items():

        categorized = assembler.categorize_fields(records)

        timestamp = records[0]["timestamp"]

        logical_event = reconstructor.reconstruct(
            serial,
            timestamp,
            categorized
        )

        session_tracker.add_event(logical_event)

    sessions = session_tracker.get_sessions()

    with open(destination_file, "w") as file:
        json.dump(
            sessions,
            file,
            indent=4
        )

    print(f"Exported sessions to {destination_file}")


if __name__ == "__main__":

    if len(sys.argv) != 3:

        print(
            "Usage: python lift.py <audit_log> <output_json>"
        )

        sys.exit(1)

    export_sessions(
        sys.argv[1],
        sys.argv[2]
    )