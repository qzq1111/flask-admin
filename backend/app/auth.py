import jwt
from datetime import datetime, timedelta
from flask import request, g
from functools import wraps

from app.response import ResMsg

key = 'super-man$&123das%qzq'


def generate_access_token(user_id, role_id, algorithm: str = 'HS256', exp: float = 2):
    """
    生成access_token
    :param user_id: 用户Id
    :param role_id: 角色Id
    :param algorithm: 加密算法
    :param exp: 过期时间
    :return:
    """

    now = datetime.utcnow()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'iat': now,  # 开始时间
        'iss': 'qin',  # 签名
        'user_id': user_id,  # 用户ID
        'role_id': role_id,  # 角色Id
    }
    access_token = jwt.encode(access_payload, key, algorithm=algorithm)
    return access_token


def decode_auth_token(token: str):
    """
    验证token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, key=key, algorithms=['HS256'])
    except Exception as e:
        print(e)
        return None
    else:
        return payload


def login_required(f):
    """
    登陆保护，验证用户是否登陆
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        res = ResMsg()

        token = request.headers.get("Authorization", default=None)
        if not token:
            res.update(code=-1, msg="请登录")
            return res.data
        payload = decode_auth_token(token)
        if not payload:
            res.update(code=-1, msg="请登录")
            return res.data

        g.user_id = payload.get("user_id")  # 用户ID，当前请求上下文使用
        g.role_id = payload.get("role_id")  # 角色ID，当前请求上下文使用
        return f(*args, **kwargs)

    return wrapper
