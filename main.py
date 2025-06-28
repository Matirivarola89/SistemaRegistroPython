import tkinter as tk
from tkinter import messagebox
from db import crear_base, validar_usuario, insertar_usuario
from registro import ventana_registro
from principal import mostrar_principal

crear_base()

# --- Crear un usuario administrador si no existe ---
# Asegúrate de que el usuario admin tenga un apellido también
if not validar_usuario("admin@example.com", "adminpass"):
    # Insertar_usuario ahora requiere apellido, sexo, edad
    insertar_usuario("Administrador", "Admin", "Otro", 30, "admin@example.com", "adminpass", es_admin=1)
    print("Usuario administrador creado: admin@example.com / adminpass")
# --------------------------------------------------

ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("400x250")

tk.Label(ventana, text="Email").pack(pady=5)
entrada_email = tk.Entry(ventana)
entrada_email.pack()

tk.Label(ventana, text="Contraseña").pack(pady=5)
entrada_pass = tk.Entry(ventana, show="*")
entrada_pass.pack()

def login():
    email = entrada_email.get()
    passw = entrada_pass.get()
    usuario = validar_usuario(email, passw) # usuario ahora contiene (nombre, apellido, es_admin)
    if usuario:
        nombre_usuario = usuario[0]
        apellido_usuario = usuario[1] # Obtener el apellido
        es_admin = usuario[2]
        messagebox.showinfo("Bienvenido", f"Iniciaste sesión como {nombre_usuario} {apellido_usuario}")
        mostrar_principal(nombre_usuario, apellido_usuario, es_admin) # Pasar nombre y apellido
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

tk.Button(ventana, text="Iniciar sesión", command=login).pack(pady=10)
tk.Button(ventana, text="Registrarse", command=ventana_registro).pack()

ventana.mainloop()