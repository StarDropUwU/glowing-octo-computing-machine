import sys
import os
from flask import jsonify
from sqlalchemy import select
from utils.validators import validate_operation_data
from models import FinancialOperation, TransactionHistory, session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class FinancialService:
    """
    Classe de serviço para operações financeiras.

    Esta classe contém métodos para realizar operações CRUD em dados financeiros, utilizando modelos SQLAlchemy e integração com o banco de dados.
    As operações incluem criação, leitura, atualização e exclusão, além de operações em lote.
    """

    @staticmethod
    def post(data):
        """
        Registra uma nova operação financeira no banco de dados.

        :param data: Dicionário contendo os dados da operação.
        :return: Resposta JSON da operação criada ou erro de validação de dados.
        """
        if not validate_operation_data(data):
            return jsonify({"error": "Invalid data"}), 400

        operation = FinancialOperation(**data)
        session.add(operation)
        session.commit()

        # Cria um registro no histórico de transações
        history = TransactionHistory(operation_id=operation.id, mudancas="Criado")
        session.add(history)
        session.commit()

        return jsonify(operation.create_exportable()), 200

    @staticmethod
    def get_operations(page, per_page, data):
        """
        Retorna uma lista paginada de operações financeiras, com filtros opcionais.

        :param page: Número da página a ser retornada.
        :param per_page: Número de operações por página.
        :param data: Dicionário contendo filtros opcionais (tipo_operacao, valor, descricao, data).
        :return: Resposta JSON com a lista de operações filtradas.
        """
        stmt = select(FinancialOperation)

        # Aplica filtros com base nos dados fornecidos
        if "tipo_operacao" in data and data["tipo_operacao"]:
            stmt = stmt.where(FinancialOperation.tipo_operacao == data["tipo_operacao"])
        if "valor" in data and data["valor"] is not None:
            stmt = stmt.where(FinancialOperation.valor == data["valor"])
        if "descricao" in data and data["descricao"]:
            stmt = stmt.where(FinancialOperation.descricao.contains(data["descricao"]))
        if "data" in data and data["data"]:
            stmt = stmt.where(FinancialOperation.data == data["data"])

        # Paginação
        stmt = stmt.limit(per_page).offset((page - 1) * per_page)
        operations = session.scalars(stmt)

        # Cria a lista de resposta
        output = [operation.create_exportable() for operation in operations]

        return jsonify(output), 200

    @staticmethod
    def get_operation(id):
        """
        Retorna uma operação financeira específica.

        :param id: ID da operação a ser recuperada.
        :return: Resposta JSON com os dados da operação ou erro se não encontrada.
        """
        stmt = select(FinancialOperation).where(FinancialOperation.id == id)
        operation = session.scalars(stmt).one_or_none()

        if operation is None:
            return jsonify({"error": "Nenhuma operação encontrada"}), 404

        return jsonify(operation.create_exportable()), 200

    @staticmethod
    def put(id, data):
        """
        Atualiza uma operação financeira específica.

        :param id: ID da operação a ser atualizada.
        :param data: Dicionário contendo os novos dados da operação.
        :return: Resposta JSON da operação atualizada ou erro de validação.
        """
        if not validate_operation_data(data):
            return jsonify({"error": "Invalid data"}), 400

        stmt = select(FinancialOperation).where(FinancialOperation.id == id)
        operation = session.scalars(stmt).one_or_none()

        if operation is None:
            return jsonify({"error": "Nenhuma operação encontrada"}), 404

        # Atualiza os campos da operação
        if data.get("tipo_operacao"):
            operation.tipo_operacao = data["tipo_operacao"]
        if data.get("valor") is not None:
            operation.valor = data["valor"]
        if data.get("descricao"):
            operation.descricao = data["descricao"]

        session.commit()

        # Atualiza o histórico
        history = TransactionHistory(operation_id=operation.id, mudancas="Alterado")
        session.add(history)
        session.commit()

        return jsonify(operation.create_exportable()), 200

    @staticmethod
    def delete(id):
        """
        Deleta uma operação financeira específica.

        :param id: ID da operação a ser deletada.
        :return: Resposta JSON confirmando a exclusão ou erro se não encontrada.
        """
        stmt = select(FinancialOperation).where(FinancialOperation.id == id)
        operation = session.scalars(stmt).one_or_none()

        if operation is None:
            return jsonify({"error": "Operação não encontrada"}), 404

        session.delete(operation)
        session.commit()

        # Registra a exclusão no histórico
        history = TransactionHistory(operation_id=operation.id, mudancas="Deletado")
        session.add(history)
        session.commit()

        return jsonify({"success": f'Operação de id {id} deletada com sucesso'}), 200

    @staticmethod
    def post_bulk(data):
        """
        Registra várias operações financeiras no banco de dados.

        :param data: Lista de dicionários contendo os dados de cada operação.
        :return: Resposta JSON indicando o sucesso ou falha na inserção de cada operação.
        """
        if not data:
            return jsonify({"error": "Invalid data: no items in List"}), 400

        additions = []
        invalids = []
        history_list = []

        # Valida e prepara as operações
        for op in data:
            if not validate_operation_data(op):
                invalids.append(op)
                continue
            operation = FinancialOperation(**op)
            additions.append(operation)

        session.add_all(additions)
        session.commit()

        # Registra histórico para cada operação criada
        for operation in additions:
            history = TransactionHistory(operation_id=operation.id, mudancas="Criado")
            history_list.append(history)

        session.add_all(history_list)
        session.commit()

        valid_operations = [op.create_exportable() for op in additions]

        return jsonify({
            "success": f'Operações {valid_operations} adicionadas, falha em adicionar {invalids} devido a dados inválidos'
        }), 200
