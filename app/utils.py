import psycopg2
from flask import current_app as app

def get_db_connection():
    conn = psycopg2.connect(app.config["DATABASE_URL"])
    return conn

def insert_user(form):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        email = form.email.data

        if email_validate(email):
            return False, "E-mail já cadastrado. Por favor, escolha outro e-mail."

        nome_completo = form.nome_completo.data 
        data_nascimento = form.data_nascimento.raw_data
        data_nascimento_str = ''.join(data_nascimento)
        nome_usuario = form.nome_usuario.data
        senha = form.senha.data
        tipo_usuario = form.tipo_usuario.data

        cursor.execute("INSERT INTO usuarios(nome_completo, data_nascimento, nome_usuario, senha, email, tipo_usuario) VALUES(%s, %s, %s, %s, %s, %s)", (nome_completo, data_nascimento_str, nome_usuario, senha, email, tipo_usuario))
        
        conn.commit()
        return True, "Usuário cadastrado com sucesso."
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao inserir usuário:", e)
        return False, "Erro ao inserir usuário. Por favor, tente novamente."
    finally:
        cursor.close()
        conn.close()

def recovery_event():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.tb_eventos")
        result = cursor.fetchall()
        return result
    except psycopg2.Error as e:
        print("Nenhuma aula cadastrada", e)
        flash("Nenhuma aula cadastrada")
        return False
    finally:
        cursor.close()
        conn.close()

def insert_event(form):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        data = form.data.data
        hora = form.hora.data
        nome_aula = form.nome_aula.data
        link_aula = form.link_aula.data

        email = session['usuario_logado']
        usuario = user_select(email)
        professor = usuario[1]

        cursor.execute("INSERT INTO tb_eventos(data, hora, nome_aula, professor, link_aula) VALUES(%s, %s, %s, %s, %s)", (data, hora, nome_aula, professor, link_aula))
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao inserir evento:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def user_select(email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result
    except psycopg2.Error as e:
        print("Erro ao selecionar usuário:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def password_check(email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result
    except psycopg2.Error as e:
        print("Erro ao verificar senha:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def email_validate(email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result is not None
    except psycopg2.Error as e:
        print("Erro ao validar e-mail:", e)
        return False
    finally:
        cursor.close()
        conn.close()