from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "POST" in response.text

def test_contato():
    response = client.get("/contato")
    assert response.status_code == 200
    assert "entre em contato" in response.text.lower()

def test_servicos():
    response = client.get("/servicos")
    assert response.status_code == 200
    assert "Serviços" in response.text

def test_quem_somos():
    response = client.get("/quem-somos")
    assert response.status_code == 200
    assert "quem somos" in response.text.lower()


def test_envio_formulario_contato():
    response = client.post("/enviar-contato", data={
        "nome": "Pedro",
        "email": "pedro@email.com",
        "mensagem": "Gostaria de saber mais sobre os serviços."
    })
    assert response.status_code == 200
    assert "contato" in response.text.lower()

