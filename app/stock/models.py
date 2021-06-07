from app import db

class Company(db.Model):
    __tablename__ = "company"
    company_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement = True, index = True)
    company_name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
