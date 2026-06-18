from pathlib import Path

data_folder = Path("data")

for file in data_folder.glob("*.txt"):
    print(f"\nReading: {file.name}")
    
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    print(content)