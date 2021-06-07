import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, NumberRange, Length, Regexp

def containDigitAndAlpha(form,field):
    s=field.data
    pattern=re.compile('[a-zA-Z0-9]')
    match = pattern.findall(s)
    if (not match) or s.isdigit() or s.isalpha():
        raise ValidationError('必须含数字与字母')

def allDigit(form,field):
    s=field.data
    if not s.isdigit() :
        raise ValidationError('必须全为数字')

class LoginForm(FlaskForm):
    user_id = StringField(
        '用户ID',
        validators=[DataRequired()],
        render_kw={
            'class':'form-control'
        }
    )
    password = PasswordField(
        '密码',
        validators=[DataRequired()],
        render_kw={
            'class':'form-control'
        }
    )
    identification = SelectField(
        '身份',
        validators=[DataRequired()],
        choices=[
            ('User', '普通用户'),
            ('Admin', '管理员')
        ],
        default='User',
        render_kw={
            'class':'wide'
        }
    )
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录',
                         render_kw={
                             'class': 'd-block py-3 px-5 bg-primary text-white border-0 rounded font-weight-bold mt-3 center p-2'
                         })

class RegisterForm(FlaskForm):
    user_id = StringField(
        '用户ID',
        validators=[DataRequired(message='请输入ID!'),allDigit],
        render_kw={
            'class': 'form-control',
            'placeholder': 'ID长度：普通用户7位数字/管理员5位数字'
        }
    )
    user_name = StringField(
        '用户名',
        validators=[DataRequired(message='请输入用户名!')],
        render_kw={
            'class': 'form-control'
        }
    )
    password1 = PasswordField(
        '密码',
        validators=[
            DataRequired(message='请输入密码!'),
            Length(min = 8, max = 16, message='密码必须是8-16位'),
            containDigitAndAlpha
            ],
        render_kw={
            'class': 'form-control',
            'placeholder':'密码长度8-16位，必须含数字与字母'
        }
    )
    password2 = PasswordField(
        '重复密码',
        validators=[DataRequired(), 
                    EqualTo('password1', message='两次输入的密码不一致!')
                    ],
        render_kw={
            'class': 'form-control'
        }
    )
    identification = SelectField(
        '身份',
        validators=[DataRequired()],
        choices=[
            ('User', '普通用户'),
            ('Admin', '管理员')
        ],
        default='User',
        render_kw={
            'class': 'wide'
        }
    )
    email = StringField(
        '邮箱',
        validators=[
            DataRequired(), 
            Email(message='非法邮箱格式!')],
        render_kw={
            'class': 'form-control'
        })
    phone = StringField('手机',
                        validators=[Optional()],
                        render_kw={
                            'class': 'form-control'
                        })
    submit = SubmitField('注册',
                         render_kw={
                             'class': 'd-block py-3 px-5 bg-primary text-white border-0 rounded font-weight-bold mt-3 center'
                         })

class MyInfoEditForm(FlaskForm):
    user_name = StringField(
        '用户名',
        validators=[Optional()],
        render_kw={
            'class': 'form-control'
        }
    )
    profile_photo = FileField(
        '头像',
        validators=[Optional()]
    )
    submit = SubmitField('保存更改',
                         render_kw={
                             'class': 'btn btn-transparent'
                         })

class AccountHasPasswordResetForm(FlaskForm):
    password_old = PasswordField(
        '旧密码',
        validators=[DataRequired(message='请输入密码!')],
        render_kw={
            'class': 'form-control'
        }
    )
    password1 = PasswordField(
        '新密码',
        validators=[DataRequired(message='请输入密码!'),
                    Length(min = 8, max = 16, message='密码必须是8-16位'),
                    containDigitAndAlpha],
        render_kw={
            'class': 'form-control',
            'placeholder':'密码长度8-16位，必须含数字与字母'
        }
    )
    password2 = PasswordField(
        '重复新密码',
        validators=[DataRequired(), EqualTo('password1', message='两次输入的密码不一致!')],
        render_kw={
            'class': 'form-control'
        }
    )    
    submit = SubmitField('修改密码',
                         render_kw={
                             'class': 'btn btn-transparent'
                         })

class AccountNoPasswordResetForm(FlaskForm):
    password1 = PasswordField(
        '新密码',
        validators=[DataRequired(message='请输入密码!'),
                    Length(min = 8, max = 16, message='密码必须是8-16位'),
                    containDigitAndAlpha],
        render_kw={
            'class': 'form-control',
            'placeholder': '密码长度8-16位，必须含数字与字母'
        }
    )
    password2 = PasswordField(
        '重复新密码',
        validators=[DataRequired(), EqualTo('password1', message='两次输入的密码不一致!')],
        render_kw={
            'class': 'form-control'
        }
    )    
    submit = SubmitField('重置密码',
                         render_kw={
                             'class': 'd-block py-3 px-5 bg-primary text-white border-0 rounded font-weight-bold mt-3 center'
                         })

class AccountCheckForm(FlaskForm):
    user_id = StringField(
        '用户ID',
        validators=[DataRequired(message='请输入ID!')],
        render_kw={
            'class': 'form-control'
        }
    )
    email = StringField(
        '邮箱',
        validators=[Email(message='非法邮箱格式!')],
        render_kw={
            'class': 'form-control'
        })
    phone = StringField('手机',
                        validators=[Optional()],
                        render_kw={
                            'class': 'form-control'
                        })
    submit = SubmitField('验证',
                         render_kw={
                             'class': 'd-block py-3 px-5 bg-primary text-white border-0 rounded font-weight-bold mt-3 center'
                         })
