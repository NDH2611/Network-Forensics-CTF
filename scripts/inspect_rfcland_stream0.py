import json
import base64
import binascii
from pathlib import Path

input_path = Path("evidence/rfcland-stream-0-client.json")
raw = input_path.read_bytes()

print("Input file:", input_path)
print("Input size:", len(raw), "bytes")

text = raw.decode("utf-8-sig")
document = json.loads(text)
data = document["data"]

print("JSON parsed successfully")
print("Data length:", len(data), "characters")
print("Length modulo 4:", len(data) % 4)
print("Data prefix:", data[:20])

try:
    decoded = base64.b64decode(data, validate=True)
except binascii.Error as error:
    print("Base64 decoding failed:", error)
else:
    print("Base64 decoding succeeded")
    print("Decoded size:", len(decoded), "bytes")
    print("First 16 bytes:", decoded[:16].hex(" ").upper())
    print("Last 16 bytes:", decoded[-16:].hex(" ").upper())

    output_path = Path("output/rfcland-stream-0.bin")
    output_path.write_bytes(decoded)
    print("Output saved:", output_path)