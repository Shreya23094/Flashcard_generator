import json
import csv
import io

def export_as_json(cards):
    return json.dumps(cards, indent=2).encode("utf-8")

def export_as_csv(cards):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["question", "answer"])
    writer.writeheader()
    writer.writerows(cards)
    return output.getvalue().encode("utf-8")
