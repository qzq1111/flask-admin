from flask_restful import Resource, reqparse

from app.auth import Auth
from app.models import SysUser, db
from app.response import ResMsg


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_name', type=str, required=True, help='账号缺失')
    parser.add_argument('password', type=str, required=True, help='密码缺失')

    def post(self):
        res = ResMsg()
        args = self.parser.parse_args()
        user_name = args.get("user_name")
        password = args.get("password")
        user = SysUser.query.filter(SysUser.user_name == user_name, SysUser.status == 0).first()
        if not user:
            res.update(code=-1, msg="账号或密码错误")
            return res.data

        if not user.check_password(password):
            res.update(code=-1, msg="账号或密码错误")
            return res.data

        res.update(data={"token": Auth.generate_access_token(user_id=user.user_id)})

        return res.data
