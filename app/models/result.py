from app.database import Database
import json

class Result:
    def __init__(self):
        self.db = Database()
    
    def create(self, survey_id, json_data, user_id=None):
        query = '''
            INSERT INTO results (survey_id, user_id, json_data)
            VALUES (%s, %s, %s)
        '''
        return self.db.execute_query(
            query,
            (survey_id, user_id, json.dumps(json_data)),
            fetch=False
        )
    
    def get_survey_results(self, survey_id):
        query = "SELECT * FROM results WHERE survey_id = %s"
        results = self.db.execute_query(query, (survey_id,))
        if not results:
            return None
        return {
            'id': survey_id,
            'data': [json.loads(r['json_data']) for r in results]
        }
    
    def get_user_results(self, user_id):
        query = "SELECT * FROM results WHERE user_id = %s"
        return self.db.execute_query(query, (user_id,))