import pandas as pd
from utils import RAW_CSV_DIR, TRAIN_CSV, VAL_CSV, TEST_CSV, RANDOM_SEED, TRAIN_FRAC, VAL_FRAC

INPUT_CSV = RAW_CSV_DIR / "cleaned_patients.csv"


def main():
    df = pd.read_csv(INPUT_CSV)

    df = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)

    n = len(df)
    train_end = int(n * TRAIN_FRAC)
    val_end   = int(n * (TRAIN_FRAC + VAL_FRAC))

    train = df.iloc[:train_end]
    val   = df.iloc[train_end:val_end]
    test  = df.iloc[val_end:]

    print(f"Begin writing train CSV.")
    train.to_csv(TRAIN_CSV, index=False)

    print(f"Begin writing val CSV.")
    val.to_csv(VAL_CSV, index=False)

    print(f"Begin writing test CSV.")
    test.to_csv(TEST_CSV, index=False)

    print("Finished splitting CSV.")


if __name__ == "__main__":
    main()