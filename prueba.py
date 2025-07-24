from SistemaAerolinea import SistemaAerolinea
import tkinter as tk
from tkinter import messagebox, ttk
from Usuario import Usuario
from Administrador import Administrador
from SistemaAerolinea import SistemaAerolinea
from Reserva import Reserva
from Vuelo import Vuelo
from Pasajero import Pasajero

sistema = SistemaAerolinea()

user1 = Usuario("Ana", 123, "pass1", "ana@gmail.com")
user2 = Usuario("Juan", 122, "pass2", "juan@gmail.com")
user3 = Usuario("Jose", 1234567, "pass", "jose@gmail.com")
user4 = Usuario("Miguel", 51813066, "pass", "miguel@gmail.com")
user5 = Usuario("Manuel", 211, "pass", "manuel@gmail.com")

reserva1 = Reserva(
    idReserva="RES001",
    usuario=Usuario("Ana López", "AL123", "pass123", "ana@email.com"),  # Objeto Usuario
    vuelo=Vuelo("AV123", "BOG", "MDE", "10:00 AM", 10, 30),           # Objeto Vuelo
    cantSillasPref=1,
    cantSillasEcono=0,
    precioTotal=850000,      # 1 × $850,000 (preferencial)
    millasRedimidas=False
)

reserva2 = Reserva(
    idReserva="RES002",
    usuario=Usuario("Carlos Rojas", "CR456", "pass456", "carlos@email.com"),
    vuelo=Vuelo("AV456", "MDE", "CTG", "02:00 PM", 5, 20),
    cantSillasPref=2,
    cantSillasEcono=0,
    precioTotal=1700000,     # 2 × $850,000 (preferencial)
    millasRedimidas=True     # Millas aplicadas (descuento en pagarReserva)
)

# Añadir pasajeros
reserva2.addPasajero(Pasajero("María González", "MG789"))
reserva2.addPasajero(Pasajero("Pedro Sánchez", "PS012"))

reserva3 = Reserva(
    idReserva="RES003",
    usuario=Usuario("Luisa Díaz", "LD789", "pass789", "luisa@email.com"),
    vuelo=Vuelo("AV789", "CTG", "BOG", "06:00 PM", 15, 50),
    cantSillasPref=0,
    cantSillasEcono=3,
    precioTotal=705000,      # 3 × $235,000 (económica)
    millasRedimidas=False
)

# Añadir pasajeros (máximo permitido)
reserva3.addPasajero(Pasajero("Juan Pérez", "JP345"))
reserva3.addPasajero(Pasajero("Laura Ramírez", "LR678"))
reserva3.addPasajero(Pasajero("Sofía Castro", "SC901"))

reserva4 = Reserva(
    idReserva="RES004",
    usuario=Usuario("David Torres", "DT234", "pass234", "david@email.com"),
    vuelo=Vuelo("AV101", "BOG", "PEI", "08:00 AM", 8, 25),
    cantSillasPref=1,
    cantSillasEcono=1,
    precioTotal=1085000,     # (1 × $850,000) + (1 × $235,000)
    millasRedimidas=False
)

# Añadir pasajeros y marcar check-in
reserva4.addPasajero(Pasajero("Daniela Vargas", "DV567"))
reserva4.addPasajero(Pasajero("Andrés Gómez", "AG890"))
reserva4.setEstadoCheckIn(True)  # Check-in realizado
sistema.addReserva(reserva1)
sistema.addReserva(reserva2)
sistema.addReserva(reserva3)
sistema.addReserva(reserva4)

sistema.toFileReservas("reservas.txt")
######PRUEBAS



sistema.registrarUsuario(user1)
sistema.registrarUsuario(user2)
sistema.registrarUsuario(user3)
sistema.registrarUsuario(user4)
sistema.registrarUsuario(user5)

sistema.importarVuelos("vuelos.txt")
sistema.toFileVuelos("vuelos2.txt")

for u in sistema._SistemaAerolinea__usuarios:
    print(u.getNombre(), u.getIdUsuario())

for r in sistema._SistemaAerolinea__reservas:
    print(r.getIdReserva() , r.getEstadoCheckIn())

# Crear la ventana principal
win = tk.Tk()

# Consfigurar ventana
win.title("AEROLINEA JJJ")
win.geometry("400x300")


def abrir_ventana(titulo, mensaje):
    ventana = tk.Toplevel(win)
    ventana.title(titulo)
    ventana.geometry("300x200")

    label = tk.Label(ventana, text=mensaje)
    label.pack(pady=20)

    boton_volver = tk.Button(ventana, text="Volver al inicio", command=ventana.destroy)
    boton_volver.pack(pady=10)


