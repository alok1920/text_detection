from dataclasses import dataclass, field 
from pathlib import Path 

@dataclass
class DetectorConfig:
    det_model: str = "DBNet" 
    device: str = "mps" 
    det_weights: str | None = None 

    box_thresh: float = 0.6
    mask_thresh: float = 0.5
    '''
    If detection score < box_thresh, ignore it.
    These are just defaults—you’ll learn to tune them later.
    '''

    max_long_side: int | None = 1600 
    draw_scores: bool = True
    line_thickness: int = 2
    font_scale: float = 0.6
    '''
    max_long_side: if an image is huge (like 4000 px wide), resize down to 1600 px for faster inference.
    draw_scores: whether to draw the confidence scores on images.
    outputs_dir and vis_dir: default save locations.
    '''

    outputs_dir: Path = field(default=Path("outputs"))
    vis_dir: Path = field(default=Path("outputs/vis"))

CFG = DetectorConfig()
