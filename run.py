from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import check_password_hash
from app.config import Config
from app.database import Database
from app.models.user import User
from app.models.survey import Survey
from app.models.result import Result
import os

app = Flask(__name__, static_folder=None, static_url_path=None)
app.config.from_object(Config)


jwt = JWTManager(app)
CORS(app)


db = Database()
db.initialize_db()

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.get_by_email(data.get('email')):
        return jsonify({'message': 'Email already registered'}), 400
        
    user = User(username=data.get('username'), email=data.get('email'))
    user_id = user.create(data.get('password'))
    
    if user_id:
        return jsonify({'message': 'User created successfully', 'id': user_id}), 201
    return jsonify({'message': 'Error creating user'}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_by_email(data.get('email'))
    
    if user and User().check_password(user['password_hash'], data.get('password')):
        access_token = create_access_token(identity=user['id'])
        return jsonify({
            'access_token': access_token,
            'user_id': user['id']
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/getActive', methods=['GET'])
def get_active():
    survey = Survey()
    return jsonify(survey.get_all())

@app.route('/api/getSurvey', methods=['GET'])
def get_survey():
    survey_id = request.args.get('surveyId')
    survey = Survey()
    return jsonify(survey.get_by_id(survey_id))

@app.route('/api/create', methods=['GET'])
@jwt_required()
def create():
    current_user_id = get_jwt_identity()
    name = request.args.get('name')
    survey = Survey()
    survey_id = survey.create(name, current_user_id)
    return jsonify(survey.get_by_id(survey_id))

@app.route('/api/changeName', methods=['GET'])
@jwt_required()
def change_name():
    survey = Survey()
    survey.update_name(request.args.get('id'), request.args.get('name'))
    return jsonify(survey.get_by_id(request.args.get('id')))

@app.route('/api/changeJson', methods=['POST'])
@jwt_required()
def change_json():
    data = request.get_json()
    survey = Survey()
    survey.update_json(data.get('id'), data.get('json'))
    return jsonify(survey.get_by_id(data.get('id')))

@app.route('/api/delete', methods=['GET'])
@jwt_required()
def delete():
    obj_id = request.args.get('id')
    survey = Survey()
    survey.delete(obj_id)
    return jsonify({'id': obj_id})

@app.route('/api/post', methods=['POST'])
def post_results():
    data = request.get_json()
    result = Result()
    current_user_id = None
    try:
        current_user_id = get_jwt_identity()
    except:
        pass
    result.create(data.get('postId'), data.get('surveyResult'), current_user_id)
    return jsonify({})

@app.route('/api/results', methods=['GET'])
def get_results():
    result = Result()
    return jsonify(result.get_survey_results(request.args.get('postId')))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'favicon.ico')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'manifest.json')

@app.route('/static/<path:filename>')
def serve_nested_static(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static', 'static'), filename)

@app.route('/logo192.png')
def logo192():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'logo192.png')

@app.route('/logo512.png')
def logo512():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'logo512.png')

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'robots.txt')

@app.route('/asset-manifest.json')
def asset_manifest():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'asset-manifest.json')

@app.route('/mockServiceWorker.js')
def mock_service_worker():
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'mockServiceWorker.js')

@app.route('/about')
@app.route('/run/<path:path>')
@app.route('/edit/<path:path>')
@app.route('/results/<path:path>')
@app.route('/', defaults={'path': 'index.html'})
def serve_static(path=None):
    return send_from_directory(os.path.join(os.getcwd(), 'app', 'static'), 'index.html')

if __name__ == '__main__':
    if not os.path.exists('flask_session'):
        os.makedirs('flask_session')
    app.run(debug=True)
