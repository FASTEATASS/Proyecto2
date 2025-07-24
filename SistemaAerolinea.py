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

    def
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
                    pasajeros_str = "|".join(
                        [f"{p.getNombre()},{p.getId()}" for p in reserva.getPasajeros()]
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
                        f"{reserva.getMillasRedimidas()}"
                    )
                    file.write(linea + '\n')
            return True
        except Exception as e:
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
                        id_reserva = datos[0]
                        id_usuario = datos[1]
                        id_vuelo = datos[2]
                        usuario = next((u for u in self.__usuarios if u.getIdUsuario() == id_usuario), None)
                        vuelo = next((v for v in self.__vuelos if v.get_idVuelo() == id_vuelo), None)
                        reserva = Reserva(
                            id_reserva, usuario, vuelo,
                            int(datos[3]), int(datos[4]),
                            float(datos[7]), datos[8].lower() == 'true'
                        )
                        reserva.setEstadoCheckIn(datos[6].lower() == 'true')
                        if datos[5]:
                            for p_str in datos[5].split(','):
                                if '|' in p_str:
                                    nombre, id_p = p_str.split('|')
                                    reserva.addPasajero(Pasajero(nombre.strip(), id_p.strip()))
                        nuevas_reservas.append(reserva)
                    except Exception as e:
                        continue
            self.__reservas = nuevas_reservas
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

