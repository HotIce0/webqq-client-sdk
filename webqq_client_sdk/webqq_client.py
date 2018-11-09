# -*- coding: UTF-8 -*-
import json
import webqq_utils
from webqq_protocol_gen import WebQQProtocolGenerator
from webqq_data_parse import WebQQDataParse
import cv2
import matplotlib.pyplot as plt
import urllib2
import cookielib
import os
import tempfile
import threading

# 65 二维码失效(应该，重新获取登录二维码)

STATUS_QR_CHECK_INVALID = "65"
# 66 二维码未失效(应该，等待扫描二维码)
STATUS_QR_CHECK_VALID = "66"
# 67 二维码认证中(应该等待，但是，可能出现，扫了码，没同意而，一直卡在这,应该提供重新获取二维码操作)
STATUS_QR_CHECKING = "67"
# 0  二维码已经登录成功
STATUS_QR_CHECK_SUCCESS = "0"


class WebQQClient:
    """实现与webqq客户端"""
    def __init__(self):
        self.__webqq_client_protocol_generator = WebQQProtocolGenerator()
        self.__webqq_data_parser = WebQQDataParse()
        # cookieJar
        self.__cj = cookielib.MozillaCookieJar()
        # Https request
        self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cj))

        # poll res
        self.__poll_res = None

        # nick name 昵称
        self.__nick_name = None
        # 通过getvfwebqq获取
        self.__vfwebqq = None
        # 通过login2获取的数据
        self.__login2_index = None
        self.__login2_psessionid = None
        self.__login2_user_state = None
        self.__login2_f = None
        self.__login2_uin = None
        self.__login2_cip = None
        self.__login2_vfwebqq = None
        self.__login2_port = None

        # 当前的在线状态
        self.__status = None

        # hash
        self.__hash = None

        # Friends
        self.friends = []
        self.groups = []
        self.discussions = []
        self.categories = []
        self.selfinfo = None

        # tempfile path
        self.temp_path = path = os.getcwd() + "/temp"

    def get_cookie(self, name):
        for cookie in self.__cj:
            if cookie.name == name:
                return cookie.value
        return False

    def show_cookie(self):
        for cookie in self.__cj:
            print cookie.name, cookie.value, cookie.domain

    def get_qr_img(self):
        """get qr img and set cookie : qrsig"""
        rsp = self.__opener.open(self.__webqq_client_protocol_generator.build_get_qr_img_url())
        # print rsp.__dict__
        if rsp.code == 200:
            return rsp.read()
        else:
            return False

    def save_qr_img_to_tempdir(self, imgData):
        """save the qr img to temp directory"""
        webqq_utils.mkdir(self.temp_path)
        foo, tf_path = tempfile.mkstemp(suffix=".png", prefix="qr_img_", dir=self.temp_path)

        # write img date into tempfile
        fd = os.open(tf_path, os.O_RDWR)
        os.write(fd, imgData)
        os.close(fd)

        return tf_path

    def __show_qr_img_window(self, tf_path):
        # 改用matplotlib.pyplot
        src = cv2.imread(tf_path)
        plt.imshow(src)
        plt.title("Please scan QR with the latest version QQ")
        plt.axis("off")
        plt.show()
        # 由于cv2为阻塞方式显示图片，mac os下，子线程创建imshow，窗口，会出异常。似乎是只有主线程可以渲染窗口，可能和opencv的，Qt实现有关。
        # src = cv2.imread(tf_path)
        # cv2.imshow('Please scan QR with the latest version QQ', src)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def show_qr_img(self, tf_path):
        show_qr_thread = threading.Thread(target=self.__show_qr_img_window, name="show_qr", args=(tf_path,))
        show_qr_thread.start()

    def poll_qr_status(self):
        """poll check the qr status"""
        qrsig = self.get_cookie("qrsig")
        rsp = self.__opener.open(self.__webqq_client_protocol_generator.build_check_qr_status_url(qrsig))
        if rsp.code == 200:
            self.__poll_res = webqq_utils.ptuiCB(rsp.read())
            # login successful, save the nickname
            if self.__poll_res["status"] == STATUS_QR_CHECK_SUCCESS:
                self.__nick_name = self.__poll_res["nickname"]
            return self.__poll_res["status"]

    # login include (__check_sig, __get_vfwebqq, __login2)
    def login(self):
        if not self.__check_sig():
            return False
        if not self.__get_vfwebqq():
            return False
        if not self.__login2():
            return False
        return True

    def __check_sig(self):
        if self.__poll_res is None:
            return False
        if not self.__poll_res["status"] == STATUS_QR_CHECK_SUCCESS:
            return False
        rsp = self.__opener.open(self.__poll_res["url"])
        if rsp.code == 200:
            return True
        return False

    def __get_vfwebqq(self):
        url = self.__webqq_client_protocol_generator.build_get_vfwebqq_url()
        request = urllib2.Request(url)
        # 获取vfwebqq必须加上referer，可能是获取的内容会根据referer不同而不同,也就是proxy代理版本不同
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(s=rsp.read())
            if data["retcode"] == 0:
                self.__vfwebqq = data["result"]["vfwebqq"]
                return True
        return False

    def __login2(self):
        url, post_data = self.__webqq_client_protocol_generator.build_login2_post()
        rsp = self.__opener.open(url, post_data)
        if rsp.code == 200:
            data = json.loads(s=rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__status = result["status"]
                self.__login2_index = result["index"]
                self.__login2_psessionid = result["psessionid"]
                self.__login2_user_state = result["user_state"]
                self.__login2_f = result["f"]
                self.__login2_uin = result["uin"]
                self.__login2_cip = result["cip"]
                self.__login2_vfwebqq = result["vfwebqq"]
                self.__login2_port = result["port"]
                # calculate the hash (used to get friends info ...)
                self.__hash = webqq_utils.hash2(uid=self.__login2_uin, ptvfwebqq="")
                return True
        return False

    # change the qq status
    def change_status(self, newstatus):
        url = self.__webqq_client_protocol_generator.build_change_status_url(newstatus, self.__login2_psessionid)
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                return True

        return False

    # 获取自己的QQ头像,可以使用qq号码获取任何人的qq头像
    def get_avatar(self, uid):
        avatar_path = self.temp_path + "/avatar.jpeg"
        rsp = self.__opener.open(self.__webqq_client_protocol_generator.build_get_qq_avatar_url(uid))
        avatar_buf = rsp.read()
        fd = os.open(avatar_path, os.O_RDWR | os.O_CREAT)
        os.write(fd, avatar_buf)
        os.close(fd)
        return avatar_path

    # get your friends info (not detail info)
    # 在获取单个好友的信息时，必须先调用该函数
    def get_user_friends_info(self):
        url, post_data = self.__webqq_client_protocol_generator.build_get_user_friends2_post(self.__vfwebqq,
                                                                                             self.__hash)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request, post_data)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.friends, self.categories = self.__webqq_data_parser.parse_get_user_friends2(result)
                return True
        return False

    # get qq group info (not detail info)
    def get_groups_info(self):
        url, post_data = self.__webqq_client_protocol_generator.build_get_group_name_list_mask2_post(self.__vfwebqq,
                                                                                                     self.__hash)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request, post_data)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.groups = self.__webqq_data_parser.parse_get_group_name_list_mask2(result)
                return True
        return False

    # get discussion
    def get_discussions_info(self):
        url = self.__webqq_client_protocol_generator.build_get_discus_list_url(self.__login2_psessionid,
                                                                               self.__vfwebqq)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.discussions = self.__webqq_data_parser.parse_get_discus_list(result)
                return True
        return False

    # get self info
    def get_self_info(self):
        url = self.__webqq_client_protocol_generator.build_get_self_info2_url()
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.selfinfo = self.__webqq_data_parser.parse_get_self_info2(result)
                return True
        return False

    # get online friends
    def get_online_buddies(self):
        url = self.__webqq_client_protocol_generator.build_get_online_buddies2_url(self.__login2_psessionid,
                                                                                   self.__vfwebqq)
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__webqq_data_parser.parse_get_online_buddies2(result, self.friends)
                return True
        return False

    # get single long nick 获取好友个性签名 use friend
    def get_single_long_nick_friend(self, friend):
        url = self.__webqq_client_protocol_generator.build_get_single_long_nick2(friend.uin, self.__vfwebqq)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__webqq_data_parser.parse_get_single_long_nick2(result, self.friends)
                return True
        return False

    # get single long nick 获取好友个性签名 use uin
    def get_single_long_nick_uin(self, uin):
        url = self.__webqq_client_protocol_generator.build_get_single_long_nick2(uin, self.__vfwebqq)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__webqq_data_parser.parse_get_single_long_nick2(result, self.friends)
                return True
        return False

    def get_frined_info_uin(self, uin):
        url = self.__webqq_client_protocol_generator.build_get_friend_info2_url(uin, self.__vfwebqq,
                                                                                self.__login2_psessionid)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__webqq_data_parser.parse_get_friend_info2(result, self.friends)
                return True
        return False

    def get_group_info_gid(self, gid):
        url = self.__webqq_client_protocol_generator.build_get_group_info_ext2_url(gid, self.__vfwebqq)
        request = urllib2.Request(url)
        request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__webqq_data_parser.parse_get_group_info_ext2(result, self.groups)
                return True
        return False

    def get_discussion_info(self, did):
        url = self.__webqq_client_protocol_generator.build_get_discu_info_url(did, self.__vfwebqq, self.__login2_psessionid)
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")
        rsp = self.__opener.open(request)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                result = data["result"]
                self.__webqq_data_parser.parse_get_discu_info(result, self.discussions)
                return True
        return False


    # 获取好友的真实qq号码，安全问题，已经被取消，返回404
    # def get_real_uin(self):
    #     url, post_data = self.__webqq_client_protocol_generator.build_get_user_friends2_post(self.__vfwebqq,
    #                                                                                          self.__hash)
    #     url = "https://s.web2.qq.com/api/get_friend_uin2"
    #     request = urllib2.Request(url)
    #     request.add_header("referer", "https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
    #     rsp = self.__opener.open(request, post_data)
    #     print rsp.read()

    # send message to friend
    def send_friend_msg_uin(self, uin, msg):
        url, post_data = self.__webqq_client_protocol_generator.build_send_buddy_msg2(
            tuin=uin,
            psessionid=self.__login2_psessionid,
            msg=msg
        )
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1")
        rsp = self.__opener.open(request, post_data)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                return True
        return False

    # send qq qun message
    def send_qun_msg_guin(self, guin, msg):
        url, post_data = self.__webqq_client_protocol_generator.build_send_qun_msg2(
            guin=guin,
            psessionid=self.__login2_psessionid,
            msg=msg
        )
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1")
        rsp = self.__opener.open(request, post_data)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                return True
        return False

    def send_discussion_msg_did(self, did, msg):
        url, post_data = self.__webqq_client_protocol_generator.build_send_discu_msg2(
            did=did,
            psessionid=self.__login2_psessionid,
            msg=msg
        )
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1")
        rsp = self.__opener.open(request, post_data)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0:
                return True
        return False

    def poll_receive_msg(self):
        url, post_data = self.__webqq_client_protocol_generator.build_poll2(self.__login2_psessionid)
        request = urllib2.Request(url)
        request.add_header("referer", "https://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")
        rsp = self.__opener.open(request, post_data)
        if rsp.code == 200:
            data = json.loads(rsp.read())
            if data["retcode"] == 0 and data["retmsg"] == "ok":
                if data.has_key("errmsg"):
                    return "no_msg"
                else:
                    result = data["result"]
                    return self.__webqq_data_parser.parse_poll2(result)
        return False

    def __del_file(self, path):
        for i in os.listdir(path):
            path_file = os.path.join(path, i)
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                self.__del_file(path_file)

    def clean_temp_files(self, path = None):
        if path is None:
            path = self.temp_path
        self.__del_file(path)
