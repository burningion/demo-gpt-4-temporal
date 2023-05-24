# GPT-4 Example Output

This directory of the repository showcases GPT-4's response to the following prompt:

## Prompt: write a fastapi api to handle sso logins and image uploads to s3

## GPT-4 Output:

In this example, I'll create a FastAPI application that will handle SSO (Single Sign-On) logins using GitHub as an authentication provider, and will also handle image uploads to Amazon S3.

Before starting, make sure you have the required dependencies installed by running:

```sh
pip install fastapi uvicorn python-dotenv python-social-auth boto3
```

Next, let's create the FastAPI application (`main.py`):

```python
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
```

Don't forget to create a `.env` file with the required environment variables:

```
AWS_REGION=<your-aws-region>
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
AWS_S3_BUCKET=<your-s3-bucket-name>
```

This FastAPI application has two routes:

1. `/sso/login/`: A route that allows users to log in using GitHub's OAuth2.
2. `/upload_image/`: A route that allows authenticated users to upload images to Amazon S3.

To run the app, execute:

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

## GPT-4 Augmented Query Output

## Prompt: write a single .gitpod.yml file for a fastapi python project. the application is named `main.py`, and the command to run it is `uvicorn main:app --host 0.0.0.0 --port 8000`. the other library dependencies are fastapi uvicorn python-dotenv python-social-auth boto3. be sure to explain your work

## Augmented GPT-4 Output:

Here's a `.gitpod.yml` file for your FastAPI Python project with an explanation of the configurations:

```yaml
image:
  # Use the default Python image
  repository: gitpod/workspace-python

tasks:
  # Install the dependencies specified in your requirements.txt file
  - init: echo "fastapi uvicorn python-dotenv python-social-auth boto3" > requirements.txt && pip install -r requirements.txt
  # Run the FastAPI application using uvicorn
  - command: uvicorn main:app --host 0.0.0.0 --port 8000

# Expose the FastAPI application port
ports:
  - port: 8000
    onOpen: open-preview
```

Explanation:

1. Use the Gitpod default Python image as the base image for your project.
2. Create a `requirements.txt` file with the specified dependencies and install them using `pip`.
3. Start the FastAPI application using `uvicorn` with the command provided (`uvicorn main:app --host 0.0.0.0 --port 8000`).
4. Expose port 8000 and open the preview automatically when the application is running.

With this configuration, after pushing your `.gitpod.yml` file to your repository, you can start a new Gitpod workspace, and it will automatically run the FastAPI application, install the dependencies,
and expose the application on port 8000 with a preview.