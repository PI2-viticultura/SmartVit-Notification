from models.notification import MongoDB
import smtplib


def save_notification_request(request):
    fields = ['type', 'winery', 'sender', 'password']

    if not all(field in request.keys() for field in fields):
        return {
            "erro": "Preencha os campos obrigatórios!"
        }, 400

    if not request["type"]:
        return {
            "erro": "Informe o tipo de notificação!"
        }, 400

    if not request["winery"]:
        return {
            "erro": "Informe a vinícola a ser notificada!"
        }, 400

    message = "Subject: Notification\n\nteste"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(request['sender'], request['password'])
    server.sendmail(request['sender'], ['lucasvitorifg@gmail.com'], message)

    return {
        "erro": "Informe a vinícola a ser notificada!"
    }, 200
