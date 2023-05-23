from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from social_core.exceptions import AuthForbidden, MissingBackend
from social_core.backends.github import GithubOAuth2
from social_core.backends.utils import get_backend
from pydantic import BaseModel
import boto3
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Setup OAuth2 with Github
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
    refreshUrl="https://github.com/login/oauth/access_token",
    scopes={"user:email"},
    auto_error=False,
)

# Setup Amazon S3 client
s3 = boto3.client(
    's3',
    region_name=os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
)

# Define SSO Users model
class User(BaseModel):
    username: str
    email: str

# Perform authentication and return user details
async def get_user_by_token(request: Request, token: str) -> User:
    try:
        backend = get_backend("social_core.backends.github.GithubOAuth2")
        if not backend:
            raise MissingBackend("Authentication backend not found.")
        user_data = await backend.user_data(token)
        return User(username=user_data["login"], email=user_data["email"])
    except AuthForbidden as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=str(e)
        )

@app.post("/sso/login/")
async def sso_login(request: Request, token: str = Depends(oauth2_scheme)):
    user = await get_user_by_token(request, token)
    return user

@app.post("/upload_image/")
async def upload_image(image: UploadFile = File(...), user: User = Depends(get_user_by_token)):
    # Upload image to S3
    s3.upload_fileobj(
        image.file,
        os.environ['AWS_S3_BUCKET'],
        f"{user.username}/{image.filename}",
        ExtraArgs={'ContentType': 'image/jpeg'}
    )
    return {"status": "success", "message": f"Image {image.filename} uploaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)