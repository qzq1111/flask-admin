from flask_restful import Resource, reqparse

from app.models import SysMenu, db
from app.response import ResMsg


class CreateMenu(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('menu_name', type=str, required=True, help='组件菜单名')
    parser.add_argument('menu_title', type=str, required=True, help='显示的菜单名')
    parser.add_argument('parent_id', type=int, required=True, help='父菜单ID')
    parser.add_argument('order_num', type=int, required=True, help='显示顺序')
    parser.add_argument('path', type=str, required=True, help='路由地址')
    parser.add_argument('component', type=str, required=True, help='组件地址')
    parser.add_argument('menu_type', type=str, required=True, help='菜单类型 M目录 C菜单 F按钮')
    parser.add_argument('status', type=int, required=True, help='菜单状态1显示 0隐藏')
    parser.add_argument('visible', type=int, required=True, help='菜单状态1正常 0停用')
    parser.add_argument('perms', type=str, required=True, help='权限标识')
    parser.add_argument('icon', type=str, required=True, help='菜单图标')
    parser.add_argument('remark', type=str, required=True, help='备注')

    def post(self):
        res = ResMsg()
        args = self.parser.parse_args()
        parent_id = args.get("parent_id")
        # 判断父级ID是否存在
        if parent_id:
            query = db.session.query(SysMenu).filter(SysMenu.menu_id == parent_id).first()
            if not query:
                res.update(code=-1, msg="父菜单不存在")
                return res.data
        else:
            args["component"] = "Layout"

        try:
            new = SysMenu(**args)
            db.session.add(new)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, msg=str(e))

        return res.data


class GetMenuList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('menu_title', type=str, required=False, help='显示的菜单名')

    def post(self):
        res = ResMsg()
        args = self.parser.parse_args()
        menu_title = args.get("menu_title")

        query = db.session.query(SysMenu)
        if menu_title:
            query = query.filter(SysMenu.menu_title.like(f"%{menu_title}%"))
        query = query.all()
        data = list(map(lambda x: {p.key: getattr(x, p.key) for p in SysMenu.__mapper__.iterate_properties}, query))
        res.update(data=data)
        return res.data
