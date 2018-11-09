# -*- coding: UTF-8 -*-
import execjs
import time
import os


# Get current milli timestamps
def get_current_milli_time():
    return int(round(time.time() * 1000))


# milli timestamps to formatted time
def milli_timestamps_to_time(milli_timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(milli_timestamp / 1000))


# create dir
def mkdir(path):
    try:
        os.mkdir(path)
    except OSError as err:
        # 17 File Existing
        if err.errno != 17:
            raise err


#time33和hash33一样的结果
encrypt_fun_hash33 = execjs.compile("""
function hash33(t) {
    for (var e = 0, i = 0, n = t.length; i < n; ++i)
        e += (e << 5) + t.charCodeAt(i);
    return 2147483647 & e
}
""")

encrypt_fun_time33 = execjs.compile("""
function time33(t) {
    for (var e = 0, i = 0, n = t.length; i < n; i++)
        e = (33 * e + t.charCodeAt(i)) % 4294967296;
    return e
}
""")

encrypt_fun_hash2 = execjs.compile("""
        function byte2hex(bytes){//bytes array
            var hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
            var buf = "";

            for (var i=0;i<bytes.length;i++){
                buf += (hex[(bytes[i]>>4) & 0xF]);
                buf += (hex[bytes[i] & 0xF]);
            }
            return buf;
        }
        
            function hash2(uin,ptvfwebqq){
            uin += "";
            var ptb = [];
            for (var i=0;i<ptvfwebqq.length;i++){
                var ptbIndex = i%4;
                ptb[ptbIndex] ^= ptvfwebqq.charCodeAt(i);
            }
            var salt = ["EC", "OK"];
            var uinByte = [];
            uinByte[0] = (((uin >> 24) & 0xFF) ^ salt[0].charCodeAt(0));
            uinByte[1] = (((uin >> 16) & 0xFF) ^ salt[0].charCodeAt(1));
            uinByte[2] = (((uin >> 8) & 0xFF) ^ salt[1].charCodeAt(0));
            uinByte[3] = ((uin & 0xFF) ^ salt[1].charCodeAt(1));
            var result = [];
            for (var i=0;i<8;i++){
                if (i%2 == 0)
                    result[i] = ptb[i>>1];
                else
                    result[i] = uinByte[i>>1];
            }
            return byte2hex(result);

        };
""")

encrypt_fun_get_pgv = execjs.compile("""
function get_pgv(c) {
    return (c || "") + Math.round(2147483647 * (Math.random() || .5)) * +new Date % 1E10
}
""")

fun_get_msg_id = execjs.compile("""
var t = (new Date()).getTime();
t = (t - t % 1000) / 1000;
t = t % 10000 * 10000;
function getMsgId(sequence) {
    return t + sequence
}
""")


# used to calc ptqrtoken (use qrsig)
def hash33(t):
    res = encrypt_fun_hash33.call("hash33", t)
    return res


def time33(t):
    res = encrypt_fun_time33.call("time33", t)
    return res


# 用于计算hash，请求好友列表时使用。hash2(uid, "") ptvfwebqq无用
def hash2(uid, ptvfwebqq):
    return encrypt_fun_hash2.call("hash2", uid, ptvfwebqq)


# 用于pgv_pvi = get_pgv(""), pgv_si = get_pgv("s") 暂时没用
def get_pgv(str):
    res = encrypt_fun_get_pgv.call("get_pgv", str)


def get_msg_id(sequence):
    res = fun_get_msg_id.call("getMsgId", sequence)
    return res


# status, msg
# 65 二维码失效
# 66 二维码未失效
# 67 二维码认证中
# 对应qq登录协议中的ptuiCB()函数
def ptuiCB(call_str):
    fun_def = """
    function ptuiCB(status, b, url, d, msg, nickname) {
        return {'status' : status, 'url' : url, 'msg' : msg, 'nickname' : nickname}
    }
    return """
    # {'status': '66', 'url': '', 'msg': '二维码未失效。(187707424)'}
    return execjs.compile(fun_def + call_str).call("")


#print ptuiCB("ptuiCB('66','0','','0', '二维码未失效。(187707424)', '')")
#print hash33("sao"), time33("sao")
