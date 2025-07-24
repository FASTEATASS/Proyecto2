from SistemaAerolinea import SistemaAerolinea
import tkinter as tk
from tkinter import messagebox, ttk
from Usuario import Usuario
from Pasajero import Pasajero
from Administrador import Administrador
from Reserva import Reserva
from Vuelo import Vuelo
import uuid

sistema = SistemaAerolinea()

user1 = Usuario("Ana", 123, "pass1", "ana@gmail.com")
user2 = Usuario("Juan", 122, "pass2", "juan@gmail.com")
user3 = Usuario("Jose", 1234567, "pass", "jose@gmail.com")
user4 = Usuario("Miguel", 51813066, "pass", "miguel@gmail.com")
user5 = Usuario("Manuel", 211, "pass", "manuel@gmail.com")
usuario = Usuario("Carlos Rojas", 54321, "pass", "carlos@email.com")

sistema.registrarUsuario(user1)
sistema.registrarUsuario(user2)
sistema.registrarUsuario(user3)
sistema.registrarUsuario(user4)
sistema.registrarUsuario(user5)
sistema.registrarUsuario(usuario)

user1.setMillas(5000)

adm = Administrador("adm", 111, "adm1", "adm@gmail.com")
sistema.registrarUsuario(adm)

sistema.importarVuelos("vuelos.txt")

Vuelo1 = Vuelo("VU1234L", "MEDELLIN", "BOGOTA", "LUNES 8:00", 10, 130)

reserva2 = Reserva(
    idReserva=222,
    usuario=usuario,
    vuelo=Vuelo1,
    cantSillasPref=2,
    cantSillasEcono=0,
    precioTotal=1700000,
    millasRedimidas=True
)

usuario.addReserva(reserva2)

reserva2 = Reserva(
    idReserva=233,
    usuario=usuario,
    vuelo=Vuelo1,
    cantSillasPref=2,
    cantSillasEcono=0,
    precioTotal=1700000,
    millasRedimidas=True
)

usuario.addReserva(reserva2)

sistema.addReserva(reserva2)

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


