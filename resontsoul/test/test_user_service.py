#!/usr/bin/env python
# encoding: utf-8
"""
@author: hhjk
@file: test_user_service.py
@time: 2025/7/23
@project: resonant-soul
@desc: 用户服务单元测试
"""
import hashlib
import os
import tempfile

import bcrypt
import pytest

from api.db.db_models import User, BaseModel, db_proxy
from api.db.services.user_service import UserService


@pytest.fixture
def test_db():
    """创建临时测试数据库"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    from peewee import SqliteDatabase
    db = SqliteDatabase(path)
    db_proxy.initialize(db)
    with db:
        db.create_tables([User], safe=True)
    yield
    db.close()
    os.unlink(path)


@pytest.fixture
def clean_db(test_db):
    """每个测试前清空数据"""
    User.delete().execute()
    yield
    User.delete().execute()


class TestPasswordHashing:
    """密码哈希测试"""

    def test_hash_produces_bcrypt_format(self):
        """密码哈希应生成 bcrypt 格式"""
        hashed = UserService._hash_password("test123")
        assert hashed.startswith("$2b$")
        assert len(hashed) == 60  # bcrypt 哈希长度

    def test_hash_is_different_each_time(self):
        """每次哈希应产生不同结果(salt 随机)"""
        h1 = UserService._hash_password("test123")
        h2 = UserService._hash_password("test123")
        assert h1 != h2

    def test_bcrypt_verify_correct(self):
        """bcrypt 验证正确密码"""
        hashed = bcrypt.hashpw("test123".encode(), bcrypt.gensalt()).decode()
        assert UserService._verify_bcrypt("test123", hashed)

    def test_bcrypt_verify_wrong(self):
        """bcrypt 验证错误密码"""
        hashed = bcrypt.hashpw("test123".encode(), bcrypt.gensalt()).decode()
        assert not UserService._verify_bcrypt("wrong", hashed)

    def test_sha256_verify_correct(self):
        """SHA-256 验证正确密码"""
        hashed = hashlib.sha256("test123".encode()).hexdigest()
        assert UserService._verify_sha256("test123", hashed)

    def test_sha256_verify_wrong(self):
        """SHA-256 验证错误密码"""
        hashed = hashlib.sha256("test123".encode()).hexdigest()
        assert not UserService._verify_sha256("wrong", hashed)

    def test_is_sha256_hash_positive(self):
        """正确的 SHA-256 哈希识别"""
        sha = hashlib.sha256("test".encode()).hexdigest()
        assert UserService._is_sha256_hash(sha)

    def test_is_sha256_hash_negative(self):
        """bcrypt 哈希不应被识别为 SHA-256"""
        bcrypt_hash = bcrypt.hashpw("test".encode(), bcrypt.gensalt()).decode()
        assert not UserService._is_sha256_hash(bcrypt_hash)


class TestUserRegistration:
    """用户注册测试"""

    def test_register_new_user(self, clean_db):
        """注册新用户应使用 bcrypt 哈希"""
        user = UserService.register("testuser", "测试用户", "password123")
        assert user is not None
        assert user.username == "testuser"
        assert user.password.startswith("$2b$")  # 新用户使用 bcrypt

    def test_register_duplicate_username(self, clean_db):
        """重复用户名注册应返回 None"""
        UserService.register("testuser", "用户1", "pass1")
        result = UserService.register("testuser", "用户2", "pass2")
        assert result is None

    def test_register_admin(self, clean_db):
        """注册管理员"""
        user = UserService.register_admin("admin", "管理员", "admin123")
        assert user.is_admin is True


class TestPasswordVerification:
    """密码验证测试"""

    def test_verify_bcrypt_password(self, clean_db):
        """验证 bcrypt 密码"""
        user = UserService.register("user1", "用户", "mypassword")
        assert UserService.verify_password(user, "mypassword")

    def test_verify_wrong_password(self, clean_db):
        """验证错误密码"""
        user = UserService.register("user1", "用户", "mypassword")
        assert not UserService.verify_password(user, "wrongpassword")

    def test_auto_upgrade_sha256_to_bcrypt(self, clean_db):
        """旧 SHA-256 密码自动升级为 bcrypt"""
        # 模拟旧用户（SHA-256 密码）
        sha_hash = hashlib.sha256("oldpassword".encode()).hexdigest()
        from datetime import datetime
        user = User.create(
            username="olduser",
            password=sha_hash,
            name_nick="老用户",
            is_admin=False,
            status=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # 验证旧密码
        assert UserService.verify_password(user, "oldpassword")
        # 重新获取用户，密码应已升级为 bcrypt
        user = UserService.get_by_username("olduser")
        assert user.password.startswith("$2b$")


class TestPasswordUpdate:
    """密码更新测试"""

    def test_update_password(self, clean_db):
        """更新密码"""
        user = UserService.register("user1", "用户", "oldpass")
        UserService.update_password(user.id, "newpass")
        user = UserService.get_by_id(user.id)
        assert UserService.verify_password(user, "newpass")
        assert not UserService.verify_password(user, "oldpass")

    def test_update_password_uses_bcrypt(self, clean_db):
        """更新后的密码应使用 bcrypt"""
        user = UserService.register("user1", "用户", "oldpass")
        UserService.update_password(user.id, "newpass")
        user = UserService.get_by_id(user.id)
        assert user.password.startswith("$2b$")


class TestDefaultPasswordCheck:
    """默认密码检测测试"""

    def test_admin_default_password(self, clean_db):
        """管理员使用默认密码应被检测到"""
        admin = UserService.register_admin("admin", "管理员", "admin@123")
        assert UserService.is_default_admin_password(admin.id, "admin@123")

    def test_admin_changed_password(self, clean_db):
        """管理员修改密码后不应被检测到"""
        admin = UserService.register_admin("admin", "管理员", "admin@123")
        UserService.update_password(admin.id, "new_secure_password")
        assert not UserService.is_default_admin_password(admin.id, "admin@123")

    def test_normal_user_not_checked(self, clean_db):
        """普通用户不应被检测"""
        user = UserService.register("user1", "用户", "admin@123")
        assert not UserService.is_default_admin_password(user.id, "admin@123")


class TestUserStatus:
    """用户状态管理测试"""

    def test_disable_user(self, clean_db):
        """禁用用户"""
        user = UserService.register("user1", "用户", "pass")
        assert UserService.update_status(user.id, False)
        user = UserService.get_by_id(user.id)
        assert user.status is False

    def test_cannot_disable_admin(self, clean_db):
        """不能禁用管理员"""
        admin = UserService.register_admin("admin", "管理员", "pass")
        assert not UserService.update_status(admin.id, False)

    def test_cannot_delete_admin(self, clean_db):
        """不能删除管理员"""
        admin = UserService.register_admin("admin", "管理员", "pass")
        assert not UserService.delete_user(admin.id)

    def test_delete_normal_user(self, clean_db):
        """删除普通用户"""
        user = UserService.register("user1", "用户", "pass")
        assert UserService.delete_user(user.id)
        assert UserService.get_by_id(user.id) is None