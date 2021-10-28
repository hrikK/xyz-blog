from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)

class user(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(8), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    f_name = db.Column(db.String(18), unique=False, nullable=False)
    password = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False, default="default.png")
    post = db.relationship('blogpost', lazy=True, backref='post')

    def __repr__(self):
        return f"{self.username}-{self.id}"

class blogpost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text)
    author = db.Column(db.String(18))
    date = db.Column(db.DateTime)
    publish = db.Column(db.Boolean(), nullable=False, default=False)
    post_pic = db.Column(db.String(), nullable=False, default="defaul.png")
    post_owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.title[:3]}-{self.id}"