import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validators import validate_operation_data
from flask import jsonify
from models import FinancialOperation, TransactionHistory, session
from sqlalchemy import select

class financialService:
    
    def create_operation(data):
        if not validate_operation_data(data):
            return jsonify({"error": "Invalid data"}), 400
        operation = FinancialOperation(**data)
        session.add(operation)
        session.commit()
        history = TransactionHistory()
        history.operation_id = operation.id
        history.mudancas = "Criado"
        session.add(history)
        session.commit()
        return jsonify(operation.create_exportable()), 200
    
    def get_operations(page, per_page, data):
        stmt = select(FinancialOperation)
        if "tipo_operacao" in data and data["tipo_operacao"]:
            stmt = stmt.where(FinancialOperation.tipo_operacao == data["tipo_operacao"])
        if "valor" in data and data["valor"] is not None:
            stmt = stmt.where(FinancialOperation.valor == data["valor"])
        if "descricao" in data and data["descricao"]:
            stmt = stmt.where(FinancialOperation.descricao.contains(data["descricao"]))
        if "data" in data and data["data"]:
            stmt = stmt.where(FinancialOperation.data == data["data"])
        stmt.limit(per_page).offset((page-1)*per_page)
        operations = session.scalars(stmt)
        output = []
        for operation in operations:
         output.append(operation.create_exportable())
        return jsonify(output), 200
    
    def get_singular_operation(id):
        stmt = select(FinancialOperation).where(FinancialOperation.id == id)
        operations = session.scalars(stmt).one_or_none()
        if operations == None:
            return jsonify({"error": "Nenhuma operacao encontrada"}), 404
        return jsonify(operations.create_exportable()), 200
    
    def update_operation(id, data):
        if not validate_operation_data(data):
            return jsonify({"error": "Invalid data"}), 400
        stmt = select(FinancialOperation).where(FinancialOperation.id == id)
        operation = session.scalars(stmt).one_or_none()
        if operation == None:
            return jsonify({"error": "Nenhuma operacao encontrada"}), 404
        if data["tipo_operacao"] is not None or data["tipo_operacao"] != '':
            operation.tipo_operacao = data["tipo_operacao"]
        if data["valor"] is not None:
            operation.valor = data["valor"]
        if data["descricao"] is not None or data["descricao"] != '':
            operation.descricao = data["descricao"]
        session.commit()
        history = TransactionHistory()
        history.operation_id = operation.id
        history.mudancas = "Alterado"
        session.add(history)
        session.commit()
        return jsonify(operation.create_exportable()), 200
    
    def delete_operation(id):
        stmt = select(FinancialOperation).where(FinancialOperation.id == id)
        operation = session.scalars(stmt).one_or_none()
        if operation is None:
            return jsonify({"error": "Operação não encontrada"}), 404
        session.delete(operation)
        session.commit()
        history = TransactionHistory()
        history.operation_id = operation.id
        history.mudancas = "Deletado"
        session.add(history)
        session.commit()
        return jsonify({"success":f'Operação de id {id} deletada com sucesso'}), 200
    
    def create_bulk_operation(data):
        additions = []
        valids = []
        invalids = []
        historyl = []
        if len(data) <= 0:
            return jsonify({"error": "Invalid data: no items in List"}), 400
        for op in data:
            if not validate_operation_data(op):
                invalids.append(op)
                continue
            operation = FinancialOperation(**op)
            additions.append(operation)
        session.add_all(additions)
        session.commit()
        for i in additions:
            valids.append(i.create_exportable())
            history = TransactionHistory()
            history.operation_id = i.id
            history.mudancas = "Criado"
            historyl.append(history)
        session.add_all(historyl)
        session.commit()
        return jsonify({"success": f'Operations {valids} added, could not add {invalids} due to bad data'}), 200
    