class Reserva:
    def _init_(self, idReserva, usuario, vuelo, cantSillasPref, cantSillasEcono, precioTotal, millasRedimidas):
        self.__idReserva = idReserva
        self.__usuario = usuario
        self.__vuelos = vuelo
        self.__cantSillasPref = cantSillasPref
        self.__cantSillasEcono = cantSillasEcono
        self.__pasajeros = []
        self.__estadoCheckIn = False
        self.__precioTotal = precioTotal
        self.__millasRedimidas = millasRedimidas

    def calcularPrecio(self):
        self._precioTotal = (self.cantSillasPref * 850000) + (self._cantSillasEcono * 235000)
        return self.__precioTotal

    def pagarReserva(self):
        if self._millasRedimidas and self._usuario.millas > 2000:
            sillasARedimir = self.__usuario.millas // 2000
            if sillasARedimir <= self.__cantSillasPref:
                self.__precioTotal -= (sillasARedimir * 615000)
            else:
                self._precioTotal -= (self._cantSillasPref * 615000)

        return True

    def yaHizoCheckin(self):
        return self.__estadoCheckIn

    def setEstadoCheckIn(self, estadoCheckIn):
        self.__estadoCheckIn = estadoCheckIn

    def getIdReserva(self):
        return self.__idReserva

    def addPasajero(self, pasajero):
        self.__pasajeros.append(pasajero)

    def getPasajeros(self):
        for pasajero in self.__pasajeros:
            print(pasajero.toString())

    def getUsuario(self):
        return self.__usuario