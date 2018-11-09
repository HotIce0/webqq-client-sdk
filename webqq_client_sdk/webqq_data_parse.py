# -*- coding: UTF-8 -*-
from models.Categories import Categories
from models.Friend import Friend
from models.Group import Group
from models.Group import GMemberInfo
from models.Discussion import Discussion
from models.Discussion import DiscussionMember
import webqq_protocol_gen


class WebQQDataParse:
    def parse_get_user_friends2(self, result):
        friends = result["friends"]
        categories = result["categories"]
        info = result["info"]
        marknames = result["marknames"]
        vipinfo = result["vipinfo"]

        ret_friends = {}
        ret_categories = []

        # parse categories info
        for categorie in categories:
            categorie_obj = Categories()
            categorie_obj.index = categorie["index"]
            categorie_obj.name = categorie["name"]
            categorie_obj.sort = categorie["sort"]
            ret_categories.append(categorie_obj)

        # parse friends
        for i in range(0, len(friends)):
            friend_obj = Friend()
            friend_obj.friends_flag = friends[i]["flag"]
            friend_obj.friends_categories = friends[i]["categories"]

            ret_friends[friends[i]["uin"]] = friend_obj

        # parse info
        for i in range(0, len(info)):
            friend_obj = ret_friends[info[i]["uin"]]
            friend_obj.info_face = info[i]["face"]
            friend_obj.info_flag = info[i]["flag"]
            friend_obj.info_nick = info[i]["nick"]

        # parse marknames
        for i in range(0, len(marknames)):
            friend_obj = ret_friends[marknames[i]["uin"]]
            friend_obj.marknames_markname = marknames[i]["markname"]
            friend_obj.marknames_type = marknames[i]["type"]

        # parse vipinfo
        for i in range(0, len(vipinfo)):
            friend_obj = ret_friends[vipinfo[i]["u"]]
            friend_obj.vip_info["level"] = vipinfo[i]["vip_level"]
            friend_obj.vip_info["is_vip"] = vipinfo[i]["is_vip"]

        return ret_friends, ret_categories

    def parse_get_group_name_list_mask2(self, result):
        gmarklist = result["gmarklist"]
        gmasklist = result["gmasklist"]
        gnamelist = result["gnamelist"]

        ret_groups = {}

        # parse gmarklist 似乎没有没使用
        # parse gmasklist [群屏蔽] 暂时没写，我的qq获取没数据
        # parse gnamelist
        for i in range(0, len(gnamelist)):
            group_obj = Group()
            group_obj.flag = gnamelist[i]["flag"]
            group_obj.name = gnamelist[i]["name"]
            group_obj.gid = gnamelist[i]["gid"]
            group_obj.code = gnamelist[i]["code"]

            ret_groups[group_obj.gid] = group_obj

        return ret_groups

    def parse_get_discus_list(self, result):
        dnamelist = result["dnamelist"]

        ret_discussion = {}

        # parse dnamelist
        for i in range(0, len(dnamelist)):
            discussion_obj = Discussion()
            discussion_obj.dnamelist_did = dnamelist[i]["did"]
            discussion_obj.dnamelist_name = dnamelist[i]["name"]

            ret_discussion[discussion_obj.dnamelist_did] = discussion_obj

        return ret_discussion

    def parse_get_self_info2(self, result):
        ret_selfinfo = Friend()
        # result["account"] 就是qq号与uin取值相同,所以不保存account
        ret_selfinfo.uin = result["uin"]
        ret_selfinfo.detailed_info["allow"] = result["allow"]
        ret_selfinfo.detailed_info["birthday"] = result["birthday"]
        ret_selfinfo.detailed_info["blood"] = result["blood"]
        ret_selfinfo.detailed_info["position"]["country"] = result["country"]
        ret_selfinfo.detailed_info["position"]["city"] = result["city"]
        ret_selfinfo.detailed_info["position"]["province"] = result["province"]
        ret_selfinfo.detailed_info["college"] = result["college"]
        ret_selfinfo.detailed_info["constel"] = result["constel"]
        ret_selfinfo.detailed_info["email"] = result["email"]
        ret_selfinfo.info_face = result["face"]
        ret_selfinfo.detailed_info["gender"] = result["gender"]
        ret_selfinfo.detailed_info["homepage"]= result["homepage"]
        ret_selfinfo.detailed_info["shengxiao"] = result["shengxiao"]
        ret_selfinfo.detailed_info["vfwebqq"] = result["vfwebqq"]
        ret_selfinfo.vip_info["level"] = result["vip_info"]
        if result["vip_info"] > 0:
            ret_selfinfo.vip_info["is_vip"] = 1
        else:
            ret_selfinfo.vip_info["is_vip"] = 0
        return ret_selfinfo

    def parse_get_online_buddies2(self, result, friends):
        # set all offline
        for index in friends:
            friends[index].status["status"] = webqq_protocol_gen.LOGIN_STATUS.OFFLINE
        # parse online buddies
        for i in range(0, len(result)):
            # 这里判断是否存在key是因为，查询好友在线状态，里面出现的uid，有好友列表里面不存在的uid
            # 出现这种情况的原因是，自己加了自己好友
            if friends.has_key(result[i]["uin"]):
                friends[result[i]["uin"]].status["client_type"] = result[i]["client_type"]
                friends[result[i]["uin"]].status["status"] = result[i]["status"]

    def parse_get_single_long_nick2(self, result, friends):
        for i in range(0, len(result)):
            friends[result[i]["uin"]].lnick = result[i]["lnick"]

    def parse_get_friend_info2(self, result, friends):
        friend = friends[result["uin"]]
        friend.detailed_info["allow"] = result["allow"]
        friend.detailed_info["birthday"] = result["birthday"]
        friend.detailed_info["blood"] = result["blood"]
        friend.detailed_info["position"]["country"] = result["country"]
        friend.detailed_info["position"]["city"] = result["city"]
        friend.detailed_info["position"]["province"] = result["province"]
        friend.detailed_info["college"] = result["college"]
        friend.detailed_info["constel"] = result["constel"]
        friend.detailed_info["email"] = result["email"]
        friend.info_face = result["face"]
        friend.detailed_info["gender"] = result["gender"]
        friend.detailed_info["homepage"] = result["homepage"]
        friend.detailed_info["mobile"] = result["mobile"]
        friend.detailed_info["occupation"] = result["occupation"]
        friend.detailed_info["personal"] = result["personal"]
        friend.detailed_info["phone"] = result["phone"]
        friend.detailed_info["shengxiao"] = result["shengxiao"]
        friend.info_nick = result["nick"]
        # vipinfo
        if result["vip_info"] > 0:
            friend.vip_info["is_vip"] = 1
        else:
            friend.vip_info["is_vip"] = 0
        # stat
        friend.status["status"] = webqq_protocol_gen.LOGIN_STATUS.num_to_string_dict[result["stat"]]

    def parse_get_group_info_ext2(self, result, groups):
        cards = result["cards"]
        ginfo = result["ginfo"]
        minfo = result["minfo"]
        stats = result["stats"]
        vipinfo = result["vipinfo"]
        members = ginfo["members"]

        # parse ginfo
        group = groups[ginfo["gid"]]
        group.gclass = ginfo["class"]
        group.code = ginfo["code"]
        group.createtime = ginfo["createtime"]
        group.face = ginfo["face"]
        group.fingermemo = ginfo["fingermemo"]
        group.flag = ginfo["flag"]
        group.gid = ginfo["gid"]
        group.level = ginfo["level"]
        group.memo = ginfo["memo"]
        group.name = ginfo["name"]
        group.option = ginfo["option"]
        group.owner = ginfo["owner"]

        # parse ginfo["members"]
        for i in range(0, len(members)):
            if group.gmembers_info is None:
                group.gmembers_info = {}
            gmmember = GMemberInfo()
            gmmember.uin = members[i]["muin"]
            gmmember.mflag = members[i]["mflag"]
            group.gmembers_info[gmmember.uin] = gmmember

        # parse cards
        for i in range(0, len(cards)):
            gmmember = group.gmembers_info[cards[i]["muin"]]
            gmmember.card = cards[i]["card"]

        # parse minfo
        for i in range(0, len(minfo)):
            gmmember = group.gmembers_info[minfo[i]["uin"]]
            gmmember.nick = minfo[i]["nick"]
            gmmember.gender = minfo[i]["gender"]
            gmmember.position["country"] = minfo[i]["country"]
            gmmember.position["province"] = minfo[i]["province"]
            gmmember.position["city"] = minfo[i]["city"]

        # parse vipinfo
        for i in range(0, len(vipinfo)):
            gmmember = group.gmembers_info[vipinfo[i]["u"]]
            gmmember.vip_info["is_vip"] = vipinfo[i]["is_vip"]
            gmmember.vip_info["level"] = vipinfo[i]["vip_level"]

        # parse stats
        for i in range(0, len(stats)):
            gmmember = group.gmembers_info[stats[i]["uin"]]
            gmmember.status["stat"] = stats[i]["stat"]
            gmmember.status["client_type"] = stats[i]["client_type"]

    def parse_get_discu_info(self, result, discussions):
        info = result["info"]
        mem_info = result["mem_info"]
        mem_status = result["mem_status"]

        discussion = discussions[info["did"]]

        # parse info
        discussion.name = info["discu_name"]
        discussion.did = info["did"]

        if discussion.members is None:
            discussion.members = {}
        # parse mem_info
        for i in range(0, len(mem_info)):
            member = DiscussionMember()
            member.nick = mem_info[i]["nick"]
            member.uin = mem_info[i]["uin"]
            discussion.members[member.uin] = member

        # parse mem_status
        for i in range(0, len(mem_status)):
            member = discussion.members[mem_status[i]["uin"]]
            member.status["stat"] = mem_status[i]["status"]
            member.status["client_type"] = mem_status[i]["client_type"]

    def parse_poll2(self, result):
        friend_msg = []
        group_msg = []
        discussion_msg = []
        print result
        for i in range(0, len(result)):
            if result[i]["poll_type"] == "message":
                value = result[i]["value"]
                # 当接收到图片时，value["content"][1]不存在
                if len(value["content"]) == 1:
                    # 补充一个空消息
                    value["content"].append("")
                friend_msg.append({
                    "from_uin": value["from_uin"],
                    "msg_id": value["msg_id"],
                    "msg_type": value["msg_type"], # 1
                    "time": value["time"],
                    "to_uin": value["to_uin"],
                    "msg": value["content"][1],
                    "font": value["content"][0],
                })
            elif result[i]["poll_type"] == "group_message":
                value = result[i]["value"]
                # 当接收到图片时，value["content"][1]不存在
                if len(value["content"]) == 1:
                    # 补充一个空消息
                    value["content"].append("")
                group_msg.append({
                    "from_uin": value["from_uin"], # 与group_code相同guin相同
                    "group_code": value["group_code"],
                    "msg_id": value["msg_id"],
                    "msg_type": value["msg_type"], # 4
                    "send_uin": value["send_uin"],
                    "time": value["time"],
                    "to_uin": value["to_uin"],
                    "msg": value["content"][1],
                    "font": value["content"][0],
                })
            elif result[i]["poll_type"] == "discu_message":
                value = result[i]["value"]
                # 当接收到图片时，value["content"][1]不存在
                if len(value["content"]) == 1:
                    # 补充一个空消息
                    value["content"].append("")
                discussion_msg.append({
                    "did": value["did"],
                    "from_uin": value["from_uin"],# 与did相同
                    "msg_id": value["msg_id"],
                    "msg_type": value["msg_type"], # 5
                    "send_uin": value["send_uin"],
                    "time": value["time"],
                    "to_uin": value["to_uin"],
                    "msg": value["content"][1],
                    "font": value["content"][0],
                })
        return friend_msg, group_msg, discussion_msg
