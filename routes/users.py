from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, UserSignIn
from auth.hash_password import HashPassword
from database.connection import Database

hash_password = HashPassword()
user_database = Database(User)
user_router = APIRouter(
    tags=["User"],
)

users = {}

@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    # await user.insert()
    return {
        "message": "User created successfully."
    }

@user_router.post("/signin")
async def sign_user_in(user_sign_in: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user_sign_in.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email provided does not exist"
        )
    if user_exist.password == user_sign_in.password:
        return {
            "message": "User signed in successfully."
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed"
    )
