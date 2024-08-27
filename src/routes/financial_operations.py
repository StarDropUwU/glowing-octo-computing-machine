from auth import token_required
from services.services import financialService
from flask import request
import jwt
from config import Config

def create_routes(app):
    @app.route('/health', methods=['GET'])
    def health_check():
        return "Hemlo " + jwt.encode(payload={"data": "idunno"},key=Config.SECRET_KEY)
    
    @app.route('/operations', methods=['POST'])
    @token_required
    def create_operation():
        data = request.get_json()
        return financialService.create_operation(data)

    @app.route('/operations', methods=['GET'])
    @token_required
    def get_operations():
        data = request.get_json()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return financialService.get_operations(page, per_page, data)
    
    @app.route('/operations/<int:id>', methods=['GET'])
    @token_required
    def get_singular_operation(id):
        return financialService.get_singular_operation(id)

    @app.route('/operations/<int:id>', methods=['PUT'])
    @token_required
    def update_operation(id):
        data = request.get_json()
        return financialService.update_operation(id, data)
    
    @app.route('/operations/<int:id>', methods=['DELETE'])
    @token_required
    def delete_operation(id):
        return financialService.delete_operation(id)

    @app.route('/operations/bulk', methods=['POST'])
    @token_required
    def create_bulk_operation():
        data = request.get_json()
        return financialService.create_bulk_operation(data)
    
