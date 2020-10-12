from flask import Blueprint, request
from flask_cors import CORS
import controllers.notification_controller as controller

app = Blueprint('notification', __name__)
CORS(app)


@app.route("/notification", methods=["POST"])
def notification():
    return controller.save_notification_request(request.json)
