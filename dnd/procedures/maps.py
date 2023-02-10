from hashlib import md5
from pathlib import Path

from fastapi import HTTPException, UploadFile
from hashids import Hashids
from PIL import Image

from dnd.storages.images import images


async def save_image(image: UploadFile, shortcut: Hashids) -> str:
    file_hash = md5()
    while chunk := (await image.read(8192)):
        file_hash.update(chunk)
    short_url = shortcut.encode_hex(file_hash.hexdigest())
    path = Path(images.directory)
    path /= short_url
    if not path.exists():
        im = Image.open(image.file)
        try:
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")

            im.save(path.absolute(), "JPEG", quality=50)
        except Exception:
            raise HTTPException(status_code=500, detail="Something went wrong")
        finally:
            image.file.close()
            im.close()
    return short_url
