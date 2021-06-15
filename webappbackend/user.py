from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):

    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)