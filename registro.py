import tkinter as tk
from tkinter import messagebox
from db import insertar_usuario
from utils import validar_email, formatear_nombre # Importar formatear_nombre

def ventana_registro():
    reg = tk.Toplevel()
    reg.title("Registro")
    reg.geometry("400x550") # Aumentar el tamaño de la ventana de registro

    tk.Label(reg, text="Nombre").pack(pady=2)
    nombre_entry = tk.Entry(reg)
    nombre_entry.pack()

    tk.Label(reg, text="Apellido").pack(pady=2)
    apellido_entry = tk.Entry(reg)
    apellido_entry.pack()

    tk.Label(reg, text="Sexo").pack(pady=2)
    sexo_var = tk.StringVar(reg)
    sexo_var.set("Seleccionar") # Opción predeterminada
    opciones_sexo = ["Masculino", "Femenino", "Otro"]
    sexo_menu = tk.OptionMenu(reg, sexo_var, *opciones_sexo)
    sexo_menu.pack()

    tk.Label(reg, text="Edad").pack(pady=2)
    edad_entry = tk.Entry(reg)
    edad_entry.pack()

    tk.Label(reg, text="Correo Electrónico").pack(pady=2) # Cambiado a Correo Electrónico
    email_entry = tk.Entry(reg)
    email_entry.pack()

    tk.Label(reg, text="Contraseña").pack(pady=2)
    contrasena_entry = tk.Entry(reg, show="*")
    contrasena_entry.pack()

    tk.Label(reg, text="Repetir Contraseña").pack(pady=2)
    repetir_contrasena_entry = tk.Entry(reg, show="*")
    repetir_contrasena_entry.pack()

    def registrar():
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        sexo = sexo_var.get()
        edad = edad_entry.get()
        email = email_entry.get()
        contrasena = contrasena_entry.get()
        repetir_contrasena = repetir_contrasena_entry.get()

        if not nombre or not apellido or sexo == "Seleccionar" or not edad or \
           not email or not contrasena or not repetir_contrasena:
            messagebox.showwarning("Campos vacíos", "Completá todos los campos")
            return

        if not validar_email(email):
            messagebox.showerror("Email inválido", "Ingresá un correo electrónico válido")
            return

        if contrasena != repetir_contrasena:
            messagebox.showerror("Contraseñas no coinciden", "Las contraseñas no coinciden")
            return
        
        try:
            edad_num = int(edad)
            if edad_num <= 0:
                messagebox.showerror("Edad inválida", "La edad debe ser un número positivo.")
                return
        except ValueError:
            messagebox.showerror("Edad inválida", "La edad debe ser un número.")
            return

        nombre_formateado = formatear_nombre(nombre)
        apellido_formateado = formatear_nombre(apellido)

        if not insertar_usuario(nombre_formateado, apellido_formateado, sexo, edad_num, email, contrasena):
            messagebox.showerror("Error", "Este correo electrónico ya está registrado")
        else:
            messagebox.showinfo("Éxito", "Registrado correctamente")
            reg.destroy()

    tk.Button(reg, text="Registrar", command=registrar).pack(pady=15)