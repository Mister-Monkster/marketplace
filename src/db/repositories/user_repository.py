from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.models import UserModel, RoleModel, AnnouncementsModel, TokenModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_rights(self, user_id):
        query = (
            select(RoleModel)
            .join(UserModel.roles_rel)
            .where(UserModel.yandex_id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_or_update(self, user):
        query = (
            insert(UserModel)
            .values(**user)
            .on_conflict_do_update(
                index_elements=["yandex_id"],
                set_=user
            )
            .returning(UserModel.yandex_id, UserModel.is_active)
        )
        user = await self.session.execute(query)
        result = user.one()
        await self.session.commit()
        return result

    async def get_user_by_id(self, id: int):
        query = select(UserModel).where(UserModel.yandex_id == id).options(joinedload(UserModel.roles_rel))
        user = await self.session.execute(query)
        result = user.scalars().one_or_none()
        return result

    async def update(self, user_id: int, data: dict):
        query = update(UserModel).where(UserModel.yandex_id == user_id).values(**data)
        await self.session.execute(query)
        await self.session.commit()
        return True

    async def ban(self, user_id: int):
        query_u = (update(UserModel)
                 .where(UserModel.yandex_id == user_id and UserModel.role_id != 2)
                 .values(is_active=False))
        query_a = update(AnnouncementsModel).where(AnnouncementsModel.user_id == user_id).values(status=False)
        query_t = update(TokenModel).where(UserModel.yandex_id == user_id).values(is_banned=True).returning(TokenModel.token_id)
        await self.session.execute(query_u)
        await self.session.execute(query_a)
        tokens = await self.session.execute(query_t)
        result = tokens.scalars().all()
        await self.session.commit()
        return result