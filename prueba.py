from SistemaAerolinea import SistemaAerolinea
class prueba:
    sis = SistemaAerolinea()
    sis.importarVuelos("vuelos.txt")
    for vuelo in sis._SistemaAerolinea__vuelos:
        print(
            f"{vuelo.get_idVuelo()} - {vuelo.get_origen()} -> {vuelo.get_destino()}, {vuelo.get_horario()}, Pref: {vuelo.get_sillasPreDisp()}, Econo: {vuelo.get_sillasEconoDisp()}")

