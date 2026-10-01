from fastapi.testclient import TestClient


def test_health_reports_api_and_database_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}
