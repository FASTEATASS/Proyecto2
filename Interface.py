import tkinter as tk
from Usuario import Usuario

# Crear la ventana principal
win = tk.Tk()
win.title("Crear usuario")
win.geometry("400x300")

# Insertar objetos
label1 = tk.Label(win, text="Nombre Completo")
label2 = tk.Label(win, text="ID (Número documento de identidad)")
label3 = tk.Label(win, text="Contraseña")
label4 = tk.Label(win, text="Correo Electrónico")
label_Registrado = tk.Label(win, text="¿Ya esta registrado?")

# Crear los campos de texto
entry1 = tk.Entry(win)
entry2 = tk.Entry(win)
entry3 = tk.Entry(win, show="*")
entry4 = tk.Entry(win)

# Etiqueta para mostrar mensajes
mensaje_label = tk.Label(win, text="", fg="green")


# Función para crear usuario
def crearUsuario():
    try:
        nombre = entry1.get()
        id = int(entry2.get())
        contraseña = entry3.get()
        correo = entry4.get()

        nuevo_usuario = Usuario(nombre, id, contraseña, correo)

        # Mostrar mensaje de éxito
        mensaje_label.config(text=f"Usuario {nombre} registrado con éxito.")
    except ValueError:
        mensaje_label.config(text="Error: ID debe ser un número.", fg="red")
    except Exception as e:
        mensaje_label.config(text=f"Error: {str(e)}", fg="red")


# Botón para crear usuario
boton = tk.Button(win, text="Ingresar", command=crearUsuario)

# Organizar los elementos
label_Registrado.grid(row=0, column=5)
label1.grid(row=3, column=5)
entry1.grid(row=4, column=5)
label2.grid(row=5, column=5)
entry2.grid(row=6, column=5)
label3.grid(row=7, column=5)
entry3.grid(row=8, column=5)
label4.grid(row=9, column=5)
entry4.grid(row=10, column=5)
boton.grid(row=11, column=5)
mensaje_label.grid(row=15, column=5, columnspan=2)

# Mostrar la ventana
win.mainloop()