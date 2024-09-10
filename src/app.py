from flask import Flask
from routes.financial_operations import health_bp, operations_bp 

app = Flask(__name__)

app.register_blueprint(health_bp)
app.register_blueprint(operations_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)