from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.models import UserModel, AnnouncementsModel, TokenModel


class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def ban(self, user_id: int):
        try:
            query_u = (update(UserModel)
                     .where(UserModel.yandex_id == user_id and UserModel.role_id != 2)
                     .values(is_active=False, role_id=1))

            query_a = (update(AnnouncementsModel)
                       .where(AnnouncementsModel.user_id == user_id)
                       .values(status=False))

            query_t = (update(TokenModel)
                       .where(TokenModel.user_id == user_id)
                       .values(is_banned=True)
                       .returning(TokenModel.token_id))

            await self.session.execute(query_u)
            await self.session.execute(query_a)
            tokens = await self.session.execute(query_t)
            result = tokens.scalars().all()
            await self.session.commit()
            return result
        except:
            await self.session.rollback()
            return False

    async def unban(self, user_id: int):
        try:
            query_u = (update(UserModel)
                       .where(UserModel.yandex_id == user_id)
                       .values(is_active=True))

            query_t = (update(TokenModel)
                       .where(TokenModel.user_id == user_id)
                       .values(is_banned=False)
                       .returning(TokenModel.token_id))

            await self.session.execute(query_u)
            tokens = await self.session.execute(query_t)
            result = tokens.scalars().all()
            await self.session.commit()
            return result
        except:
            await self.session.rollback()
            return False

    async def delete_announcement(self, announcement_id: int):
        try:
            query = (update(AnnouncementsModel)
                     .where(AnnouncementsModel.id == announcement_id)
                     .values(status=False))
            await self.session.execute(query)
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return False

    async def give_role(self, user_id: int, role_id: int):
        try:
            query = (update(UserModel)
                     .where(UserModel.yandex_id == user_id)
                     .values(role_id=role_id))
            await self.session.execute(query)
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return False