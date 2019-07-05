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
import time

app = Flask(__name__)
app.debug = True

TEMP_PATH = './tmp/'

TASK_BUFFER = []


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
        TASK_BUFFER.append(task)
        # print("the new task id is %d" % task['id'])
        # return jsonify({'id': task['id']})
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
            return make_response("请求的文件不存在", 400)
    except Exception as e:
        return "请求文件时发生异常"
    except Exception as e:
        logger.error(e)
        return make_response("请求异常", 400)


@app.route('/api/upload_config', methods=['POST'])
def upload_config():
    qs = str(request.query_string, encoding='utf-8')
    try:
        qp = cgi.urllib.parse.parse_qs(qs)
        type = qp['type'][0]
        host = qp['host'][0]
        inventory = qp['inventory'][0]
        content = request.data
        task = create_task()
        play_upload_etc_config(task, inventory=inventory, type=type, host=host,
                               content=content)
        print("the new task id is %d" % task['id'])
        return jsonify({'id': task['id']})

    except Exception as e:
        logger.exception(e)
        return make_response("请求异常", 400)


@app.route('/api/get_task', methods=['GET'])
def get_task():
    qs = str(request.query_string, encoding='utf-8')
    try:
        qp = cgi.urllib.parse.parse_qs(qs)
        task_id = qp['id'][0]
        print('the query id is %s' % task_id)
        for task in TASK_BUFFER:
            print(task['id'])
            if task['id'] == int(task_id):
                return jsonify(task)
        return make_response("not found", 204)
    except Exception as e:
        logger.error(e)
        return make_response("请求异常", 400)


@app.route('/', methods=['GET', 'POST'])
def root():
    render = render_template('index.html')
    print(render)
    return render


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=3389)
