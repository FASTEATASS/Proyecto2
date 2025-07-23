class Vuelo:
    def __init__(self, idVuelo, origen, destino, horario, noSillasPref, noSillasEcono):
        self.__idVuelo = idVuelo
        self.__origen = origen
        self.__destino = destino
        self.__horario = horario
        self.__noSillasPref = noSillasPref
        self.__noSillasEcono = noSillasEcono

    def get_idVuelo(self):
        return self.__idVuelo

    def get_origen(self):
        return self.__origen

    def get_destino(self):
        return self.__destino

    def get_horario(self):
        return self.__horario

    def get_sillasPreDisp(self):
        return self.__noSillasPref

    def get_sillasEconoDisp(self):
        return self.__noSillasEcono

    def set_origen(self, nuevo_origen):
        self.__origen = nuevo_origen

    def set_destino(self, nuevo_destino):
        self.__destino = nuevo_destino

    def set_horario(self, nuevo_horario):
        self.__horario = nuevo_horario

    def set_sillasPreDisp(self, nuevas_sillas_pref):
        self.__noSillasPref = nuevas_sillas_pref

    def set_sillasEconoDisp(self, nuevas_sillas_econo):
        self.__noSillasEcono = nuevas_sillas_econo