from Maleta import Maleta
from CheckIn import CheckIn

class Usuario:
    def __init__(self, nombre, idUsuario, contraseña, correoElectronico):
        self._nombre = nombre
        self._idUsuario = idUsuario
        self._contraseña = contraseña
        self._correoElectronico = correoElectronico
        self.__millas = 0
        self._reservas = []

    def addReserva(self, idReserva):
        self._reservas.append(idReserva)

    def getNombre(self):
        return self._nombre

    def getIdUsuario(self):
        return self._idUsuario

    def getMillas(self):
        return self.__millas

    def getCorreo(self):
        return self._correoElectronico

    def getReservas(self):
        return self._reservas

    def setContraseña(self, contraseña):
        self._contraseña = contraseña

    def setMillas(self, millas):
        self.__millas = millas

    def actualizarMillas(self, millasASumar):
        self.__millas += millasASumar
        return self.__millas

    def redimirMillas(self, millasARedimir):
        if self.__millas >= 2000 and millasARedimir >= 2000:
            cantidadSillas = millasARedimir // 2000
            self.__millas -= (millasARedimir // 2000)
            return cantidadSillas
        else:
            return "Las millas son insuficientes"

    def validarCredenciales(self, idUsuario, contraseña):
        return self._idUsuario == idUsuario and self._contraseña == contraseña

    def verificarReserva(self, id):
        for i in range(len(self._reservas)):
            if self._reservas[i].get_idReserva() == id:
                return i
        return -1

    def cancelarReserva(self, idReserva):
        inx = self.verificarReserva(idReserva)
        if inx == -1:
            return False
        else:
            self._reservas.pop(inx)
            return True

    def modificarReserva(self, reserva):
        id = reserva.get_idReserva()
        inx = self.verificarReserva(id)
        if inx == -1:
            return False
        else:
            self._reservas[inx] = reserva
            return True

    def checkIn(self, idUsuario, ReservaCod, maletas_pesos):
        for reserva in self._reservas:
            if reserva.get_idReserva() == ReservaCod and self._idUsuario == idUsuario:
                if hasattr(reserva, 'checkInRealizado') and reserva.checkInRealizado:
                    print("Ya se ha realizado el check-in para esta reserva.")
                    return False

                maletas = [Maleta(peso) for peso in maletas_pesos]
                checkin = CheckIn(reserva, maletas)
                checkin.procesar()

                reserva.checkInRealizado = True

                print("Check in realizado con éxito")
                print(f"Millas totales: {checkin.getMillas()}")
                print(f"Costo total por equipaje: ${checkin.getCostoEquipaje()}")
                return True
        print("Reserva no encontrada")
        return False