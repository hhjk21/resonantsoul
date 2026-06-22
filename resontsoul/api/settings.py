#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: settings.py
@time: 2025/7/23
@project: resonant-soul
@desc: 
"""

import os

# 绕过不可用的系统代理
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'
# 删除系统代理环境变量，避免 httpx 读取
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']:
    os.environ.pop(key, None)

# Monkey-patch httpx 禁用代理
import httpx
_original_client_init = httpx.Client.__init__
_original_async_client_init = httpx.AsyncClient.__init__

def _patched_init(self, *args, **kwargs):
    kwargs.setdefault('trust_env', False)
    _original_client_init(self, *args, **kwargs)

def _patched_async_init(self, *args, **kwargs):
    kwargs.setdefault('trust_env', False)
    _original_async_client_init(self, *args, **kwargs)

httpx.Client.__init__ = _patched_init
httpx.AsyncClient.__init__ = _patched_async_init

from camel.models import ModelFactory
from camel.types import ModelPlatformType
from dotenv import load_dotenv

from api.db.db_models import DBManager
from api.utils import get_base_config
from api.utils.t_crypt import decrypt_api_key, generate_key

EMOTION_RECORDS = []
databaseConn = None
CHAT_MDL = None
ADMIN_USER = None


def init_settings():
    global EMOTION_RECORDS, databaseConn, CHAT_MDL, ADMIN_USER
    # 存储情绪记录和日记
    databaseConn = DBManager()

    # 加载环境变量
    load_dotenv(dotenv_path='.env')

    LLM = get_base_config("llm")
    api_key = LLM['api_key']
    try:
        api_key = decrypt_api_key(api_key, generate_key())
    except Exception:
        # 如果解密失败，说明 api_key 已是明文，直接使用
        pass

    # 初始化模型
    CHAT_MDL = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type=LLM['model_type'],
        url=LLM['model_url'],
        api_key=api_key,
    )
    ADMIN_USER = get_base_config("admin")
