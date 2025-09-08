#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse
import json

import numpy as np
import cv2

from detector.config import CFG


def draw_polys(img, boxes, draw_scores=True, color=(0, 255, 0)):
    for b in boxes:
        pts = np.array(b["points"], dtype=np.int32).reshape(-1, 1, 2)
        cv2.polylines(img, [pts], isClosed=True, color=color, thickness=CFG.line_thickness)
        if draw_scores and "score" in b:
            x, y = b["points"][0]
            cv2.putText(
                img,
                f"{b['score']:.2f}",
                (int(x), int(y) - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                CFG.font_scale,
                color,
                1,
                lineType=cv2.LINE_AA,
            )
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preds", default="outputs/preds.jsonl", help="JSONL from infer_image.py")
    ap.add_argument("--out_dir", default="outputs/vis", help="Directory to save _vis images")
    ap.add_argument("--hide_scores", action="store_true", help="Do not draw score text")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    n = 0
    with open(args.preds, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            img_path = row["file"]
            boxes = row.get("boxes", [])

            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"[skip] cannot read image: {img_path}")
                continue

            vis = draw_polys(img.copy(), boxes, draw_scores=not args.hide_scores)
            out_path = out_dir / (Path(img_path).stem + "_vis.jpg")
            cv2.imwrite(str(out_path), vis)
            print(f"[ok] {Path(img_path).name:>25s} -> {out_path.name:>25s}  boxes: {len(boxes):3d}")
            n += 1

    print(f"\nWrote {n} visualization(s) to: {out_dir}")


if __name__ == "__main__":
    main()
