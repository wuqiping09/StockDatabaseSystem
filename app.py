from app import app
from app.account_manage import account_bp
from app.balance import balance_bp
from app.stock import stock_bp
from app.transaction import transaction_bp

app.register_blueprint(account_bp)
app.register_blueprint(balance_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(transaction_bp)

if __name__ == '__main__':
    app.run(debug=True)
