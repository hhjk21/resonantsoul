#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: conversation_app.py
@time: 2025/7/21 15:20
@project: resonant-soul
@desc: 
"""
from api.apps.emotion_app import analyze_emotion, save_emotion_record, generate_emotion_chart
from api.db.services.conversation_service import ConversationService


def process_user_input(current_user, user_input, history: list):
    from api.settings import CHAT_MDL
    user_id = current_user['id']
    """处理用户输入并返回响应"""
    try:
        emotions = analyze_emotion(user_input)
        save_emotion_record(emotions, user_input, user_id)
        print(f"检测到的情绪: {emotions}")

        # 构建对话消息
        system_prompt = (
            "你是心灵伙伴AI心理健康助手，一名温暖、专业、有同理心的心理咨询师。"
            "请以第一人称直接与大学生进行心理健康对话。\n"
            "要求：\n"
            "1. 使用温暖、共情的语气\n"
            "2. 以第一人称'我'回应，不要用第三人称\n"
            "3. 根据用户情绪提供针对性的支持和建议\n"
            "4. 回复简洁，控制在200字以内\n"
            "5. 不要自称'心理咨询师'、'AI助手'等，直接以朋友身份对话"
        )
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append(msg)
        messages.append({"role": "user", "content": user_input})

        # 调用大模型
        response = CHAT_MDL.run(messages)
        response_content = response.choices[0].message.content

        # 保存对话记录到数据库
        ConversationService.save_conversation(user_input, response_content, user_id)

        # 返回新的对话历史
        new_history = history + [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response_content}
        ]

        return new_history, generate_emotion_chart()
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_msg = f"抱歉，模型调用失败：{str(e)}"
        new_history = history + [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": error_msg}
        ]
        return new_history, generate_emotion_chart()
