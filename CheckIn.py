class CheckIn:
    def __init__(self, reserva):
        self.__reserva = reserva
        self.__maletas = []
        self.__millas = 500
        self.__costoEquipaje = 0
        self.__cantMaletasBodega = 0
        self.__cantMaletasCabina = 0

    def procesar(self):
        self.getCostoEquipaje()
        self.__reserva.usuario.millas += 500
        self.__reserva.estadoCheckIn = True

    def addMaletaBodega(self, maleta):
        self.__cantMaletasBodega += 1
        self.__maletas.append(maleta)
        if self.__cantMaletasBodega > self.__reserva.cantSillasPref:
            self.__costoEquipaje += 40.000

    def addMaletaCabina(self, maleta):
        self.__cantMaletasCabina += 1
        self.__maletas.append(maleta)
        if self.__cantMaletasCabina > self.__reserva.cantSillasPref:
            self.__costoEquipaje += (maleta.peso * 5000)

    def getCostoEquipaje(self):
        return self.__costoEquipaje

    def getMaletaBodega(self):
        return self.__cantMaletasBodega

    def getMaletaCabina(self):
        return self.__cantMaletasCabina