from flask import g
from flask_restful import Resource, reqparse

from app import utils, mark
from app.auth import login_required, generate_access_token
from app.models import SysUser, db, SysRole, SysUserRole, SysMenu, SysRoleMenu
from app.response import ResMsg
from app.utils import BuildMenuTree


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_name', type=str, required=True, help='账号缺失')
    parser.add_argument('password', type=str, required=True, help='密码缺失')

    def post(self):
        """用户登录"""
        res = ResMsg()
        args = self.parser.parse_args()
        user_name = args.get("user_name")
        password = args.get("password")

        # step1 获取用户
        user = SysUser.query.filter(SysUser.user_name == user_name, SysUser.status == mark.Enable).first()
        if not user:
            res.update(code=-1, msg="账号或密码错误")
            return res.data

        if not user.check_password(password):
            res.update(code=-1, msg="账号或密码错误")
            return res.data

        # step2 获取用户角色
        role = db.session.query(SysRole). \
            join(SysUserRole, SysUserRole.role_id == SysRole.role_id). \
            filter(SysUserRole.user_id == user.user_id, SysRole.status == mark.Enable).first()
        if not role:
            res.update(code=-1, msg="用户角色已被禁用或不存在")
            return res.data

        res.update(data={"token": generate_access_token(user_id=user.user_id, role_id=role.role_id)})

        return res.data


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_name', type=str, required=True, help='账号缺失')
    parser.add_argument('password', type=str, required=True, help='密码缺失')
    parser.add_argument('role_id', type=int, required=True, help='角色缺失')

    @login_required
    def post(self):
        """新建用户"""
        res = ResMsg()
        args = self.parser.parse_args()
        user_name = args.get("user_name")
        password = args.get("password")
        role_id = args.get("role_id")

        if not user_name or not password or not role_id:
            res.update(code=-1, msg="参数缺失")
            return res.data

        # 判断用户名是否重复
        user = SysUser.query.filter(SysUser.user_name == user_name).first()
        if user:
            res.update(code=-1, msg="用户已存在")
            return res.data

        # 判断角色是否存在
        role = SysRole.query.filter(SysRole.role_id == role_id, SysRole.status == mark.Enable).first()
        if not role:
            res.update(code=-1, msg="角色不存在或已被禁用")
            return res.data

        try:
            new_user = SysUser()
            new_user.user_name = str(user_name).strip()
            new_user.password = utils.get_md5(str(password).strip().encode("utf-8"))
            db.session.add(new_user)
            db.session.flush()

            new_user_role = SysUserRole()
            new_user_role.user_id = new_user.user_id
            new_user_role.role_id = role_id
            db.session.add(new_user_role)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, msg=str(e))
            return res.data

        return res.data

    @login_required
    def get(self, user_id):
        """获取用户"""
        res = ResMsg()
        if not user_id:
            res.update(code=-1, msg="参数缺失")
            return res.data

        user = SysUser.query.filter(SysUser.user_id == user_id).first()
        if not user:
            res.update(code=-1, msg="用户不存在")
            return res.data
        data = {p.key: getattr(user, p.key) for p in SysUser.__mapper__.iterate_properties}
        res.update(data=data)
        return res.data

    @login_required
    def delete(self, user_id):
        """删除用户"""
        res = ResMsg()
        if not user_id:
            res.update(code=-1, msg="参数缺失")
            return res.data

        user = SysUser.query.filter(SysUser.user_id == user_id).first()
        if not user:
            return res.data

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, msg=str(e))
            return res.data

        return res.data


class UserListResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('user_name', type=str, help='用户账号')
    parser.add_argument('page', type=int, help='页码')
    parser.add_argument('page_size', type=int, help='条数')

    @login_required
    def get(self):
        """获取用户列表"""
        res = ResMsg()
        args = self.parser.parse_args()
        user_name = args.get("user_name")
        page = args.get("page") or mark.DefaultPage
        page_size = args.get("page_size") or mark.DefaultPageSize

        query = db.session.query(SysUser.user_id, SysUser.user_name,
                                 SysUser.status, SysUser.create_time,
                                 SysRole.role_id, SysRole.role_name,
                                 ). \
            join(SysUserRole, SysUserRole.user_id == SysUser.user_id). \
            join(SysRole, SysRole.role_id == SysUserRole.role_id)
        if user_name:
            query = query.filter(SysUser.user_name.like(f"%{user_name}%"))

        total = query.count()

        users = query.slice((page - 1) * page_size, page * page_size).all()
        data = [dict(zip(user.keys(), user)) for user in users]
        res.update(data=data)
        res.add_field("total", total)

        return res.data


class UserInfoResource(Resource):

    @login_required
    def get(self):
        """获取用户信息"""
        res = ResMsg()
        # step1 获取用户信息
        user_id = g.user_id
        user = SysUser.query.filter(SysUser.user_id == user_id).first()
        if not user:
            res.update(code=-1, msg="用户不存在")
            return res.data

        # step2 获取用户角色
        role = db.session.query(SysRole). \
            join(SysUserRole, SysUserRole.role_id == SysRole.role_id). \
            filter(SysUserRole.user_id == user_id).first()
        if not role:
            res.update(code=-1, msg="用户角色不存在")
            return res.data

        # step3 获取用户菜单权限
        perm = db.session.query(SysMenu.perms). \
            join(SysRoleMenu, SysRoleMenu.menu_id == SysMenu.menu_id). \
            filter(SysRoleMenu.role_id == role.role_id).all()

        data = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_status": user.status,
            "role_id": role.role_id,
            "role_name": role.role_name
        }
        if user_id == 1:
            data["permissions"] = "*:*:*"
        else:
            data["permissions"] = [item.perms for item in perm]

        res.update(data=data)
        return res.data


class UserMenuResource(Resource):

    @login_required
    def get(self):
        """获取用户菜单"""
        res = ResMsg()
        role_id = g.role_id
        user_id = g.user_id

        if user_id == 1:
            query = db.session.query(SysMenu).all()
        else:
            query = db.session.query(SysMenu). \
                join(SysRoleMenu, SysRoleMenu.menu_id == SysMenu.menu_id). \
                filter(SysRoleMenu.role_id == role_id).all()
        tree = BuildMenuTree(query)
        data = tree.sidebar_tree()
        res.update(data=data)
        return res.data


class UserStatusResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('status', type=int, required=True, help='用户状态码缺失')

    @login_required
    def put(self, user_id):
        """修改用户状态"""
        res = ResMsg()
        args = self.parser.parse_args()
        status = args.get("status")
        if not user_id or status not in [mark.Enable, mark.Disable]:
            res.update(code=-1, msg="参数缺失")
            return res.data

        user = SysUser.query.filter(SysUser.user_id == user_id).first()
        if not user:
            res.update(code=-1, msg="用户不存在")
            return res.data

        try:
            user.status = status
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            res.update(code=-1, msg=str(e))
            return res.data
        return res.data


class UserLogout(Resource):

    def post(self):
        """退出登录"""
        res = ResMsg()
        return res.data
