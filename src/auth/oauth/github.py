import httpx

from src.config import settings


def get_github_auth_url():
    return f"{settings.GITHUB_AUTH_URL}?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_REDIRECT_URI}&scope=read:user"


async def exchange_code_for_token(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_REDIRECT_URI
            }
        )
        response.raise_for_status()
        return response.json().get("access_token")


async def get_github_user(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.GITHUB_USER_URL,
            headers={
                "Authorization": f"token {token}"
            }
        )
        response.raise_for_status()
        return response.json()
