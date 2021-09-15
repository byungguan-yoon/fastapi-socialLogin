from fastapi import FastAPI, Depends, Request, Response, Cookie
from fastapi.responses import RedirectResponse, StreamingResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional


templates = Jinja2Templates(directory='./static/templates')

app = FastAPI()

origins = ['http://localhost:8000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)



@app.get('/kakao')
def kakao():
    # REST API KEY IN
    REST_API_KEY = ""
    REDIRECT_URI = "http://127.0.0.1:8000/kakaoAuth"
    url = f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&response_type=code&redirect_uri={REDIRECT_URI}"
    response = RedirectResponse(url)
    return response


@app.get('/kakaoAuth')
async def kakaoAuth(response: Response, code: Optional[str]="NONE"):
    # REST API KEY IN
    REST_API_KEY = ''
    REDIRECT_URI = 'http://127.0.0.1:8000/kakaoAuth'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&code={code}&redirect_uri={REDIRECT_URI}'
    _res = requests.post(_url)
    _result = _res.json()
    response.set_cookie(key="kakao", value=str(_result["access_token"]))
    return {"code":_result}


@app.get('/kakaoLogout')
def kakaoLogout(request: Request, response: Response):
    url = "https://kapi.kakao.com/v1/user/unlink"
    KEY = request.cookies['kakao']
    headers = dict(Authorization=f"Bearer {KEY}")
    _res = requests.post(url,headers=headers)
    response.set_cookie(key="kakao", value=None)
    return {"logout": _res.json()}


@app.get('/naver')
def naver():
    # NAVER CLIENT ID KEY IN
    CLIENT_ID = ""
    REDIRECT_URI = 'http://127.0.0.1:8000/naverAuth'
    url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=state"
    response = RedirectResponse(url)
    return response


@app.get('/naverAuth')
async def naverAuth(response: Response, code: Optional[str]="NONE", state: Optional[str]="NONE"):
    # NAVER CLIENT ID/SECRET KEY IN
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    _url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={code}&state={state}'
    _res = requests.post(_url)
    _result = _res.json()
    print(_result)
    response.set_cookie(key="naver", value=str(_result["access_token"]))
    return {"code":_result}


@app.get('/naverLogout')
def naverLogout(request: Request, response: Response):
    # NAVER CLIENT ID/SECRET KEY IN
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    ACCESS_TOKEN = request.cookies["naver"]
    url = f"https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&access_token={ACCESS_TOKEN}&service_provider=NAVER"
    _res = requests.post(url)
    response.set_cookie(key="naver", value=None)
    return {"logout": _res.json()}