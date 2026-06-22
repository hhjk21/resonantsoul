#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: user_service.py
@time: 2025/7/22 17:00
@project: resonant-soul
@desc: 用户服务
"""
import hashlib
import re
from datetime import datetime

import bcrypt

from api.db.db_models import User

# bcrypt 哈希前缀，用于区分新旧密码格式
BCRYPT_PREFIX = "$2b$"


class UserService:
    @staticmethod
    def _hash_password(password: str) -> str:
        """使用 bcrypt 哈希密码"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def _verify_bcrypt(password: str, hashed: str) -> bool:
        """验证 bcrypt 密码"""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    @staticmethod
    def _verify_sha256(password: str, hashed: str) -> bool:
        """验证旧版 SHA-256 密码（兼容存量数据）"""
        return hashed == hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def _is_sha256_hash(hashed: str) -> bool:
        """判断是否为旧版 SHA-256 哈希（64位十六进制）"""
        return bool(re.fullmatch(r'[a-f0-9]{64}', hashed))

    @staticmethod
    def get_by_username(username):
        try:
            return User.get(User.username == username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def verify_password(user, password):
        """验证密码，自动将旧 SHA-256 哈希升级为 bcrypt"""
        if UserService._is_sha256_hash(user.password):
            if UserService._verify_sha256(password, user.password):
                # 自动升级为 bcrypt
                user.password = UserService._hash_password(password)
                user.updated_at = datetime.now()
                user.save()
                return True
            return False
        return UserService._verify_bcrypt(password, user.password)

    @staticmethod
    def check_user_status(user):
        """检查用户状态"""
        message = "正常"
        status_ok = True
        if not user.status:
            message = "账号已被禁用，请联系管理员"
            status_ok = False
        return status_ok, message

    @staticmethod
    def register(username, name_nick, password, is_admin=False):
        if UserService.get_by_username(username):
            return None

        # 使用 bcrypt 哈希
        password_hash = UserService._hash_password(password)
        current_time = datetime.now()

        user = User.create(
            username=username,
            password=password_hash,
            name_nick=name_nick,
            is_admin=is_admin,
            status=True,
            created_at=current_time,
            updated_at=current_time
        )
        return user

    @staticmethod
    def register_admin(username, name_nick, password):
        return UserService.register(username, name_nick, password, is_admin=True)

    @staticmethod
    def get_all_users():
        return User.select()

    @staticmethod
    def update_status(user_id, status):
        try:
            user = User.get_by_id(user_id)
            if user.is_admin and not status:
                return False
            user.status = status
            user.updated_at = datetime.now()
            user.save()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.get_by_id(user_id)
            if user.is_admin:
                return False
            user.delete_instance()
            return True
        except User.DoesNotExist:
            return False

    @classmethod
    def update_password(cls, user_id, new_password):
        user = User.get_by_id(user_id)
        user.password = cls._hash_password(new_password)
        user.updated_at = datetime.now()
        user.save()
        return True

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return User.get_by_id(user_id)
        except User.DoesNotExist:
            return None

    @classmethod
    def is_default_admin_password(cls, user_id, default_password):
        """检查管理员是否仍在使用默认密码"""
        user = cls.get_by_id(user_id)
        if not user or not user.is_admin:
            return False
        # 兼容旧 SHA-256 和新 bcrypt 两种格式
        if cls._is_sha256_hash(user.password):
            return cls._verify_sha256(default_password, user.password)
        return cls._verify_bcrypt(default_password, user.password)
