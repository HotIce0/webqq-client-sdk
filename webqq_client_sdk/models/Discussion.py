# -*- coding: UTF-8 -*-
class Discussion:
    def __init__(self):
        self.name = None
        self.did = None
        self.members = None

class DiscussionMember:
    def __init__(self):
        self.nick = None
        self.uin = None
        # 在线状态status
        self.status = {
            "client_type": None,
            "stat": None,
        }
