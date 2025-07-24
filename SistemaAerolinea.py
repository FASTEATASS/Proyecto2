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

    def getVuelos(self):
        return self.__vuelos

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
            with open(filename, 'w', encoding='0utf-8') as file:
                for reserva in self.__reservas:
                    pasajerosStr = '|'.join([p.toString() for p in reserva.getPasajeros()])
                    linea = (
                        f"{reserva.getIdReserva()},"
                        f"{reserva.getUsuario().getIdUsuario()},"
                        f"{reserva.getVuelo().get_idVuelo()},"
                        f"{reserva.getcantSillasPref()},"
                        f"{reserva.getcantSillasEcono()},"
                        f"{pasajerosStr},"
                        f"{reserva.getEstadoCheckin()},"
                        f"{reserva.getPrecioTotal()},"
                        f"{reserva.getMillasREdimidas()}"
                    )
                    file.write(linea + '\n')
            return True
        except Exception as e:
            return False

    def importarReservas(self, filename):
        try:
            nuevasReservas = []
            with open(filename, 'r', encoding='utf-8') as file:
                for linea in file:
                    datos = linea.strip().split(',')
                    if len(datos) < 9:
                        continue
                    idReserva = datos[0]
                    idUsuario = datos[1]
                    idVuelo = datos[2]
                    sillasPref = int(datos[3])
                    sillasEcono = int(datos[4])

                    pasajerosReserva = []
                    datosPasajero = datos[5].split('|')
                    if len(datosPasajero) == 2:
                        p = Pasajero()
                        p.setNombre(datosPasajero[0])
                        p.setId(datosPasajero[1])
                        pasajerosReserva.append(p)

                    estadoCheckin = datos[6].lower() == 'true'
                    precioTotal = float(datos[7])
                    millasRedimidas = datos[8].lower() == 'true'

                    reserva = Reserva(idReserva, idUsuario, idVuelo, sillasPref, sillasEcono, pasajerosReserva, estadoCheckin, precioTotal, millasRedimidas)
                    nuevasReservas.append(reserva)
                self.__reservas = nuevasReservas
                return True
        except Exception as e:
            return False

    def tofileusuarios(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                for u in self.__usuarios:
                    reservasStr = '|'.join([r.getIdReserva() for r in u.getReservas()])
                    linea = (f"{u.getNombre()},"
                             f"{u.getIdUsuario()},"
                             f"{u.getContraseña()},"
                             f"{u.getCorreoElectronico()},"
                             f"{u.getMillas()},"
                             f"{reservasStr}"
                             )
                    file.write(linea + '\n')
            return True
        except Exception:
            return False

    def importarUsuarios(self, filename):
        try:
            nuevos_usuarios = []
            with open(filename, 'r', encoding='utf-8') as file:
                for linea in file:
                    datos = linea.strip().split(',')
                    if len(datos) < 5:
                        continue

                    nombre = datos[0]
                    idUsuario = datos[1]
                    contraseña = datos[2]
                    correo = datos[3]
                    millas = int(datos[4])
                    reservas_ids = datos[5].split('|') if len(datos) == 6 and datos[5] else []

                    u = Usuario(nombre, idUsuario, contraseña, correo)
                    u.setMillas(millas)
                    for idReserva in reservas_ids:
                        u.addReserva(idReserva)

                    nuevos_usuarios.append(u)

            self.__usuarios = nuevos_usuarios
            return True
        except Exception as e:
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

