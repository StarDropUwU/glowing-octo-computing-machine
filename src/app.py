from flask import Flask
from routes.financial_operations import OperationsAPI, HealthCheck

app = Flask(__name__)

HealthCheck.create_health_check_route(app) 
OperationsAPI.create_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)