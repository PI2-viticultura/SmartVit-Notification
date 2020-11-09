from flask import Blueprint, request
from flask_cors import CORS
import controllers.notification_controller as controller

app = Blueprint('notification', __name__)
CORS(app)


@app.route("/notification", methods=["POST"])
def notification():
    return controller.save_notification_request(request.json)


@app.route("/notification/<string:user_id>", methods=["GET"])
def notification_get(user_id):
    return controller.retrieve_notification_request(user_id)


@app.route("/notification/<string:notification_id>", methods=["PATCH"])
def notification_read(notification_id):
    return controller.mark_as_read(notification_id)


@app.route("/user-notification", methods=["POST"])
def notification_user():
    return controller.save_notification_request_by_user(request.json)


@app.route("/contract-notification", methods=["POST"])
def notification_contract():
    return controller.save_notification_request_by_contract(request.json)
