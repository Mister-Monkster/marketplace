from unittest.mock import MagicMock

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from api.depends.service_depend import auth_service
from api.depends.user_depends import current_user_refresh

router = APIRouter(prefix="/auth", tags=["Авторизация🔐"])


@router.get("/yandex", summary="Авторизация через Яндекс🆔")
async def yandex_login(request: Request, service: auth_service):
    redirect_uri = "http://127.0.0.1:8000/auth/yandex/auth"
    return await service.oauth.yandex.authorize_redirect(request, redirect_uri)


@router.get("/yandex/auth", summary="Ответ от Яндекса✉️")
async def yandex_auth(request: Request, service: auth_service):
    try:
        token = await service.oauth.yandex.authorize_access_token(request)
        user = await service.oauth.yandex.get('https://login.yandex.ru/info?format=json', token=token)
        user_json = user.json()
        tokens = await service.register_or_update(user_json)
        if not tokens:
            raise HTTPException(status_code=401, detail="Your account is banned.")
        response = RedirectResponse(url='/docs', status_code=303)
        response.set_cookie(key='users_refresh_token',
                            value=tokens['refresh_token'],
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=604800)
        response.set_cookie(key='users_access_token',
                            value=tokens['access_token'],
                            httponly=True,
                            samesite='lax',
                            secure=False,
                            max_age=900)
        return response
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/refresh", summary='Обновление токена♻️')
async def refresh(response: Response, user: current_user_refresh, service: auth_service):
    if not user['status']:
        raise HTTPException(status_code=401, detail="Your account is banned.")
    id = int(user['payload'].sub)
    acces_token = await service.refresh(id)
    if not acces_token:
        raise HTTPException(status_code=401, detail="You've got banned")
    response.set_cookie(key='users_access_token',
                        value=acces_token,
                        httponly=True,
                        samesite='lax',
                        secure=False,
                        max_age=900)
    return {"ok": True, "detail": acces_token}


@router.post("/logout", summary='Выход➡️🚪')
async def logout(response: Response, service: auth_service, user: current_user_refresh):
    await service.logout(user['payload'].jti)
    response.delete_cookie(key='users_access_token',
                           httponly=True,
                           samesite='lax',
                           secure=False,
                           )
    response.delete_cookie(key='users_refresh_token',
                           httponly=True,
                           samesite='lax',
                           secure=False,
                           )
    return {"ok": True, "detail": "success logout"}


