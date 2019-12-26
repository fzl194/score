#对象未找到
class ModelNotFoundError(Exception):
    def __init__(self,err='ModelNotFoundError'):
        Exception.__init__(self,err)

#请求拒绝
class PermissionDeniedError(Exception):
    def __init__(self,err='PermissionDeniedError'):
        Exception.__init__(self,err)

#主键重复
class PrimaryKeyError(Exception):
    def __init__(self,err='PrimaryKeyError'):
        Exception.__init__(self,err)
