from pathlib import Path
import hashlib

folder = Path("output/rfcland-selected")

names = [
    "test-669-746-1565.jpg",
    "test-first-four.jpg",
    "test-all-five.jpg",
]

for name in names:
    source_path = folder / name
    data = source_path.read_bytes()

    if b"\xff\xd9" in data:
        raise ValueError(f"FF D9 already exists in {name}; stop.")

    candidate = data + b"\xff\xd9"
    output_path = folder / f"{source_path.stem}-eoi-test.jpg"
    output_path.write_bytes(candidate)

    print("Source:", name)
    print("Added bytes: FF D9")
    print("Size:", len(data), "->", len(candidate))
    print("SHA256:", hashlib.sha256(candidate).hexdigest())
    print("Output:", output_path)
    print()