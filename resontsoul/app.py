#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: main_mind.py
@time: 2025/7/21 13:57
@project: resonant-soul
@desc: 心灵伙伴 - AI 心理健康助手（优化版 UI）
"""
import os

import gradio as gr

from api import bootstrap
from api.apps.admin_app import get_all_users, update_user_status, delete_user
from api.apps.conversation_app import process_user_input
from api.apps.emotion_app import get_all_emotion_records
from api.apps.relaxation_app import record_relaxation, get_relaxation_stats
from api.apps.sas_app import process_sas_scores
from api.apps.statistics_app import generate_stats_charts, get_stats_text
from api.apps.user_app import user_login, user_register, get_user_info_by_username, update_password, get_user_info_by_id, check_default_admin_password
from api.utils import get_base_config

# SAS焦虑自评量表题目（标准20题，题号后带 * 的为反向计分题）
sas_questions = [
    "1. 我觉得比平时容易紧张和着急",
    "2. 我无缘无故地感到害怕",
    "3. 我容易心里烦乱或觉得惊恐",
    "4. 我觉得我可能将要发疯",
    "5. 我觉得一切都很好，也不会发生什么不幸 *",
    "6. 我手脚发抖打颤",
    "7. 我因为头痛、颈痛和背痛而苦恼",
    "8. 我感觉容易衰弱和疲乏",
    "9. 我觉得心平气和，并且容易安静坐着 *",
    "10. 我觉得心跳得很快",
    "11. 我因为一阵阵头晕而苦恼",
    "12. 我有晕倒发作，或觉得要晕倒似的",
    "13. 我吸气呼气都感到很容易 *",
    "14. 我的手脚麻木和刺痛",
    "15. 我因为胃痛和消化不良而苦恼",
    "16. 我常常要小便",
    "17. 我的手脚常常是干燥温暖的 *",
    "18. 我脸红发热",
    "19. 我容易入睡并且一夜睡得很好 *",
    "20. 我做恶梦",
]

# 放松训练指导内容
relaxation_guides = {
    "呼吸放松": """
### 🫁 呼吸放松训练

1. 找一个安静、舒适的地方坐下
2. 缓慢吸气，数 4 秒
3. 屏住呼吸，数 4 秒
4. 缓慢呼气，数 6 秒
5. 重复以上步骤 5-10 次

> 💡 **小提示**：想象把所有的紧张和焦虑都随着呼气排出体外。
""",
    "渐进性肌肉放松": """
### 💪 渐进性肌肉放松

1. 从脚趾开始，绷紧肌肉 5 秒
2. 完全放松 10 秒，感受放松的感觉
3. 逐渐向上移动到小腿、大腿
4. 继续到腹部、胸部、手臂
5. 最后是面部肌肉

> 💡 **小提示**：每个部位都要对比紧张和放松的感觉差异。
""",
    "正念冥想": """
### 🧠 正念冥想

1. 选择一个安静的环境
2. 采用舒适的坐姿，背挺直
3. 闭上眼睛，关注呼吸
4. 让思绪自然流动，不评判
5. 温和地将注意力带回呼吸

