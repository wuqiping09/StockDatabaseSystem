from datetime import datetime
from .models import Transaction
from .forms import BuyForm,SellForm
from app.transaction import transaction_bp
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required
from app import app, db, login
from app.stock.models import Company
from app.account_manage.models import User, Admin
from app.balance.models import StockOwn
from sqlalchemy import and_, text
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_paginate import Pagination, get_page_parameter



def Fetch_Pagination_MsgList(curPage, perPage, msgList):
    # curPage = request.args.get(get_page_parameter(), type=int, default=1)
    # perPage = 15
    msgList_inCurPage = msgList[(curPage - 1) * perPage : curPage * perPage]
    pagination = Pagination(
        page = curPage,
        per_page = perPage,
        total = len(msgList),
        bs_version=4
    )
    return msgList_inCurPage, pagination

#获取当前用户信息
def getCurrentUserInfo(current_user):
    #当前用户已登录
    if current_user.is_authenticated:
        #管理员
        if current_user.identification == 'Admin':
            user_identity = 0
            user_id = current_user.admin_id
            user_name = current_user.admin_name
        #普通用户
        else:
            user_identity = 1
            user_id = current_user.user_id
            user_name = current_user.user_name
    #返回用户身份、用户ID、用户名
    return user_identity, user_id, user_name

#设置分页
def setPaginate(page_num, per_page_num):
    page = int(request.args.get('page', page_num))              #当前页
    per_page = int(request.args.get('per_page', per_page_num))  #每页条数
    return page, per_page

#交易列表
@transaction_bp.route('/alltransactions/', methods=['GET', 'POST'])
@login_required
def allTransactions():
    user_identity, user_id, user_name=getCurrentUserInfo(current_user)
    #普通用户只能看见自己的交易记录
    if user_identity==1:
        transactions = Transaction.query.filter(Transaction.user_id==user_id)
    #管理员可以看见所有交易记录
    else:
        transactions = Transaction.query.all()
    #加上公司名称
    transactions_with_companyname = []
    for transaction in transactions:
        new_transaction = {}
        new_transaction['company_id'] = transaction.company_id
        company = Company.query.filter(Company.company_id == transaction.company_id).first()
        new_transaction['company_name'] = company.company_name
        #管理员可查看用户ID和用户名
        if user_identity==0:
            new_transaction['user_id']=transaction.user_id
            user = User.query.filter(User.user_id == transaction.user_id).first()
            new_transaction['user_name']=user.user_name
        new_transaction['price'] = transaction.price
        new_transaction['amount']=transaction.amount
        new_transaction['total']=transaction.total
        if transaction.buy:
            new_transaction['buy_or_sell']='买入'
        else:
            new_transaction['buy_or_sell']='卖出'
        transactions_with_companyname.append(new_transaction)
    transaction_list, pagination = Fetch_Pagination_MsgList(
        curPage = request.args.get(get_page_parameter(), type=int, default=1),
        perPage = 15,
        msgList = transactions_with_companyname
    )
    return render_template(
        'transactions.html',
        title = '交易列表',
        transaction_list = transaction_list,
        pagination = pagination
        )

