import sqlite3
import hashlib

def conectar():
    return sqlite3.connect("base_datos.db")

def crear_base():
    with conectar() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            sexo TEXT NOT NULL,
            edad INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            es_admin INTEGER DEFAULT 0
        )""")
        conn.commit()

def hashear_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def insertar_usuario(nombre, apellido, sexo, edad, email, contrasena, es_admin=0):
    try:
        with conectar() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO usuarios (nombre, apellido, sexo, edad, email, contrasena, es_admin) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (nombre, apellido, sexo, edad, email, hashear_password(contrasena), es_admin))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def validar_usuario(email, contrasena):
    with conectar() as conn:
        c = conn.cursor()
        c.execute("SELECT nombre, apellido, es_admin FROM usuarios WHERE email = ? AND contrasena = ?", # Obtener nombre, apellido y es_admin
                  (email, hashear_password(contrasena)))
        return c.fetchone()

def obtener_todos_los_usuarios():
    with conectar() as conn:
        c = conn.cursor()
        c.execute("SELECT id, nombre, apellido, sexo, edad, email FROM usuarios") # Obtener todos los campos relevantes
        return c.fetchall()

def actualizar_usuario(user_id, nuevo_nombre, nuevo_apellido, nuevo_sexo, nueva_edad, nuevo_email, nueva_contrasena):
    try:
        with conectar() as conn:
            c = conn.cursor()
            if nueva_contrasena:
                c.execute("UPDATE usuarios SET nombre = ?, apellido = ?, sexo = ?, edad = ?, email = ?, contrasena = ? WHERE id = ?",
                          (nuevo_nombre, nuevo_apellido, nuevo_sexo, nueva_edad, nuevo_email, hashear_password(nueva_contrasena), user_id))
            else:
                c.execute("UPDATE usuarios SET nombre = ?, apellido = ?, sexo = ?, edad = ?, email = ? WHERE id = ?",
                          (nuevo_nombre, nuevo_apellido, nuevo_sexo, nueva_edad, nuevo_email, user_id))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def eliminar_usuario(user_id):
    try:
        with conectar() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Error al eliminar usuario: {e}")
        return False