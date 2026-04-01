import hashlib
from sqlite3 import IntegrityError

from Hangy import db
from Hangy.models import User, Profile


def get_user_by_id(user_id):
    return User.query.get(user_id)

def auth_user(username, password):
    return User.query.filter_by(username=username).first()

def add_user(email, first_name,last_name, phone, address, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    name = f"{last_name} {first_name}".strip()
    if not avatar:
        avatar = f"https://ui-avatars.com/api/?name={name}&background=0D8ABC&color=fff&size=128"

    try:

        u = User(username=username,password=password)
        db.session.add(u)
        db.session.flush()

        user_profile = Profile(email=email, first_name=first_name, last_name=last_name,
                    phone=phone, address=address,
                    avatar=avatar,user_id=u.id)

        db.session.add(user_profile)

        db.session.commit()


        return True
    except IntegrityError as ex:
        db.session.rollback()
        print(f"Lỗi Integrity: {ex}")
        return False
    except Exception as ex:
        db.session.rollback()
        print(f"Lỗi chung: {ex}")
        return False