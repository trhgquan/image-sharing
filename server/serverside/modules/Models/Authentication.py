from serverside.db import get_db
import secrets

class UserAuthentication:
    def __init__(self, token_length = 16):
        self.__db = get_db()
        self.__token_length = token_length
    
    def generate_token(self):
        return secrets.token_hex(self.__token_length)

    def check_user_exist(self, user_id):
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM user WHERE (id = ?)',
            (user_id)
        )

        row = db_exec.fetchone()

        return not (row[0] == 0)

    def check_api_token(self, user_id, api_token):
        db_exec = self.__db.execute(
            'SELECT * FROM user WHERE (id = ?) AND (api_token = ?)', 
            (user_id, api_token)
        )

        row = db_exec.fetchone()
        
        return not (row == None)


    def check_verify_token(self, user_id, verify_token):
        db_exec = self.__db.execute(
            'SELECT verify_token FROM user WHERE (id = ?)',
            (user_id)
        )

        row = db_exec.fetchone()
        
        return verify_token == row[0]

    def loginable(self, user_id):
        return self.check_user_exist(user_id)

    def login_pending(self, user_id, verify_token):
        self.__db.execute(
            'UPDATE user SET verify_token = ? WHERE id = ?',
            (verify_token, user_id)
        )

        self.__db.commit()

    def login_accepted(self, user_id):
        api_token = self.generate_token()

        self.__db.execute(
            'UPDATE user SET verify_token = NULL, api_token = ? WHERE (id = ?)',
            (api_token, user_id)
        )

        self.__db.commit()

        return api_token