def CrearCuenta():
    crear = tk.Toplevel()
    crear.title("Crear Cuenta")
    crear.geometry("400x300")

    # Entradas y textos
    tk.Label(crear, text="Nombre:").pack()
    entry1 = tk.Entry(crear)
    entry1.pack()

    tk.Label(crear, text="ID (Número de identidad):").pack()
    entry2 = tk.Entry(crear)
    entry2.pack()

    tk.Label(crear, text="Contraseña:").pack()
    entry3 = tk.Entry(crear, show="*")
    entry3.pack()

    tk.Label(crear, text="Correo:").pack()
    entry4 = tk.Entry(crear)
    entry4.pack()

    mensaje_label = tk.Label(crear, text="")
    mensaje_label.pack()

    def crearUsuario():
        try:
            nombre = entry1.get()
            id = int(entry2.get())
            contraseña = entry3.get()
            correo = entry4.get()

            nuevo_usuario = Usuario(nombre, id, contraseña, correo)
            registrado = sistema.registrarUsuario(nuevo_usuario)

            if registrado:
                mensaje_label.config(text=f"Usuario {nombre} registrado con éxito.", fg="green")
            else:
                mensaje_label.config(text="Ya existe un usuario con ese ID.", fg="red")

        except ValueError:
            mensaje_label.config(text="Error: ID debe ser un número.", fg="red")
        except Exception as e:
            mensaje_label.config(text=f"Error: {str(e)}", fg="red")

    # Botones
    tk.Button(crear, text="Registrar", command=crearUsuario).pack(pady=5)
    tk.Button(crear, text="Volver al inicio", command=crear.destroy).pack(pady=5)


def ventana_admin(usuario):
    ventana = tk.Toplevel()
    ventana.title("Ingreso administrador")
    ventana.geometry("600x500")

    tk.Label(ventana, text=f"Bienvenido/a Administrador", font=("Helvetica", 12)).pack(pady=10)

    vuelos_disponibles = sistema.getVuelos()

    origenes = sorted(set(v.get_origen() for v in vuelos_disponibles))
    destinos = sorted(set(v.get_destino() for v in vuelos_disponibles))

    origen_var = tk.StringVar()
    destino_var = tk.StringVar()

    tk.Label(ventana, text="Origen:").pack()
    combo_origen = ttk.Combobox(ventana, textvariable=origen_var, values=origenes, state="readonly")
    combo_origen.pack()

    tk.Label(ventana, text="Destino:").pack()
    combo_destino = ttk.Combobox(ventana, textvariable=destino_var, values=destinos, state="readonly")
    combo_destino.pack()

    vuelos_frame = tk.Frame(ventana)
    vuelos_frame.pack(pady=15)


