from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length

class ChargeForm(FlaskForm):
    amount = IntegerField(
        '金额',
        validators=[DataRequired(message='未输入金额')],
        render_kw={
            'placeholder':'请输入金额',
        }
    )
    submit = SubmitField(
        '充值',
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
