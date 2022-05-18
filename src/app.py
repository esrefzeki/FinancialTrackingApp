from fastapi import FastAPI, Request
from src.routers import user, expense, auth, expense_type, login, income_type, income
from src import config
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache()
def get_settings():
    return config.GlobalConfig()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(expense.router)
app.include_router(expense_type.router)
app.include_router(income.router)
app.include_router(income_type.router)




# OAuth settings
GOOGLE_CLIENT_ID = '1005157772057-r4t0dnjja3f6nkupgne85s0msk18llb3.apps.googleusercontent.com' or None
GOOGLE_CLIENT_SECRET = "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" or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': "1005157772057-r4t0dnjja3f6nkupgne85s0msk18llb3.apps.googleusercontent.com",
               'GOOGLE_CLIENT_SECRET': "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"}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

SECRET_KEY = "09saw7eq9q6f51vf6g8h4w6936gh13hn7r7re856eq1f6sb1as63ax1b6f51hs6v" or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/asd')
    user_data = access_token["userinfo"]
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/docs')
