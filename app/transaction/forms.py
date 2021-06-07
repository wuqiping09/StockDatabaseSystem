from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Optional, NumberRange

def validCompanyId(form,field):
    s=field.data
    if not s.isdigit() or len(s)!=6:
        raise ValidationError('股票代码应为6位数字')

class BuyForm(FlaskForm):
    company_id=StringField(
        '股票代码',
        validators=[DataRequired(message='未输入股票代码'),validCompanyId],
        render_kw={
            'placeholder':'请输入6位股票代码',
            'maxlength':'6'
        }
    )
    amount=IntegerField(
        '买入股数',
        validators=[DataRequired(message='未输入股数')],
        render_kw={
            'placeholder':'请输入股数',
        }
    )
    submit = SubmitField(
        '买入',
        render_kw={
            'class': 'center btn btn-primary d-block mt-2 px-5'
        }
    )
    cancel = SubmitField(
        '取消',
        render_kw={
            'class': 'center btn btn-primary d-block mt-2 px-5'
        }
    )

class SellForm(FlaskForm):
    company_id=StringField(
        '股票代码',
        validators=[DataRequired(message='未输入股票代码'),validCompanyId],
        render_kw={
            'placeholder':'请输入6位股票代码',
            'maxlength':'6'
        }
    )
    amount=IntegerField(
        '卖出股数',
        validators=[DataRequired(message='未输入股数')],
        render_kw={
            'placeholder':'请输入股数',
        }
    )
    submit = SubmitField(
        '卖出',
        render_kw={
            'class': 'center btn btn-primary d-block mt-2 px-5'
        }
    )
    cancel = SubmitField(
        '取消',
        render_kw={
            'class': 'center btn btn-primary d-block mt-2 px-5'
        }
    )
