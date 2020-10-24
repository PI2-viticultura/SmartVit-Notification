from settings import load_database_params
import pymongo


class MongoDB():
    def __init__(self):
        """Constructor to model class."""
        self.params = load_database_params()
        try:
            self.client = pymongo.MongoClient(**self.params,
                                              serverSelectionTimeoutMS=10)
        except Exception as err:
            print(f'Erro ao conectar no banco de dados: {err}')

    def test_connection(self):
        try:
            self.client.server_info()
            return True
        except Exception as err:
            print(f'Erro ao conectar no banco de dados: {err}')
            return False

    def close_connection(self):
        self.client.close()

    def get_collection(self, collection='notifications'):
        db = self.client['smart-dev']
        collection = db[collection]
        return collection

    def insert_one(self, body):
        try:
            collection = self.get_collection()
            collection.insert_one(body)
            return True
        except Exception as err:
            print(f'Erro ao inserir no banco de dados: {err}')
            return False

    def update_one(self, body, collection='notifications'):
        try:
            collection = self.get_collection(collection)

            collection.update_one(
                {"_id": body["_id"]},
                {"$set": body}
            )
            return True

        except Exception as err:
            print(f'Erro ao atualizar no banco de dados: {err}')

    def delete_one(self, identifier):
        try:
            collection = self.get_collection()
            res = collection.delete_one({"_id": identifier})
            if res.deleted_count == 1:
                print(f'Praga removida com sucesso {identifier}'
                      'removida com sucesso')
            else:
                print(f'Erro ao remover a praga {identifier}:'
                      'nenhuma praga encontrada para o id')
        except Exception as err:
            print(f'Erro ao deletar no banco de dados: {err}')

    def get_one(self, identifier, collection='notifications'):
        collection = self.get_collection(collection)
        return collection.find_one({"_id": identifier})

    def get_all(self, collection='notifications'):
        collection = self.get_collection(collection)
        return collection.fin()

    def get_notification_by_user_id(self, identifier):
        collection = self.get_collection('notifications')
        return collection.find({"user": identifier, "read": False})
