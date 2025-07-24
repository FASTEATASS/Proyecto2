from Usuario import Usuario
from Vuelo import Vuelo
from CheckIn import CheckIn
from Reserva import Reserva
from Pasajero import Pasajero
from MaletaBodega import MaletaBodega
from MaletaCabina import MaletaCabina

class SistemaAerolinea:
    def __init__(self):
        self.__vuelos = []
        self.__usuarios = []
        self.__reservas = []
        self.__no_usuarios = None

    def verificarVuelo(self, codigo):
        for i, vuelo in enumerate(self.__vuelos):
            if vuelo.get_idVuelo() == codigo:
                return i
        return -1

    def crearVuelo(self, codigo, origen, destino, horario, sillasPremium, sillasEcono):
        if self.verificarVuelo(codigo) != -1:
            return False
        nuevo_vuelo = Vuelo(codigo, origen, destino, horario, sillasPremium, sillasEcono)
        self.__vuelos.append(nuevo_vuelo)
        return True

    def modificarVuelo(self, codigo, nuevo_origen=None, nuevo_destino=None, nuevo_horario=None,
                       nuevas_sillasPremium=None, nuevas_sillasEcono=None):
        inx = self.verificarVuelo(codigo)
        if inx == -1:
            return False

        vuelo = self.__vuelos[inx]
        if nuevo_origen: vuelo.set_origen(nuevo_origen)
        if nuevo_destino: vuelo.set_destino(nuevo_destino)
        if nuevo_horario: vuelo.set_horario(nuevo_horario)
        if nuevas_sillasPremium is not None: vuelo.set_sillasPreDisp(nuevas_sillasPremium)
        if nuevas_sillasEcono is not None: vuelo.set_sillasEconoDisp(nuevas_sillasEcono)
        return True

    def addReserva(self, Reserva):
        self.__reservas.append(Reserva)

    def getVuelos(self):
        return self.__vuelos

    def getReservas(self):
        return self.__reservas

    def verificarUsuario(self, idUsuario):
        for i, usuario in enumerate(self.__usuarios):
            if usuario.getIdUsuario() == idUsuario:
                return i
        return -1

    def logIn(self, idUsuario, contraseña):
        for usuario in self.__usuarios:
            if usuario.validarCredenciales(idUsuario, contraseña):
                return usuario
        return None

    def cambiarContraseña(self, idUsuario, contraseñaVieja, contraseñaNueva):
        for usuario in self.__usuarios:
            if usuario.getIdUsuario() == idUsuario:
                if usuario.validarCredenciales(idUsuario, contraseñaVieja):
                    usuario.setContraseña(contraseñaNueva)
                    return True
                else:
                    return False
        return False

    def registrarUsuario(self, nuevoUsuario):
        if self.verificarUsuario(nuevoUsuario.getIdUsuario()) != -1:
            return False
        self.__usuarios.append(nuevoUsuario)
        return True

    def buscarVuelo(self, origen, destino):
        v_filtrados = [
            vuelo for vuelo in self.__vuelos
            if vuelo.get_origen().upper() == origen.get().upper() and vuelo.get_destino().upper() == destino.get().upper()
        ]
        return v_filtrados

    def toFileReservas(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for reserva in self.__reservas:
                    # Formato: "Nombre|ID,Nombre2|ID2"
                    pasajeros_str = ",".join(
                        [f"{p.getNombre()}|{p.getId()}" for p in reserva.getPasajeros()]
                    )
                    linea = (
                        f"{reserva.getIdReserva()},"
                        f"{reserva.getUsuario().getIdUsuario()},"
                        f"{reserva.getVuelo().get_idVuelo()},"
                        f"{reserva.getCantSillasPref()},"
                        f"{reserva.getCantSillasEcono()},"
                        f"{pasajeros_str},"
                        f"{reserva.getEstadoCheckIn()},"
                        f"{reserva.getPrecioTotal()},"
                        f"{reserva.getMillasRedimidas()}\n"
                    )
                    file.write(linea)
            return True
        except Exception as e:
            print(f"Error al guardar: {str(e)}")
            return False

    def importarReservas(self, filename):
        nuevas_reservas = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for linea in file:
                    datos = linea.strip().split(',')
                    if len(datos) < 9:
                        continue

                    try:
                        # Buscar usuario y vuelo
                        usuario = next((u for u in self.__usuarios if u.getIdUsuario() == datos[1]), None)
                        vuelo = next((v for v in self.__vuelos if v.get_idVuelo() == datos[2]), None)
                        if not usuario or not vuelo:
                            continue

                        # Crear reserva
                        reserva = Reserva(
                            datos[0], usuario, vuelo,
                            int(datos[3]), int(datos[4]),  # sillas_pref, sillas_econo
                            float(datos[7]),  # precio_total
                            datos[8].lower() == 'true'  # millas_redimidas
                        )
                        reserva.setEstadoCheckIn(datos[6].lower() == 'true')

                        # Añadir pasajeros (formato: "Nombre|ID,Nombre2|ID2")
                        if datos[5]:
                            for p_str in datos[5].split(','):
                                nombre, id_p = p_str.split('|')
                                reserva.addPasajero(Pasajero(nombre.strip(), id_p.strip()))

                        nuevas_reservas.append(reserva)

                    except (ValueError, AttributeError) as e:
                        print(f"Error en línea: {linea} - {str(e)}")
                        continue

            self.__reservas = nuevas_reservas
            return True
        except FileNotFoundError:
            print(f"Archivo no encontrado: {filename}")
            return False
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return False

    def toFileUsuarios(self, filename):
        """
        Guarda usuarios en formato:
        nombre,id,contraseña,correo,millas[,reservas]
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for u in self.__usuarios:
                    # Obtener IDs de reservas (maneja caso cuando getReservas() retorna strings u objetos)
                    reservas = u.getReservas()
                    reservas_str = ''

                    if reservas:
                        if isinstance(reservas[0], str):  # Si son strings (IDs)
                            reservas_str = '|'.join(reservas)
                        else:  # Si son objetos Reserva
                            reservas_str = '|'.join([r.getIdReserva() for r in reservas if hasattr(r, 'getIdReserva')])

                    # Escribir línea (siempre incluye la coma final para reservas, aunque esté vacía)
                    linea = f"{u.getNombre()},{u.getIdUsuario()},{u.getContraseña()},{u.getCorreo()},{u.getMillas()},{reservas_str}\n"
                    file.write(linea)

            print(f"✅ Usuarios guardados correctamente en {filename}")
            return True
        except Exception as e:
            print(f"❌ Error al guardar usuarios: {e}")
            return False

    def importarUsuarios(self, filename):
        """
        Importa usuarios desde archivo con formato:
        nombre,id,contraseña,correo,millas[,reservas]
        """
        try:
            nuevos_usuarios = []
            with open(filename, 'r', encoding='utf-8') as file:
                for linea in file:
                    # Dividir línea y limpiar elementos
                    datos = [d.strip() for d in linea.strip().split(',')]

                    # Validar campos mínimos (5 campos obligatorios)
                    if len(datos) < 5:
                        print(f"⚠ Línea ignorada (faltan datos): {linea}")
                        continue

                    # Procesar datos básicos
                    try:
                        usuario = Usuario(
                            nombre=datos[0],
                            idUsuario=int(datos[1]),
                            contraseña=datos[2],
                            correoElectronico=datos[3]
                        )
                        usuario.setMillas(int(datos[4]) if datos[4].isdigit() else 0)

                        # Procesar reservas (campo opcional después de la 5ta coma)
                        if len(datos) > 5 and datos[5]:
                            for id_reserva in datos[5].split('|'):
                                if id_reserva.strip():
                                    usuario.addReserva(id_reserva.strip())

                        nuevos_usuarios.append(usuario)

                    except Exception as e:
                        print(f"⚠ Error procesando línea '{linea}': {e}")
                        continue

            self.__usuarios = nuevos_usuarios
            print(f"✅ Se importaron {len(nuevos_usuarios)} usuarios de {filename}")
            return True

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {filename}")
            return False
        except Exception as e:
            print(f"❌ Error crítico: {str(e)}")
            return False

    def importarVuelos(self, filename):
        try:
            vuelos = []
            with open(filename, 'r', encoding='utf-8') as file:
                for linea in file:
                    datos = linea.strip().split('\t')
                    if len(datos) < 7:
                        continue
                    idVuelo = datos[0]
                    origen = datos[1]
                    destino = datos[2]
                    hora = datos[3] + " " + datos[4]
                    sillasPref = int(datos[5])
                    sillasEcono = int(datos[6])
                    v = Vuelo(idVuelo, origen, destino, hora, sillasPref, sillasEcono)
                    vuelos.append(v)
            self.__vuelos = vuelos
            return True
        except Exception as e:
            return False

    def toFileVuelos(self, filename):
        """
        Guarda los vuelos en formato compatible con importarVuelos:
        idVuelo\torigen\tdestino\tdia\thora\tsillasPref\tsillasEcono

        Args:
            filename (str): Ruta del archivo de salida

        Returns:
            bool: True si se guardó correctamente, False si hubo error
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for vuelo in self.__vuelos:
                    # Separar día y hora del horario
                    horario = vuelo.get_horario().split(' ', 1)
                    dia = horario[0] if len(horario) > 0 else ""
                    hora = horario[1] if len(horario) > 1 else ""

                    linea = (
                        f"{vuelo.get_idVuelo()}\t"
                        f"{vuelo.get_origen()}\t"
                        f"{vuelo.get_destino()}\t"
                        f"{dia}\t"
                        f"{hora}\t"
                        f"{vuelo.get_sillasPreDisp()}\t"
                        f"{vuelo.get_sillasEconoDisp()}\n"
                    )
                    file.write(linea)
            return True
        except Exception as e:
            print(f"Error al guardar vuelos: {str(e)}")
            return False

    def importarCheckins(self, filename):
        try:
            nuevos_checkins = []

            with open(filename, 'r', encoding='utf-8') as file:
                for linea in file:
                    datos = linea.strip().split(',')
                    if len(datos) < 3:
                        continue

                    idReserva = datos[0]
                    millas = int(datos[1])
                    costoEquipaje = float(datos[2])
                    maletas = []

                    for maleta_str in datos[3:]:
                        tipo, peso_str = maleta_str.split('-')
                        peso = float(peso_str)

                        if tipo == 'cabina':
                            m = MaletaCabina(peso)
                        elif tipo == 'bodega':
                            m = MaletaBodega(peso)
                        else:
                            continue

                        maletas.append(m)

                    c = CheckIn(idReserva, maletas, millas, costoEquipaje)
                    nuevos_checkins.append(c)
            self.__checkins = nuevos_checkins
            return True
        except Exception as e:
            return False

    def tofileCheckins(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for checkin in self.__checkins:
                    idReserva = checkin.getReserva()
                    millas = checkin.getMillas()
                    costo = checkin.getCostoEquipaje()
                    maletas = checkin.getMaletas()

                    linea = f"{idReserva},{millas},{costo}"

                    for maleta in maletas:
                        if isinstance(maleta, MaletaCabina):
                            tipo = "cabina"
                        elif isinstance(maleta, MaletaBodega):
                            tipo = "bodega"
                        else:
                            continue

                        linea += f",{tipo}-{maleta.getPeso()}"

                    file.write(linea + '\n')
            return True
        except Exception as e:
            return False

