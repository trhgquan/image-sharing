from serverside.db import get_db
import secrets

class UserModel:
    def __init__(self, token_length = 16):
        self.__db = get_db()
        self.__token_length = token_length
    
    def generate_token(self):
        return secrets.token_hex(self.__token_length)

    def get_total_users(self):
        '''Get total users in the database (for creating new ID procedure)

        Output:
            - total_user : Total users
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM user WHERE 1', ()
        )

        row = db_exec.fetchone()

        return row[0]
    
    def get_user_public_key(self, user_id):
        '''Get user Public Key and Key Length (n)

        Input:
            - user_id : User ID
        
        Output:
            - public_key : user_id's public key
            - key_length : user_id's key length (n)
        '''
        db_exec = self.__db.execute(
            'SELECT public_key, key_length FROM user WHERE id = ?',
            (user_id,)
        )

        row = db_exec.fetchone()

        return row[0], row[1]

    def get_user_name(self, user_id):
        '''Get user's name

        Input:
            - user_id

        Output:
            - user_name
        '''
        db_exec = self.__db.execute(
            'SELECT name FROM user WHERE id = ?',
            (user_id,)
        )

        row = db_exec.fetchone()

        return row[0]

    def check_user_exist(self, user_id):
        '''Check if user exist a.k.a has a record on database

        Input:
            - user_id
        
        Output:
            - True if user existed, False otherwise
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM user WHERE (id = ?)',
            (user_id,)
        )

        row = db_exec.fetchone()

        return not (row[0] == 0)

    def check_api_token(self, user_id, api_token):
        '''Check if api_token is valid

        Input:
            - user_id
            - api_token
        
        Output:
            - True if api_token is valid, False otherwise
        '''
        db_exec = self.__db.execute(
            'SELECT * FROM user WHERE (id = ?) AND (api_token = ?)', 
            (user_id, api_token)
        )

        row = db_exec.fetchone()
        
        return not (row == None)

    def check_verify_token(self, user_id, verify_token):
        '''Check if verify_token is valid

        Input:
            - user_id
            - verify_token
        
        Output:
            - True if verify_token is valid, False otherwise
        '''
        db_exec = self.__db.execute(
            'SELECT verify_token FROM user WHERE (id = ?)',
            (user_id,)
        )

        row = db_exec.fetchone()
        
        return row != None and verify_token == row[0]

    def check_public_key_exist(self, public_key, key_length):
        '''Check if public_key existed

        Input:
            - public_key
            - key_length (n)
        
        Output:
            - True if existed, False otherwise
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM user WHERE public_key = ? AND key_length = ?',
            (public_key, key_length)
        )

        row = db_exec.fetchone()

        return row[0] > 0

    def loginable(self, user_id):
        '''Conditions for user to be loginable
        '''
        return self.check_user_exist(user_id)

    def login_pending(self, user_id, verify_token):
        '''Create a new verify token for user.

        Input:
            - user_id 
            - verify_token (encrypted with RSA)
        '''
        self.__db.execute(
            'UPDATE user SET verify_token = ? WHERE id = ?',
            (verify_token, user_id)
        )

        self.__db.commit()

    def login_accepted(self, user_id):
        '''Create a new API token for user.

        Input:
            - user_id
        
        Output:
            - api_token
        '''
        api_token = self.generate_token()

        self.__db.execute(
            'UPDATE user SET verify_token = NULL, api_token = ? WHERE (id = ?)',
            (api_token, user_id)
        )

        self.__db.commit()

        return api_token
   
    def logout(self, user_id):
        '''Log user out aka remove his API token.

        Input:
            - user_id
        '''
        self.__db.execute(
            'UPDATE user SET api_token = NULL, verify_token = NULL WHERE id = ?',
            (user_id,)
        )

        self.__db.commit()

    def create_user(self, name, public_key, key_length):
        '''Save a new user

        Input:
            - name
            - public_key : RSA public key e
            - key_length : n
        '''
        new_id = self.get_total_users() + 1

        self.__db.execute(
            'INSERT INTO user (id, name, public_key, key_length) VALUES (?, ?, ?, ?)',
            (new_id, name, public_key, key_length)
        )

        self.__db.commit()

        return new_id
