import datetime
import decimal
import uuid

import flask_restful
from flask import Flask
from flask.json import JSONEncoder as BaseJSONEncoder

from app.models import db
from app.api import api_user_bp, api_role_bp
from app.response import custom_abort


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_AS_ASCII'] = False
    app.config["RESTFUL_JSON"] = {"cls": JSONEncoder, "ensure_ascii": False}

    app.json_encoder = JSONEncoder
    flask_restful.abort = custom_abort
    db.init_app(app)
    
    app.register_blueprint(api_user_bp)
    app.register_blueprint(api_role_bp)

    return app


class JSONEncoder(BaseJSONEncoder):

    def default(self, o):
        """
        如有其他的需求可直接在下面添加
        :param o:
        :return:
        """
        if isinstance(o, datetime.datetime):
            # 格式化时间
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            # 格式化日期
            return o.strftime('%Y-%m-%d')
        if isinstance(o, decimal.Decimal):
            # 格式化高精度数字
            return float(o)
        if isinstance(o, uuid.UUID):
            # 格式化uuid
            return str(o)
        if isinstance(o, bytes):
            # 格式化字节数据
            return o.decode("utf-8")
        return super(JSONEncoder, self).default(o)
