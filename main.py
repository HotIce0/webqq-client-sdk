# -*- coding: UTF-8 -*-
import json
from time import sleep
import webqq_client_sdk.webqq_client as webqq_client
import webqq_client_sdk.webqq_protocol_gen as webqq_protocol


def main():
    # client instance
    client = webqq_client.WebQQClient()
    # Get QR
    qr_img_buf = client.get_qr_img()
    # Save QR Image to temp directory
    qr_img_path = client.save_qr_img_to_tempdir(qr_img_buf)
    # Show the QR Image via matplotlib.pyplot in window
    client.show_qr_img(qr_img_path)

    # Polling to check status of QR Image
    while True:
        sleep(1)
        poll_res = client.poll_qr_status()
        if poll_res == webqq_client.STATUS_QR_CHECK_INVALID:
            print ">二维码过期"
        elif poll_res == webqq_client.STATUS_QR_CHECKING:
            print ">认证中"
        elif poll_res == webqq_client.STATUS_QR_CHECK_VALID:
            print ">二维码未过期"
        elif poll_res == webqq_client.STATUS_QR_CHECK_SUCCESS:
            if client.login():
                print ">成功登录"
                break
            else:
                print ">登录失败"

    # Change my qq status
    if client.change_status(webqq_protocol.LOGIN_STATUS.HIDDEN):
        print ">隐身状态设置成功"
    else:
        print ">隐身状态设置失败"

    # Get user avatar
    client.get_avatar(51747708)
    # Get friends
    if client.get_user_friends_info():
        print ">成功获取好友基础数据"
    else:
        print ">获取好友基础数据失败"

    # Get online buddies
    if client.get_online_buddies():
        print ">成功获取好友在线状态数据"
    else:
        print ">获取好友在线状态失败"

    # Get Groups
    if client.get_groups_info():
        print ">成功获取QQ群基础数据"
    else:
        print ">获取QQ群基础数据失败"

    # Get Discussion
    if client.get_discussions_info():
        print ">成功获取多人聊天基础数据"
    else:
        print "v获取多人聊天基础数据失败"

    # Get self info
    if client.get_self_info():
        print ">成功获取自己的详细信息"
    else:
        print ">获取自己的详细信息失败"

    # 获取好友个性签名
    if client.get_single_long_nick_uin(1520166780):
        print ">成功获取好友个新签名信息", client.friends[1520166780].lnick
    else:
        print ">获取好友个性签名信息失败"
    # client.get_single_long_nick_friend(friend=friend对象)

    # 获取好友个人详细信息
    if client.get_frined_info_uin(1520166780):
        print ">获取好友详细信息成功", client.friends[1520166780].detailed_info
    else:
        print ">获取好友详细信息失败"

    # 获取QQ群详细信息
    if client.get_group_info_gid(2070283452):
        print ">获取QQ群详细信息成功", "群名称", client.groups[2070283452].name,\
            "群的所有者", client.groups[2070283452].owner
    else:
        print ">获取QQ群详细信息失败"

    # 获取多人聊天详细信息
    if client.get_discussion_info(3584583310):
        print ">获取多人聊天详细信息成功", "多人聊天名称", client.discussions[3584583310].name, \
            "多人聊天群的人数", len(client.discussions[3584583310].members)
    else:
        print ">获取多人聊天详细信息失败"

    # 给好友发送信息
    if client.send_friend_msg_uin(1520166780, "Hotice0:牛逼呀老哥"):
        print ">好友信息发送成功"
    else:
        print ">好友信息发送失败"

    # 给QQ群发送信息
    if client.send_qun_msg_guin(2070283452, "Hotice0:测试消息"):
        print ">QQ群信息发送成功"
    else:
        print ">QQ群信息发送失败"

    # 给多人聊天群发信息
    if client.send_discussion_msg_did(3584583310, "Hotice0:测试消息"):
        print ">多人聊天群信息发送成功"
    else:
        print ">多人聊天群信息发送失败"

    # 轮询接收消息
    while True:
        sleep(1)
        print ">正在轮询接收消息"
        res = client.poll_receive_msg()
        if res == "no_msg":
            print ">没有接收到消息"
        elif res is False:
            print ">接收消息发送错误"
        elif type(res) is tuple:
            print ">接收到消息", json.dumps(res)

    # 清空临时文件夹
    #client.clean_temp_file()


if __name__ == "__main__":
    main()
