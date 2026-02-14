from src.models.apikey_model import ApiKeyModel

class ExchangeController:
    def __init__(self):
        self.model = ApiKeyModel()

    def list_exchanges(self):
        return self.model.get_exchanges()

    def add_exchange(self, name, display_name):
        return self.model.add_exchange(name, display_name)

    def get_api_keys_for_user(self, user_id):
        return self.model.get_api_keys_for_user(user_id)

    def add_api_key(self, account_id, exchange_id, api_key, api_secret, label=None):
        return self.model.add_api_key(account_id, exchange_id, api_key, api_secret, label)

    def delete_api_key(self, api_key_id):
        return self.model.delete_api_key(api_key_id)

    def update_api_key(self, api_key_id, api_key, api_secret, label=None):
        return self.model.update_api_key(api_key_id, api_key, api_secret, label)