def ventana_admin(Administrador):
    ventana = tk.Toplevel()
    ventana.title("Ingreso usuario")
    ventana.geometry("600x500")

    tk.Label(ventana, text=f"Bienvenido/a Administrador", font=("Helvetica", 12)).pack(pady=10)

    vuelos_disponibles = sistema.getVuelos()

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

    canvas = tk.Canvas(ventana, height=200)
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

            desc = f"Vuelo {vuelo.get_idVuelo()}: Horario: {vuelo.get_horario()} | Sillas Pref: {vuelo.get_sillasPreDisp()} - Sillas econo: {vuelo.get_sillasEconoDisp()}"
            tk.Label(fila, text=desc, anchor="w").pack(side="left", padx=5)

            boton_modificar = tk.Button(fila, text="Modificar", command=lambda v=vuelo: ModificarVuelo(v))
            boton_modificar.pack(side="right", padx=5)

    def datosVuelo():
        crear = tk.Toplevel()
        crear.title("Crear Vuelo")
        crear.geometry("400x300")

        tk.Label(crear, text="Codigo vuelo:").pack()
        entry1 = tk.Entry(crear)
        entry1.pack()

        tk.Label(crear, text="Origen:").pack()
        entry2 = tk.Entry(crear)
        entry2.pack()

        tk.Label(crear, text="Destino:").pack()
        entry3 = tk.Entry(crear, show="*")
        entry3.pack()

        tk.Label(crear, text="Cantidad sillas preferencial:").pack()
        entry4 = tk.Entry(crear)
        entry4.pack()

        tk.Label(crear, text="Cantidad sillas economicas").pack()
        entry5 = tk.Entry(crear)
        entry5.pack()

        mensaje_label = tk.Label(crear, text="")
        mensaje_label.pack()

        def nuevoVuelo():
            try:
                codigo = entry1.get()
                origen = entry2.get()
                destino = entry3.get()
                premium = int(entry4.get())
                econo = int(entry5.get())

                nuevo_vuelo = Vuelo(codigo, origen, destino, premium, econo)
                registrado = sistema.crearVuelo(nuevo_vuelo)

                if registrado:
                    mensaje_label.config(text=f"Vuelo {codigo} registrado con éxito.", fg="green")
                else:
                    mensaje_label.config(text="Ya existe un vuelo con ese código.", fg="red")

            except ValueError:
                mensaje_label.config(text="Error: las cantidad de sillas deben ser números enteros.", fg="red")
            except Exception as e:
                mensaje_label.config(text=f"Error: {str(e)}", fg="red")

        tk.Button(crear, text="Crear vuelo", command=nuevoVuelo).pack(pady=10)

    def ModificarVuelo(vuelo):
        ventana_detalle = tk.Toplevel()
        ventana_detalle.title("Modificar vuelo")
        ventana_detalle.geometry("500x650")

        tk.Label(ventana_detalle, text="Modificar Vuelo").pack(pady=20)

        frame_info = tk.Frame(ventana_detalle)
        frame_info.pack(pady=10)

        # Mostrar el ID (no modificable)
        tk.Label(frame_info, text="Código vuelo").pack(fill="x")
        tk.Label(frame_info, text=vuelo.get_idVuelo()).pack(fill="x", pady=(0, 10))

        # Campos editables
        tk.Label(frame_info, text="Origen").pack(fill="x")
        entry_origen = tk.Entry(frame_info)
        entry_origen.insert(0, vuelo.get_origen())
        entry_origen.pack(fill="x", pady=(0, 10))

        tk.Label(frame_info, text="Destino").pack(fill="x")
        entry_destino = tk.Entry(frame_info)
        entry_destino.insert(0, vuelo.get_destino())
        entry_destino.pack(fill="x", pady=(0, 10))

        tk.Label(frame_info, text="Sillas Preferenciales").pack(fill="x")
        entry_pref = tk.Entry(frame_info)
        entry_pref.insert(0, vuelo.get_sillasPreDisp())
        entry_pref.pack(fill="x", pady=(0, 10))

        tk.Label(frame_info, text="Sillas Económicas").pack(fill="x")
        entry_econo = tk.Entry(frame_info)
        entry_econo.insert(0, vuelo.get_sillasEconoDisp())
        entry_econo.pack(fill="x", pady=(0, 10))

        mensaje = tk.Label(ventana_detalle, text="")
        mensaje.pack(pady=10)

        def modificar():
            try:
                codigo = vuelo.get_idVuelo()
                nuevo_origen = entry_origen.get().strip() or None
                nuevo_destino = entry_destino.get().strip() or None
                sillas_premium = int(entry_pref.get().strip()) if entry_pref.get().strip() else None
                sillas_econo = int(entry_econo.get().strip()) if entry_econo.get().strip() else None

                resultado = sistema.modificarVuelo(
                    codigo,
                    nuevo_origen=nuevo_origen,
                    nuevo_destino=nuevo_destino,
                    nuevas_sillasPremium=sillas_premium,
                    nuevas_sillasEcono=sillas_econo
                )

                if resultado:
                    mensaje.config(text="Vuelo modificado con éxito.", fg="green")
                else:
                    mensaje.config(text="No se encontró el vuelo.", fg="red")
            except ValueError:
                mensaje.config(text="Error: Las cantidades deben ser números enteros.", fg="red")
            except Exception as e:
                mensaje.config(text=f"Error inesperado: {str(e)}", fg="red")

        frame_botones = tk.Frame(ventana_detalle)
        frame_botones.pack(pady=20)

        tk.Button(frame_botones, text="Modificar", command=modificar, width=10).pack()

    def Archivos():
        ventana = tk.Tk()
        ventana.title("Archivos")
        ventana.geometry("800x700")

        tk.Label(ventana, text="Archivos").pack(pady=10)

        mensaje = tk.Label(ventana, text="")
        mensaje.pack(pady=10)

        # Función auxiliar para crear una fila
        def fila_archivo(texto, comando_boton):
            frame = tk.Frame(ventana)
            frame.pack(pady=10)

            tk.Label(frame, text=texto.upper()).grid(row=0, column=0, padx=20)
            entry = tk.Entry(frame, width=30)
            entry.grid(row=0, column=1, padx=20)
            boton = tk.Button(
                frame,
                text="Cargar" if "CARGAR" in texto.upper() else "Descargar",
                command=lambda: comando_boton(entry.get())
            )
            boton.grid(row=0, column=2)

        # FUNCIONES DE CARGA (si tienes métodos, puedes reemplazarlos también)
        def cargar_vuelos(nombre_archivo):
            try:
                sistema.importarVuelos(nombre_archivo)
                mensaje.config(text=f"Vuelos cargados desde '{nombre_archivo}'", fg="green")
            except Exception as e:
                mensaje.config(text=f"Error al cargar vuelos: {e}", fg="red")

        def cargar_usuarios(nombre_archivo):
            try:
                sistema.importarUsuarios(nombre_archivo)
                mensaje.config(text=f"Usuarios cargados desde '{nombre_archivo}'", fg="green")
            except Exception as e:
                mensaje.config(text=f"Error al cargar usuarios: {e}", fg="red")

        def cargar_reservas(nombre_archivo):
            try:
                sistema.importarReservas(nombre_archivo)
                mensaje.config(text=f"Reservas cargadas desde '{nombre_archivo}'", fg="green")
            except Exception as e:
                mensaje.config(text=f"Error al cargar reservas: {e}", fg="red")

        def descargar_vuelos(nombre_archivo):
            try:
                sistema.toFileVuelos(nombre_archivo)
                mensaje.config(text=f"Vuelos guardados en '{nombre_archivo}'", fg="green")
            except Exception as e:
                mensaje.config(text=f"Error al guardar vuelos: {e}", fg="red")

        def descargar_usuarios(nombre_archivo):
            try:
                sistema.toFileUsuarios(nombre_archivo)
                mensaje.config(text=f"Usuarios guardados en '{nombre_archivo}'", fg="green")
            except Exception as e:
                mensaje.config(text=f"Error al guardar usuarios: {e}", fg="red")

        def descargar_reservas(nombre_archivo):
            try:
                sistema.toFileReservas(nombre_archivo)
                mensaje.config(text=f"Reservas guardadas en '{nombre_archivo}'", fg="green")
            except Exception as e:
                mensaje.config(text=f"Error al guardar reservas: {e}", fg="red")

        # Crear las filas con sus funciones conectadas
        fila_archivo("Cargar vuelos", cargar_vuelos)
        fila_archivo("Cargar usuarios", cargar_usuarios)
        fila_archivo("Cargar reservas", cargar_reservas)
        fila_archivo("Descargar vuelos", descargar_vuelos)
        fila_archivo("Descargar usuarios", descargar_usuarios)
        fila_archivo("Descargar reservas", descargar_reservas)

        # Botón para volver al inicio
        boton_volver = tk.Button(ventana, text="VOLVER AL INICIO", command=ventana.destroy)
        boton_volver.pack(pady=30)

    tk.Button(ventana, text="Buscar vuelos", command=buscar_vuelos).pack(pady=5)
    tk.Button(ventana, text="Crear vuelo", command=datosVuelo).pack(pady=5)
    tk.Button(ventana, text="Archivos", command=Archivos).pack(pady=5)


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
####YOOOO
    def mostrar_detalle(vuelo):
        ventana = tk.Toplevel()
        ventana.title("Reserva de Vuelo")
        ventana.geometry("500x850")

        # Info del vuelo
        tk.Label(ventana, text="Reserva de Vuelo", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_info = tk.Frame(ventana)
        frame_info.pack(pady=10)
        info = [
            ("Código vuelo", vuelo.get_idVuelo()),
            ("Origen", vuelo.get_origen()),
            ("Destino", vuelo.get_destino()),
            ("Horario", vuelo.get_horario()),
            ("Sillas preferenciales disponibles", vuelo.get_sillasPreDisp()),
            ("Sillas económicas disponibles", vuelo.get_sillasEconoDisp())
        ]
        for texto, val in info:
            tk.Label(frame_info, text=f"{texto}: {val}", anchor="w").pack(fill="x")

        # Selección de sillas
        frame_sel = tk.Frame(ventana)
        frame_sel.pack(pady=10)

        tk.Label(frame_sel, text="Sillas Preferenciales ($850.000)").grid(row=0, column=0, sticky="w")
        entry_pref = tk.Entry(frame_sel, width=10)
        entry_pref.grid(row=0, column=1)

        tk.Label(frame_sel, text="Sillas Económicas ($235.000)").grid(row=1, column=0, sticky="w")
        entry_econo = tk.Entry(frame_sel, width=10)
        entry_econo.grid(row=1, column=1)

        # Total
        frame_total = tk.Frame(ventana)
        frame_total.pack(pady=10)
        tk.Label(frame_total, text="TOTAL A PAGAR:").grid(row=0, column=0)
        entry_total = tk.Entry(frame_total, width=20)
        entry_total.grid(row=0, column=1)

        # Frame pasajeros dinámico
        frame_pasajeros = tk.Frame(ventana)
        frame_pasajeros.pack(pady=10)
        entradas_pasajeros = []
        reserva_temp = None

        def calcular_total_e_ingresar_pasajeros():
            nonlocal reserva_temp, entradas_pasajeros
            entradas_pasajeros.clear()
            for widget in frame_pasajeros.winfo_children():
                widget.destroy()

            try:
                pref = int(entry_pref.get() or "0")
                econ = int(entry_econo.get() or "0")
                total = pref + econ

                if total > 3:
                    messagebox.showerror("Error", "Solo puedes comprar hasta 3 sillas.")
                    return
                if pref > vuelo.get_sillasPreDisp() or econ > vuelo.get_sillasEconoDisp():
                    messagebox.showerror("Error", "No hay suficientes sillas disponibles.")
                    return

                precio_pref = 850000
                precio_econo = 235000
                millas = usuario.getMillas()
                sillas_con_descuento = min(pref, millas // 2000)
                sillas_sin_descuento = pref - sillas_con_descuento

                total_pagar = (sillas_con_descuento * precio_econo) + (sillas_sin_descuento * precio_pref) + (
                            econ * precio_econo)

                # Actualizar total
                entry_total.delete(0, tk.END)
                entry_total.insert(0, f"${total_pagar:,}".replace(",", "."))

                # Crear reserva temporal
                reserva_temp = Reserva("temp", usuario, vuelo, pref, econ, total_pagar, False)

                # Mostrar formulario de pasajeros
                tk.Label(frame_pasajeros, text="Ingrese datos de pasajeros", font=("Helvetica", 12, "bold")).pack(
                    pady=5)
                for i in range(total):
                    frame_p = tk.Frame(frame_pasajeros)
                    frame_p.pack(pady=3)
                    tk.Label(frame_p, text=f"Pasajero {i + 1}").grid(row=0, column=0, columnspan=2)

                    tk.Label(frame_p, text="Nombre:").grid(row=1, column=0)
                    entry_nombre = tk.Entry(frame_p)
                    entry_nombre.grid(row=1, column=1)

                    tk.Label(frame_p, text="Documento:").grid(row=2, column=0)
                    entry_doc = tk.Entry(frame_p)
                    entry_doc.grid(row=2, column=1)

                    entradas_pasajeros.append((entry_nombre, entry_doc))

            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa solo números.")

        def confirmar_reserva():
            nonlocal reserva_temp
            if not reserva_temp:
                messagebox.showerror("Error", "Primero calcula el total e ingresa los pasajeros.")
                return

            pasajeros = []
            for entry_nombre, entry_doc in entradas_pasajeros:
                nombre = entry_nombre.get().strip()
                doc = entry_doc.get().strip()
                if not nombre or not doc:
                    messagebox.showerror("Error", "Todos los pasajeros deben tener nombre y documento.")
                    return
                pasajeros.append(Pasajero(nombre, doc))

            id_reserva = sistema.generar_id_unico()

            nueva_reserva = Reserva(
                id_reserva,
                usuario,
                vuelo,
                reserva_temp.getCantSillasPref(),
                reserva_temp.getCantSillasEcono(),
                reserva_temp.getPrecioTotal(),
                True
            )

            # Redimir millas y actualizar vuelo
            usuario.redimirMillas(min(reserva_temp.getCantSillasPref(), usuario.getMillas() // 2000) * 2000)
            vuelo.set_sillasPreDisp(vuelo.get_sillasPreDisp() - reserva_temp.getCantSillasPref())
            vuelo.set_sillasEconoDisp(vuelo.get_sillasEconoDisp() - reserva_temp.getCantSillasEcono())

            sistema.addReserva(nueva_reserva)
            messagebox.showinfo("Reserva completada", f"Reserva ID: {id_reserva} creada con éxito.")
            ventana.destroy()

        # Botones
        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="Calcular Total", command=calcular_total_e_ingresar_pasajeros).pack(side="left",
                                                                                                          padx=10)
        tk.Button(frame_botones, text="Confirmar Reserva", command=confirmar_reserva).pack(side="right", padx=10)

        def ventana_pago():
            ventana = tk.Toplevel()
            ventana.title("Pagos - Tarjeta")
            ventana.geometry("400x450")

            fuente = ("Helvetica", 10)

            tk.Label(ventana, text="Pagos - Tarjeta", font=("Helvetica", 18, "bold")).pack(pady=20)


            frame = tk.Frame(ventana)
            frame.pack(pady=10)

            tk.Label(frame, text="Nombre del titular", font=fuente, anchor="w").pack(fill="x")
            entry_nombre = tk.Entry(frame)
            entry_nombre.pack(fill="x", pady=5)

            tk.Label(frame, text="ID", font=fuente, anchor="w").pack(fill="x")
            entry_id = tk.Entry(frame)
            entry_id.pack(fill="x", pady=5)

            tk.Label(frame, text="Numero de tarjeta", font=fuente, anchor="w").pack(fill="x")
            entry_tarjeta = tk.Entry(frame)
            entry_tarjeta.pack(fill="x", pady=5)

            tk.Label(frame, text="Codigo de seguridad", font=fuente, anchor="w").pack(fill="x")
            entry_cvv = tk.Entry(frame, show="*")
            entry_cvv.pack(fill="x", pady=5)

            def pagar():
                try:
                    nombre = entry_nombre.get().strip()
                    id_usuario = entry_id.get().strip()
                    tarjeta = entry_tarjeta.get().strip()
                    cvv = entry_cvv.get().strip()

                    if not nombre or not id_usuario or not tarjeta or not cvv:
                        messagebox.showerror("Error", "Por favor completa todos los campos.")
                        return

                    int_id = int(id_usuario)
                    int_cvv = int(cvv)
                    int_tarjeta = int(tarjeta)


                except ValueError:
                    messagebox.showerror("Error", "El ID, el cvv y el numero de tajerta deben ser números enteros.")
                    return

                messagebox.showinfo("Pago", "Pago realizado con éxito.")
                # id_reserva = generar_id_reserva()
                # precio = reserva_temp.calcularPrecio()
                # nueva_reserva = Reserva(id_reserva, usuario, vuelo, reserva_temp.getSillasPref(),reserva_temp.getSillasEcono(), precio, False)

                ventana.destroy()

            tk.Button(ventana, text="Pagar", command=pagar, bg="black", fg="white", width=15).pack(pady=20)

        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=20)

        #tk.Button(frame_botones, text="Total", command=calcular_total_e_ingresar_pasajeros(), width=10).pack(side="left", padx=10)
        #tk.Button(frame_botones, text="Reservar", command=ventana_pago, width=10).pack(side="left", padx=10)

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

    def consultar_reservas(usuario):
        ventana = tk.Toplevel()
        ventana.title("Consultar reservas")
        ventana.geometry("600x500")

        tk.Label(ventana, text="Consultar reservas", font=("Helvetica", 12)).pack(pady=10)

        reservas = usuario.getReservas()

        if not reservas:
            return

        def modificar_reserva(reserva):
            ventana_mod = tk.Toplevel()
            ventana_mod.title("Modificar reservas")
            ventana_mod.geometry("300x400")

            tk.Label(ventana_mod, text="Reserva", font=("Helvetica", 12)).pack(pady=10)

            vuelo = reserva.getVuelo()

            try:
                info_labels = [
                    ("Código vuelo", vuelo.get_idVuelo()),
                    ("Origen", vuelo.get_origen()),
                    ("Destino", vuelo.get_destino()),
                    ("Horario", vuelo.get_horario()),
                    ("Sillas preferenciales reservadas", reserva.getCantSillasPref()),
                    ("Sillas económicas reservadas", reserva.getCantSillasEcono())
                ]
            except Exception as e:
                tk.Label(ventana_mod, text=f"Error: {str(e)}", fg="red").pack()
                return

            frame_info = tk.Frame(ventana_mod)
            frame_info.pack(pady=10, expand=True)

            for texto, valor in info_labels:
                tk.Label(
                    frame_info,
                    text=f"{texto}: {valor}",
                    font=("Helvetica", 10),
                    anchor="center",
                    justify="center"
                ).pack(fill="x", padx=10, pady=4)

            frame_botones = tk.Frame(ventana_mod)
            frame_botones.pack(pady=20)

            def eliminar_reserva():
                confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar esta reserva?")
                if confirm:
                    usuario = reserva.getUsuario()
                    id_reserva = reserva.getIdReserva()

                    usuario.getReservas().remove(reserva)

                    # Elimina del sistema usando el método
                    if sistema.removeReserva(id_reserva):
                        messagebox.showinfo("Eliminado", "La reserva ha sido eliminada.")
                    else:
                        messagebox.showwarning("Error", "No se pudo eliminar la reserva del sistema.")

                    ventana_mod.destroy()

            tk.Button(frame_botones, text="Eliminar reserva", command=eliminar_reserva, bg="red", fg="white").pack(
                side="left", padx=10)
            tk.Button(frame_botones, text="Volver", command=ventana_mod.destroy).pack(side="left", padx=10)

        contenedor = tk.Frame(ventana)
        contenedor.pack(pady=10)

        for reserva in reservas:
            vuelo = reserva.getVuelo()
            descripcion = f"{reserva.getIdReserva()} - {vuelo.get_idVuelo()}\n{vuelo.get_origen()} - {vuelo.get_destino()} - {vuelo.get_horario()}"

            frame_reserva = tk.Frame(contenedor, pady=10)
            frame_reserva.pack(fill="x")

            tk.Label(frame_reserva, text=descripcion, justify="left").pack(side="left", padx=10)
            tk.Button(frame_reserva, text="Modificar reserva", command=lambda r=reserva: modificar_reserva(r)).pack(
                side="right", padx=10)

    tk.Button(ventana, text="Buscar vuelos", command=buscar_vuelos).pack(pady=5)
    tk.Button(ventana, text="Consultar reservas", command=lambda: consultar_reservas(usuario)).pack(pady=5)

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
                    ventana_admin(Administrador)

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

            sistema.cambiarContraseña(id, contraseña_ant, contraseña_nueva)

            # Mostrar mensaje de éxito
            mensaje_label.config(text=f"Contraseña cambiada con éxito", fg="green")
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
            id_usuario = int(entry2.get())
            numero_reserva = int(entry1.get())

            reserva_encontrada = None
            for reserva in sistema.getReservas():
                if reserva.getUsuario().getIdUsuario() == id_usuario and reserva.getIdReserva() == numero_reserva:
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