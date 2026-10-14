from pathlib import Path
import hashlib

folder = Path("output/rfcland-selected")

paths = [
    folder / "frame-669-stream-95.bin",
    folder / "frame-746-stream-106.bin",
    folder / "frame-1565-stream-223.bin",
]

parts = [path.read_bytes() for path in paths]
combined = b"".join(parts)

output_path = folder / "test-669-746-1565.jpg"
output_path.write_bytes(combined)

print("Order: 669 -> 746 -> 1565")
print("Part sizes:", [len(part) for part in parts])
print("Combined bytes:", len(combined))
print("Last 16 bytes:", combined[-16:].hex(" ").upper())
print("SHA256:", hashlib.sha256(combined).hexdigest())
print("Output:", output_path)