#买入
@transaction_bp.route('/buy/', methods=['GET', 'POST'])
@login_required
def buy():
    form = BuyForm()
    #获取当前用户信息：身份、ID、用户名
    user_identity, user_id, user_name = getCurrentUserInfo(current_user)
    #提交表单
    if form.validate_on_submit():
        #点击买入
        if form.submit.data:
            #错误信息提示
            error_message = '操作失败！'
            company_id_error = '股票代码错误'
            amount_error='买入股数错误'
            balance_error='余额不足'
            company = Company.query.filter(Company.company_id == form.company_id.data).first()
            #股票代码合法
            if company:
                amount = form.amount.data
                #获取股票价格
                price=company.price
                #transaction_id = None
                #获取用户的余额
                balance=current_user.balance
                #股数错误
                if amount is not None and amount<=0:
                    error_message+=amount_error
                    flash(error_message)
                #余额不足
                elif balance<price*amount:
                    error_message+=balance_error
                    flash(error_message)
                else:
                    flash('交易成功')
                    timestamp = datetime.now()
                    transaction = Transaction(
                        company_id = company.company_id,
                        user_id=user_id,
                        buy=True,
                        price=price,
                        amount=amount,
                        total=price*amount,
                        timestamp = timestamp
                        )
                    db.session.add(transaction)
                    db.session.flush()
                    db.session.commit()
                    #更新用户余额
                    user=User.query.filter(User.user_id==user_id).first()
                    user.balance-=price*amount
                    db.session.commit()
                    #更新用户股权
                    stock_own=StockOwn.query.filter(StockOwn.user_id==user_id and StockOwn.company_id==company.company_id).first()
                    #已拥有此公司股权
                    if stock_own:
                        stock_own.amount+=amount
                    #未拥有此公司股权
                    else:
                        stock_own=StockOwn(
                            user_id=user_id,
                            company_id=company.company_id,
                            amount=amount
                        )
                        db.session.add(stock_own)
                    db.session.commit()
                    #跳转到交易列表
                    return redirect(url_for('transaction.allTransactions'))
            #股票代码错误
            else:
                error_message += company_id_error
                flash(error_message)
        #点击取消
        else:
            flash('交易已取消')
            #返回交易列表页
            return redirect(url_for('transaction.allTransactions'))
    return render_template("buy.html",
                           title = '买入股票',
                           form = form
                           )

#卖出
@transaction_bp.route('/sell/', methods=['GET', 'POST'])
@login_required
def sell():
    form = SellForm()
    #获取当前用户信息：身份、ID、用户名
    user_identity, user_id, user_name = getCurrentUserInfo(current_user)
    #提交表单
    if form.validate_on_submit():
        #点击卖出
        if form.submit.data:
            #错误信息提示
            error_message = '操作失败！'
            company_id_error = '股票代码错误'
            amount_error='卖出股数错误'
            balance_error='卖出股数大于拥有的股权数'
            company = Company.query.filter(Company.company_id == form.company_id.data).first()
            #股票代码合法
            if company:
                amount = form.amount.data
                #获取股票价格
                price=company.price
                #transaction_id = None
                #获取用户拥有的股权数
                stock_own=StockOwn.query.filter(StockOwn.user_id==user_id).first()
                #股数错误
                if amount is not None and amount<=0:
                    error_message+=amount_error
                    flash(error_message)
                #股权不足
                elif stock_own.amount<amount:
                    error_message+=balance_error
                    flash(error_message)
                else:
                    flash('交易成功')
                    timestamp = datetime.now()
                    transaction = Transaction(
                        company_id = company.company_id,
                        user_id=user_id,
                        buy=False,
                        price=price,
                        amount=amount,
                        total=price*amount,
                        timestamp = timestamp
                        )
                    db.session.add(transaction)
                    db.session.flush()
                    db.session.commit()
                    #更新用户余额
                    user=User.query.filter(User.user_id==user_id).first()
                    user.balance+=price*amount
                    db.session.commit()
                    #更新用户股权
                    stock_own=StockOwn.query.filter(StockOwn.user_id==user_id and StockOwn.company_id==company.company_id).first()
                    stock_own.amount-=amount
                    #股权为0则删除
                    if stock_own.amount==0:
                        db.session.delete(stock_own)
                    db.session.commit()
                    #跳转到交易列表
                    return redirect(url_for('transaction.allTransactions'))
            #股票代码错误
            else:
                error_message += company_id_error
                flash(error_message)
        #点击取消
        else:
            flash('交易已取消')
            #返回交易列表页
            return redirect(url_for('transaction.allTransactions'))
    return render_template("sell.html",
                           title = '卖出股票',
                           form = form
                           )
