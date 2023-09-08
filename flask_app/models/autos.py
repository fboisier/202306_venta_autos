import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
from flask_app.models.usuarios import Usuario

class Auto:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.modelo = data['modelo']
        self.precio = data['precio']
        self.marca = data['marca']
        self.anio = data['anio']
        self.descripcion = data['descripcion']
        self.usuario_id = data['usuario_id']
        self.usuario = None
        self.comprador_id = data.get('comprador_id')
        self.comprador = None
        self.vendido = data['vendido']

    def __str__(self) -> str:
        return f"{self.modelo}"


    @classmethod
    def validar(cls, formulario):

        errores = []

        if len(formulario['modelo']) == 0:
            errores.append(
                "modelo es obligatorio"
            )
        if len(formulario['marca']) == 0:
            errores.append(
                "marca es obligatorio"
            )
        if len(formulario['descripcion']) == 0:
            errores.append(
                "descripcion es obligatorio"
            )

        if len(formulario['precio']) == 0:
            errores.append(
                "precio es obligatorio"
            )

        if len(formulario['anio']) == 0:
            errores.append(
                "anio es obligatorio"
            )


        if formulario['precio'] != "" and int(formulario['precio']) <= 0:
            errores.append(
                "no puede ser 0 o menor el precio. debe ser mayor"
            )

        if formulario['anio'] != "" and int(formulario['anio']) <= 0:
            errores.append(
                "no puede ser 0 o menor el año. debe ser mayor"
            )

        return errores

    @classmethod
    def get_all(cls, comprador_id = None):
        resultados_instancias = []

        data = {}
        query = "SELECT * FROM autos"
        
        if comprador_id:
            query += " WHERE comprador_id = %(comprador_id)s"
            data["comprador_id"] = comprador_id


        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)
        print(resultados)
        for resultado in resultados:
            instancia = cls(resultado)

            instancia.usuario = Usuario.get(instancia.usuario_id)
            if instancia.comprador_id:
                instancia.comprador = Usuario.get(instancia.comprador_id)

            resultados_instancias.append(instancia)

        return resultados_instancias

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO autos (modelo, precio, marca, anio, descripcion, usuario_id) VALUES (%(modelo)s, %(precio)s, %(marca)s, %(anio)s, %(descripcion)s, %(usuario_id)s);"
        data = {
            **data,
            "usuario_id": session['usuario']['id'],
        }

        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get(cls, id ):
        query = "SELECT * FROM autos WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            instancia = cls(resultados[0])
            instancia.usuario = Usuario.get(instancia.usuario_id)
            if instancia.comprador_id:
                instancia.comprador = Usuario.get(instancia.comprador_id)
            return instancia
        
        return None
    
    
    @classmethod
    def eliminar(cls, id ):
        query = "DELETE FROM autos WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def delete(self):
        query = "DELETE FROM autos WHERE id = %(id)s;"
        data = { 'id': self.id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def update(self):
        query = "UPDATE autos SET modelo = %(modelo)s, precio = %(precio)s, marca = %(marca)s, anio = %(anio)s, descripcion = %(descripcion)s WHERE id = %(id)s"
        data = {
            'id': self.id,
            'modelo': self.modelo,
            'precio': self.precio,
            'marca': self.marca,
            'anio': self.anio,
            'descripcion': self.descripcion,
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def vender(self):
        query = "UPDATE autos SET comprador_id = %(comprador_id)s, vendido = 1 WHERE id = %(id)s"
        data = {
            'id': self.id,
            'comprador_id': session['usuario']['id'],
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    