from Usuario import Usuario


class Administrador(Usuario):
    def __init__(self, nombre, idUsuario, contraseña, correoElectronico):
        super().__init__(nombre, idUsuario, contraseña, correoElectronico)
        self.vuelos = []

    def verificarVuelo(self, codigo):
        for i in range(len(self.vuelos)):
            if (self.vuelos[i].get_idVuelo() == codigo):
                return (i)

        return (-1)

    def crearVuelo(self, codigo, origen, destino, horario, sillasPremium, sillasEcono):
        if self.verificarVuelo(codigo) != -1:
            return False

        else:
            self.vuelos.append(codigo, origen, destino, horario, sillasPremium, sillasEcono)
            return True

    def consultarVuelo(self, codigo):
        inx = self.verificarVuelo(codigo)
        if inx == -1:
            print("El vuelo no existe")

        else:
            vuelo = self.vuelos[inx]
            print("Origen:", vuelo.get_origen(), "\n",
                  "Destino:", vuelo.get_destino(), "\n",
                  "Horario:", vuelo.get_horario(), "\n",
                  "Cantidad sillas preferencial:", vuelo.get_sillasPreDisp(), "\n",
                  "Cantidad sillas economicas:", vuelo.sillasEconoDisp())