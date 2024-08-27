from flask import Flask
from routes.financial_operations import create_routes


app = Flask(__name__)

create_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)