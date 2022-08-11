from utils.handler_conf.conf_control import conf


def db_status():
    """
    获取数据库开关状态
    """
    status = conf.getboolean('mysql', 'status')
    return status
