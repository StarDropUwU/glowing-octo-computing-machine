from auth import TokenRequired
from services.services import FinancialService
from flask import request, jsonify
from flask.views import MethodView
import jwt
from config import Config


class HealthCheck(MethodView):
    """Classe definindo uma rota de Health Check, de momento retorna um token JWT válido."""
    def create_health_check_route(app):
        @app.route('/health', methods=['GET'])
        def get():
            token = jwt.encode(payload={"data": "idunno"}, key=Config.SECRET_KEY)
            return jsonify(token=token)


class OperationsAPI(MethodView):
    def create_routes(app):
        decorators = [TokenRequired]

        def get_json_data():
            return request.get_json()

        def get_pagination_params():
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            return page, per_page
        """
        Classe definindo todas as rotas para operações financeiras.
            - A função create_routes() é chamada em app.py e é responsável por aplicar os decorators em cada endpoint.
            - Aplica o decorator TokenRequired para garantir que apenas usuários autenticados podem acessar as rota
            - A função get_json_data() extrai os dados JSON da requisição
        """

        @app.route('/operations', methods=['POST'])
        def post():
            data = get_json_data()
            return FinancialService.post(data)
        """POST: Rota para registro de uma única operação financeira."""
        
        @app.route('/operations/bulk', methods=['POST'])
        def post_bulk():
            data = request.get_json()
            return FinancialService.post_bulk(data)
        """POST: Rota para registro de várias operações financeiras em lote."""
            
        @app.route('/operations/<int:id>', methods=['GET'])
        def get_operation(id):
            return FinancialService.get_operation(id)
        """GET: Rota para consulta de uma operação financeira específica à partir de seu id."""
        
        @app.route('/operations', methods=['GET'])
        def get_operations():
            page, per_page = get_pagination_params()
            data = get_json_data()
            return FinancialService.get_operations(page, per_page, data)
        """GET: Rota para consulta paginada de várias operações financeiras à partir de filtros"""

        @app.route('/operations/<int:id>', methods=['PUT'])
        def put(id):
            data = get_json_data()
            return FinancialService.put(id, data)
        """PUT: Rota para atualizar uma operação financeira específica à partir de seu id"""
        
        @app.route('/operations/<int:id>', methods=['DELETE'])
        def delete(id):
            return FinancialService.delete(id)
        """DELETE: Rota para deletar uma operação financeira"""
            