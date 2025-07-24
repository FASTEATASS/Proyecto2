from Maleta import Maleta
from CheckIn import CheckIn
class Usuario:
    def __init__(self, nombre, idUsuario, contraseña, correoElectronico):
        self.nombre = nombre
        self.idUsuario = idUsuario
        self.contraseña = contraseña
        self.correoElectronico = correoElectronico
        self.millas = 0
        self.reservas = []

    def addReserva(self, idReserva):
        self.reservas.append(idReserva)

    def getNombre(self):
        return self.nombre

    def getIdUsuario(self):
        return self.idUsuario

    def getMillas(self):
        return self.millas

    def getCorreo(self):
        return self.correoElectronico

    def getReservas(self):
        return self.reservas

    def setContraseña(self, contraseña):
        self.contraseña = contraseña

    def setMillas(self, millas):
        self.millas = millas

    def actualizarMillas(self, millasASumar):
        self.millas += millasASumar
        return self.millas

    def redimirMillas(self, millasARedimir):
        if self.millas >= 2000 and millasARedimir >= 2000:
            cantidadSillas = millasARedimir // 2000
            self.millas -= (millasARedimir // 2000)
            return cantidadSillas
        else:
            return "Las millas son insuficientes"

    def validarCredenciales(self, idUsuario, contraseña):
        if self.idUsuario == idUsuario and self.contraseña == contraseña:
            return True
        else:
            return False

    def verificarReserva(self, id):
        for i in range(len(self.reservas)):
            if (self.reservas[i].get_idReserva() == id):
                return i
        return -1

    def cancelarReserva(self, idReserva):
        inx = self.reservas(idReserva)
        if inx == -1:
            return False
        else:
            self.reservas.pop(inx)
            return True

    def modificarReserva(self, reserva):
        id = reserva.get_idReserva()
        inx = self.verificarReserva(id)
        if inx == -1:
            return False
        else:
            self.reservas[inx] = reserva
            return True

    def checkIn(self, idUsuario, ReservaCod, maletas_pesos):
        for reserva in self.reservas:
            if reserva.get_idReserva() == ReservaCod and self.idUsuario == idUsuario:
                if hasattr(reserva, 'checkInRealizado') and reserva.checkInRealizado:
                    print("Ya se ha realizado el check-in para esta reserva.")
                    return False

                maletas = [Maleta(peso) for peso in maletas_pesos]
                checkin = CheckIn(reserva, maletas)
                checkin.procesar()

                reserva.checkInRealizado = True

                print("Check in realizado con éxitos")
                print(f"Millas totales: {checkin.getMillas()}")
                print(f"Costo total por equipaje: ${checkin.getCostoEquipaje()}")
                return True
        print("Reserva no encontrada")
        return False