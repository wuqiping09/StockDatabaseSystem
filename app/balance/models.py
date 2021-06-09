from app import db

class StockOwn(db.Model):
    __tablename__ = "stockown"
    user_id = db.Column(db.String(7),primary_key=True,unique=True,nullable=False,index=True)
    company_id = db.Column(db.String(6),nullable=False)
    amount = db.Column(db.Integer)
