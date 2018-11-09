# -*- coding: UTF-8 -*-
import json
import webqq_utils


# 登录状态
class LOGIN_STATUS:
    ONLINE = "online"
    OFFLINE = "offline"
    AWAY = "away"
    HIDDEN = "hidden"
    BUSY = "busy"
    CALLME = "callme"
    SILENT = "silent"
    num_to_string_dict = {
        10: "online",
        20: "offline",
        30: "away",
        40: "hidden",
        50: "busy",
        60: "callme",
        70: "silent",
    }


class WebQQProtocolGenerator:
    'webqq客户端的协议生成类'
    # 静态参数
    __client_id = 53999199
    __aid = 501004106
    __face = 603

    def __init__(self):
        self.__sequence = 0

    """webqq login urls"""
    def build_get_qr_img_url(self):
        return "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&" \
               "t=0.2904360772892842&daid=164&pt_3rd_aid=0"

    def build_check_qr_status_url(self, qrsig):
        # milli_timestamps
        milli_timestamps = webqq_utils.get_current_milli_time()
        ptqrtoken = webqq_utils.hash33(qrsig)
        return "https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https://web2.qq.com/proxy.html&ptqrtoken=" + (bytes)(
            ptqrtoken) + "&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-" + (bytes)(
            milli_timestamps) + "&js_ver=10284&js_type=1&login_sig=&pt_uistyle=40&aid=" + (bytes)(self.__aid)\
               + "&daid=164&mibao_css=m_webqq&"

    def build_report_url(self):
        return "https://report.url.cn/report/report?strValue=0&nValue=11202&tag=0&qver=0.0.1&t="\
               + (bytes)(webqq_utils.get_current_milli_time())

    def build_get_vfwebqq_url(self):
        return "https://s.web2.qq.com/api/getvfwebqq?ptwebqq=&clientid=" + (bytes)(self.__client_id)\
               + "&psessionid=&t=" + (bytes)(webqq_utils.get_current_milli_time())

    # 登录，但是这里不能更改登录状态，不管status是offline还是busy，登录后都是online状态
    def build_login2_post(self):
        url = "https://d1.web2.qq.com/channel/login2"
        post = {
            "ptwebqq": "",
            "clientid": self.__client_id,
            "psessionid": "",
            "status": "online",
        }
        post = "r=" + json.dumps(post)
        return url, post

    def build_change_status_url(self, newstatus, psessionid):
        url = "https://d1.web2.qq.com/channel/change_status2?newstatus=" + newstatus + "&clientid="\
              + (bytes)(self.__client_id) + "&psessionid=" + psessionid + "&t=" \
              + (bytes)(webqq_utils.get_current_milli_time())
        return url


    def build_get_qq_avatar_url(self, uid):
        """get qq avatar"""
        return "https://q.qlogo.cn/g?b=qq&nk=" + (bytes)(uid) + "&s=100&t=" + (bytes)(
            webqq_utils.get_current_milli_time())

    def build_get_user_friends2_post(self, vfwebqq, hash):
        url = "https://s.web2.qq.com/api/get_user_friends2"
        post = {
            "vfwebqq": vfwebqq,
            "hash": hash,
        }
        post = "r=" + json.dumps(post)
        return url, post

    def build_get_group_name_list_mask2_post(self, vfwebqq, hash):
        url = "https://s.web2.qq.com/api/get_group_name_list_mask2"
        post = {
            "vfwebqq": vfwebqq,
            "hash": hash,
        }
        post = "r=" + json.dumps(post)
        return url, post

    def build_get_discus_list_url(self, psessionid, vfwebqq):
        url = "https://s.web2.qq.com/api/get_discus_list?clientid=" + (bytes)(self.__client_id) + "&psessionid=" +\
              psessionid + "&vfwebqq=" + vfwebqq + "&t=" + (bytes)(webqq_utils.get_current_milli_time())
        return url

    def build_get_self_info2_url(self):
        url = "https://s.web2.qq.com/api/get_self_info2?t=" + (bytes)(webqq_utils.get_current_milli_time())
        return url

    def build_get_online_buddies2_url(self, psessionid, vfwebqq):
        url = "https://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq=" + vfwebqq + "&clientid="\
              + (bytes)(self.__client_id) + "&psessionid=" + psessionid + "&t="\
              + (bytes)(webqq_utils.get_current_milli_time())
        return url

    def build_get_single_long_nick2(self, tuin, vfwebqq):
        url = "https://s.web2.qq.com/api/get_single_long_nick2?tuin=" + (bytes)(tuin) + "&vfwebqq=" + vfwebqq + "&t=" \
              + (bytes)(webqq_utils.get_current_milli_time())
        return url

    def build_get_friend_info2_url(self, tuin, vfwebqq, psessionid):
        url = "https://s.web2.qq.com/api/get_friend_info2?tuin=" + (bytes)(tuin) + "&vfwebqq=" + vfwebqq \
              + "&clientid=" + (bytes)(self.__client_id) + "&psessionid=" + psessionid\
              + "&t=" + (bytes)(webqq_utils.get_current_milli_time())
        return url

    # qcode和gid一样
    def build_get_group_info_ext2_url(self, gcode, vfwebqq):
        url = "https://s.web2.qq.com/api/get_group_info_ext2?gcode=" + (bytes)(gcode) + "&vfwebqq=" + vfwebqq + "&t="\
              + (bytes)(webqq_utils.get_current_milli_time())
        return url

    def build_get_discu_info_url(self, did, vfwebqq, psessionid):
        url = "https://d1.web2.qq.com/channel/get_discu_info?did=" + (bytes)(did) + "&vfwebqq=" + vfwebqq\
              + "&clientid=" + (bytes)(self.__client_id) + "&psessionid=" + psessionid\
              + "&t=" + (bytes)(webqq_utils.get_current_milli_time())
        return url

    # 经过测试，字体的属性改变没有任何作用
    def __get_content(self, msg, font="宋体", font_size=10, font_style1=0, font_style2=0,
                              font_style3=0, font_color="000000"):
        content = [
            msg,
            [
                "font",
                {
                    "name": font,
                    "size": font_size,
                    "style": [font_style1, font_style2, font_style3],
                    "color": font_color,
                }
            ]
        ]
        return json.dumps(content)


    def build_send_buddy_msg2(self, tuin, psessionid, msg=""):
        url = "https://d1.web2.qq.com/channel/send_buddy_msg2"
        self.__sequence = self.__sequence + 1
        post = {
            "to":  tuin,
            "content": self.__get_content(msg),
            "face": self.__face,
            "clientid": self.__client_id,
            "msg_id": webqq_utils.get_msg_id(self.__sequence),
            "psessionid": psessionid,
        }
        post = "r=" + json.dumps(post)
        return url, post

    def build_send_qun_msg2(self, guin, psessionid, msg=""):
        url = "https://d1.web2.qq.com/channel/send_qun_msg2"
        self.__sequence = self.__sequence + 1
        post = {
            "group_uin": guin,
            "content": self.__get_content(msg),
            "face": self.__face,
            "clientid": self.__client_id,
            "msg_id": webqq_utils.get_msg_id(self.__sequence),
            "psessionid": psessionid,
        }
        post = "r=" + json.dumps(post)
        return url, post

    def build_send_discu_msg2(self, did, psessionid, msg=""):
        url = "https://d1.web2.qq.com/channel/send_discu_msg2"
        self.__sequence = self.__sequence + 1
        post = {
            "did": did,
            "content": self.__get_content(msg),
            "face": self.__face,
            "clientid": self.__client_id,
            "msg_id": webqq_utils.get_msg_id(self.__sequence),
            "psessionid": psessionid,
        }
        post = "r=" + json.dumps(post)
        return url, post

    # 给陌生人发信息,应该是接收到消息之后，能回消息
    def build_get_c2cmsg_sig2(self):
        pass

    # 获取消息
    def build_poll2(self, psessionid):
        url = "https://d1.web2.qq.com/channel/poll2"
        post = {
            "ptwebqq": "",
            "clientid": self.__client_id,
            "psessionid": psessionid,
            "key": "",
        }
        post = "r=" + json.dumps(post)
        return url, post
