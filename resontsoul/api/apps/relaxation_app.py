#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: relaxation_app.py
@time: 2025/7/23
@project: resonant-soul
@desc: 放松训练业务逻辑
"""
from api.db.services.relaxation_service import RelaxationService


def record_relaxation(relaxation_type, user_id):
    """记录放松训练完成"""
    if user_id is not None:
        RelaxationService.save_relaxation(relaxation_type, user_id)


def get_relaxation_history(user_id):
    """获取放松训练历史"""
    return RelaxationService.get_recent_relaxations(user_id)


def get_relaxation_stats(user_id):
    """获取放松训练统计"""
    return RelaxationService.get_relaxation_stats(user_id)