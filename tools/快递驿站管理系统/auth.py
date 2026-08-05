"""
用户认证模块 - 管理登录账户
"""
import os
from typing import Optional, Tuple
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"          # 库存管理员
    RECIPIENT = "recipient"  # 取件人


class User:
    """用户账户类"""

    def __init__(self, username: str, password: str, role: UserRole, display_name: str = ""):
        self.username = username
        self.password = password
        self.role = role
        self.display_name = display_name if display_name else username


class AuthManager:
    """认证管理器"""

    def __init__(self, file_path: str = "users.txt"):
        self.file_path = file_path
        self.users: list[User] = []
        self._init_default_users()
        self._load_from_file()

    def _init_default_users(self):
        """初始化默认账户"""
        self.users = [
            User("admin", "admin123", UserRole.ADMIN, "库存管理员"),
        ]

    def _load_from_file(self):
        """从文件加载用户"""
        if not os.path.exists(self.file_path):
            self._save_to_file()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                loaded_users = []
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) >= 4:
                        username, password, role_str, display_name = parts[:4]
                        try:
                            role = UserRole(role_str)
                            loaded_users.append(User(username, password, role, display_name))
                        except ValueError:
                            continue
                if loaded_users:
                    self.users = loaded_users
        except IOError:
            pass

    def _save_to_file(self):
        """保存用户到文件"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                for user in self.users:
                    f.write(f"{user.username},{user.password},{user.role.value},{user.display_name}\n")
        except IOError:
            pass

    def login(self, username: str, password: str) -> Optional[User]:
        """用户登录验证"""
        username = username.strip()
        password = password.strip()
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def register_recipient(self, username: str, password: str, display_name: str = "") -> bool:
        """注册取件人账户"""
        username = username.strip()
        if not username or not password:
            return False

        # 检查是否已存在
        for user in self.users:
            if user.username == username:
                return False

        new_user = User(username, password, UserRole.RECIPIENT, display_name or username)
        self.users.append(new_user)
        self._save_to_file()
        return True

    def is_admin(self, user: Optional[User]) -> bool:
        """判断是否为管理员"""
        return user is not None and user.role == UserRole.ADMIN

    def is_recipient(self, user: Optional[User]) -> bool:
        """判断是否为取件人"""
        return user is not None and user.role == UserRole.RECIPIENT