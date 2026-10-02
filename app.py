from flask import Flask
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError
from routes.rooms import rooms_bp
from routes.auth import auth_bp
from routes.reservations import reservations_bp


app = Flask(__name__)

app.secret_key = "dev-secret-key"

app.register_blueprint(rooms_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(reservations_bp)

# エラーハンドラ
@app.errorhandler(BadRequest)
def handle_bad_request(error):
    return {"error": "invalid_json"}, 400

@app.errorhandler(NotFound)
def handle_not_found(error):
    return {"error": "not_found"}, 404

@app.errorhandler(InternalServerError)
def handle_internal_server_error(error):
    return{"error": "internal_server_error"}, 500


if __name__ == "__main__":
    app.run(debug=True)
