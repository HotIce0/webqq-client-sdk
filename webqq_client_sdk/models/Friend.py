# -*- coding: UTF-8 -*-
class Friend:
    def __init__(self):
        # 自己的uin就是qq号
        self.uin = None
        # flag is categories(categories is the index of the categories arrays)
        self.friends_categories = None
        self.friends_flag = None
        self.info_face = None
        self.info_flag = None
        # QQ昵称
        self.info_nick = None
        # 个性签名
        self.lnick = None
        # 好友的备注名称
        self.marknames_markname = None
        # 意义未知(所有的值都是0)
        self.marknames_type = None
        # 详细信息
        self.detailed_info = {
            # 被添加好友的验证方式
            "allow": None,
            "birthday": {
                "year": None,
                "month": None,
                "day": None,
            },
            "blood": None,
            # 所在地
            "position": {
                "country": None,
                "province": None,
                "city": None,
            },
            "college": None,
            "constel": None,
            "email": None,
            "gender": None,
            "homepage": None,
            "mobile": None,
            "occupation": None,
            "personal": None,
            "phone": None,
            "shengxiao": None,
            # 只有当这个对象存储的是自己的信息时有效
            "vfwebqq": None,
        }

        # vip 信息
        self.vip_info = {
            "level": None,
            "is_vip": None,
        }
        # 在线状态
        self.status = {
            "client_type": None,
            "status": None,
        }