def ventana_user(usuario):
    ventana = tk.Toplevel()
    ventana.title("Ingreso usuario")
    ventana.geometry("600x500")

    tk.Label(ventana, text=f"Bienvenido/a {usuario.getNombre()}", font=("Helvetica", 12)).pack(pady=10)

    vuelos_disponibles = sistema.getVuelos()

    # Marco horizontal para millas
    frame_millas = tk.Frame(ventana)
    frame_millas.pack(pady=10)

    tk.Label(frame_millas, text=f"Cantidad de millas acumuladas: {usuario.getMillas()}",
             font=("Helvetica", 10)).pack(side=tk.LEFT, padx=10)

    origenes = sorted(list(set(v.get_origen() for v in vuelos_disponibles)))
    destinos = sorted(list(set(v.get_destino() for v in vuelos_disponibles)))

    origen_var = tk.StringVar()
    destino_var = tk.StringVar()

    tk.Label(ventana, text="Origen:").pack()
    combo_origen = ttk.Combobox(ventana, textvariable=origen_var, values=origenes, state="readonly")
    combo_origen.pack()

    tk.Label(ventana, text="Destino:").pack()
    combo_destino = ttk.Combobox(ventana, textvariable=destino_var, values=destinos, state="readonly")
    combo_destino.pack()

    canvas = tk.Canvas(ventana, height=200)  # Puedes ajustar la altura aquí
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
    scrollbar.pack(side="right", fill="y")

    vuelos_frame = scrollable_frame

    def mostrar_detalle(vuelo):
        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Reserva")
        ventana_detalle.geometry("500x750")
        ventana_detalle.config(bg="white")
        fuente_general = ("Helvetica", 12)

        titulo = tk.Label(ventana_detalle, text="Reserva", font=("Helvetica", 20, "bold"), bg="white")
        titulo.pack(pady=20)

        frame_info = tk.Frame(ventana_detalle, bg="white")
        frame_info.pack(pady=10)

        info_labels = [
            ("Código vuelo", vuelo.get_idVuelo()),
            ("Origen", vuelo.get_origen()),
            ("Destino", vuelo.get_destino()),
            ("Horario", vuelo.get_horario()),
            ("Cantidad de sillas preferenciales disponibles", vuelo.get_sillasPreDisp()),
            ("Cantidad de sillas economicas dispobles", vuelo.get_sillasEconoDisp())]

        for texto, valor in info_labels:
            tk.Label(frame_info, text=texto, font=fuente_general, anchor="w", bg="white").pack(fill="x")
            tk.Label(frame_info, text=str(valor), font=fuente_general, anchor="w", bg="white").pack(fill="x",
                                                                                                    pady=(0, 10))

        frame_seleccion = tk.Frame(ventana_detalle, bg="white")
        frame_seleccion.pack(pady=20)

        tk.Label(frame_seleccion, text="SILLAS PREFERENCIALES\n$850.000", font=fuente_general, bg="white",
                 anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        entry_pref = tk.Entry(frame_seleccion, width=10)
        entry_pref.grid(row=0, column=1, padx=10)

        tk.Label(frame_seleccion, text="SILLAS ECONÓMICAS\n$235.000", font=fuente_general, bg="white", anchor="w").grid(
            row=1, column=0, sticky="w", padx=10, pady=5)
        entry_econo = tk.Entry(frame_seleccion, width=10)
        entry_econo.grid(row=1, column=1, padx=10)

        frame_total = tk.Frame(ventana_detalle, bg="white")
        frame_total.pack(pady=15)

        tk.Label(frame_total, text="TOTAL A PAGAR:", font=fuente_general, bg="white").grid(row=0, column=0, padx=10)
        entry_total = tk.Entry(frame_total, width=15)
        entry_total.grid(row=0, column=1)

        frame_botones = tk.Frame(ventana_detalle, bg="white")
        frame_botones.pack(pady=20)

        # tk.Button(frame_botones, text="Total", command=calcular_total, font=fuente_general, bg="black", fg="white", width=10).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Reservar", font=fuente_general, bg="black", fg="white", width=10).pack(
            side="left", padx=10)

    def buscar_vuelos():
        for widget in vuelos_frame.winfo_children():
            widget.destroy()

        origen = origen_var.get()
        destino = destino_var.get()

        if not origen or not destino:
            tk.Label(vuelos_frame, text="Por favor selecciona origen y destino.").pack()
            return

        encontrados = [v for v in vuelos_disponibles
                       if v.get_origen().strip().lower() == origen.strip().lower()
                       and v.get_destino().strip().lower() == destino.strip().lower()]

        if not encontrados:
            tk.Label(vuelos_frame, text="No hay vuelos disponibles para esa ruta.").pack()
            return

        for vuelo in encontrados:
            fila = tk.Frame(vuelos_frame)
            fila.pack(pady=5, fill="x")

            desc = f"Vuelo {vuelo.get_idVuelo()}: {vuelo.get_origen()} → {vuelo.get_destino()} | Horario: {vuelo.get_horario()}"

            tk.Label(fila, text=desc, anchor="w").pack(side="left", padx=5)

            boton_reserva = tk.Button(fila, text="Reservar", command=lambda v=vuelo: mostrar_detalle(v))
            boton_reserva.pack(side="right", padx=5)

    def consultar_reservas():

        def modificar_reserva():
            pass

    tk.Button(ventana, text="Buscar vuelos", command=buscar_vuelos).pack(pady=5)
    tk.Button(ventana, text="Consultar reservas", command=consultar_reservas).pack(pady=5)


def logInUser():
    log = tk.Toplevel()
    log.title("Iniciar sesión")
    log.geometry("400x300")

    tk.Label(log, text="ID (Número documento de identidad)").pack()
    entry1 = tk.Entry(log)
    entry1.pack()

    tk.Label(log, text="Contraseña").pack()
    entry2 = tk.Entry(log, show="*")
    entry2.pack()

    mensaje_label = tk.Label(log, text="")
    mensaje_label.pack()

    def ingresar():
        try:
            id_ingresado = int(entry1.get())
            contraseña = entry2.get()

            usuario = sistema.logIn(id_ingresado, contraseña)

            if usuario:
                if isinstance(usuario, Administrador):
                    mensaje_label.config(text="Ingreso exitoso (Administrador)", fg="blue")
                    ventana_admin(usuario)

                else:
                    mensaje_label.config(text="Ingreso exitoso (Usuario)", fg="green")
                    ventana_user(usuario)
            else:
                mensaje_label.config(text="ID o contraseña incorrectos", fg="red")
        except ValueError:
            mensaje_label.config(text="El ID debe ser numérico", fg="red")

    tk.Button(log, text="Ingresar", command=ingresar).pack(pady=10)
    tk.Button(log, text="Volver al inicio", command=log.destroy).pack(pady=5)


