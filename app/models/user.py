from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Database

class User:
    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email
        self.db = Database()
        
    def set_password(self, password):
        return generate_password_hash(password)
        
    def check_password(self, password_hash, password):
        return check_password_hash(password_hash, password)
        
    def create(self, password):
        password_hash = self.set_password(password)
        query = '''
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
        '''
        return self.db.execute_query(
            query, 
            (self.username, self.email, password_hash),
            fetch=False
        )
        
    @staticmethod
    def get_by_email(email):
        db = Database()
        query = "SELECT * FROM users WHERE email = %s"
        result = db.execute_query(query, (email,))
        return result[0] if result else None
        
    @staticmethod
    def get_by_id(user_id):
        db = Database()
        query = "SELECT * FROM users WHERE id = %s"
        result = db.execute_query(query, (user_id,))
        return result[0] if result else None