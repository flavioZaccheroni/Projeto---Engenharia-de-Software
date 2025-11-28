import requests

BASE_URL = "http://127.0.0.1:5000"

# ---------- TESTE 1: Cadastrar Paciente ----------
def test_cadastrar_paciente():
    data = {
        "nome": "Carlos Oliveira",
        "cpf": "222.333.444-55",
        "telefone": "98888-1111",
        "endereco": "Av. Brasil, 500"
    }
    resposta = requests.post(f"{BASE_URL}/pacientes", json=data)
    assert resposta.status_code == 201
    assert "sucesso" in resposta.json()["mensagem"].lower()

# ---------- TESTE 2: Listar Pacientes ----------
def test_listar_pacientes():
    resposta = requests.get(f"{BASE_URL}/pacientes")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)

# ---------- TESTE 3: Atualizar Paciente ----------
def test_atualizar_paciente():
    data = {"telefone": "97777-2222"}
    resposta = requests.put(f"{BASE_URL}/pacientes/1", json=data)
    assert resposta.status_code == 200
    assert "atualizado" in resposta.json()["mensagem"].lower()

# ---------- TESTE 4: Deletar Paciente ----------
def test_deletar_paciente():
    resposta = requests.delete(f"{BASE_URL}/pacientes/1")
    assert resposta.status_code == 200
    assert "excluído" in resposta.json()["mensagem"].lower()
