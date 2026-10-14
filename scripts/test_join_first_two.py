from pathlib import Path
import hashlib

folder = Path("output/rfcland-selected")

first_path = folder / "frame-669-stream-95.bin"
second_path = folder / "frame-746-stream-106.bin"

first = first_path.read_bytes()
second = second_path.read_bytes()

combined = first + second

output_path = folder / "test-669-746.jpg"
output_path.write_bytes(combined)

print("Order: frame 669 -> frame 746")
print("First bytes:", len(first))
print("Second bytes:", len(second))
print("Combined bytes:", len(combined))
print("SHA256:", hashlib.sha256(combined).hexdigest())
print("Output:", output_path)