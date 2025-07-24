class Reserva:
    def __init__(self, idReserva, usuario, vuelo, cantSillasPref, cantSillasEcono, precioTotal, millasRedimidas):
        self.__idReserva = idReserva
        self.__usuario = usuario
        self.__vuelos = vuelo
        self.__cantSillasPref = cantSillasPref
        self.__cantSillasEcono = cantSillasEcono
        self.__pasajeros = []
        self.__estadoCheckIn = False
        self.__precioTotal = precioTotal
        self.__millasRedimidas = millasRedimidas
        self.__cantPasajeros = 0

    def calcularPrecio(self):
        self.__precioTotal = (self.__cantSillasPref * 850000) + (self.__cantSillasEcono * 235000)
        return self.__precioTotal

    def pagarReserva(self):
        if self.__millasRedimidas and self.__usuario.millas > 2000:
            sillasARedimir = self.__usuario.millas // 2000
            if sillasARedimir <= self.__cantSillasPref:
                self.__precioTotal -= (sillasARedimir * 615000)
            else:
                self.__precioTotal -= (self.__cantSillasPref * 615000)

        return True

    def yaHizoCheckin(self):
        return self.__estadoCheckIn

    def setEstadoCheckIn(self, estadoCheckIn):
        self.__estadoCheckIn = estadoCheckIn

    def getIdReserva(self):
        return self.__idReserva

    def addPasajero(self, pasajero):
        if self.__cantPasajeros < 3:
            self.__pasajeros.append(pasajero)
            self.__cantPasajeros +=1
            return True
        else:
            return False


    def getPasajeros(self):
        for pasajero in self.__pasajeros:
            print(pasajero.toString())

    def getUsuario(self):
        return self.__usuario