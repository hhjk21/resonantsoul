#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: relaxation_service.py
@time: 2025/7/23
@project: resonant-soul
@desc: 放松训练记录服务
"""
from datetime import datetime, timedelta

from peewee import fn

from api.db.db_models import Relaxation


class RelaxationService:
    model = Relaxation

    @classmethod
    def save_relaxation(cls, relaxation_type, user_id):
        """保存放松训练记录"""
        cls.model.create(
            relaxation_type=relaxation_type,
            user_id=user_id,
            timestamp=datetime.now()
        )

    @classmethod
    def get_recent_relaxations(cls, user_id, limit=10):
        """获取最近的放松训练记录"""
        query = (cls.model
                 .select()
                 .where(cls.model.user_id == user_id)
                 .order_by(cls.model.timestamp.desc())
                 .limit(limit))
        return [(r.timestamp.strftime("%Y-%m-%d %H:%M:%S"), r.relaxation_type)
                for r in query]

    @classmethod
    def get_relaxation_stats(cls, user_id, days=7):
        """获取放松训练统计"""
        start_date = datetime.now() - timedelta(days=days)
        query = (cls.model
                 .select()
                 .where(cls.model.user_id == user_id,
                        cls.model.timestamp >= start_date))

        total = query.count()
        type_counts = dict(
            (row.relaxation_type, row.count)
            for row in query.select(
                cls.model.relaxation_type,
                fn.COUNT(cls.model.id).alias('count')
            ).group_by(cls.model.relaxation_type)
        )

        return {
            'total_sessions': total,
            'type_distribution': type_counts
        }