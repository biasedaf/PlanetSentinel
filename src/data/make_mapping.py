# src/data/make_mapping.py
import argparse, os, csv
from pathlib import Path

def make_mapping(processed_dir, out_csv):
    before_dir = Path(processed_dir) / "before"
    after_dir  = Path(processed_dir) / "after"
    masks_dir  = Path(processed_dir) / "masks"

    if not before_dir.exists() or not after_dir.exists() or not masks_dir.exists():
        raise SystemExit(f"Missing dirs: {before_dir}, {after_dir}, or {masks_dir}")

    # assume matching filenames between before/after/masks
    files = sorted([p.name for p in before_dir.iterdir() if p.is_file()])
    if len(files) == 0:
        raise SystemExit("No files found in before/ directory")

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["before", "after", "mask"])
        for name in files:
            b = str((before_dir / name).resolve())
            a = str((after_dir  / name).resolve())
            m = str((masks_dir  / name).resolve())
            # only write if all three exist
            if Path(a).exists() and Path(m).exists():
                writer.writerow([b, a, m])
    print(f"Wrote mapping to {out_csv}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--processed", default="data/processed")
    p.add_argument("--out", default="data/processed/mapping_levir_processed.csv")
    args = p.parse_args()
    make_mapping(args.processed, args.out)
