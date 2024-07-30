#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import request,Flask,jsonify
import docker_tools
import logger
app = Flask(__name__)
TOKEN='XXXXX'
log = logger.Logger("log/app.log").logger
@app.route('/search_page',methods=['GET'])
def search_pages():
    try:
        page=1
        page_size=1024
        args= request.args
        if 'name' in args.keys():
            name=args['name']
        else:
            return jsonify({'code':'-1','msg':'no query'})
        if 'page' in args.keys():
            page=int(args['page'])
        if 'page_size' in args.keys():
            page_size=int(args['page_size'])
        return jsonify(docker_tools.search_pages(name,page=page,page_size=page_size))
    except Exception as e:
        log.error("Error in search")
        log.exception(e)

@app.route('/search_key',methods=['GET'])
def search_key():
    try:
        args= request.args
        if 'name' in args.keys():
            name=args['name']
        else:
            return jsonify({'code':'-1','msg':'no query'})
        return jsonify(docker_tools.search_key(name))
    except Exception as e:
        log.error("Error in search")
        log.exception(e)
@app.route('/pull',methods=['post'])
def pull():
    try:
        args= request.args
        if args and 'name' in args.keys():
            name=args['name']
        rs= request.form
        print(rs)
        token=None
        if 'token' in rs.keys():
            token = rs['token']
        if token ==None or token !=TOKEN:
            print(token)
            return jsonify({'code': '-1', 'msg': '非法入侵'})
        if 'file' in request.files:

            file = request.files['file']
            file_s = file.read()
            if file_s == None:
                return jsonify({'code': '-1', 'msg': 'no file'})
            f_l = file_s.decode().split('\n')
            log.info(f_l)
            return jsonify(docker_tools.pull_bath(f_l))
    
        else:
            return jsonify(docker_tools.pull(name))
    except Exception as e:
        log.error("Error in pull")
        log.exception(e)

if __name__ == '__main__':
    app.run(host="0.0.0.0")

    

