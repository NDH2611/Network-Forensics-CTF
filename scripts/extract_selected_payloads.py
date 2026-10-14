import csv
import json
import base64
import hashlib
from pathlib import Path

selected = {669, 746, 1565, 1712, 1719}
output_dir = Path("output/rfcland-selected")
output_dir.mkdir(parents=True, exist_ok=True)

with Path("evidence/rfcland-client-payloads.tsv").open(
    encoding="utf-8-sig", newline=""
) as source:
    rows = list(csv.reader(source, delimiter="\t"))

for frame, stream, sequence, length, payload_hex in sorted(
    rows, key=lambda row: int(row[0])
):
    if int(frame) not in selected:
        continue

    payload = bytes.fromhex(payload_hex.replace(":", ""))
    data = json.loads(payload.decode("utf-8"))["data"]

    padding = (-len(data)) % 4
    if padding == 3:
        raise ValueError("Length modulo 4 is 1; stop for inspection.")

    decoded = base64.b64decode(data + "=" * padding, validate=True)

    prefix = output_dir / f"frame-{frame}-stream-{stream}"
    prefix.with_suffix(".json").write_bytes(payload)
    prefix.with_suffix(".bin").write_bytes(decoded)

    print("Frame:", frame, "| Stream:", stream)
    print("Padding added:", padding, "| Decoded bytes:", len(decoded))
    print("First 16:", decoded[:16].hex(" ").upper())
    print("Last 16:", decoded[-16:].hex(" ").upper())
    print("SHA256:", hashlib.sha256(decoded).hexdigest())
    print()