import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "static"
TARGET = ROOT / "public" / "static"

EXCLUDED_DIRS = {
    "__pycache__",
    "comprovantes",
}


def ignore_entries(directory, names):
    ignored = []
    for name in names:
        path = Path(directory) / name
        if path.is_dir() and name in EXCLUDED_DIRS:
            ignored.append(name)
    return ignored


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Pasta static nao encontrada: {SOURCE}")

    if TARGET.exists():
        shutil.rmtree(TARGET)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, TARGET, ignore=ignore_entries)
    print(f"Static preparado para Vercel: {TARGET}")


if __name__ == "__main__":
    main()
