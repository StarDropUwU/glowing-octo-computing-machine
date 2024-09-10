from auth import token_required
from services.services import FinancialService
from flask import request, jsonify, Blueprint
from flask.views import MethodView
import jwt
from config import Config

# Definindo os blueprints para os endpoints de health check e operações
health_bp = Blueprint('health', __name__)
operations_bp = Blueprint('operations', __name__)

class HealthCheck:
    """
    Endpoint para verificação de saúde do sistema.
    Retorna um token JWT válido para fins de health check.
    """

    @staticmethod
    @health_bp.route('/health', methods=['GET'])
    def get():
        """
        Gera e retorna um token JWT para verificação da saúde da aplicação.

        :return: JSON contendo o token JWT.
        """
        token = jwt.encode(payload={"purpose": "health_check"}, key=Config.SECRET_KEY)
        return jsonify(token=token)

class OperationsAPI:
    """
    API para operações financeiras, incluindo criação, atualização, exclusão e listagem.
    Todos os endpoints requerem um token JWT válido para autenticação.
    """

    @staticmethod
    def get_json_data():
        """
        Extrai e retorna os dados JSON do corpo da requisição.

        :return: Dados em formato JSON.
        """
        return request.get_json()

    @staticmethod
    def get_pagination_params():
        """
        Extrai e retorna os parâmetros de paginação (page, per_page) da requisição.

        :return: Uma tupla contendo page e per_page.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return page, per_page

    @staticmethod
    @operations_bp.route('/operations', methods=['POST'])
    @token_required
    def create_operation():
        """
        Cria uma operação financeira individual.

        :return: Resposta JSON com o status da criação da operação.
        """
        data = OperationsAPI.get_json_data()
        return FinancialService.post(data)

    @staticmethod
    @operations_bp.route('/operations/bulk', methods=['POST'])
    @token_required
    def create_bulk_operations():
        """
        Cria múltiplas operações financeiras em lote.

        :return: Resposta JSON com o status da criação das operações em lote.
        """
        data = OperationsAPI.get_json_data()
        return FinancialService.post_bulk(data)

    @staticmethod
    @operations_bp.route('/operations/<int:operation_id>', methods=['GET'])
    @token_required
    def get_operation(operation_id):
        """
        Recupera uma operação financeira específica pelo seu ID.

        :param operation_id: ID da operação a ser recuperada.
        :return: Resposta JSON com os dados da operação ou erro se não for encontrada.
        """
        return FinancialService.get_operation(operation_id)

    @staticmethod
    @operations_bp.route('/operations', methods=['GET'])
    @token_required
    def get_operations():
        """
        Recupera uma lista paginada de operações financeiras com filtros opcionais.

        :return: Resposta JSON com a lista de operações financeiras filtradas.
        """
        page, per_page = OperationsAPI.get_pagination_params()
        filters = OperationsAPI.get_json_data() or {}  # Garantir que o filtro seja um dicionário vazio se não houver dados
        return FinancialService.get_operations(page, per_page, filters)

    @staticmethod
    @operations_bp.route('/operations/<int:operation_id>', methods=['PUT'])
    @token_required
    def update_operation(operation_id):
        """
        Atualiza uma operação financeira específica pelo seu ID.

        :param operation_id: ID da operação a ser atualizada.
        :return: Resposta JSON com o status da atualização.
        """
        data = OperationsAPI.get_json_data()
        return FinancialService.put(operation_id, data)

    @staticmethod
    @operations_bp.route('/operations/<int:operation_id>', methods=['DELETE'])
    @token_required
    def delete_operation(operation_id):
        """
        Exclui uma operação financeira específica pelo seu ID.

        :param operation_id: ID da operação a ser excluída.
        :return: Resposta JSON confirmando a exclusão da operação.
        """
        return FinancialService.delete(operation_id)
