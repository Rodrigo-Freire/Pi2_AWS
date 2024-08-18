from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired

class FormUser(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=1, max=100)])
    data_nascimento = DateField("Data de Nascimento", format='%d-%m-%Y', validators=[InputRequired()])
    nome_usuario = StringField("Nickname", validators=[DataRequired(), Length(min=1, max=50)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField("E-mail", validators=[DataRequired(), Length(min=1, max=100)])
    tipo_usuario = SelectField("Tipo de Usuário", choices=[('aluno', 'Aluno'), ('professor', 'Professor')], validators=[DataRequired()])
    salvar = SubmitField('Salvar')

class FormLogin(FlaskForm):
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField("E-mail", validators=[DataRequired(), Length(min=1, max=100)])
    login = SubmitField("Login")

class FormEvent(FlaskForm):
    data = DateField('Data', validators=[DataRequired()])
    hora = StringField('Hora', validators=[DataRequired(), Length(min=1, max=100)])
    nome_aula = StringField('Nome da Aula', validators=[DataRequired(), Length(min=1, max=200)])
    link_aula = StringField('Link da Aula', validators=[DataRequired(), Length(min=1, max=255)])
    salvar = SubmitField('Salvar')