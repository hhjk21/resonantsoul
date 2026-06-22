#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: init_data.py
@time: 2025/7/23 9:52
@project: resonant-soul
@desc: 
"""
from api import settings
from api.apps.admin_app import create_admin_user
from api.apps.user_app import user_login
from loguru import logger


def init_web_data():
    # 初始化管理员账号
    username = settings.ADMIN_USER['username']
    password = settings.ADMIN_USER['password']
    name_nick = settings.ADMIN_USER['name_nick']
    create_admin_user(username, name_nick, password)
    logger.info("管理员账号初始化完成")

    # 检查是否使用默认密码，发出安全警告
    DEFAULT_ADMIN_PASSWORD = "admin@123"
    if password == DEFAULT_ADMIN_PASSWORD:
        logger.warning(
            "【安全警告】管理员仍在使用默认密码 'admin@123',"
            "建议立即通过系统界面修改密码！"
        )
