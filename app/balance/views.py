from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from datetime import datetime
from .models import *
from .forms import *
from app.stock.models import Company
from app.account_manage.models import User,Admin
from app.balance import balance_bp



#股权列表
@balance_bp.route('/allstockown')
@login_required
def allStockOwn():
    page = int(request.args.get('page', 1))             #当前页
    per_page = int(request.args.get('per_page', 5))     #每页条数
    paginate2 = StockOwn.query.filter(StockOwn.user_id==current_user.user_id).order_by(StockOwn.company_id.asc()).paginate(page, per_page, error_out = False)
    stock_own_list = paginate2.items
    #加上公司名称和股价
    stockown_with_info = []
    for stockown in stock_own_list:
        new_stockown = {}
        new_stockown['company_id'] = stockown.company_id
        company = Company.query.filter(Company.company_id == stockown.company_id).first()
        new_stockown['company_name'] = company.company_name
        new_stockown['price'] = company.price
        new_stockown['amount']=stockown.amount
        stockown_with_info.append(new_stockown)
    return render_template("allstockown.html",
                           title='股权列表',
                           stock_own_list = stockown_with_info,
                           pagination = paginate2)

#充值
@balance_bp.route('/charge', methods = ['GET','POST'])
@login_required
def charge():
    form = ChargeForm()
    if form.validate_on_submit():
        #点击充值
        if form.submit.data:
            amount = form.amount.data
            if amount<=0:
                flash('金额错误')
            else:
                user=User.query.filter(User.user_id==current_user.user_id).first()
                user.balance+=amount
                #db.session.add(notice)
                #获取自增的Post_ID
                #db.session.flush()
                #notice_id = notice.Notice_ID
                db.session.commit()
                flash('充值成功')
                #跳转到账户页面
                return redirect(url_for('account.myinfo',info_action='checkdetail'))
        #点击取消
        else:
            flash('充值已取消')
            #跳转到账户页面
            return redirect(url_for('account.myinfo',info_action='checkdetail'))
    return render_template("charge.html",
                           title='充值',
                           form = form)
