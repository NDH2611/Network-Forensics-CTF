import csv
import json
import base64
import binascii
from collections import Counter
from pathlib import Path

input_path = Path("evidence/rfcland-client-payloads.tsv")
results = []

with input_path.open(encoding="utf-8-sig", newline="") as source:
    reader = csv.reader(source, delimiter="\t")

    for frame, stream, sequence, length, payload_hex in reader:
        record = {
            "frame": frame,
            "stream": stream,
            "tcp_length": length,
            "data_length": "",
            "modulo_4": "",
            "status": "",
            "padding_added": 0,
            "decoded_bytes": "",
            "jpeg_start": "",
            "jpeg_end": "",
            "error": "",
        }

        try:
            payload = bytes.fromhex(payload_hex.replace(":", ""))
            if len(payload) != int(length):
                raise ValueError("Payload length does not match tcp.len")

            document = json.loads(payload.decode("utf-8"))
            data = document["data"]

            if not isinstance(data, str):
                raise ValueError("data is not a string")

        except (ValueError, KeyError) as error:
            record["status"] = "input_error"
            record["error"] = str(error)
            results.append(record)
            continue

        record["data_length"] = len(data)
        record["modulo_4"] = len(data) % 4
        decoded = None

        try:
            decoded = base64.b64decode(data, validate=True)
            record["status"] = "original_ok"

        except (binascii.Error, ValueError) as error:
            record["status"] = "decode_failed"
            record["error"] = str(error)

            if len(data) % 4 in (2, 3):
                padding = (-len(data)) % 4

                try:
                    decoded = base64.b64decode(
                        data + "=" * padding, validate=True
                    )
                    record["status"] = "padding_test_ok"
                    record["padding_added"] = padding

                except (binascii.Error, ValueError) as padding_error:
                    record["error"] += " | Padding test: " + str(padding_error)

        if decoded is not None:
            record["decoded_bytes"] = len(decoded)
            record["jpeg_start"] = decoded.startswith(b"\xff\xd8\xff")
            record["jpeg_end"] = decoded.endswith(b"\xff\xd9")

        results.append(record)

output_path = Path("evidence/rfcland-payload-survey.csv")

with output_path.open("w", encoding="utf-8-sig", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=list(results[0]))
    writer.writeheader()
    writer.writerows(results)

print("Rows surveyed:", len(results))

for status, count in sorted(Counter(r["status"] for r in results).items()):
    print(status + ":", count)

print("JPEG-start matches:", sum(r["jpeg_start"] is True for r in results))
print("JPEG-end matches:", sum(r["jpeg_end"] is True for r in results))
print("Survey saved:", output_path)