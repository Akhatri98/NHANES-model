from pathlib import Path

RANDOM_SEED = 42

# directory structure
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_CSV_DIR = ROOT_DIR / "data" / "raw_csv"
RAW_XPT_DIR = ROOT_DIR / "data" / "raw_xpt"
CLEAN_DIR = ROOT_DIR / "data" / "clean_data"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)