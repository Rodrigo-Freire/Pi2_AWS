from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from app.forms import FormUser, FormLogin, FormEvent
from app.utils import insert_user, recovery_event, insert_event, user_select, password_check, email_validate

main = Blueprint('main', __name__)
user_routes = Blueprint('user_routes', __name__)
event_routes = Blueprint('event_routes', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/politica_privacidade')
def politica_privacidade():
    return render_template("politica_privacidade.html")

@event_routes.route('/calendario-aulas')
def calendario_aulas():
    if 'usuario_logado' not in session or session["usuario_logado"] == None:
        flash("Você precisa estar logado para acessar o calendário.")
        return redirect(url_for("login"))
    
    eventos = recovery_event()
    return render_template("calendario_aulas.html", eventos=eventos)

@event_routes.route('/criar-evento')
def criar_evento():
    email = session['usuario_logado']
    usuario = user_select(email)
    if usuario[6] != 'professor':
        flash("Somente professores podem inserir aulas")
        return redirect(url_for("calendario_aulas"))

    form = FormEvent()
    return render_template("criar_evento.html", form=form)

@event_routes.route("/cadastro_bd_evento", methods=["POST"])
def cadastro_bd_evento():
    form = FormEvent(request.form)
    insert_event(form)
    return redirect(url_for("calendario_aulas"))

@user_routes.route('/login')
def login():
    form = FormLogin()
    if session['usuario_logado'] != None:
        flash("Usuário já logado.")
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

@user_routes.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Usuário deslogado!")
    return redirect(url_for("index"))

@user_routes.route('/autenticar', methods=["POST"])
def autenticar():
    form = FormLogin(request.form)
    email = form.email.data
    senha = form.senha.data
    senha_db = password_check(email)
    usuario = user_select(email)

    if not usuario:
        flash(f"Usuário: {email} não cadastrado!")
        return redirect(url_for("login"))
    
    if senha != senha_db[0]:
        flash("Senha Incorreta!")
        return redirect(url_for("login"))
    else:
        session['usuario_logado'] = usuario[5]
        flash(f"Usuário: {usuario[1]} logado com sucesso!")
        return redirect(url_for('index'))

@user_routes.route('/criar-conta')
def criar_conta():
    form = FormUser()
    return render_template("criar_conta.html", titulo='Criar Conta', form=form)

@user_routes.route('/cadastro-bd-conta', methods=["POST"])
def cadastro_bd_conta():
    form = FormUser(request.form)
    if not insert_user(form):
        flash("Erro ao cadastrar usuário!")
        return redirect(url_for('criar_conta'))
    flash("Usuário Cadastrado com Sucesso!")
    return redirect(url_for('login'))