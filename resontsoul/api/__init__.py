#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: __init__.py
@time: 2025/7/21 14:27
@project: resonant-soul
@desc: 延迟初始化，避免测试导入时触发全量加载
"""

_inited = False


def bootstrap():
    """应用启动初始化（仅在 app.py 中调用）"""
    global _inited
    if _inited:
        return
    _inited = True

    import logging
    from api.utils.log_utils import initRootLogger
    initRootLogger("resonant-soul")

    logging.info(r"""
______                                  _     _____             _ 
| ___ \                                | |   /  ___|           | |
| |_/ /___  ___  ___  _ __   __ _ _ __ | |_  \ `--.  ___  _   _| |
|    // _ \/ __|/ _ \| '_ \ / _` | '_ \| __|  `--. \/ _ \| | | | |
| |\ \  __/\__ \ (_) | | | | (_| | | | | |_  /\__/ / (_) | |_| | |
\_| \_\___||___/\___/|_| |_|\__,_|_| |_|\__| \____/ \___/ \__,_|_|
                                                                  
""")

    from api.utils import file_utils
    logging.info(
        f'project base: {file_utils.get_project_base_directory()}'
    )

    from api.utils import show_configs
    show_configs()

    from api import settings
    settings.init_settings()

    from api.db.init_data import init_web_data
    init_web_data()
