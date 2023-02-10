from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
)
from hashids import Hashids
from pydantic import constr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dnd.database.db import get_db
from dnd.database.schemas.maps import Map, MapMeta
from dnd.database.schemas.users import User
from dnd.models.map import MapModel
from dnd.procedures.auth import check_user
from dnd.procedures.maps import save_image
from dnd.storages.images import images
from dnd.utils.crypto import get_shortcut

router = APIRouter(prefix="/map", tags=["map"])


@router.put(
    "/{map_name}/",
    response_model=MapModel,
    status_code=201,
)
async def create_map(
    map_name: str,
    len_x: int = Form(10, ge=10, le=1000),
    len_y: int = Form(10, ge=10, le=1000),
    image: UploadFile | None = File(None, media_type="image/jpg"),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
    shortcut: Hashids = Depends(get_shortcut),
):
    exists_map = await Map.get_by_name_and_user_id(
        session=session, name=map_name, user_id=user.id
    )
    if exists_map:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    new_map = await Map.create(
        session=session,
        user_id=user.id,
        name=map_name,
    )
    short_url = None
    if image:
        short_url = await save_image(image=image, shortcut=shortcut)

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


@router.patch(
    "/{map_name}/",
    response_model=MapModel,
    status_code=201,
)
async def update_map(
    map_name: str,
    new_map_name: str | None = Form(None, max_length=60),
    len_x: int | None = Form(None, ge=10, le=1000),
    len_y: int | None = Form(None, ge=10, le=1000),
    image: UploadFile | None = File(None, media_type="image/jpg"),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
    shortcut: Hashids = Depends(get_shortcut),
):
    exists_map = await Map.get_by_name_and_user_id(
        session=session, name=new_map_name, user_id=user.id
    )
    if exists_map:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    current_map = await Map.get_by_name_and_user_id(
        session=session, name=map_name, user_id=user.id
    )

    await Map.update(
        session=session,
        id=current_map.id,
        name=new_map_name or map_name,
    )
    short_url = None
    if image:
        short_url = await save_image(image=image, shortcut=shortcut)

    await MapMeta.update(
        session=session,
        id=current_map.meta.id,
        len_x=len_x or current_map.meta.len_x,
        len_y=len_y or current_map.meta.len_y,
        image_short_url=short_url or current_map.meta.image_short_url,
    )
    await session.flush()
    await session.commit()
    return MapModel.from_orm(current_map)


@router.delete("/{map_name}/")
async def remove_map(
    map_name: constr(max_length=30),
    user: User = Depends(check_user),
    session: AsyncSession = Depends(get_db),
):
    map = await Map.get_by_name_and_user_id(
        session=session, name=map_name, user_id=user.id
    )
    if map:
        await session.delete(map)
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
