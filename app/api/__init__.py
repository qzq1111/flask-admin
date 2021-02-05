from flask_restful import Api

from app.api.user import UserLogin

api = Api(prefix="/api/v1")

api.add_resource(UserLogin, '/login')
