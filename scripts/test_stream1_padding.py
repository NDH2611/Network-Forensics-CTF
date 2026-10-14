import json
import base64
from pathlib import Path

input_path = Path("evidence/rfcland-stream-1-client.json")
document = json.loads(input_path.read_text(encoding="utf-8-sig"))
data = document["data"]

padding_count = (-len(data)) % 4
candidate = data + "=" * padding_count

print("Original length:", len(data))
print("Added padding characters:", padding_count)
print("Input file unchanged")

decoded = base64.b64decode(candidate, validate=True)

print("Decoding succeeded")
print("Decoded size:", len(decoded), "bytes")
print("First 16 bytes:", decoded[:16].hex(" ").upper())
print("Last 16 bytes:", decoded[-16:].hex(" ").upper())

output_path = Path("output/rfcland-stream-1-padding-test.bin")
output_path.write_bytes(decoded)
print("Output saved:", output_path)