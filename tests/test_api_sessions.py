from http import HTTPStatus
from httpx import AsyncClient


async def test_client_get_sessions(auth_client: AsyncClient):
    response = await auth_client.get('/api/v1/session')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data[0].get('id')
    assert response_data[0].get('created_at')


async def test_not_auth_client_get_sessions(client: AsyncClient):
    response = await client.get('/api/v1/session')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
