from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")

async def authenticate(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    if not token:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sign in for access"
            )
    decoded_token = await verify_access_token(token)
    return decoded_token["user"]