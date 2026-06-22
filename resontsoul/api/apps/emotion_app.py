#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: emotion_app.py
@time: 2025/7/21 14:56
@project: resonant-soul
@desc: 情绪分析模块（LLM为主，关键词为兜底）
"""
import json
from datetime import datetime

import matplotlib.pyplot as plt

from api.db.services.emotion_service import EmotionService


def analyze_emotion(text):
    """使用 LLM 分析用户情绪，关键词匹配作为兜底"""
    # 尝试使用 LLM 识别情绪
    try:
        return _analyze_emotion_by_llm(text)
    except Exception:
        # LLM 不可用时回退到关键词匹配
        return _analyze_emotion_by_keywords(text)


def _analyze_emotion_by_llm(text):
    """使用 LLM 分析情绪"""
    from api.settings import CHAT_MDL
    prompt = (
        "你是一个情绪分析专家。请分析以下用户输入文本中包含的情绪，"
        "只从以下五类中选择：焦虑、抑郁、愤怒、积极、平静。\n"
        "请严格按照 JSON 数组格式返回，例如：[\"焦虑\", \"积极\"]\n"
        "只返回 JSON 数组，不要包含其他任何文字。\n\n"
        f"用户输入：{text}"
    )
    messages = [
        {"role": "system", "content": "你是一个专业的情绪分析助手，只输出JSON数组格式的情绪标签。"},
        {"role": "user", "content": prompt},
    ]
    response = CHAT_MDL.run(messages)
    content = response.choices[0].message.content.strip()

    # 解析 LLM 返回的 JSON
    valid_emotions = {'焦虑', '抑郁', '愤怒', '积极', '平静'}
    try:
        emotions = json.loads(content)
        if isinstance(emotions, list):
            result = [e for e in emotions if e in valid_emotions]
            return result if result else ['平静']
    except json.JSONDecodeError:
        pass

    # 如果 LLM 返回格式异常，回退到关键词匹配
    return _analyze_emotion_by_keywords(text)


def _analyze_emotion_by_keywords(text):
    """关键词匹配情绪识别（兜底方案）"""
    emotions = {
        '焦虑': ['焦虑', '紧张', '不安', '担心', '压力', '烦恼'],
        '抑郁': ['抑郁', '难过', '消沉', '伤心', '悲伤', '失落'],
        '愤怒': ['生气', '愤怒', '烦躁', '恼火', '不满', '讨厌'],
        '积极': ['开心', '快乐', '高兴', '兴奋', '满足']
    }

    detected_emotions = []
    for emotion, keywords in emotions.items():
        if any(keyword in text for keyword in keywords):
            detected_emotions.append(emotion)

    return detected_emotions if detected_emotions else ['平静']


def save_emotion_record(emotion, user_input, user_id):
    """保存情绪记录"""
    from api.settings import EMOTION_RECORDS
    record = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'emotion': emotion,
    }
    EMOTION_RECORDS.append(record)
    record['user_input'] = user_input
    # 添加数据库存储
    EmotionService.save_emotion(emotion, user_input, user_id)


def generate_emotion_chart():
    """生成情绪趋势图表"""
    from api.settings import EMOTION_RECORDS
    if not EMOTION_RECORDS:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No Emotion Data', ha='center', va='center')
        ax.set_axis_off()
        return fig

    emotion_en_map = {
        '焦虑': 'Anxiety',
        '抑郁': 'Depression',
        '愤怒': 'Anger',
        '积极': 'Positive',
        '平静': 'Calm'
    }

    emotion_counts = {}
    for record in EMOTION_RECORDS:
        for emotion in record['emotion']:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1

    fig, ax = plt.subplots()
    labels = list(emotion_counts.keys())
    sizes = list(emotion_counts.values())
    labels_en = [emotion_en_map.get(label, label) for label in labels]

    colors = {
        '焦虑': 'orange',
        '抑郁': 'blue',
        '愤怒': 'red',
        '积极': 'green',
        '平静': 'gray'
    }

    color_list = [colors.get(label, 'gray') for label in labels]
    ax.pie(sizes, labels=labels_en, autopct='%1.1f%%', colors=color_list)
    ax.set_title('Emotion Distribution')

    return fig


def get_all_emotion_records(user_id, page=1, page_size=20):
    """
    获取情绪记录，支持分页。
    返回 (records, total_count) 元组。

    records: 按 date, content, emotions 的数组返回
    """
    records = []
    offset = (page - 1) * page_size
    # 获取所有情绪记录
    emotions = EmotionService.get_recent_all_emotions(user_id, limit=page_size, offset=offset)
    for timestamp, emotion_json, user_input in emotions:
        emotions_list = json.loads(emotion_json)
        record = {
            "date": timestamp,
            "content": user_input,
            "emotions": emotions_list
        }
        records.append(record)
    total = EmotionService.get_emotion_count(user_id)
    return records, total
