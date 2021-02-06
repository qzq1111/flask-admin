from flask_restful import Resource, reqparse

from app.models import SysRole, SysMenu, SysRoleMenu, db
from app.response import ResMsg


class CreateRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('role_name', type=str, required=True, help='角色名')
    parser.add_argument('menu_ids', type=int, action='append', help='菜单列表')

    def post(self):
        res = ResMsg()
        args = self.parser.parse_args()
        role_name = args.get("role_name")
        menu_ids = args.get("menu_ids") or []

        if not role_name:
            res.update(code=-1, msg="参数缺失")
            return res.data

        user = SysRole.query.filter(SysRole.role_name == role_name).first()
        if user:
            res.update(code=-1, msg="角色已存在")
            return res.data

        menu_ids = set(menu_ids)
        if menu_ids:
            query_menu = db.session.query(SysMenu.menu_id).filter(SysMenu.menu_id.in_(menu_ids)).all()
            is_exist_menu = set([item.menu_id for item in query_menu])

            if len(menu_ids) != len(is_exist_menu):
                res.update(code=-1, msg="绑定了不存在的菜单")
                return res.data

        try:
            new = SysRole()
            new.role_name = str(role_name).strip()
            db.session.add(new)
            db.session.flush()
            if menu_ids:
                role_menus = [dict(menu_id=item, role_id=new.role_id) for item in menu_ids]
                db.session.execute(SysRoleMenu.__table__.insert(role_menus))
                db.session.flush()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, msg=str(e))
            return res.data

        return res.data
