from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List
import base64, io

import numpy as np
import cv2
from PIL import Image

from mmocr.apis import MMOCRInferencer
from .config import CFG, DetectorConfig


def _ensure_rgb(img: np.ndarray) -> np.ndarray:
    """If image is BGR (OpenCV default), convert to RGB."""
    if img.ndim == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def _maybe_resize(img: np.ndarray, max_long_side: int | None) -> np.ndarray:
    """Downscale very large images to speed inference (keeps aspect)."""
    if max_long_side is None:
        return img
    h, w = img.shape[:2]
    long_side = max(h, w)
    if long_side <= max_long_side:
        return img
    scale = max_long_side / long_side
    new_w, new_h = int(w * scale), int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)


class DetectText:
    def __init__(self, cfg: DetectorConfig | None = None) -> None:
        self.cfg = cfg or CFG
        # Build MMOCR inferencer once
        self.infer = MMOCRInferencer(det=self.cfg.det_model, device=self.cfg.device)

    def _infer(self, img_rgb: np.ndarray) -> List[Dict[str, Any]]:
        """Run detection and return list of {points, score}."""
        result = self.infer(img_rgb, return_vis=False)
        preds = result["predictions"][0]
        polys = preds.get("det_polygons", [])
        scores = preds.get("det_scores", [])
        boxes: List[Dict[str, Any]] = []
        for poly, sc in zip(polys, scores):
            pts = np.array(poly, dtype=np.float32).reshape(-1, 2).tolist()
            boxes.append({"points": pts, "score": float(sc)})
        return boxes

    def run_on_image(self, image: np.ndarray | str | Path) -> Dict[str, Any]:
        """
        Accepts a numpy image (BGR or RGB) or a path.
        Applies optional resize for speed; outputs coords in resized space.
        """
        if isinstance(image, (str, Path)):
            img_bgr = cv2.imread(str(image), cv2.IMREAD_COLOR)
            if img_bgr is None:
                raise FileNotFoundError(f"Cannot read image: {image}")
        else:
            img_bgr = image

        img_rgb = _ensure_rgb(img_bgr)
        img_rgb = _maybe_resize(img_rgb, self.cfg.max_long_side)

        boxes = self._infer(img_rgb)
        h, w = img_rgb.shape[:2]
        return {"boxes": boxes, "input_size": {"width": w, "height": h}}

    @staticmethod
    def from_data_url(data_url: str) -> np.ndarray:
        """Decode a dataURL ('data:image/png;base64,...') → BGR numpy image."""
        header, b64 = data_url.split(",", 1)
        raw = base64.b64decode(b64)
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        arr = np.array(img)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    def describe(self) -> dict:
        """Return current config as a plain dict (for logging)."""
        return asdict(self.cfg)
