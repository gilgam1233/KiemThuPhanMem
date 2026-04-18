import hashlib
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
    ) -> bool:
        try:
            if User.query.filter_by(username=username).first():
                raise ValueError("Username đã tồn tại!")

            if User.query.filter_by(email=email).first():
                raise ValueError("Email đã được sử dụng!")

            full_name = f"{last_name} {first_name}".strip()

            new_user = User(
                username=username,
                password=self._hash_pw(password),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=kwargs.get("phone"),
                address=kwargs.get("address"),
                avatar=kwargs.get(
                    "avatar",
                    f"https://ui-avatars.com/api/?name={full_name}&background=0D8ABC&color=fff&size=128",  # Trường avatar sẽ cần được bọc trong 1 phương thức đưa lên cloudinary rồi trả về link: str
                ),
            )

            db.session.add(new_user)
            db.session.commit()
            return True

        except IntegrityError as ex:
            db.session.rollback()
            print(f"Lỗi Integrity: {ex}")
            return False

        except Exception as e:
            db.session.rollback()
            print(f"Lỗi chung: {e}")
            return False


user_service = UserService()