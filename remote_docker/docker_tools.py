#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
# import subprocess
import docker
import re
import logger
log = logger.Logger("log/docker_tools.log").logger

registry_aliyun = 'registry.cn-hangzhou.aliyuncs.com/reg_pub/{}'
client = docker.from_env()
# debug配置
# client = docker.DockerClient('ssh://root@yourhost',use_ssh_client=True)
registry_api='https://registry.hub.docker.com/v2/repositories/library/'

"""
    查询指定名称的页面信息

    Args:
        name (str): 需要查询的页面名称
        page (int, optional): 查询的页码，默认为1
        page_size (int, optional): 每页显示的数据量，默认为1024

    Returns:
        dict: 查询结果，以字典形式返回

"""
def search_pages(name,page=1,page_size=100):
    print(registry_api)
    api = registry_api+"{}/tags/?page={}&page_size={}".format(name,page,page_size)
    log.debug(api)
    rs = requests.get(api)
    return rs.json()

# 执行 docker search 命令
def search_key(name):
    rs = client.images.search(name)
    return {'code':200,'rs':rs}

# 拉群镜像并push到阿里云
def pull(name):
    rs = client.images.pull(name)
    # log.debug('image:'+rs)
    if rs:
        tag_name = str(rs.tags[0]).replace('/',"_")
        log.debug('source tag:'+tag_name)
        new_name= registry_aliyun.format(tag_name)
        log.debug('target tag:'+new_name)
        rs.tag(new_name)
        ps = client.images.push(new_name)
        log.debug('push result:'+ps)
        if ps:
            rs.remove(force=True)
            return {'code':200,'data':new_name}
        else:
            return {'code':500, 'rs':ps}
    else:
        return {'code':500, 'rs':rs}

# 批量拉取并push到阿里云
def pull_bath(names):
    imgs = []
    for name in names:
        img ={'source':name, 'target':''}
        rs = pull(name)
        if rs and rs['code'] == 200:
            img['target']= rs['data']
        imgs.append(img)
    
    return {"code":200,"data":imgs}
