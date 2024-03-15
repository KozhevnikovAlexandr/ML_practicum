import sys
from pathlib import Path

from hashlib import md5

from utils.exeptions import NotFoundError


sys.path.append(str(Path(__file__).resolve().parents[2]))
from schemas.auth_schema import UserLoginSchema, UserRegisterSchema, UserLoginResponseSchema, UserSchema
from database.models import User
from repository.base_repository import AbstractRepository
from utils.security import create_jwt_token
from repository.user_repository import UserRepository



class AuthService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def login(self, user: UserLoginSchema):

        db_user: User = await self.users_repo.find_by_options(email=user.email, unique=True)
        print(db_user.password, user.password)
        if db_user is None:
            raise Exception("User not found")
        if db_user.password !=  user.password: # md5(user.password.encode('utf-8')).hexdigest():
            raise Exception("Password is incorrect")

        user: UserSchema = UserSchema(id=db_user.id, name=db_user.name, email=db_user.email)

        access_token = create_jwt_token(user)


        return UserLoginResponseSchema(access_token=access_token,
                                 user_info=user)

    async def register(self, user: UserSchema):

        db_user = await self.users_repo.find_by_options(email=user.email, unique=True)

        if db_user is not None:
            raise Exception("Email already exists")
        
        user_id = await self.users_repo.add(data={"name": user.name, 
                                                  "password": user.password, # md5(user.password.encode('utf-8')).hexdigest(),
                                                  "email": user.email,
                                                  "balance": 100})

        user: UserSchema = UserSchema(id=user_id, name=user.name, email=user.email)

        access_token = create_jwt_token(user)

        return UserLoginResponseSchema(access_token=access_token,
                                 user_info=user)

    async def get_balance(self, user: UserSchema):

        db_user = await self.users_repo.find_by_options(email=user.email, unique=True)
        if db_user is None:
            raise Exception("User not found")
        return {'balance': db_user.balance}


def get_auth_service():
    return AuthService(UserRepository)