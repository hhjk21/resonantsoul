#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: test_sas_app.py
@time: 2025/7/23
@project: resonant-soul
@desc: SAS 评估模块单元测试
"""
import pytest

from api.apps.sas_app import calculate_sas_score, get_sas_result


class TestSASScore:
    """SAS 计分逻辑测试"""

    def test_all_minimum_score(self):
        """全部选1分（反问题变成4分）：标准分 = (15*1 + 5*4) * 1.25 = 35*1.25 = 43"""
        answers = [1] * 20
        assert calculate_sas_score(answers) == 43

    def test_all_maximum_score(self):
        """全部选4分（反问题变成1分）：标准分 = (15*4 + 5*1) * 1.25 = 65*1.25 = 81"""
        answers = [4] * 20
        assert calculate_sas_score(answers) == 81

    def test_reverse_items_scoring(self):
        """反向题计分：第5题选4应得1分，第9题选1应得4分"""
        answers = [1] * 20
        # 反向题: 5(索引4), 9(索引8), 13(索引12), 17(索引16), 19(索引18)
        answers[4] = 4   # 选4 → 计1分
        answers[8] = 1   # 选1 → 计4分
        answers[12] = 4  # 选4 → 计1分
        answers[16] = 1  # 选1 → 计4分
        answers[18] = 4  # 选4 → 计1分
        expected = int((15 + 1 + 4 + 1 + 4 + 1) * 1.25)  # 26 * 1.25 = 32
        assert calculate_sas_score(answers) == expected

    def test_normal_case(self):
        """正常计分：所有题选2分（反问题变成3分）"""
        answers = [2] * 20
        expected = int((15 * 2 + 5 * 3) * 1.25)  # 45 * 1.25 = 56
        assert calculate_sas_score(answers) == expected


class TestSASResult:
    """SAS 结果解读测试"""

    @pytest.mark.parametrize("score, expected", [
        (25, "焦虑水平在正常范围内"),
        (49, "焦虑水平在正常范围内"),
        (50, "轻度焦虑"),
        (59, "轻度焦虑"),
        (60, "中度焦虑"),
        (69, "中度焦虑"),
        (70, "重度焦虑"),
        (81, "重度焦虑"),
    ])
    def test_result_levels(self, score, expected):
        """测试各分数段结果解读"""
        assert get_sas_result(score) == expected


class TestSASReverseItems:
    """反问题索引测试"""

    def test_reverse_item_indices(self):
        """验证反向题索引正确"""
        from api.apps.sas_app import SAS_REVERSE_ITEMS
        assert SAS_REVERSE_ITEMS == {4, 8, 12, 16, 18}
        # 5题的反向题对应 5, 9, 13, 17, 19（1-based）→ 4, 8, 12, 16, 18（0-based）
        assert len(SAS_REVERSE_ITEMS) == 5

    def test_reverse_calculation(self):
        """验证反向计分公式：5 - ans"""
        for ans in range(1, 5):
            assert 5 - ans == {1: 4, 2: 3, 3: 2, 4: 1}[ans]