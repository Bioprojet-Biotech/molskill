import os

import requests
from tqdm import tqdm
from molskill.helpers.logging import get_logger

LOGGER = get_logger(__name__)

def download(src: str, dest: str) -> None:
    """Simple GET request with progress bar and caching
    Args:
        src (str): Source link to download from
        dest (str): Destination file
    """
    # Check if file already exists (cache hit)
    if os.path.exists(dest):
        LOGGER.info(f"File {dest} already exists. Skipping download.")
        return

    # Create parent directory if it doesn't exist
    dest_dir = os.path.dirname(dest)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    r = requests.get(src, stream=True)
    tsize = int(r.headers.get("content-length", 0))
    progress = tqdm(total=tsize, unit="iB", unit_scale=True, position=0, leave=False)

    with open(dest, "wb") as handle:
        progress.set_description(os.path.basename(dest))
        for chunk in r.iter_content(chunk_size=1024):
            handle.write(chunk)
            progress.update(len(chunk))
