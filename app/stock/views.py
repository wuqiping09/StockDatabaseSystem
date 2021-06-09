from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required
from app import app, db
from .forms import AddStockForm,ChangePriceForm
from .models import Company
from app.account_manage.models import User, Admin
from datetime import datetime
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_paginate import Pagination, get_page_parameter
from app.stock import stock_bp



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

#设置分页
def setPaginate(page_num, per_page_num):
    page = int(request.args.get('page', page_num))              #当前页
    per_page = int(request.args.get('per_page', per_page_num))  #每页条数
    return page, per_page

#股票列表
@stock_bp.route('/stock/companies')
@login_required
def stockCompanies():
    companies = Company.query.all()
    company_list, pagination = Fetch_Pagination_MsgList(
        curPage = request.args.get(get_page_parameter(), type=int, default=1),
        perPage = 15,
        msgList = companies
    )
    return render_template(
        "companies.html",
        title = '股票列表',
        company_list = company_list,
        pagination = pagination
    )

#添加股票
@stock_bp.route('/stock/addstock', methods=['GET', 'POST'])
@login_required
def addStock():
    #只有管理员能添加股票
    form = AddStockForm()
    if current_user.identification == 'Admin':
        # 验证CSRF令牌
        '''
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('oj.oj_problems'))
        '''
        if form.validate_on_submit():
            if form.price.data<=0:
                flash("股票价格错误")
            else:
                company = Company(
                    company_id=form.company_id.data,
                    company_name = form.company_name.data,
                    price=form.price.data
                )
                db.session.add(company)
                db.session.flush()
                db.session.commit()
                flash('股票添加成功')
                #跳转到股票列表
                return redirect(url_for('stock.stockCompanies'))
    #普通用户
    else:
        return redirect(url_for('stock.stockCompanies'))
    return render_template('add_stock.html',form = form)

#更新股票价格
@stock_bp.route('/stock/changeprice', methods=['GET', 'POST'])
@login_required
def changePrice():
    #只有管理员能更新股票价格
    form = ChangePriceForm()
    if current_user.identification == 'Admin':
        # 验证CSRF令牌
        '''
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('oj.oj_problems'))
        '''
        if form.validate_on_submit():
            company=Company.query.filter(Company.company_id==form.company_id.data).first()
            if company:
                if form.price.data<=0:
                    flash("股票价格错误")
                else:
                    company.price=form.price.data
                    db.session.commit()
                    flash('价格更新成功')
                    #跳转到股票列表
                    return redirect(url_for('stock.stockCompanies'))
            else:
                flash("股票代码错误")
    #普通用户
    else:
        return redirect(url_for('stock.stockCompanies'))
    return render_template('change_price.html',form = form)
