from Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, nombre, idUsuario, contraseña, correoElectronico):
        super().__init__(nombre, idUsuario, contraseña, correoElectronico)


    def crearVuelo(self, sistema, codigo, origen, destino, horario, sillasPremium, sillasEcono):
        return sistema.crearVuelo(codigo, origen, destino, horario, sillasPremium, sillasEcono)

    def modificarVuelo(self, sistema, codigo, nuevo_origen=None, nuevo_destino=None, nuevo_horario=None,
                       nuevas_sillasPremium=None, nuevas_sillasEcono=None):
        return sistema.modificarVuelo(codigo, nuevo_origen, nuevo_destino, nuevo_horario,
                                      nuevas_sillasPremium, nuevas_sillasEcono)