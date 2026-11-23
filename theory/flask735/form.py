from flask_wtf import FlaskForm
from wtforms import StringField, URLField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
import string


class DemoForm(FlaskForm):

    def validator_url(self, field):
        url = field.data
        if "vk.ru" in url or "ok.ru" in url or "vk.com" in url:
            return
        msg = "URL должен содержать ссылки на ВК или ОК"
        raise ValidationError(msg)

    def validator_username(self, field):
        username = field.data
        if set(username) <= set(string.ascii_lowercase + string.digits + "_"):
            return
        msg = "Имя пользователя должно содержать только латинские буквы, цифры и подчеркивание"
        raise ValidationError(msg)

    is_correct = BooleanField("is_correct")
    username = StringField("Username", validators=[DataRequired(), validator_username])
    url = URLField("URL", validators=[DataRequired(), validator_url])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")
