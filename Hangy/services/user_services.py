import hashlib
import re
from typing import Dict

from docutils.nodes import address

from Hangy import db
from Hangy.models import User
from sqlalchemy.exc import IntegrityError


class UserService:
    def _hash_pw(self, password: str) -> str:
        return hashlib.md5(password.strip().encode("utf-8")).hexdigest()

    def get_user_by_id(self, uid: int) -> User | None:
        if not uid or uid <= 0:
            return None
        return User.query.get(uid)
    def authenticate(self, username: str, password: str) -> User | None:
        if not username or not username.strip() or not password or not password.strip():
            return None

        pw_hashed = self._hash_pw(password)
        return User.query.filter_by(username=username, password=pw_hashed).first()

    def create_user(
        self,
        username: str,
        password: str,
        last_name: str,
        first_name: str,
        email: str,
        **kwargs,
    ) -> Dict[bool,str]:
        try:

            fields = [username, last_name, first_name]

            if any(f != f.strip() for f in fields):
                return [False, "UKhông được chứa khoảng trắng ở đầu hoặc cuối!"]

            if User.query.filter_by(username=username).first():
                return [False,"Username đã tồn tại!"]

            if User.query.filter_by(email=email).first():
                return [False,"Email đã được sử dụng!"]

            if re.match(r"^[a-zA-Z]+$", kwargs.get("phone")):
                return [False,'Số điện thoại chứa ký tự chữ hoặc đặt biệt!']

            if len(username) > 30 or len(password) > 255 or len(first_name) > 30 or len(last_name) > 30 or len(email) > 50 or len(kwargs.get("phone")) > 15 or len(kwargs.get('address')) > 255:
                return [False,'Nhập quá ký tự cho phép!']

            if username.__contains__("\s") or last_name.__contains__("\s") or first_name.__contains__("\s"):
                return [False,'Tồn tại khoảng trắng']

            full_name = f"{last_name} {first_name}".strip()
            username = username.strip()
            last_name = last_name.strip()

            avt = kwargs.get("avatar")

            if not avt:
                avt =  f"https://ui-avatars.com/api/?name={full_name}&background=0D8ABC&color=fff&size=128"

            new_user = User(
                username=username,
                password=self._hash_pw(password),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=kwargs.get("phone"),
                address=kwargs.get("address"),
                avatar=avt,
            )

            db.session.add(new_user)
            db.session.commit()
            return [True,"Tạo tài khoản thành công"]

        except Exception as e:
            db.session.rollback()
            print(f"Lỗi chung: {e}")
            return [False,"Hệ thống gặp lỗi"]


user_service = UserService()