import base64
import copy
import json
import time
from flask import request
from api.main import main_bp
from api.models.brush_model import syslog

request_list = ['add','save','update','shBatch','delete','alipay','importExcel','compose','batch']

def printLog(request):
    request_url = request.url

    new_log =False
    for item in request_list:
        if item in request_url:
            new_log =True
            break
    if not new_log:
        return
    try:
        # 获取请求参数
        request_params = request.get_json()
        # 获取请求 IP 地址
        remote_ip = request.remote_addr
        auth_header = request.headers.get('token')
        auth_token = copy.deepcopy(auth_header)
        decode_str = base64.b64decode(auth_token).decode("utf8")
        decode_dict = eval(decode_str)
        username = ''
        if decode_dict.get("tablename")=='':
            username = decode_dict.get('params').get('yonghuzhanghao')
        elif decode_dict.get("tablename")=='users':
            username = decode_dict.get('params').get('username')
        dict = {
            'method': request.endpoint,
            'params': json.dumps(request_params),
            'username': username,
            'time': request.request_time,
            'ip': remote_ip,
            'operation': request.operation,
        }
        syslog.createbyreq(syslog, syslog, dict)
    except Exception as e:
        pass
    return

