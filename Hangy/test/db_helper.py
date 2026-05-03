from Hangy import db, app
from Hangy.models import User, UserVoucher, Voucher, Order


def get_user_by_username(username):
    data = User.query.filter_by(username=username).first()
    return data

def get_user_by_email(email):
    data = User.query.filter_by(email=email).first()
    return data

def delete_user_by_email(email):
    data = User.query.filter_by(email=email).first()
    db.session.delete(data)
    db.session.commit()


def delete_user_by_username(username):
    data = User.query.filter_by(username=username).first()
    db.session.delete(data)
    db.session.commit()

def get_voucher_by_id(user_id):
    result = (db.session.query(Voucher.code)
            .join(UserVoucher, UserVoucher.voucher_id == Voucher.id)
            .filter(
                UserVoucher.user_id == user_id,
                UserVoucher.is_used==0,
                UserVoucher.is_active==1
            ).all()
    )

    data = [r.code for r in result]

    return data

def get_order_by_id(user_id):
    result = db.session.query(Order.created_date).filter(Order.user_id == user_id).all()

    data = [str(r.created_date) for r in result]

    return data

with app.app_context():
    print(get_order_by_id(2))