from flask import jsonify, request
from database import app, db, init_db
from models import Paciente, Medico, Consulta
from utils import log_info, log_error

@app.route('/')
def home():
    return jsonify({"mensagem": "API SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde"})

# ------------------- PACIENTES -------------------
@app.route('/pacientes', methods=['POST'])
def criar_paciente():
    try:
        data = request.json
        if not data.get('nome') or not data.get('cpf'):
            return jsonify({"erro": "Nome e CPF são obrigatórios."}), 400

        novo = Paciente(
            nome=data['nome'],
            cpf=data['cpf'],
            telefone=data.get('telefone'),
            endereco=data.get('endereco')
        )
        db.session.add(novo)
        db.session.commit()
        log_info(f"Paciente cadastrado: {data['nome']}")
        return jsonify({"mensagem": "Paciente cadastrado com sucesso!"}), 201
    except Exception as e:
        log_error(str(e))
        return jsonify({"erro": "Erro ao cadastrar paciente."}), 500

@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([
        {"id": p.id, "nome": p.nome, "cpf": p.cpf, "telefone": p.telefone, "endereco": p.endereco}
        for p in pacientes
    ])

@app.route('/pacientes/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    data = request.json
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404
    paciente.nome = data.get('nome', paciente.nome)
    paciente.telefone = data.get('telefone', paciente.telefone)
    paciente.endereco = data.get('endereco', paciente.endereco)
    db.session.commit()
    log_info(f"Paciente atualizado: {paciente.nome}")
    return jsonify({"mensagem": "Paciente atualizado com sucesso!"})

@app.route('/pacientes/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    paciente = Paciente.query.get(id)
    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404
    db.session.delete(paciente)
    db.session.commit()
    log_info(f"Paciente excluído: ID {id}")
    return jsonify({"mensagem": "Paciente excluído com sucesso!"})

# ------------------- MÉDICOS -------------------
@app.route('/medicos', methods=['POST'])
def criar_medico():
    data = request.json
    novo = Medico(nome=data['nome'], especialidade=data['especialidade'])
    db.session.add(novo)
    db.session.commit()
    log_info(f"Médico cadastrado: {data['nome']}")
    return jsonify({"mensagem": "Médico cadastrado com sucesso!"}), 201

@app.route('/medicos', methods=['GET'])
def listar_medicos():
    medicos = Medico.query.all()
    return jsonify([
        {"id": m.id, "nome": m.nome, "especialidade": m.especialidade}
        for m in medicos
    ])

# ------------------- CONSULTAS -------------------
@app.route('/consultas', methods=['POST'])
def criar_consulta():
    data = request.json
    nova = Consulta(
        data=data['data'],
        paciente_id=data['paciente_id'],
        medico_id=data['medico_id']
    )
    db.session.add(nova)
    db.session.commit()
    log_info(f"Consulta agendada em {data['data']}")
    return jsonify({"mensagem": "Consulta agendada com sucesso!"}), 201

@app.route('/consultas', methods=['GET'])
def listar_consultas():
    consultas = Consulta.query.all()
    return jsonify([
        {"id": c.id, "data": c.data, "paciente_id": c.paciente_id, "medico_id": c.medico_id}
        for c in consultas
    ])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
