from auth import TokenRequired
from services.services import financialService
from flask import request, jsonify
from flask.views import MethodView
import jwt
from config import Config

class BaseAPI(MethodView):
    decorators = [TokenRequired]

    def get_json_data(self):
        return request.get_json()

    def get_pagination_params(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return page, per_page

class HealthCheck(MethodView):
    def get(self):
        token = jwt.encode(payload={"data": "idunno"}, key=Config.SECRET_KEY)
        return jsonify(token=token)

class OperationAPI(BaseAPI):
    def post(self):
        data = self.get_json_data()
        return financialService.create_operation(data)

    def get(self):
        page, per_page = self.get_pagination_params()
        data = self.get_json_data()
        return financialService.get_operations(page, per_page, data)

class SingularOperationAPI(BaseAPI):
    def get(self, id):
        return financialService.get_singular_operation(id)

    def put(self, id):
        data = self.get_json_data()
        return financialService.update_operation(id, data)

    def delete(self, id):
        return financialService.delete_operation(id)

class BulkOperationAPI(BaseAPI):
    def post(self):
        data = self.get_json_data()
        return financialService.create_bulk_operation(data)

def create_routes(app):
    app.add_url_rule('/health', view_func=HealthCheck.as_view('health_check'))
    app.add_url_rule('/operations', view_func=OperationAPI.as_view('operations_api'))
    app.add_url_rule('/operations/<int:id>', view_func=SingularOperationAPI.as_view('singular_operation_api'))
    app.add_url_rule('/operations/bulk', view_func=BulkOperationAPI.as_view('bulk_operation_api'))