> 💡 **小提示**：刚开始可以从 5 分钟开始，慢慢延长到 15-20 分钟。
"""
}

# 放松训练元数据（用于卡片展示）
relaxation_meta = [
    {"key": "呼吸放松", "icon": "🫁", "title": "呼吸放松", "desc": "4-4-6 呼吸法，快速缓解紧张"},
    {"key": "渐进性肌肉放松", "icon": "💪", "title": "渐进性肌肉放松", "desc": "全身逐部位放松，释放身体压力"},
    {"key": "正念冥想", "icon": "🧠", "title": "正念冥想", "desc": "专注当下，接纳自我"},
]

SAS_PAGE_SIZE = 5  # 每页显示 5 题
DIARY_PAGE_SIZE = 20

# 读取自定义 CSS
_css_path = os.path.join(os.path.dirname(__file__), "static", "custom.css")
with open(_css_path, "r", encoding="utf-8") as _f:
    CUSTOM_CSS = _f.read()


def create_gradio_interface():
    with gr.Blocks(
        title="心灵伙伴 - AI心理健康助手",
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="emerald",
        ),
        css=CUSTOM_CSS,
    ) as _interface:
        current_user = gr.State({"id": None, "name": None, "is_admin": False})

        # ==================== 登录页 ====================
        with gr.Column(visible=True, elem_classes="rs-auth-container") as auth_panel:
            gr.HTML("""
            <div class="rs-auth-hero">心灵伙伴</div>
            <div class="rs-auth-subtitle">AI 心理健康助手 · 7×24 小时温暖陪伴</div>
            <div class="rs-feature-grid">
                <div class="rs-feature-card">
                    <div class="rs-feature-icon">💬</div>
                    <div class="rs-feature-title">智能对话</div>
                    <div class="rs-feature-desc">AI 心理咨询师随时倾听</div>
                </div>
                <div class="rs-feature-card">
                    <div class="rs-feature-icon">📊</div>
                    <div class="rs-feature-title">心理评估</div>
                    <div class="rs-feature-desc">专业量表评估焦虑水平</div>
                </div>
                <div class="rs-feature-card">
                    <div class="rs-feature-icon">🧘</div>
                    <div class="rs-feature-title">放松训练</div>
                    <div class="rs-feature-desc">呼吸、冥想、肌肉放松</div>
                </div>
            </div>
            """)

            with gr.Tabs():
                with gr.Tab("登录", id="login"):
                    with gr.Column(elem_classes="rs-card"):
                        login_username = gr.Textbox(
                            label="用户名",
                            placeholder="请输入用户名",
                            container=False,
                        )
                        login_password = gr.Textbox(
                            label="密码",
                            type="password",
                            placeholder="请输入密码",
                            container=False,
                        )
                        login_btn = gr.Button("登 录", variant="primary", size="lg")
                        login_status = gr.Markdown(visible=False)

                with gr.Tab("注册", id="register"):
                    with gr.Column(elem_classes="rs-card"):
                        register_username = gr.Textbox(
                            label="用户名",
                            placeholder="4-20 位字母或数字",
                            container=False,
                        )
                        register_name_nick = gr.Textbox(
                            label="昵称",
                            placeholder="怎么称呼您？",
                            container=False,
                        )
                        register_password = gr.Textbox(
                            label="密码",
                            type="password",
                            placeholder="至少 8 位，包含字母和数字",
                            container=False,
                        )
                        register_btn = gr.Button("注 册", variant="primary", size="lg")
                        register_status = gr.Markdown(visible=False)

        # ==================== 主面板 ====================
        with gr.Column(visible=False, elem_id="main_panel") as main_panel:
            # 顶部导航栏
            gr.HTML("""
            <div class="rs-navbar">
                <div>
                    <span class="rs-navbar-title">心灵伙伴</span>
                    <span class="rs-navbar-subtitle">AI 心理健康助手</span>
                </div>
                <div class="rs-navbar-user" id="rs-nav-user">未登录</div>
            </div>
            """)

            # 安全警告横幅
            security_warning = gr.Markdown(visible=False)

            with gr.Tabs() as main_tabs:
                # ============ 主对话 ============
                with gr.Tab("💬 主对话", id="chat_tab"):
                    with gr.Row():
                        with gr.Column(scale=1, elem_classes="rs-card"):
                            chatbot = gr.Chatbot(
                                height=500,
                                type="messages",
                                avatar_images=(None, None),
                            )
                            with gr.Row():
                                input_text = gr.Textbox(
                                    label="",
                                    placeholder="请告诉我您的想法或感受...",
                                    scale=5,
                                    container=False,
                                    submit_btn=True,
                                    stop_btn=True,
                                )
                    with gr.Accordion("📊 情绪趋势图", open=False):
                        emotion_chart = gr.Plot(label="")

                # ============ 心理评估（SAS 分页） ============
                with gr.Tab("📋 心理评估", id="sas_tab"):
                    gr.HTML("""
                    <div class="rs-sas-instruction">
                        <p style="font-weight:600;color:var(--rs-text);font-size:1.1em;">焦虑自评量表 (SAS)</p>
                        <p style="color:var(--rs-text-light);">
                            1 = 很少或没有 &nbsp;|&nbsp; 2 = 有时 &nbsp;|&nbsp; 3 = 经常 &nbsp;|&nbsp; 4 = 总是如此
                        </p>
                        <p style="color:var(--rs-text-light);">请根据<strong>最近一周</strong>的感受进行评分</p>
                    </div>
                    """)

                    sas_page = gr.State(0)
                    sas_all_scores = gr.State([1] * 20)

                    # 进度条
                    gr.HTML("""
                    <div class="rs-progress-bar">
                        <div id="sas-progress-bar" class="rs-progress-fill" style="width:5%"></div>
                    </div>
                    """)

                    sas_page_info = gr.Markdown("### 第 1 / 4 页（第 1-5 题）")

                    sas_sliders = []
                    with gr.Column(elem_classes="rs-card"):
                        for i in range(SAS_PAGE_SIZE):
                            sas_sliders.append(
                                gr.Slider(
                                    minimum=1, maximum=4, step=1, value=1,
                                    label=sas_questions[i],
                                    interactive=True,
                                )
                            )

                    with gr.Row():
                        sas_prev_btn = gr.Button("← 上一页", size="sm", interactive=False)
                        sas_next_btn = gr.Button("下一页 →", size="sm", variant="primary")

                    sas_submit = gr.Button("提交评估", variant="primary", size="lg")
                    sas_result = gr.Markdown(visible=False)

                    def render_sas_page(page_num, all_scores):
                        """渲染 SAS 当前页的题目和分数"""
                        start = page_num * SAS_PAGE_SIZE
                        end = min(start + SAS_PAGE_SIZE, 20)
                        total_pages = (20 + SAS_PAGE_SIZE - 1) // SAS_PAGE_SIZE
                        pct = int((page_num + 1) / total_pages * 100)

                        # 更新题目标签
                        updates = []
                        for i in range(SAS_PAGE_SIZE):
                            idx = start + i
                            if idx < 20:
                                updates.append(gr.Slider(
                                    label=sas_questions[idx],
                                    value=all_scores[idx],
                                ))
                            else:
                                updates.append(gr.Slider(visible=False))
                        # 填充剩余的 slider
                        while len(updates) < len(sas_sliders):
                            updates.append(gr.Slider(visible=False))

                        page_indicator = f"### 第 {page_num + 1} / {total_pages} 页（第 {start + 1}-{min(end, 20)} 题）"
                        prev_enabled = page_num > 0
                        next_enabled = page_num < total_pages - 1
                        return (*updates, page_indicator, prev_enabled, next_enabled)

                    def on_sas_page_change(page_num, all_scores, *current_sliders):
                        """翻页时保存当前页分数并切换"""
                        start = page_num * SAS_PAGE_SIZE
                        for i in range(SAS_PAGE_SIZE):
                            idx = start + i
                            if idx < 20:
                                all_scores[idx] = int(current_sliders[i])
                        return render_sas_page(page_num, all_scores)

                    def go_sas_prev(page_num, all_scores, *current_sliders):
                        if page_num <= 0:
                            return (*render_sas_page(0, all_scores), 0, all_scores)
                        start = page_num * SAS_PAGE_SIZE
                        for i in range(SAS_PAGE_SIZE):
                            idx = start + i
                            if idx < 20:
                                all_scores[idx] = int(current_sliders[i])
                        new_page = page_num - 1
                        return (*render_sas_page(new_page, all_scores), new_page, all_scores)

                    def go_sas_next(page_num, all_scores, *current_sliders):
                        total_pages = (20 + SAS_PAGE_SIZE - 1) // SAS_PAGE_SIZE
                        if page_num >= total_pages - 1:
                            return (*render_sas_page(page_num, all_scores), page_num, all_scores)
                        start = page_num * SAS_PAGE_SIZE
                        for i in range(SAS_PAGE_SIZE):
                            idx = start + i
                            if idx < 20:
                                all_scores[idx] = int(current_sliders[i])
                        new_page = page_num + 1
                        return (*render_sas_page(new_page, all_scores), new_page, all_scores)

                    sas_prev_btn.click(
                        go_sas_prev,
                        inputs=[sas_page, sas_all_scores, *sas_sliders],
                        outputs=[*sas_sliders, sas_page_info, sas_prev_btn, sas_next_btn, sas_page, sas_all_scores],
                    )
                    sas_next_btn.click(
                        go_sas_next,
                        inputs=[sas_page, sas_all_scores, *sas_sliders],
                        outputs=[*sas_sliders, sas_page_info, sas_prev_btn, sas_next_btn, sas_page, sas_all_scores],
                    )

                    def submit_sas(current_user, all_scores, *current_sliders):
                        """提交评估：先保存最后一页的分数"""
                        start = sas_page.value * SAS_PAGE_SIZE
                        for i in range(SAS_PAGE_SIZE):
                            idx = start + i
                            if idx < 20:
                                all_scores[idx] = int(current_sliders[i])
                        user_id = current_user['id']
                        result = process_sas_scores(user_id, *all_scores)
                        return result

                    sas_submit.click(
                        submit_sas,
                        inputs=[current_user, sas_all_scores, *sas_sliders],
                        outputs=sas_result,
                    ).success(
                        fn=lambda: gr.Markdown(visible=True),
                        outputs=sas_result,
                    )

                # ============ 放松训练 ============
                with gr.Tab("🧘 放松训练", id="relaxation_tab"):
                    gr.Markdown("## 选择一种放松训练方式")

                    # 卡片式选择
                    cards_html = '<div class="rs-relaxation-grid">'
                    for meta in relaxation_meta:
                        cards_html += f"""
                        <div class="rs-relaxation-card" onclick="document.querySelector('#relaxation_radio input[value=\\'{meta['key']}\\']').click()">
                            <div class="rs-feature-icon">{meta['icon']}</div>
                            <div class="rs-feature-title">{meta['title']}</div>
                            <div class="rs-feature-desc">{meta['desc']}</div>
                        </div>
                        """
                    cards_html += '</div>'
                    gr.HTML(cards_html)

                    relaxation_type = gr.Radio(
                        choices=list(relaxation_guides.keys()),
                        label="",
                        visible=True,
                        elem_id="relaxation_radio",
                    )

                    relaxation_guide = gr.Markdown(
                        value="请选择一种放松训练方式",
                        elem_classes="rs-card",
                    )

                    def on_relaxation_select(choice, current_user):
                        """选择放松训练时记录"""
                        if choice and current_user and current_user.get('id'):
                            record_relaxation(choice, current_user['id'])
                        return relaxation_guides.get(choice, "请选择一种放松训练方式")

                    relaxation_type.change(
                        on_relaxation_select,
                        [relaxation_type, current_user],
                        relaxation_guide,
                    )

                # ============ 情绪日记 ============
                with gr.Tab("📔 情绪日记", id="diary_tab"):
                    gr.Markdown("## 我的情绪日记")
                    diary_page = gr.State(1)
                    diary_page_info = gr.Markdown("第 1 页")

                    with gr.Column(elem_classes="rs-table-wrap"):
                        diary_list = gr.HTML()

                    with gr.Row():
                        prev_page_btn = gr.Button("← 上一页", size="sm")
                        next_page_btn = gr.Button("下一页 →", size="sm", variant="primary")
                        refresh_diary_btn = gr.Button("🔄 刷新", size="sm")

                    def build_diary_html(records, page, total, page_size=DIARY_PAGE_SIZE):
                        """构建日记 HTML 表格"""
                        total_pages = max(1, (total + page_size - 1) // page_size)
                        if not records:
                            html = (
                                '<div style="text-align:center;padding:40px;color:var(--rs-text-light);">'
                                '暂无情绪记录，开始对话后会自动记录'
                                '</div>'
                            )
                        else:
                            rows = ""
                            for i, entry in enumerate(records):
                                emotion_tags = ''.join([
                                    f'<span class="rs-emotion-tag rs-emotion-{e}">{e}</span>'
                                    for e in entry['emotions']
                                ])
                                content = entry['content'][:50] + ('...' if len(entry['content']) > 50 else '')
                                rows += f"""
                                <tr>
                                    <td>{entry['date']}</td>
                                    <td>{content}</td>
                                    <td>{emotion_tags}</td>
                                </tr>
                                """
                            html = f"""
                            <table>
                                <thead><tr><th>日期</th><th>内容</th><th>情绪</th></tr></thead>
                                <tbody>{rows}</tbody>
                            </table>
                            """
                        page_text = f"第 {page} 页 / 共 {total_pages} 页（{total} 条记录）"
                        return html, page_text, page

                    def update_diary(current_user, page=1, page_size=DIARY_PAGE_SIZE):
                        user_id = current_user['id']
                        records, total = get_all_emotion_records(user_id, page=page, page_size=page_size)
                        entries = [
                            {"date": r[0], "content": r[1], "emotions": r[2].split(', ') if isinstance(r[2], str) else r[2]}
                            for r in [
                                [entry['date'], entry['content'], ', '.join(entry['emotions'])]
                                for entry in records
                            ]
                        ]
                        return build_diary_html(entries, page, total, page_size)

                    def go_prev_page(current_user, page):
                        if page > 1:
                            return update_diary(current_user, page=page - 1)
                        return update_diary(current_user, page=page)

                    def go_next_page(current_user, page):
                        try:
                            records, total = get_all_emotion_records(current_user['id'], page=1, page_size=DIARY_PAGE_SIZE)
                            total_pages = max(1, (total + DIARY_PAGE_SIZE - 1) // DIARY_PAGE_SIZE)
                            if page < total_pages:
                                return update_diary(current_user, page=page + 1)
                        except Exception:
                            pass
                        return update_diary(current_user, page=page)

                    refresh_diary_btn.click(
                        update_diary,
                        inputs=[current_user, diary_page],
                        outputs=[diary_list, diary_page_info, diary_page],
                    )
                    prev_page_btn.click(
                        go_prev_page,
                        inputs=[current_user, diary_page],
                        outputs=[diary_list, diary_page_info, diary_page],
                    )
                    next_page_btn.click(
                        go_next_page,
                        inputs=[current_user, diary_page],
                        outputs=[diary_list, diary_page_info, diary_page],
                    )
                    _interface.load(
                        update_diary,
                        inputs=[current_user, diary_page],
                        outputs=[diary_list, diary_page_info, diary_page],
                    )

                # ============ 统计分析 ============
                with gr.Tab("📊 统计分析", id="stats_tab"):
                    gr.Markdown("## 使用统计")
                    with gr.Row():
                        with gr.Column(scale=2):
                            stats_plot = gr.Plot()
                        with gr.Column(scale=1):
                            stats_text = gr.Markdown(elem_classes="rs-stat-card")
                    refresh_stats_btn = gr.Button("🔄 刷新统计", variant="secondary")

                    def update_stats(current_user):
                        user_id = current_user['id']
                        return generate_stats_charts(user_id), get_stats_text(user_id)

                    refresh_stats_btn.click(
                        update_stats,
                        inputs=current_user,
                        outputs=[stats_plot, stats_text],
                    )

                # ============ 用户信息 ============
                with gr.Tab("👤 用户信息", id="user_info_tab"):
                    with gr.Column(elem_classes="rs-card"):
                        gr.Markdown("### 基本信息")
                        with gr.Row():
                            user_info = gr.Textbox(label="用户名", interactive=False, container=False)
                            nick_info = gr.Textbox(label="用户昵称", interactive=False, container=False)
                        reg_date_info = gr.Textbox(label="注册时间", interactive=False, container=False)

                    with gr.Column(elem_classes="rs-card"):
                        gr.Markdown("### 修改密码")
                        with gr.Row():
                            new_password = gr.Textbox(
                                label="新密码", type="password",
                                placeholder="至少 8 位", container=False,
                            )
                            confirm_password = gr.Textbox(
                                label="确认新密码", type="password",
                                placeholder="再次输入新密码", container=False,
                            )
                        update_pwd_btn = gr.Button("修改密码", variant="primary")
                        pwd_status = gr.Markdown(visible=False)

                    def update_user_info(current_user):
                        if current_user is not None:
                            user = get_user_info_by_id(current_user['id'])
                            if user:
                                return [user['username'], user['name'], user['created_at']]
                        return ["", "", ""]

                    def change_password(current_user, new_pwd, confirm_pwd):
                        if new_pwd != confirm_pwd:
                            return '<div class="rs-alert rs-alert-error">新密码与确认密码不一致</div>'
                        if len(new_pwd) < 8:
                            return '<div class="rs-alert rs-alert-error">密码长度至少 8 位</div>'
                        try:
                            update_password(current_user['id'], new_pwd)
                            return '<div class="rs-alert rs-alert-success">✅ 密码修改成功</div>'
                        except Exception as e:
                            return f'<div class="rs-alert rs-alert-error">密码修改失败：{str(e)}</div>'

                    update_pwd_btn.click(
                        change_password,
                        inputs=[current_user, new_password, confirm_password],
                        outputs=pwd_status,
                    ).success(
                        fn=lambda: gr.Markdown(visible=True),
                        outputs=pwd_status,
                    )

                # ============ 管理员功能 ============
                with gr.Tab("⚙️ 管理员功能", visible=False, id="admin_tab") as admin_tab:
                    gr.Markdown("## 用户管理")

                    with gr.Column(elem_classes="rs-table-wrap"):
                        users_table = gr.Dataframe(
                            headers=["用户ID", "用户名", "昵称", "状态", "注册时间"],
                            label="用户列表",
                            interactive=False,
                            value=[],
                        )

                    with gr.Row():
                        with gr.Column(scale=1):
                            selected_user_id = gr.Number(
                                label="选择用户 ID",
                                precision=0,
                                minimum=1,
                                value=2,
                            )
                        with gr.Column(scale=1):
                            user_actions = gr.Radio(
                                choices=[
                                    ("✅ 启用用户", "enable"),
                                    ("🛑 禁用用户", "disable"),
                                    ("❌ 删除用户", "delete"),
                                ],
                                label="选择操作",
                                type="value",
                            )
                        with gr.Column(scale=1):
                            execute_action_btn = gr.Button("执行操作", variant="secondary")
                            refresh_users_btn = gr.Button("🔄 刷新列表", size="sm")

                    operation_status = gr.Markdown(visible=False)

                    def update_users_list():
                        users = get_all_users()
                        if users:
                            return [[
                                user['id'], user['username'], user['name'],
                                user['status'], user['created_at'],
                            ] for user in users]
                        return []

                    def handle_user_action(user_id, action):
                        if not user_id:
                            return '<div class="rs-alert rs-alert-warning">请选择用户 ID</div>', None
                        try:
                            action_map = {
                                "disable": (update_user_status, (user_id, False)),
                                "enable": (update_user_status, (user_id, True)),
                                "delete": (delete_user, (user_id,)),
                            }
                            if action in action_map:
                                func, args = action_map[action]
                                result = func(*args)
                                if result:
                                    return (
                                        f'<div class="rs-alert rs-alert-success">操作成功：{action}</div>',
                                        update_users_list(),
                                    )
                                return '<div class="rs-alert rs-alert-error">操作失败</div>', None
                            return '<div class="rs-alert rs-alert-warning">无效的操作类型</div>', None
                        except Exception as e:
                            return f'<div class="rs-alert rs-alert-error">操作出错：{str(e)}</div>', None

                    execute_action_btn.click(
                        handle_user_action,
                        inputs=[selected_user_id, user_actions],
                        outputs=[operation_status, users_table],
                    )
                    refresh_users_btn.click(update_users_list, outputs=users_table)

            # 页脚
            gr.HTML('<div class="rs-footer">心灵伙伴 © 2025 · AI 心理健康助手 · 您的情绪值得被温柔对待</div>')

        # ==================== 事件处理 ====================
        def login(username, password):
            user_data = user_login(username, password)
            if not user_data:
                return '<div class="rs-alert rs-alert-error">用户名或密码错误</div>', None
            if user_data.get("error"):
                return f'<div class="rs-alert rs-alert-error">{user_data["error"]}</div>', None
            user = get_user_info_by_username(username)
            return "登录成功", user

        def get_login_status_msg(status, user):
            """管理员默认密码检测"""
            if user and user.get('is_admin'):
                admin_config = get_base_config("admin")
                if admin_config and check_default_admin_password(user['id'], admin_config['password']):
                    return (
                        '<div class="rs-security-warning">'
                        '⚠️ <strong>安全警告</strong>：您正在使用默认管理员密码，请立即修改！'
                        '</div>'
                    )
            return ""

        def update_nav_user(user):
            """更新导航栏用户名显示"""
            if user and user.get('name'):
                badge = ' (管理员)' if user.get('is_admin') else ''
                return f"<span class='rs-navbar-title'>心灵伙伴</span>" \
                       f"<span class='rs-navbar-subtitle'>AI 心理健康助手</span>" \
                       f"</div><div class='rs-navbar-user'>{user['name']}{badge}</div>" \
                       f"<div>"
            return "<span class='rs-navbar-title'>心灵伙伴</span>" \
                   "<span class='rs-navbar-subtitle'>AI 心理健康助手</span>" \
                   "</div><div class='rs-navbar-user'>未登录</div><div>"

        login_event = lambda method: method(
            login,
            inputs=[login_username, login_password],
            outputs=[login_status, current_user],
        ).success(
            fn=get_login_status_msg,
            inputs=[login_status, current_user],
            outputs=security_warning,
        ).success(
            lambda s, u: (gr.Column(visible=u is None), gr.Column(visible=u is not None)),
            inputs=[login_status, current_user],
            outputs=[auth_panel, main_panel],
        ).success(
            lambda user: gr.Tab(visible=user and user.get('is_admin', False)),
            inputs=[current_user],
            outputs=admin_tab,
        ).success(
            update_user_info,
            inputs=current_user,
            outputs=[user_info, nick_info, reg_date_info],
        ).success(
            fn=update_diary,
            inputs=[current_user, diary_page],
            outputs=[diary_list, diary_page_info, diary_page],
        ).success(
            fn=lambda user: update_users_list() if user and user.get('is_admin') else None,
            inputs=[current_user],
            outputs=users_table,
        )

        # 绑定登录事件
        login_event(login_btn.click)
        login_event(login_password.submit)

        # 注册
        def register(username, name_nick, password):
            result = user_register(username, name_nick, password)
            if result and 'id' in result:
                return '<div class="rs-alert rs-alert-success">✅ 注册成功</div>', result
            return '<div class="rs-alert rs-alert-error">注册失败，用户名已存在</div>', None

        register_btn.click(
            register,
            inputs=[register_username, register_name_nick, register_password],
            outputs=[register_status, current_user],
        ).success(
            lambda s, u: (gr.Column(visible=u is None), gr.Column(visible=u is not None)),
            inputs=[register_status, current_user],
            outputs=[auth_panel, main_panel],
        ).success(
            update_user_info,
            inputs=current_user,
            outputs=[user_info, nick_info, reg_date_info],
        )

        # 主对话
        welcome_message = "你好！我是你的心灵伙伴，很高兴能和你交流。请告诉我你最近的感受或者有什么想聊的？"

        input_text.submit(
            fn=process_user_input,
            inputs=[current_user, input_text, chatbot],
            outputs=[chatbot, emotion_chart],
        ).then(
            fn=lambda: "",
            inputs=None,
            outputs=input_text,
        ).then(
            fn=update_diary,
            inputs=[current_user, diary_page],
            outputs=[diary_list, diary_page_info, diary_page],
        )

        _interface.load(
            fn=lambda: [{"role": "assistant", "content": welcome_message}],
            outputs=chatbot,
        )

    return _interface


interface = create_gradio_interface()
bootstrap()
interface.launch()