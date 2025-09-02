from dataclasses import dataclass, field # lets us define a simple “settings box” without writing extra boilerplate (__init__, etc.).
from pathlib import Path # better than plain strings for file/folder paths (you get methods like .mkdir(), .exists(), etc.).

@dataclass
class DetectorConfig:
    det_model: str = "DBNet" # which detection model
    device: str = "mps"  # choose "mps" (Mac GPU), "cuda" (NVIDIA), "cpu" (fallback).
    det_weights: str | None = None  # if you train your own model later, put the .pth file path here.

    # Add thresholds
    box_thresh: float = 0.6
    mask_thresh: float = 0.5
    '''
    If detection score < box_thresh, ignore it.
    These are just defaults—you’ll learn to tune them later.
    '''

    # Add some drawing + output options
    max_long_side: int | None = 1600  # resize long side if too big (speed up)
    draw_scores: bool = True
    line_thickness: int = 2
    font_scale: float = 0.6
    '''
    max_long_side: if an image is huge (like 4000 px wide), resize down to 1600 px for faster inference.
    draw_scores: whether to draw the confidence scores on images.
    outputs_dir and vis_dir: default save locations.
    '''

    #output folders
    outputs_dir: Path = field(default=Path("outputs"))
    vis_dir: Path = field(default=Path("outputs/vis"))

CFG = DetectorConfig()
'''
Now CFG is an object with all the defaults.
Other files will just from detector.config import CFG.
'''