from flask import Blueprint
from flask_restful import Api

from app.api.menu import CreateMenu, GetMenuList, SelectMenus
from app.api.role import CreateRole
from app.api.user import UserLogin, CreateUser

# 用户
api_user_bp = Blueprint("user", __name__, url_prefix="/api/v1/user")
api_user = Api(api_user_bp)
api_user.add_resource(UserLogin, '/login')
api_user.add_resource(CreateUser, '/add')

# 角色
api_role_bp = Blueprint("role", __name__, url_prefix="/api/v1/role")
api_role = Api(api_role_bp)
api_role.add_resource(CreateRole, '/add')

# 菜单
api_menu_bp = Blueprint("menu", __name__, url_prefix="/api/v1/menu")
api_menu = Api(api_menu_bp)
api_menu.add_resource(CreateMenu, '/add')
api_menu.add_resource(GetMenuList, '/list')
api_menu.add_resource(SelectMenus, '/selectMenus')
