from migrate.versioning import api
from config import Config
from app import db
from app.account_manage.models import User,Admin
from app.stock.models import Company
from app.transaction.models import Transaction
from app.balance.models import StockOwn
import os.path

db.create_all()

# if not os.path.exists(Config.SQLALCHEMY_MIGRATE_REPO):
#     api.create(Config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
#     api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
# else:
#     api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, api.version(Config.SQLALCHEMY_MIGRATE_REPO))