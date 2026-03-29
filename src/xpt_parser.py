import pandas as pd
from utils import RAW_XPT_DIR, RAW_CSV_DIR, VAR_LABELS

FOLDERS = ["ALQ", "BMX", "DEMO", "DXX", "MCQ", "OSQ", "SMQ"]
OUTPUT_CSV = RAW_CSV_DIR / "cleaned_patients.csv"


def load_folder(folder_name: str) -> pd.DataFrame:
    folder_path = RAW_XPT_DIR / folder_name
    xpt_files = sorted(folder_path.glob("*.xpt"))

    frames = []
    for xpt_file in xpt_files:
        df = pd.read_sas(xpt_file, format="xport", encoding="utf-8")

        # in the off chance SEQN is missing, ignore that file,
        # it's format is incompatible.
        if "SEQN" not in df.columns:
            continue

        df["SEQN"] = df["SEQN"].astype(int)
        keep_cols = ["SEQN"] + [c for c in df.columns if c in VAR_LABELS and c != "SEQN"]
        frames.append(df[keep_cols])

    if not frames:
        return pd.DataFrame()

    folder_df = pd.concat(frames, axis=0, ignore_index=True)
    return folder_df.drop_duplicates(subset=["SEQN"])


def main():
    folder_dfs = {
        folder: df
        for folder in FOLDERS
        if not (df := load_folder(folder)).empty
    }

    # Only OSQ has fracture data, therefore we limit to SEQNs in OSQ only.
    if "OSQ" not in folder_dfs:
        print("No OSQ data found. Cannot proceed.")
        return

    osq_seqns = set(folder_dfs["OSQ"]["SEQN"].unique())

    merged_df = pd.DataFrame()
    folder_presence: dict[str, set] = {}

    for folder, df in folder_dfs.items():
        df_filtered = df[df["SEQN"].isin(osq_seqns)].copy()

        if df_filtered.empty:
            continue

        folder_presence[folder] = set(df_filtered["SEQN"].unique())
        merged_df = df_filtered if merged_df.empty else pd.merge(merged_df, df_filtered, on="SEQN", how="outer")

    if merged_df.empty:
        print("No data after filtering to SEQNs in OSQ.")
        return

    seqn_count = {
        seqn: sum(1 for seqs in folder_presence.values() if seqn in seqs)
        for seqn in merged_df["SEQN"].unique()
    }
    merged_df["file_count"] = merged_df["SEQN"].map(seqn_count)

    known_vars = [c for c in VAR_LABELS if c != "SEQN" and c in merged_df.columns]
    final_cols = ["SEQN", "file_count"] + known_vars
    merged_df = merged_df[final_cols].sort_values("SEQN").reset_index(drop=True)

    print(f"Begin writing CSV.")
    merged_df.to_csv(OUTPUT_CSV, index=False)
    print("Finished writing CSV.")


if __name__ == "__main__":
    main()