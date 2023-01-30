from hashlib import md5
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
)
from hashids import Hashids
from PIL import Image
from pydantic import conint, constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.database.models.gamesets import GameSet
from dnd.database.models.maps import Map, MapMeta
from dnd.database.models.users import User
from dnd.models.map import MapModel
from dnd.procedures.auth import check_user
from dnd.procedures.gameset import get_current_gameset
from dnd.storages.images import images
from dnd.utils.crypto import get_shortcut

router = APIRouter(prefix="/map", tags=["game", "map"])


@router.put(
    "/{gameset_short_url}/{map_name}/",
    response_model=MapModel,
    status_code=201,
)
async def create_map(
    map_name: constr(max_length=30),
    len_x: conint(ge=10, le=1000) = 10,
    len_y: conint(ge=10, le=1000) = 10,
    image: UploadFile = File(media_type="image/jpg"),
    gameset: GameSet = Depends(get_current_gameset),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
    shortcut: Hashids = Depends(get_shortcut),
):
    exists_map = await Map.get_by_name_and_gameset_id(
        session=session, name=map_name, gameset_id=gameset.id
    )
    if exists_map:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    new_map = await Map.create(
        session=session,
        gameset_id=gameset.id,
        user_id=user.id,
        name=map_name,
    )
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

    new_map_meta = await MapMeta.create(
        session=session,
        len_x=len_x,
        len_y=len_y,
        map_id=new_map.id,
        image_short_url=short_url,
    )
    new_map.meta = new_map_meta
    await session.commit()
    return MapModel.from_orm(new_map)


@router.delete("/{gameset_short_url}/{map_name}/")
async def remove_map(
    map_name: constr(max_length=30),
    gameset: GameSet = Depends(get_current_gameset),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    gameset_map = await Map.get_by_name_and_gameset_id(
        session=session, name=map_name, gameset_id=gameset.id
    )
    if gameset_map and (gameset.owner.id == user.id):
        for pawn in gameset_map.pawns:
            await session.delete(pawn)
        await session.delete(gameset_map)
        await session.commit()
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)


@router.get("/images/{image_short_url}/")
async def get_map_image(
    image_short_url: constr(max_length=255),
    user: User = Depends(check_user),
):
    path = Path(images.directory) / image_short_url
    if path.exists() and user:
        return Response(
            path.read_bytes(),
            status_code=200,
            media_type="image/jpg",
        )
    else:
        return Response(status_code=404)


@router.get("/{gameset_short_url}/{map_name}/")
async def get_map(
    map_name: constr(max_length=30),
    gameset: GameSet = Depends(get_current_gameset),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    gameset_map = await Map.get_by_name_and_gameset_id(
        session=session, name=map_name, gameset_id=gameset.id
    )
    if gameset_map and user:
        return MapModel.from_orm(gameset_map)
    raise HTTPException(404, "Map not found")
