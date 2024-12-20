from motor.core import AgnosticDatabase
from app.crud.base import CRUDBase
from app.models.token import Token
from app.models.user import User
from app.schemas.token import RefreshTokenCreate, RefreshTokenUpdate


class CRUDToken(CRUDBase[Token, RefreshTokenCreate, RefreshTokenUpdate]):
    async def create(self, db: AgnosticDatabase, *, obj_in: Token, user_obj: User) -> Token:
        db_obj = await self.engine.find_one(self.model, self.model.token == obj_in)
        if db_obj:
            if db_obj.authenticates_id != user_obj.id:
                raise ValueError("Token mismatch between key and user.")
            return db_obj
        else:
            new_token = self.model(token=obj_in, authenticates_id=user_obj)
            user_obj.refresh_tokens.append(new_token.id)
            await self.engine.save_all([new_token, user_obj])
            return new_token

    async def get(self, *, user: User, token: str) -> Token:
        return await self.engine.find_one(User, ((User.id == user.id) & (User.refresh_tokens == token)))

    async def remove(self, db: AgnosticDatabase, *, db_obj: Token) -> None:
        users = []
        async for user in self.engine.find(User, User.refresh_tokens.in_([db_obj.id])):
            user.refresh_tokens.remove(db_obj.id)
            users.append(user)
        await self.engine.save(users)
        await self.engine.delete(db_obj)


token = CRUDToken(Token)