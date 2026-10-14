import json
import hashlib
from pathlib import Path

table_path = Path("evidence/rfcland-stream0-client-payload.tsv")
table_bytes = table_path.read_bytes()

if table_bytes.startswith((b"\xff\xfe", b"\xfe\xff")):
    table_text = table_bytes.decode("utf-16")
else:
    table_text = table_bytes.decode("utf-8-sig")

rows = [line for line in table_text.splitlines() if line.strip()]
print("Payload rows:", len(rows))

if len(rows) != 1:
    raise SystemExit("Expected one payload row; stop for inspection.")

frame, sequence, length, hex_payload = rows[0].split("\t")
pcap_payload = bytes.fromhex(hex_payload.replace(":", ""))

exported_json = Path(
    "evidence/rfcland-stream-0-client.json"
).read_bytes()

print("Frame:", frame)
print("TCP sequence:", sequence)
print("TCP length:", length)
print("Extracted payload bytes:", len(pcap_payload))
print("Exported JSON bytes:", len(exported_json))
print("Byte-for-byte identical:", pcap_payload == exported_json)

print("Payload SHA256:", hashlib.sha256(pcap_payload).hexdigest())
print("JSON SHA256:", hashlib.sha256(exported_json).hexdigest())

document = json.loads(pcap_payload.decode("utf-8"))
data = document["data"]

print("Data length directly from PCAP:", len(data))
print("Length modulo 4:", len(data) % 4)