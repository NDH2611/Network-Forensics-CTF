from pathlib import Path
import json
import base64
import hashlib

folder = Path("output/rfcland-selected")
names = [
    "frame-669-stream-95.json",
    "frame-746-stream-106.json",
    "frame-1565-stream-223.json",
    "frame-1712-stream-244.json",
    "frame-1719-stream-245.json",
]

parts = []
for name in names:
    obj = json.loads((folder / name).read_bytes())
    parts.append(obj["data"])
    print(f"{name}: {len(obj['data'])} characters")

joined = "".join(parts)
print("Combined characters:", len(joined))
print("Length modulo 4:", len(joined) % 4)

decoded = base64.b64decode(joined, validate=True)

output = folder / "test-base64-joined-first.jpg"
output.write_bytes(decoded)

print("Decoded bytes:", len(decoded))
print("Starts with FF D8:", decoded.startswith(b"\xff\xd8"))
print("Ends with FF D9:", decoded.endswith(b"\xff\xd9"))
print("SHA256:", hashlib.sha256(decoded).hexdigest())
print("Output:", output)