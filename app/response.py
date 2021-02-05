import time

from flask_restful import abort


def custom_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        # 重定义400返回参数
        res = ResMsg()
        res.update(code=-1, data=kwargs.get('message'), msg="参数错误！")
        abort(400, **res.data)

    abort(http_status_code)


class ResMsg(object):
    """
    封装响应文本
    """

    def __init__(self, data=None, code=200, msg="ok"):

        self._data = data
        self._msg = msg
        self._code = code
        self._time = time.time()

    def update(self, code=None, data=None, msg=None):
        """
        更新默认响应文本
        :param code:响应编码
        :param data: 响应数据
        :param msg: 响应消息
        :return:
        """
        if code is not None:
            self._code = code
        if data is not None:
            self._data = data
        if msg is not None:
            self._msg = msg

    def add_field(self, name=None, value=None):
        """
        在响应文本中加入新的字段，方便使用
        :param name: 变量名
        :param value: 变量值
        :return:
        """
        if name is not None and value is not None:
            self.__dict__[name] = value

    @property
    def data(self):
        """
        输出响应文本内容
        :return:
        """
        body = self.__dict__
        body["data"] = body.pop("_data")
        body["message"] = body.pop("_msg")
        body["code"] = body.pop("_code")
        body["timeout"] = '%.3f' % (time.time() - body.pop("_time"))
        return body
