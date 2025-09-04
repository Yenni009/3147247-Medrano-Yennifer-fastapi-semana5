import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_autor():
    response = client.post(
        "/autores/",
        json={"nombre": "Gabriel García Márquez", "nacionalidad": "Colombiana"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Gabriel García Márquez"

def test_crear_libro_con_autor():
    autor_response = client.post(
        "/autores/",
        json={"nombre": "Isabel Allende", "nacionalidad": "Chilena"}
    )
    autor_id = autor_response.json()["id"]

    response = client.post(
        "/libros/",
        json={"titulo": "La Casa de los Espíritus", "precio": 25.99, "paginas": 450, "autor_id": autor_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "La Casa de los Espíritus"
    assert data["autor"]["nombre"] == "Isabel Allende"

def test_validacion_precio_negativo():
    response = client.post(
        "/libros/",
        json={"titulo": "Libro Inválido", "precio": -10.99, "paginas": 100}
    )
    assert response.status_code == 422
