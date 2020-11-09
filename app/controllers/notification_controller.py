from models.notification import MongoDB
from datetime import datetime
from bson import ObjectId
from bson.json_util import dumps
import smtplib
import os


def retrieve_notification_request(user_id):
    db = MongoDB()
    connection_is_alive = db.test_connection()

    if connection_is_alive:
        notification = db.get_notification_by_user_id(user_id)

        return dumps(notification), 200

    db.close_connection()

    return {'error': 'Something gone wrong'}, 500


def save_notification_request_by_user(request):
    now = datetime.now()

    responsibles_emails = request['emails']
    responsibles_ids = request['users_ids']

    db = MongoDB()
    connection_is_alive = db.test_connection()

    if connection_is_alive:
        for responsible_id in responsibles_ids:

            notification = dict()
            notification['date'] = now.strftime("%m/%d/%Y, %H:%M:%S")
            notification['type'] = request["type"]
            notification['title'] = request["title"]
            notification['message'] = request["message"]
            notification['user'] = responsible_id
            notification['read'] = False

            db.insert_one(notification)

        send_email(request, responsibles_emails)
    else:
        return {"erro": "Erro ao conectar no banco de dados!"}, 500
    return {"msg": "Notificação cadastrada!"}, 200


def save_notification_request_by_contract(request):
    db = MongoDB()
    connection_is_alive = db.test_connection()
    if connection_is_alive:
        contract_id = ObjectId(request['contract'])
        contract = db.get_one(contract_id, 'contract')

        if not contract:
            return {"erro": "Contrato não encontrado!"}, 404
    else:
        return {"erro": "Erro ao conectar no banco de dados!"}, 500

    if 'responsibles' not in contract.keys():
        return {"erro": "O contrato não possui responsaveis!"}, 404

    responsibles = contract['responsibles']
    resposible_emails = []
    now = datetime.now()

    for responsible in responsibles:
        if 'email' in responsible.keys():
            resposible_emails.append(responsible['email'])

        notification = dict()
        notification['date'] = now.strftime("%m/%d/%Y, %H:%M:%S")
        notification['type'] = request["type"]
        notification['title'] = request["title"]
        notification['message'] = request["message"]
        notification['contract'] = request["contract"]
        notification['user'] = responsible["_id"]
        notification['read'] = False
        db.insert_one(notification)

    send_email(request, resposible_emails)

    return {"msg": "Notificação cadastrada!"}, 200


def save_notification_request(request):
    fields = ['type', 'winery', 'message', 'title']

    if not all(field in request.keys() for field in fields):
        return {
            "erro": "Preencha os campos obrigatórios!"
        }, 400

    if not request["type"]:
        return {
            "erro": "Informe o tipo de notificação!"
        }, 400

    if not request["title"]:
        return {
            "erro": "Informe o título da notificação!"
        }, 400

    if not request["message"]:
        return {
            "erro": "Informe a mensagem da notificação!"
        }, 400

    if not request["winery"]:
        return {
            "erro": "Informe a vinícola a ser notificada!"
        }, 400

    db = MongoDB()
    connection_is_alive = db.test_connection()
    if connection_is_alive:
        winery_id = ObjectId(request['winery'])
        winery = db.get_one(winery_id, 'winery')

        if not winery:
            return {"erro": "Vinícola não encontrada!"}, 404
    else:
        return {"erro": "Erro ao conectar no banco de dados!"}, 500

    if 'responsibles' not in winery.keys():
        return {"erro": "A vinícola não possui responsaveis!"}, 404

    responsibles = winery['responsibles']
    resposible_emails = []
    now = datetime.now()

    for responsible in responsibles:
        if 'email' in responsible.keys():
            resposible_emails.append(responsible['email'])

        notification = dict()
        notification['date'] = now.strftime("%m/%d/%Y, %H:%M:%S")
        notification['type'] = request["type"]
        notification['title'] = request["title"]
        notification['message'] = request["message"]
        notification['winery'] = request["winery"]
        notification['user'] = responsible["_id"]
        notification['read'] = False
        db.insert_one(notification)

    send_email(request, resposible_emails)

    return {"msg": "Notificação cadastrada!"}, 200


def mark_as_read(notification_id):
    notification_id = ObjectId(notification_id)
    db = MongoDB()
    connection_is_alive = db.test_connection()
    if connection_is_alive:
        notification = db.get_one(notification_id)

        if not notification:
            return {"erro": "Notificação não encontrada!"}, 404

        notification["read"] = True
        updated = db.update_one(notification)
        if updated:
            return {"message": "Success"}, 200

    return {'message': 'Something gone wrong'}, 500


def send_email(request, resposible_emails):
    if resposible_emails:
        message = "Subject: Notification\n\n" + request['message']
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.sendmail(os.getenv('EMAIL_USER'), resposible_emails, message)
