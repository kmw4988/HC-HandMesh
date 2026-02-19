"""Export hand mesh face data from .npy to JSON for web demo."""

import json
import os
import numpy as np


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    faces_path = os.path.join(project_root, "template", "right_faces.npy")

    faces = np.load(faces_path).astype(int).tolist()
    print(f"Loaded {len(faces)} faces from {faces_path}")

    hand_data = {"faces": faces}

    out_path = os.path.join(script_dir, "hand_data.json")
    with open(out_path, "w") as f:
        json.dump(hand_data, f)

    print(f"Saved hand_data.json ({os.path.getsize(out_path)} bytes) to {out_path}")


if __name__ == "__main__":
    main()
