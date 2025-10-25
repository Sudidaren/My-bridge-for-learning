from app.database import Database
import json

class Survey:
    def __init__(self):
        self.db = Database()
        
    def get_all(self):
        query = "SELECT * FROM surveys WHERE is_public = TRUE"
        return self.db.execute_query(query)
        
    def get_by_id(self, survey_id):
        query = "SELECT * FROM surveys WHERE id = %s"
        result = self.db.execute_query(query, (survey_id,))
        return result[0] if result else None
        
    def create(self, name, author_id=None, is_public=True):
        query = '''
            INSERT INTO surveys (name, json_data, author_id, is_public)
            VALUES (%s, %s, %s, %s)
        '''
        return self.db.execute_query(
            query,
            (name, '{}', author_id, is_public),
            fetch=False
        )
        
    def update_json(self, survey_id, json_data):
        query = "UPDATE surveys SET json_data = %s WHERE id = %s"
        return self.db.execute_query(
            query,
            (json.dumps(json_data), survey_id),
            fetch=False
        )
        
    def update_name(self, survey_id, name):
        query = "UPDATE surveys SET name = %s WHERE id = %s"
        return self.db.execute_query(query, (name, survey_id), fetch=False)
        
    def delete(self, survey_id):
        query = "DELETE FROM surveys WHERE id = %s"
        return self.db.execute_query(query, (survey_id,), fetch=False)
        
    def get_user_surveys(self, user_id):
        query = "SELECT * FROM surveys WHERE author_id = %s"
        return self.db.execute_query(query, (user_id,))