## WebQQ Client SDK by Hotice0

## Description
1. The complete webQQ client sdk, Base on WebQQ 2.0(https://web2.qq.com/) protocol, coding with python2.
2. You can build a QQ chat robot with this sdk, And more creative functions.

## Project Structure
- main.py : Demo of using sdk.
- webqq_client_sdk
    - requirements.txt : `Requirements output with cmd : pip2.7 freeze > webqq_client_sdk/requirements.txt`
    - webqq_client.py : `qqweb client, instance of sdk.`
    - webqq_data_parse.py : `Parse the data to Data Models, that recevied from server.`
    - webqq_protocol_gen.py : `To build request url and param, I'll call this Protocol Generator.`
    - webqq_utils.py :  `Utils : encrypt javascript code...`
    - models(directory)
        - Friend.py     : `Friend Data Models`
        - Group.py      : `Group Data Models`
        - Discussion.py : `Discussion Data Models`
        - Categories.py : `Friend Categories Data Models`
        - Rencent.py    : `Rencent Contacts Data Models`
        
## Usage
1. install requirements. run `pip install -r webqq_client_sdk/requirements.txt`
2. run the main.py (Demo)

## Version Log
2018.11.9 version 0.01 basic function

## Notice
1. Can't set stats when loging.But you can change the stats after logined with call WebQQClient.change_status()

## Lisencse

MIT License

Copyright (c) 2018 HotIce0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
