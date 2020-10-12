from models.pest import MongoDB


def save_pest_request(request):
    fields = ['type', 'winery']

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

    
    # db = MongoDB()
    # connection_is_alive = db.test_connection()

    # if connection_is_alive:
    #     if(db.insert_one(request)):
    #         return {"message": "Sucess"}, 200
    # db.close_connection()

    return {'error': 'Something gone wrong'}, 500
