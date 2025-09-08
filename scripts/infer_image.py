#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
import json

from detector.runner import DetectText


def iter_images(p: Path):
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    if p.is_file():
        if p.suffix.lower() in exts:
            yield p
        return
    for fp in sorted(p.rglob("*")):
        if fp.suffix.lower() in exts:
            yield fp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Image file or folder")
    ap.add_argument("--out", default="outputs/preds.jsonl", help="JSONL output path")
    ap.add_argument("--min_score", type=float, default=0.0, help="Filter boxes below this score")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    det = DetectText()

    n_imgs = 0
    n_boxes_total = 0

    with out_path.open("w", encoding="utf-8") as f:
        for img_path in iter_images(Path(args.input)):
            res = det.run_on_image(str(img_path)) 
            boxes = [b for b in res["boxes"] if b["score"] >= args.min_score]
            n_boxes_total += len(boxes)

            line = {"file": str(img_path), "boxes": boxes}
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

            n_imgs += 1
            print(f"[OK] {img_path.name:>25s}  boxes: {len(boxes):3d}")

    print(f"\nDone. Images: {n_imgs}, Total boxes kept: {n_boxes_total}")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
