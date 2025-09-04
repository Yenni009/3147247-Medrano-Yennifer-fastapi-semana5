import pytest
from fastapi.testclient import TestClient

def test_crear_categoria(client: TestClient):
    response = client.post(
        "/categorias/",
        json={"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Electrónicos"
    assert data["descripcion"] == "Dispositivos electrónicos"
    assert "id" in data

def test_listar_categorias_vacio(client: TestClient):
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert response.json() == []

def test_listar_categorias_con_datos(client: TestClient):
    client.post(
        "/categorias/",
        json={"nombre": "Libros", "descripcion": "Libros y literatura"}
    )
    response = client.get("/categorias/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Libros"

def test_obtener_categoria(client: TestClient):
    create_response = client.post(
        "/categorias/",
        json={"nombre": "Deportes", "descripcion": "Artículos deportivos"}
    )
    categoria_id = create_response.json()["id"]
    response = client.get(f"/categorias/{categoria_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Deportes"
    assert data["productos"] == []

def test_categoria_no_encontrada(client: TestClient):
    response = client.get("/categorias/999")
    assert response.status_code == 404
