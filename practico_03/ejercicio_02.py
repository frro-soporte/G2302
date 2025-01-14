"""Variables y Métodos de Clase"""
import itertools


class Articulo:
    """Clase con "nombre" como variable de instancia y un id incremental
    generado automáticamente.

    Restricciones:
        - Utilizar sólamente el constructor (__init__) y un método de
          clase (@classmethod) con una variable de clase
    """

    counter = itertools.count(1)
    _last_id  = 0

    def __init__(self, name= "") :
        self.nombre = name
        self.id_ = next(Articulo.counter)
        Articulo._last_id = self.id_

    @classmethod
    def Nombre(self):
        return self.name

    def display(self):
       return {self.name, self.id_}
    # Completar


# NO MODIFICAR - INICIO
art1 = Articulo("manzana")
art2 = Articulo("pera")
art3 = Articulo()
art3.nombre = "tv"

assert art1.nombre == "manzana"
assert art2.nombre == "pera"
assert art3.nombre == "tv"
assert art1.id_ == 1
assert art2.id_ == 2
assert art3.id_ == 3
assert Articulo._last_id == 3
# NO MODIFICAR - FIN
