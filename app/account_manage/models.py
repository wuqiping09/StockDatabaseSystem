
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

#普通用户
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'useexisting': True}
    user_id = db.Column(db.String(7), primary_key=True,unique=True, nullable=False, index = True)
    user_name = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    identification='User'
    avater=db.Column(db.String(256),nullable=True)

    def __repr__(self):
        return '<user_id:{} user_name:{} password:{} email:{}>'.format(self.user_id, self.user_name, self.password, self.email)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

    def get_name(self):
        return str(self.user_name)

    def get_identification_chinese(self):
        return '普通用户'

    def set_password(self, password_ori):
        self.password = generate_password_hash(password_ori, method='pbkdf2:md5')

    def check_password(self, password_check):
        return check_password_hash(self.password, password_check)

#管理员
class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    __table_args__ = {'useexisting': True}
    admin_id = db.Column(db.String(5), primary_key=True,unique=True, nullable=False, index = True)
    admin_name = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    identification='Admin'
    avater=db.Column(db.String(256),nullable=True)

    def __repr__(self):
        return '<admin_id:{} admin_name:{} password:{}>'.format(self.admin_id, self.admin_name, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.admin_id)

    def get_name(self):
        return str(self.admin_name)

    def get_identification_chinese(self):
        return '管理员'

    def set_password(self, password_ori):
        self.password = generate_password_hash(password_ori, method='pbkdf2:md5')

    def check_password(self, password_check):
        return check_password_hash(self.password, password_check)
