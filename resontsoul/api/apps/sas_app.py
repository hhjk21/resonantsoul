#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: sas_app.py
@time: 2025/7/21 15:16
@project: resonant-soul
@desc: SAS 焦虑自评量表(标准20题)
"""
from api.db.services.assessment_service import AssessmentService

# 反向计分题索引（0-based）：第5、9、13、17、19题
SAS_REVERSE_ITEMS = {4, 8, 12, 16, 18}


def calculate_sas_score(answers):
    """计算SAS量表得分,支持反向计分"""
    score = 0
    for i, ans in enumerate(answers):
        if i in SAS_REVERSE_ITEMS:
            # 反向计分：1→4, 2→3, 3→2, 4→1
            score += 5 - ans
        else:
            score += ans
    standard_score = int(score * 1.25)  # 粗分乘以1.25得到标准分
    return standard_score


def get_sas_result(score):
    """解释SAS得分"""
    if score < 50:
        return "焦虑水平在正常范围内"
    elif score < 60:
        return "轻度焦虑"
    elif score < 70:
        return "中度焦虑"
    else:
        return "重度焦虑"


def process_sas_scores(user_id, *scores):
    """处理SAS评估分数"""
    total_score = calculate_sas_score(scores)
    result = get_sas_result(total_score)

    if user_id is not None:
        # 保存评估结果到数据库
        AssessmentService.save_assessment(user_id, list(scores), total_score, result)

        detailed_result = f"""
    评估完成！</br>
    
    您的SAS标准分为: {total_score}</br>
    
    评估结果: {result}</br>
    
    参考说明：</br>
    - 50分以下:焦虑水平在正常范围内</br>
    - 50-59分:轻度焦虑</br>
    - 60-69分:中度焦虑</br>
    - 70分以上:重度焦虑</br>
    </br>
    注意：本测评仅供参考，如有需要请咨询专业心理医生。
        """
        return detailed_result
    return None
