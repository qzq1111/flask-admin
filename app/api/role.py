from flask_restful import Resource, reqparse

from app.models import SysRole, db
from app.response import ResMsg


class CreateRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('role_name', type=str, required=True, help='角色名')

    def post(self):
        res = ResMsg()
        args = self.parser.parse_args()
        role_name = args.get("role_name")

        if not role_name:
            res.update(code=-1, msg="参数缺失")
            return res.data

        user = SysRole.query.filter(SysRole.role_name == role_name).first()
        if user:
            res.update(code=-1, msg="角色已存在")
            return res.data

        try:
            new = SysRole()
            new.role_name = str(role_name).strip()
            db.session.add(new)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, msg=str(e))
            return res.data

        return res.data
