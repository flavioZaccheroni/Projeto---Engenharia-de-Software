import requests
import json

# URL do endpoint de cadastro de pacientes.
# Certifique-se de que o seu Back-end (Flask, FastAPI, etc.) está rodando em http://127.0.0.1:5000
URL_CADASTRO = "http://127.0.0.1:5000/pacientes"

# DADOS JSON para o cadastro do novo paciente (Payload)
dados_paciente = {
    "nome": "João da Silva",
    "cpf": "987.654.321-00",
    "telefone": "99999-1234",
    "endereco": "Rua Central, 200"
}

print(f"Iniciando requisição POST para: {URL_CADASTRO}")
print(f"Dados a serem enviados: {json.dumps(dados_paciente, indent=2)}\n")

try:
    # 1. Realiza a requisição POST, enviando o JSON no corpo
    response = requests.post(URL_CADASTRO, json=dados_paciente)

    # 2. Imprime os detalhes da resposta
    print("--- Resposta da API ---")
    print(f"Status Code: {response.status_code}")
    print(f"Corpo da Resposta (JSON): {response.json()}")
    print("-------------------------\n")

    # 3. Verificação (Assertion) - Critério de Aceitação:
    # O status 201 (Created) é o padrão para criação bem-sucedida de um recurso RESTful.
    assert response.status_code == 201, (
        f"ERRO: Esperado Status 201, mas recebido {response.status_code}. "
        f"Verifique o log do servidor Back-end."
    )

    # 4. Verificação Adicional: Confirma se o nome retornado corresponde ao enviado
    assert response.json()['nome'] == dados_paciente['nome'], "ERRO: Nome retornado no JSON é incorreto."

    # 5. Se todas as verificações passarem, o teste é um sucesso
    print("✅ TESTE FUNCIONAL DE CADASTRO DE PACIENTE BEM-SUCEDIDO!")

except requests.exceptions.ConnectionError:
    print("❌ ERRO DE CONEXÃO: Certifique-se de que seu servidor Python está em execução em http://127.0.0.1:5000.")
except AssertionError as e:
    print(f"❌ TESTE FALHOU: {e}")