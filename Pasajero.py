class Pasajero:
    def __init__(self, nombre, id):
        self.__nombre = nombre
        self.__id = id

    def getId(self):
        return self.__id

    def getNombre(self):
        return self.__nombre

    def setNombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    def setId(self, nueva_id):
        self.__id = nueva_id
        
    def toString(self):
        return f'Nombre:{self.__nombre}. Id: {self.__id}'
