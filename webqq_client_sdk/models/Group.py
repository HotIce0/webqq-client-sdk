# -*- coding: UTF-8 -*-


class Group:
    def __init__(self):
        # group id
        self.gid = None
        flag = None
        # qq群名称
        self.name = None
        # 群号，可能与uin重复
        self.code = None
        # 群屏蔽
        self.mask = None
        #
        self.gclass = None
        # 创建时间的时间戳
        self.createtime = None
        #
        self.face = None
        self.fingermemo = None
        self.level = None
        # Notice群说明
        self.memo = None
        # 似乎没什么用(协议中没有使用)
        self.option = None
        self.owner = None

        # member info class GMemberInfo
        self.gmembers_info = None


class GMemberInfo:
    def __init__(self):
        # uin
        self.uin = None
        # mflag
        self.mflag = None
        # 在群里面的muin和uin是一样的
        self.muin = None
        # 群名片，群里面的名称
        self.card = None
        # 昵称
        self.nickname = None
        # 所在地
        self.position = {
            "country": None,
            "province": None,
            "city": None,
        }
        # 性别
        self.gender = None
        # 在线状态status
        self.status = {
            "client_type": None,
            "stat": None,
        }
        # vip 信息
        self.vip_info = {
            "level": None,
            "is_vip": None,
        }