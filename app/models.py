from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.utils import get_md5

db = SQLAlchemy()


class SysUser(db.Model):
    __tablename__ = "sys_user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, info="用户ID")  # 用户ID
    user_name = db.Column(db.String(20), nullable=False, info="用户名")  # 用户名
    password = db.Column(db.String(36), nullable=False, info="密码")  # 密码
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, info="更新时间")
    status = db.Column(db.Integer, default=0, info="用户状态")  # 用户状态

    def check_password(self, p: str) -> bool:
        return get_md5(p.encode("utf-8")) == self.password


class SysUserRole(db.Model):
    __tablename__ = "sys_user_role"
    user_id = db.Column(db.Integer, primary_key=True, index=True, info="用户ID")
    role_id = db.Column(db.Integer, primary_key=True, index=True, info="角色ID")


class SysRole(db.Model):
    __tablename__ = "sys_role"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, info="角色ID")  # 角色ID
    role_name = db.Column(db.String(20), nullable=False, info="角色名")  # 角色名
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, info="更新时间")
    status = db.Column(db.Integer, default=0, info="角色状态")


class SysRoleMenu(db.Model):
    __tablename__ = "sys_role_menu"
    menu_id = db.Column(db.Integer, primary_key=True, index=True, info="菜单ID")
    role_id = db.Column(db.Integer, primary_key=True, index=True, info="角色ID")


class SysMenu(db.Model):
    __tablename__ = "sys_menu"

    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, info="菜单ID")  # 菜单ID
    menu_name = db.Column(db.String(20), nullable=False, info="组件菜单名")  # 组件菜单名
    menu_title = db.Column(db.String(255), info="显示的菜单名")  # 显示的菜单名
    parent_id = db.Column(db.Integer, info="父菜单ID")  # 父菜单ID
    order_num = db.Column(db.Integer, info="显示顺序")  # 显示顺序
    path = db.Column(db.String(200), info="路由地址")  # 路由地址
    component = db.Column(db.String(255), info="组件地址")  # 组件地址
    menu_type = db.Column(db.String(1), info="菜单类型 M目录 C菜单 F按钮")  # 菜单类型 M目录 C菜单 F按钮
    status = db.Column(db.Integer, info="菜单状态1显示 0隐藏")  # 菜单状态1显示 0隐藏
    visible = db.Column(db.Integer, info="菜单状态1正常 0停用")  # 菜单状态1正常 0停用
    perms = db.Column(db.String(50), info="权限标识")  # 权限标识
    icon = db.Column(db.String(100), info="菜单图标")  # 菜单图标
    remark = db.Column(db.String(500), info="备注")  # 备注
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now, info="创建时间")
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, info="更新时间")
