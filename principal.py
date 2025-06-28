import tkinter as tk
from tkinter import messagebox
from db import obtener_todos_los_usuarios, actualizar_usuario, eliminar_usuario
from utils import validar_email, formatear_nombre

def mostrar_principal(nombre_usuario, apellido_usuario, es_admin): # Recibe nombre y apellido
    win = tk.Toplevel()
    win.title("Bienvenido")
    win.geometry("400x300")

    tk.Label(win, text=f"¡Hola, {nombre_usuario} {apellido_usuario}!", font=("Arial", 16)).pack(expand=True)

    if es_admin:
        def mostrar_usuarios():
            ventana_usuarios = tk.Toplevel(win)
            ventana_usuarios.title("Usuarios Registrados")
            ventana_usuarios.geometry("600x550") # Aumentar el tamaño para más campos

            frame_usuarios = tk.Frame(ventana_usuarios)
            frame_usuarios.pack(pady=10)

            tk.Label(frame_usuarios, text="Lista de Usuarios:", font=("Arial", 12, "bold")).pack()

            listbox_usuarios = tk.Listbox(frame_usuarios, width=90, height=15) # Ancho adaptado
            listbox_usuarios.pack()

            usuarios = obtener_todos_los_usuarios()
            if usuarios:
                for usuario in usuarios:
                    # Formato: ID | Nombre Apellido | Sexo | Edad | Email
                    listbox_usuarios.insert(tk.END, f"ID: {usuario[0]} | Nombre: {usuario[1]} {usuario[2]} | Sexo: {usuario[3]} | Edad: {usuario[4]} | Email: {usuario[5]}")
            else:
                tk.Label(frame_usuarios, text="No hay usuarios registrados.").pack(pady=20)

            def abrir_ventana_modificar():
                seleccionado = listbox_usuarios.curselection()
                if not seleccionado:
                    messagebox.showwarning("Advertencia", "Selecciona un usuario para modificar.")
                    return

                indice_seleccionado = seleccionado[0]
                usuario_seleccionado = usuarios[indice_seleccionado]
                user_id = usuario_seleccionado[0]
                nombre_actual = usuario_seleccionado[1]
                apellido_actual = usuario_seleccionado[2]
                sexo_actual = usuario_seleccionado[3]
                edad_actual = usuario_seleccionado[4]
                email_actual = usuario_seleccionado[5]

                ventana_modificar = tk.Toplevel(ventana_usuarios)
                ventana_modificar.title(f"Modificar Usuario: {nombre_actual} {apellido_actual}")
                ventana_modificar.geometry("350x450") # Aumentar tamaño

                tk.Label(ventana_modificar, text="Nuevo Nombre").pack(pady=2)
                entrada_nuevo_nombre = tk.Entry(ventana_modificar)
                entrada_nuevo_nombre.insert(0, nombre_actual)
                entrada_nuevo_nombre.pack()

                tk.Label(ventana_modificar, text="Nuevo Apellido").pack(pady=2)
                entrada_nuevo_apellido = tk.Entry(ventana_modificar)
                entrada_nuevo_apellido.insert(0, apellido_actual)
                entrada_nuevo_apellido.pack()

                tk.Label(ventana_modificar, text="Nuevo Sexo").pack(pady=2)
                sexo_mod_var = tk.StringVar(ventana_modificar)
                sexo_mod_var.set(sexo_actual)
                opciones_sexo_mod = ["Masculino", "Femenino", "Otro"]
                sexo_mod_menu = tk.OptionMenu(ventana_modificar, sexo_mod_var, *opciones_sexo_mod)
                sexo_mod_menu.pack()

                tk.Label(ventana_modificar, text="Nueva Edad").pack(pady=2)
                entrada_nueva_edad = tk.Entry(ventana_modificar)
                entrada_nueva_edad.insert(0, str(edad_actual))
                entrada_nueva_edad.pack()

                tk.Label(ventana_modificar, text="Nuevo Correo Electrónico").pack(pady=2)
                entrada_nuevo_email = tk.Entry(ventana_modificar)
                entrada_nuevo_email.insert(0, email_actual)
                entrada_nuevo_email.pack()

                tk.Label(ventana_modificar, text="Nueva Contraseña (dejar en blanco para no cambiar)").pack(pady=2)
                entrada_nueva_contrasena = tk.Entry(ventana_modificar, show="*")
                entrada_nueva_contrasena.pack()

                def guardar_cambios():
                    nuevo_nombre = entrada_nuevo_nombre.get()
                    nuevo_apellido = entrada_nuevo_apellido.get()
                    nuevo_sexo = sexo_mod_var.get()
                    nueva_edad_str = entrada_nueva_edad.get()
                    nuevo_email = entrada_nuevo_email.get()
                    nueva_contrasena = entrada_nueva_contrasena.get()

                    if not nuevo_nombre or not nuevo_apellido or nuevo_sexo == "Seleccionar" or \
                       not nueva_edad_str or not nuevo_email:
                        messagebox.showwarning("Campos Vacíos", "Todos los campos obligatorios deben estar completos.")
                        return
                    if not validar_email(nuevo_email):
                        messagebox.showerror("Correo Inválido", "Por favor, ingresa un correo electrónico válido.")
                        return
                    
                    try:
                        nueva_edad = int(nueva_edad_str)
                        if nueva_edad <= 0:
                            messagebox.showerror("Edad inválida", "La edad debe ser un número positivo.")
                            return
                    except ValueError:
                        messagebox.showerror("Edad inválida", "La edad debe ser un número.")
                        return

                    nombre_formateado = formatear_nombre(nuevo_nombre)
                    apellido_formateado = formatear_nombre(nuevo_apellido)

                    if actualizar_usuario(user_id, nombre_formateado, apellido_formateado, nuevo_sexo, nueva_edad, nuevo_email, nueva_contrasena):
                        messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
                        ventana_modificar.destroy()
                        ventana_usuarios.destroy()
                        mostrar_usuarios()
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el usuario. El correo electrónico podría estar en uso.")

                tk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_cambios).pack(pady=10)
                tk.Button(ventana_modificar, text="Cancelar", command=ventana_modificar.destroy).pack()

            def eliminar_usuario_seleccionado():
                seleccionado = listbox_usuarios.curselection()
                if not seleccionado:
                    messagebox.showwarning("Advertencia", "Selecciona un usuario para eliminar.")
                    return

                indice_seleccionado = seleccionado[0]
                usuario_seleccionado = usuarios[indice_seleccionado]
                user_id = usuario_seleccionado[0]
                nombre_usuario_a_eliminar = usuario_seleccionado[1]
                apellido_usuario_a_eliminar = usuario_seleccionado[2]

                if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar a {nombre_usuario_a_eliminar} {apellido_usuario_a_eliminar}?"):
                    if eliminar_usuario(user_id):
                        messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                        ventana_usuarios.destroy()
                        mostrar_usuarios()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el usuario.")

            tk.Button(ventana_usuarios, text="Modificar Usuario Seleccionado", command=abrir_ventana_modificar).pack(pady=10)
            tk.Button(ventana_usuarios, text="Eliminar Usuario Seleccionado", command=eliminar_usuario_seleccionado).pack(pady=5)
            tk.Button(ventana_usuarios, text="Cerrar", command=ventana_usuarios.destroy).pack(pady=5)

        tk.Button(win, text="Ver Usuarios Registrados", command=mostrar_usuarios).pack(pady=10)

    tk.Button(win, text="Cerrar sesión", command=win.destroy).pack(pady=10)