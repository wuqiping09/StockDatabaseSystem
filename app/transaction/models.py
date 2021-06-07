from app import db

class Transaction(db.Model):
    __tablename__="transaction"
    __table_args__={"useexisting":True}
    transaction_id=db.Column(db.Integer,autoincrement=True,primary_key=True,unique=True,nullable=True)
    company_id=db.Column(db.Integer)
    user_id=db.Column(db.Integer)
    buy=db.Column(db.Boolean)
    price=db.Column(db.Integer)
    amount=db.Column(db.Integer)
    total=db.Column(db.Integer)
    timestamp=db.Column(db.DateTime)
