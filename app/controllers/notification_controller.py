from models.notification import MongoDB
from datetime import datetime
from bson import ObjectId
import smtplib


def save_notification_request(request):
    fields = ['type', 'winery', 'sender', 'password', 'message']

    if not all(field in request.keys() for field in fields):
        return {
            "erro": "Preencha os campos obrigatórios!"
        }, 400

    if not request["type"]:
        return {
            "erro": "Informe o tipo de notificação!"
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
        notification['date'] = now
        notification['type'] = request["type"]
        notification['message'] = request["message"]
        notification['winery'] = request["winery"]
        notification['user'] = responsible["_id"]
        notification['read'] = False
        db.insert_one(notification)

    send_email(request, resposible_emails)
    
    return {"msg": "Notificação cadastrada!"}, 200


def send_email(request, resposible_emails):
    if resposible_emails:
        message = "Subject: Notification\n\n" + request['message']
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(request['sender'], request['password'])
        server.sendmail(request['sender'], resposible_emails, message)
