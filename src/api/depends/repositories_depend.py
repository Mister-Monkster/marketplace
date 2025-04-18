from fastapi import Depends
from typing import Annotated

from api.depends.session_depend import SessionDep
from db.repositories.announcemets_repository import AnnouncementRepository
from db.repositories.category_repository import CategoryRepository
from db.repositories.file_repository import FileRepository

from db.repositories.user_repository import UserRepository


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

user_repository = Annotated[UserRepository, Depends(get_user_repository)]


def get_announcement_repository(session: SessionDep) -> AnnouncementRepository:
    return AnnouncementRepository(session)

announcement_repository = Annotated[AnnouncementRepository, Depends(get_announcement_repository)]


def get_file_repository(session: SessionDep) -> FileRepository:
    return FileRepository(session)

file_repository = Annotated[FileRepository, Depends(get_file_repository)]


def get_category_repository(session: SessionDep) -> CategoryRepository:
    return CategoryRepository(session)

category_repository = Annotated[CategoryRepository, Depends(get_category_repository)]