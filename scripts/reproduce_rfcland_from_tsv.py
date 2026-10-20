from pathlib import Path
import base64
import hashlib
import json

source = Path("evidence/rfcland-reproduce-selected.tsv")
rows = source.read_text(encoding="utf-8-sig").splitlines()

parts = []
previous_frame = -1

for row in rows:
    frame_text, stream_text, payload_hex = row.split("\t")
    frame = int(frame_text)

    if frame <= previous_frame:
        raise ValueError("Frames are not in increasing order")
    previous_frame = frame

    payload = bytes.fromhex(payload_hex.replace(":", ""))
    obj = json.loads(payload)
    data = obj["data"]
    parts.append(data)

    print(f"Frame {frame} | Stream {stream_text} | Characters {len(data)}")

joined = "".join(parts)
decoded = base64.b64decode(joined, validate=True)

output = Path("output/rfcland-reproduced.jpg")
output.write_bytes(decoded)

reference = Path("output/rfcland-selected/test-base64-joined-first.jpg")
same = decoded == reference.read_bytes()

print("Selected packets:", len(parts))
print("Combined characters:", len(joined))
print("Decoded bytes:", len(decoded))
print("Starts with FF D8:", decoded.startswith(b"\xff\xd8"))
print("Ends with FF D9:", decoded.endswith(b"\xff\xd9"))
print("SHA256:", hashlib.sha256(decoded).hexdigest())
print("Matches previous artifact byte-for-byte:", same)
print("Output:", output)

if not same:
    raise ValueError("Reproduced artifact differs from previous artifact")