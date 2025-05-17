from fastapi import status
from httpx import AsyncClient


async def test_client_health(api_client: AsyncClient) -> None:
    response = await api_client.get("/health")
    response.raise_for_status()
    assert response.status_code == status.HTTP_200_OK
