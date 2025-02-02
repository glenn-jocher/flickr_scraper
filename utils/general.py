# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# General utilities for use in image-handling operations
# Written by Glenn Jocher (glenn.jocher@ultralytics.com) for https://github.com/ultralytics

import os
from pathlib import Path

import requests
from PIL import Image


def download_uri(uri, dir="./"):
    """Downloads file from URI, performing checks and renaming; supports timeout and image format suffix addition."""
    # Download
    f = dir + os.path.basename(uri)  # filename
    with open(f, "wb") as file:
        file.write(requests.get(uri, timeout=10).content)

    # Rename (remove wildcard characters)
    src = f  # original name
    for c in ["%20", "%", "*", "~", "(", ")"]:
        f = f.replace(c, "_")
    f = f[: f.index("?")] if "?" in f else f  # new name
    if src != f:
        os.rename(src, f)  # rename

    # Add suffix (if missing)
    if Path(f).suffix == "":
        src = f  # original name
        f += f".{Image.open(f).format.lower()}"
        os.rename(src, f)  # rename
