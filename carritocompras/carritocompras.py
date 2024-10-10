from decimal import Decimal
from principal.models import Producto
from django.shortcuts import get_object_or_404

class Carrito():

    """
    Aqui se van a crear las funciones que van a ser utilizadas en el carrito de compras
    aqui se da la logica, por ejemplo agregar un producto, disminuir producto, calcular el precio total del carro,
    entre otras funcionalidades que pueden ser implementadas en caso de mejora 
    """

    def __init__(self, request):
        """
        el carrito funciona con sesiones, esto quiere decir que para cada usuario
        que agregue productos en el carrito de compras, se almacenara en una clase carrito distinta.
        """

        self.session = request.session
        carrito = self.session.get('skey') #sesionkey
        if 'skey' not in request.session:
            carrito = self.session['skey'] = {

            }
        self.carrito = carrito

    def agregar(self, producto, qty):
        """
          funcion que agrega un producto al carrito de compras
        """

        producto_id = str(producto.id)

        if producto_id in self.carrito:
            self.carrito[producto_id]['qty'] = qty
        else:
            self.carrito[producto_id] = {'precio': str(producto.precio), 'qty' : qty, 'id_producto': str(producto.id)}

            self.guardar()

    def __iter__(self):
        """
        funcion que permite iterar sobre un producto, se crea una copia del mismo para que no hayan errores de duplicados
        """

        producto_ids = self.carrito.keys()
        objects = Producto.objects.filter(id__in = producto_ids) #aqui utilize objects como declaracion de variable de otra forma me tira error y no reconoce objects cuando traigo los productos.
        carrito = self.carrito.copy()

        for producto in objects:
            carrito[str(producto.id)]['producto'] = producto

        for item in carrito.values():
            item['precio'] = Decimal(item['precio'])
            item['total_precio'] = item['precio'] * item['qty']
            yield item

    def __len__(self):
        """
        funcion que muestra la cantidad de productos almacenados en el carrito de compras
        """
        return sum(item['qty'] for item in self.carrito.values())
    
    def get_subtotal_precio(self):
        """
        funcion que calcula el total de los productos.
        """

        return sum(Decimal(item['precio']) * item['qty'] for item in self.carrito.values())
    
    def get_total_precio(self):
        """
        funcion que calcula el precio total de la compra
        """

        subtotal = sum(Decimal(item['precio']) * item['qty'] for item in self.carrito.values())

        if subtotal ==0: # el subtotal de la compra es 0
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(3.500) #3.500 es el costo de envio
        
        total = subtotal + Decimal(shipping) #al subtotal del producto se le agrega el costo del envio y esto seria el pago total que hace un usuario
        return total

    def eliminar(self, producto):
        """
        funcion que elimina un producto del carrito de compras
        """

        producto_id = str(producto)

        if producto_id in self.carrito:
            del self.carrito[producto_id]
            print(producto_id)
            self.guardar()
    
    def modificar(self, producto, qty):
        "modificar un producto desde el carro de compras"

        producto_id = str(producto)

        if producto_id in self.carrito:
            self.carrito[producto_id]['qty'] = qty

        self.guardar()

    def clear(self):
        """
        eliminar carrito de la sesion
        """

        del self.session['skey']
        self.guardar()

    def disminuirStock(self, producto):

        """
        disminuir stock cuando la compre este realizada, cuando el producto llegue a 0, se borra de la BD.
        """

        producto_id = producto
        qty = self.carrito[str(producto_id)]['qty']
        productos = get_object_or_404(Producto, id = int(producto_id))

        if productos.stock >= int(qty):
            productos.stock -= int(qty)
            productos.save()

            if productos.stock == 0:
                productos.delete()

    def guardar(self):
        self.session.modified = True
