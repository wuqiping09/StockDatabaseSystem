from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, FileField, MultipleFileField
from wtforms.validators import ValidationError, DataRequired, Optional, NumberRange, Length

def validCompanyId(form,field):
    s=field.data
    if not s.isdigit() or len(s)!=6:
        raise ValidationError('股票代码应为6位数字')

class AddStockForm(FlaskForm):
    company_id=StringField(
        '股票代码',
        validators=[DataRequired(message='未输入股票代码'),validCompanyId],
        render_kw={
            'placeholder':'请输入6位股票代码',
            'maxlength':'6'
        }
    )
    company_name=StringField(
        '公司名称',
        validators=[DataRequired(message='未输入公司名称')],
        render_kw={
            'placeholder':'请输入公司名称',
        }
    )
    price=IntegerField(
        '初始股价',
        validators=[DataRequired(message='未输入初始股价')],
        render_kw={
            'placeholder':'请输入初始股价',
        }
    )
    submit = SubmitField(
        '确定',
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

class ChangePriceForm(FlaskForm):
    company_id=StringField(
        '股票代码',
        validators=[DataRequired(message='未输入股票代码'),validCompanyId],
        render_kw={
            'placeholder':'请输入6位股票代码',
            'maxlength':'6'
        }
    )
    price=IntegerField(
        '新的股价',
        validators=[DataRequired(message='未输入股价')],
        render_kw={
            'placeholder':'请输入新的股价',
        }
    )
    submit = SubmitField(
        '确定',
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
