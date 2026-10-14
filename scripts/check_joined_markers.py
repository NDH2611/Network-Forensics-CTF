from pathlib import Path

folder = Path("output/rfcland-selected")

names = [
    "test-669-746-1565.jpg",
    "test-first-four.jpg",
    "test-all-five.jpg",
]

for name in names:
    data = (folder / name).read_bytes()

    positions = [
        index
        for index in range(len(data) - 1)
        if data[index:index + 2] == b"\xff\xd9"
    ]

    print("File:", name)
    print("Size:", len(data))
    print("Starts with FF D8:", data.startswith(b"\xff\xd8"))
    print("Ends with FF D9:", data.endswith(b"\xff\xd9"))
    print("FF D9 byte positions:", positions)
    print()