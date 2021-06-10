import os
import imghdr
from PIL import Image
from app import app,db,login
from flask import redirect,url_for,flash,render_template,request,session
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import and_
from .models import User,Admin
from .forms import *
from app.account_manage import account_bp
from .tools import *

@login.user_loader
def loadUser(u_id):
    #不同身份用户的id不相同，无需判断session
    if User.query.get(u_id):
        return User.query.get(u_id)
    else :
        return Admin.query.get(u_id)

#获取头像
def getAvater(identity, user_id):
    #普通用户
    if(identity == 1):
        avater = User.query.get(user_id).avater
    #管理员
    else:
        avater = Admin.query.get(user_id).avater
    return avater
#将该函数导入html
app.add_template_global(getAvater,"getAvater")

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

@account_bp.route('/', methods=['GET', 'POST'])
@account_bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html",
                           title='主页',
                           user=None)


@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 已登录
    if current_user.is_authenticated:
        return redirect(url_for('account.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # 数据判断
        flag=False
        if len(form.password2.data)<8 :
            flash("用户密码长度不能小于8")
            flag=True
        if len(form.password2.data)>16 :
            flash("用户密码长度不能超过16")
            flag=True
        if form.password2.data.isalpha() or form.password2.data.isdigit() :
            flash("用户密码应包含数字与字母")
            flag=True
        if hasSpace(form.user_id.data) :
            flash("用户ID不应包含空格")
            flag=True
        if flag == True :
            return render_template("register.html",title='注册',form=form)
        #判断user_id是否已存在，若已存在提示账号已注册
        if uniqueId(form.user_id.data,form.identification.data):
            #普通用户
            if(form.identification.data == 'User'):
                if len(form.user_id.data)!=7:
                    flash("普通用户ID长度应为7")
                    return render_template("register.html",title='注册',form=form)
                user=User(
                    phone=form.phone.data,
                    email=form.email.data,
                    user_name=form.user_name.data,
                    user_id=form.user_id.data,
                    balance=0
                    )
                user.set_password(form.password2.data)
            #管理员
            else:
                if len(form.user_id.data)!=5 :
                    flash("管理员ID长度应为5")
                    return render_template("register.html",title='注册',form=form)
                user=Admin(
                    phone=form.phone.data,
                    email=form.email.data,
                    admin_name=form.user_name.data,
                    admin_id=form.user_id.data
                    )
                user.set_password(form.password2.data)
            #默认头像
            default_avater='default_img.jpg'
            user.avater=default_avater
            db.session.add(user)
            db.session.commit()
            flash("注册成功!")
            return redirect(url_for('account.login'))
        else:
            flash("账号已注册!")
    else:
        if form.errors:
            for error in form.errors:
                if error=="user_id":
                    error_message="用户id应为5或7位纯数字"
                    flash(error_message)
    return render_template("register.html",title='注册',form=form)


@account_bp.route('/login',methods=['GET','POST'])
def login():
    # 已登录
    if current_user.is_authenticated:
        return redirect(url_for('account.index'))
    form = LoginForm()
    if request.method=='POST':
        # 根据identification检索数据库
        if form.identification.data == 'User':
            user = User.query.filter((User.user_id == form.user_id.data)).first()
        else:
            user = Admin.query.filter((Admin.admin_id == form.user_id.data)).first()
        #用户不存在
        if user is None:
            flash("用户不存在")
            return render_template('login.html',title='登录',form=form)
        flag=user.check_password(form.password.data)
        #判断输入的密码与账号密码是否相同    
        if flag:
            flash("成功登录！")
            login_user(user,form.remember_me.data)
            return redirect(url_for('account.index'))
        else:
            error = '用户名或密码错误'
            flash(error)
            return render_template('login.html',title='登录',form=form)
    return render_template('login.html',title='登录',form=form)


@account_bp.route('/logout')
@login_required
def logout():
    #flask_login提供的用户登出
    logout_user()
    return redirect(url_for('account.index'))


@account_bp.route('/myinfo/<info_action>', methods=['GET', 'POST'])
@login_required
def myinfo(info_action):
    #修改个人信息
    if info_action == 'editinfo':
        form_edit = MyInfoEditForm()
        form_passwordreset = AccountHasPasswordResetForm()
        if request.method == "POST":
            # 选择修改密码         
            if form_passwordreset.validate():
                new_password = form_passwordreset.password2.data
                # 取数据库内账户信息
                if current_user.identification == 'User':
                    user = User.query.filter(User.user_id == current_user.user_id).first()
                else:
                    user = Admin.query.filter(Admin.admin_id == current_user.admin_id).first()
                # 旧密码输入错误
                flag = user.check_password(form_passwordreset.password_old.data)     
                if not flag:
                    flash("旧密码输入错误")
                    return render_template(
                        "myinfo_edit.html",
                        title='我的信息',
                        user={
                            "identification": current_user.get_identification_chinese(),
                            "id": current_user.get_id(),
                            "name": current_user.get_name(),
                            "email": current_user.email,
                            "phone": current_user.phone
                        },
                        form_edit=form_edit,
                        form_passwordreset=form_passwordreset
                    )
                # 修改密码
                user.set_password(new_password)
                db.session.commit()
                flash("密码已修改")
                # 修改成功返回查看个人信息
                return redirect(url_for('account.myinfo', info_action='checkdetail'))
            else:
                if form_passwordreset.password_old.data and form_passwordreset.password1.data and form_passwordreset.password2.data:
                    if form_passwordreset.errors:
                        for error in form_passwordreset.errors:
                            if error=="password1":
                                error_message = "密码格式错误"
                                flash(error_message)
                            if error=="password2":
                                error_message = "两次新密码应一样"
                                flash(error_message)
            # 选择修改用户名和头像
            if not form_edit.validate_on_submit():
                # 新用户名非空则进行修改              
                # 用户未输入用户名，但form内实际存在内容
                new_username=form_edit.user_name.data
                no_input=r"''"                
                if repr(new_username)!=no_input:     
                    if current_user.identification == 'User':
                        user = User.query.filter(User.user_id == current_user.user_id).first()
                        user.user_name=new_username
                        #user_identity = 1
                        #user_id = current_user.user_id
                    else:
                        user = Admin.query.filter(Admin.admin_id == current_user.admin_id).first()
                        user.admin_nmae=new_username
                        #user_identity = 2
                        #user_id = current_user.admin_id
                    #修改post中的username
                    #posts = Post.query.filter(Post.UserIdentity == user_identity, Post.User_ID == user_id)
                    #for post in posts:
                    #    post.UserName = new_username
                    #修改comment中的username
                    #comments = Comment.query.filter(Comment.UserIdentity == user_identity, Comment.User_ID == user_id)
                    #for comment in comments:
                    #    comment.UserName = new_username 
                    db.session.commit()
                    flash("用户名修改成功")

                # 新头像非空则进行修改
                if repr(request.files['profile_photo'].filename)!=no_input:
                    new_profilephoto=request.files['profile_photo']
                    valid_filetype=imghdr.what(new_profilephoto)
                    fname=new_profilephoto.filename                
                    ftype=fname.split('.')[1]     
                    if valid_filetype:                   
                        if current_user.identification == 'User':
                            user_ID=current_user.user_id
                            user = User.query.filter(User.user_id == current_user.user_id).first()
                        else:
                            user_ID=current_user.admin_id
                            user = Admin.query.filter(Admin.admin_id == current_user.admin_id).first()
                        size = (128, 128)
                        im=Image.open(new_profilephoto)
                        im.thumbnail(size)
                        #basedir=...\shenjianjiaoxueguanlixitong\app
                        basedir = os.path.join(os.path.dirname(__file__) , "..")     
                        filename=user_ID+'.'+ftype
                        upload_path=os.path.join(basedir,'static/user/Avater',filename)
                        #upload_path=os.path.join(basedir)
                        im.save(upload_path)
                        user.avater=filename
                        db.session.commit()
                        flash("头像修改成功")
                    else :
                        flash("头像修改失败")
                    return redirect(url_for('account.myinfo', info_action='checkdetail'))
        return render_template(
            "myinfo_edit.html",
            title='我的信息',
            user={
                "identification": current_user.get_identification_chinese(),
                "id": current_user.get_id(),
                "name": current_user.get_name(),
                "email": current_user.email,
                "phone": current_user.phone
            },
            form_edit=form_edit,
            form_passwordreset=form_passwordreset
        )
    #查看个人信息
    elif info_action == 'checkdetail':
        user_identity,user_id,user_name=getCurrentUserInfo(current_user)
        user={
                "identification": current_user.get_identification_chinese(),
                "id": current_user.get_id(),
                "name": current_user.get_name(),
                "email": current_user.email,
                "phone": current_user.phone
            }
        #是普通用户，显示账户余额
        if user_identity==1:
            user['balance']=current_user.balance
        return render_template(
            "myinfo_detail.html",
            title='我的信息',
            user=user
        )


@account_bp.route('/account/<action>/<page>', methods=['GET', 'POST'])
def account(action, page):
    form = AccountCheckForm()
    form_password = AccountNoPasswordResetForm()
    #未登录修改密码验证页
    if action == 'password_reset':
        if page == 'check':
            # 用ID与邮箱来验证
            if form.validate_on_submit():
                #普通用户
                user = User.query.filter(and_(User.user_id == form.user_id.data, User.email == form.email.data)).first()
                if user:
                    session['id']=user.user_id
                    render_template(
                        "account_passwordreset.html",
                        title='账号 - 身份验证',
                        current_action='password_reset',
                        next_page='reset',
                        form_password = form_password
                    )
                    return redirect(url_for('account.account',action='password_reset',page='reset'))             
                #管理员
                user = Admin.query.filter(and_(Admin.admin_id == form.user_id.data, Admin.email == form.email.data)).first()
                if user:
                    session['id']=user.admin_id
                    render_template(
                        "account_passwordreset.html",
                        title='账号 - 身份验证',
                        current_action='password_reset',
                        next_page='reset',
                        form_password = form_password
                    )
                    return redirect(url_for('account.account',action='password_reset',page='reset'))                         
                else:
                    flash("输入ID与邮箱不匹配")
                    return render_template(
                        "account_check.html",
                        title='账号 - 身份验证',
                        current_action='password_reset',
                        next_page='check',
                        form=form
                    )  
            #表单内容错误
            else:
                return render_template(
                    "account_check.html",
                    title='账号 - 身份验证',
                    current_action='password_reset',
                    next_page='check',
                    form=form
                )
        elif page == 'reset':
            #读取id
            ID=session['id']      
            if request.method=='POST':
                if form_password.validate_on_submit() :
                    new_password=form_password.password1.data
                    #普通用户
                    user = User.query.filter(User.user_id == ID).first()
                    if user: 
                        user.set_password(new_password)
                        db.session.commit()
                        flash("密码修改成功")
                        return redirect(url_for('account.login'))
                    #管理员
                    user = Admin.query.filter(Admin.admin_id == ID).first()
                    if user: 
                        user.set_password(new_password)
                        db.session.commit()
                        flash("密码修改成功")
                        return redirect(url_for('account.login'))                            
                else:
                    return render_template(
                        "account_passwordreset.html",
                        title='账号 - 身份验证',
                        current_action='password_reset',
                        next_page='reset',
                        form_password=form_password
                    )
            else:
                return render_template(
                    "account_passwordreset.html",
                    title='账号 - 身份验证',
                    current_action='password_reset',
                    next_page='reset',
                    form_password=form_password
                )  
