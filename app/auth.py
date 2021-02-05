import jwt
from datetime import datetime, timedelta
from flask import current_app, request, session
from functools import wraps

from app.response import ResMsg


class Auth(object):
    key = 'super-man$&123das%qzq'

    @classmethod
    def generate_access_token(cls, user_id, algorithm: str = 'HS256', exp: float = 2):
        """
        生成access_token
        :param user_id:自定义部分
        :param algorithm:加密算法
        :param exp:过期时间
        :return:
        """

        now = datetime.utcnow()
        exp_datetime = now + timedelta(hours=exp)
        access_payload = {
            'exp': exp_datetime,
            'flag': 0,  # 标识是否为一次性token，0是，1不是
            'iat': now,  # 开始时间
            'iss': 'qin',  # 签名
            'user_id': user_id  # 自定义部分
        }
        access_token = jwt.encode(access_payload, cls.key, algorithm=algorithm)
        return access_token

    @classmethod
    def decode_auth_token(cls, token: str):
        """
        验证token
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(token, key=cls.key, )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
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
        token = request.headers.get("toke", default=None)
        if not token:
            res.update(code=-1, msg="请登录")
            return res.data
        return f(*args, **kwargs)

    return wrapper