def CambiarContraseña():
    cambiar = tk.Toplevel()
    cambiar.title("Cambiar contraseña")
    cambiar.geometry("400x300")

    tk.Label(cambiar, text="ID (Número documento de identidad)").pack()
    entry1 = tk.Entry(cambiar)
    entry1.pack()

    tk.Label(cambiar, text="Contraseña actual").pack()
    entry2 = tk.Entry(cambiar, show="*")
    entry2.pack()

    tk.Label(cambiar, text="Contraseña nueva").pack()
    entry3 = tk.Entry(cambiar, show="*")
    entry3.pack()

    mensaje_label = tk.Label(cambiar, text="")
    mensaje_label.pack()

    def cambioContraseña():
        try:
            id = int(entry1.get())
            contraseña_ant = entry2.get()
            contraseña_nueva = entry3.get()

            SistemaAerolinea.cambiarContraseña(id, contraseña_ant, contraseña_nueva)

            # Mostrar mensaje de éxito
            mensaje_label.config(text=f"Contraseña cambiada con éxito")
        except ValueError:
            mensaje_label.config(text="Error: ID debe ser un número.", fg="red")
        except Exception as e:
            mensaje_label.config(text=f"Error: {str(e)}", fg="red")

    tk.Button(cambiar, text="Enviar", command=cambioContraseña).pack(pady=5)
    tk.Button(cambiar, text="Volver al inicio", command=cambiar.destroy).pack(pady=5)


def CHECKIN():
    check = tk.Toplevel()
    check.title("Iniciar sesión")
    check.geometry("400x300")

    tk.Label(check, text="Número de reserva").pack()
    entry1 = tk.Entry(check)
    entry1.pack()

    tk.Label(check, text="ID (Número documento de identidad)").pack()
    entry2 = tk.Entry(check)
    entry2.pack()

    mensaje_label = tk.Label(check, text="")
    mensaje_label.pack()

    def iniciarCheck():
        try:
            id_usuario = int(entry1.get())
            numero_reserva = int(entry2.get())

            reserva_encontrada = None
            for reserva in SistemaAerolinea.reservas:
                if reserva.usuario.id == id_usuario and reserva.numero_reserva == numero_reserva:
                    reserva_encontrada = reserva
                    break

            if reserva_encontrada:
                mensaje_label.config(text=f"Reserva {numero_reserva} encontrada para el usuario {id_usuario}",
                                     fg="green")
            # ventana reserva
            else:
                mensaje_label.config(text="No se encontró ninguna reserva con ese ID y número.", fg="red")

        except ValueError:
            mensaje_label.config(text="Error: Ambos campos deben ser numéricos.", fg="red")
        except Exception as e:
            mensaje_label.config(text=f"Error inesperado: {str(e)}", fg="red")

    tk.Button(check, text="Enviar", command=iniciarCheck).pack(pady=5)
    tk.Button(check, text="Volver al inicio", command=check.destroy).pack(pady=5)


# Etiquetas
label1 = tk.Label(win, text="Usuario nuevo")
label2 = tk.Label(win, text="Usuario registrado")
label3 = tk.Label(win, text="¿Olvidaste tu contraseña?")
label4 = tk.Label(win, text="CHECK-IN")

# Botones
botonNew = tk.Button(win, text="Crear Cuenta", command=CrearCuenta)
botonOld = tk.Button(win, text="Iniciar sesión", command=logInUser)
botonPass = tk.Button(win, text="Cambiar contraseña", command=CambiarContraseña)
botonCheckIn = tk.Button(win, text="Check-In", command=CHECKIN)

# Organizar los elementos
label1.grid(row=0, column=0, pady=5)
botonNew.grid(row=0, column=4)
label2.grid(row=3, column=0)
botonOld.grid(row=3, column=4)
label3.grid(row=5, column=0)
botonPass.grid(row=5, column=4)
label4.grid(row=7, column=0)
botonCheckIn.grid(row=7, column=4)

# Ciclo para visualizar la ventana
win.mainloop()