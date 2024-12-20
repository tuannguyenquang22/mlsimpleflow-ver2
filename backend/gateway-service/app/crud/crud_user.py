from motor.core import AgnosticDatabase
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AgnosticDatabase, *, email: str) -> User | None:  # noqa
        return await self.engine.find_one(User, User.email == email)

    async def create(self, db: AgnosticDatabase, *, obj_in: UserCreate) -> User:
        user = {
            **obj_in.model_dump(),
            "email": obj_in.email,
            "hashed_password": get_password_hash(obj_in.password),
            "display_name": obj_in.display_name,
            "is_superuser": obj_in.is_superuser,
        }
        return await self.engine.save(User(**user))

    async def authenticate(self, db: AgnosticDatabase, *, email: str, password: str) -> User | None:  # noqa
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(plain_password=password, hashed_password=user.hashed_password):  # noqa
            return None
        return user

    @staticmethod
    def has_password(user: User) -> bool:
        return user.hashed_password is not None

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)