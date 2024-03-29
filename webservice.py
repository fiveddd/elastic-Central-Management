#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2019/6/26 4:31 PM
# @Author  : lij021
# @File    : webservice.py
import importlib

from flask import Flask, render_template, request, jsonify
from flask import make_response
from flask_cors import CORS

import ansible_cli_wrapper
from ansible_cli_wrapper import *
import cgi
import os

app = Flask(__name__, static_folder="frontend/dist", static_url_path='', template_folder="./frontend/dist")
app.debug = True
TEMP_PATH = './tmp/'


@app.route('/api/list_invetory', methods=['GET'])
def list_invetory():
    try:
        result = os.listdir(INVENTORY_PATH)
        print(result)

        return jsonify(result)
    except Exception as e:
        return make_response(e)


@app.route('/api/get_invetory', methods=['GET'])
def get_invetory():
    importlib.reload(ansible_cli_wrapper)
    qs = str(request.query_string, encoding='utf-8')

    try:
        qp = cgi.urllib.parse.parse_qs(qs)
        filename = qp['name'][0]
        type = qp['type'][0]
        result = pb_get_inventory(host_file=filename, type=type)
        return jsonify(result)
    except Exception as e:
        return jsonify(pb_get_inventory())


@app.route('/api/list_config', methods=['GET'])
def list_config():
    try:
        file_list = os.listdir(TEMP_PATH)
        result = '\n'.join(file_list)
        return make_response(result)
    except Exception as e:
        return "请求文件列表发生异常"


@app.route('/api/download_config', methods=['GET'])
def download_config():
    qs = str(request.query_string, encoding='utf-8')
    try:
        qp = cgi.urllib.parse.parse_qs(qs)
        inventory = qp['inventory'][0]
        type = qp['type'][0]
        host = qp['host'][0]
        task = create_task()
        play_get_etc_config(task, inventory, host, type)
        return jsonify(task)
    except Exception as e:
        logger.exception(e)
        return make_response("请求异常", 400)


@app.route('/api/get_config', methods=['GET'])
def fetch_config():
    qs = str(request.query_string, encoding='utf-8')
    try:
        qp = cgi.urllib.parse.parse_qs(qs)
        filename = qp['filename'][0]
        type = qp['type'][0]
        if filename and type:

            with open('./tmp/' + type + '-' + filename, 'r') as f:
                fs = f.read()
            return make_response(fs)
        else:
            return make_response("请求的文件不存在，请重新下载")
    except Exception as e:
        logger.error(e)
        return make_response("请求的文件不存在，请重新下载")


@app.route('/api/upload_config', methods=['POST'])
def upload_config():
    qs = str(request.query_string, encoding='utf-8')
    try:
        qp = cgi.urllib.parse.parse_qs(qs)
        type = qp['type'][0]
        host = qp['host'][0]
        inventory = qp['inventory'][0]
        reset = qp['reset'][0]
        content = request.data
        task = create_task()
        if reset:
            result = pb_upload_reset_config(task, inventory=inventory, type=type, host=host,
                                   content=content)
        else:
            result = play_upload_etc_config(task, inventory=inventory, type=type, host=host,
                                   content=content)
        if result:
            return jsonify(task)
        else:
            return make_response("异常", 500)

    except Exception as e:
        logger.exception(e)
        return make_response("请求异常", 204)



@app.route('/', methods=['GET', 'POST'])
def root():
    render = render_template('index.html')
    print(render)
    return render


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=3389)
