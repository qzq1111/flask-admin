import hashlib


def get_md5(string):
    """获取md5码"""
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()
