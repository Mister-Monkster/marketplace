from fastapi import Depends
from typing import Annotated

from api.depends.session_depend import SessionDep
from db.repositories.admin_repository import AdminRepository
from db.repositories.announcements_repository import AnnouncementRepository
from db.repositories.category_repository import CategoryRepository
from db.repositories.file_repository import FileRepository
from db.repositories.report_repository import ReportRepository
from db.repositories.token_repository import TokenRepository

from db.repositories.user_repository import UserRepository


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)

user_repository = Annotated[UserRepository, Depends(get_user_repository)]


async def get_announcement_repository(session: SessionDep) -> AnnouncementRepository:
    return AnnouncementRepository(session)

announcement_repository = Annotated[AnnouncementRepository, Depends(get_announcement_repository)]


async def get_file_repository(session: SessionDep) -> FileRepository:
    return FileRepository(session)

file_repository = Annotated[FileRepository, Depends(get_file_repository)]


async def get_category_repository(session: SessionDep) -> CategoryRepository:
    return CategoryRepository(session)

category_repository = Annotated[CategoryRepository, Depends(get_category_repository)]


async def get_token_repository(session: SessionDep) -> TokenRepository:
    return TokenRepository(session)

token_repository = Annotated[TokenRepository, Depends(get_token_repository)]


async def get_admin_repository(session: SessionDep) -> AdminRepository:
    return AdminRepository(session)

admin_repository = Annotated[AdminRepository, Depends(get_admin_repository)]


async def get_report_repository(session: SessionDep) -> ReportRepository:
    return ReportRepository(session)

report_repository = Annotated[ReportRepository, Depends(get_report_repository)]