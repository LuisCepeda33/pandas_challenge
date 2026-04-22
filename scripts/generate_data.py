from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_generation import generate_all_datasets


if __name__ == "__main__":
    saved = generate_all_datasets()
    print("Generated files:")
    for filename, path in saved.items():
        print(f"- {filename}: {path}")
