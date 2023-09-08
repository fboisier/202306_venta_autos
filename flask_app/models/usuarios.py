import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utils.expresiones_regulares import EMAIL_REGEX


class Usuario:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __str__(self) -> str:
        return f"{self.email} ({self.id})"

    @classmethod
    def validar(cls, formulario):

        errores = []
        if not EMAIL_REGEX.match(formulario['email']):
            errores.append(
                "El correo indicado es inválido"
            )

        if len(formulario['nombre']) < 3:
            errores.append(
                "nombre debe tener al menos 3 caracteres de largo"
            )

        if len(formulario['apellido']) < 3:
            errores.append(
                "apellido debe tener al menos 3 caracteres de largo"
            )


        if len(formulario['password']) < 8:
            errores.append(
                "password debe tener al menos 8 caracteres de largo"
            )

        if cls.get_by_email(formulario['email']):
            errores.append(
                "el correo ya existe"
            )

        return errores

    @classmethod
    def get_all(cls):
        resultados_instancias = []
        query = "SELECT * FROM usuarios"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get(cls, id ):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    @classmethod
    def get_by_email(cls, email ):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = { 'email': email }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    
    @classmethod
    def eliminar(cls, id ):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def delete(self):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        data = { 'id': self.id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def update(self):
        query = "UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, password = %(password)s updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'password': self.password,
            'nombre': self.nombre,
            'apellido': self.apellido,
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
