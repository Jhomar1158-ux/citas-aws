from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import time

class Cita:

    def __init__(self, data):
        self.id = data["id"]
        self.task = data["task"]
        self.date = data["date"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.user_id = data["user_id"]
    @staticmethod
    def valida_cita(formulario):
        es_valido = True

        # VALIDANDO LA FECHA ACTUAL CON LA FECHA DE LA CITA
        print(type(formulario["date"]))
        print(f'Fecha de hoy: {time.strftime("%Y-%m-%d")}')
        fecha_cita=formulario["date"] 
        fecha_actual=time.strftime("%Y-%m-%d")  #16/03/22
        temp_fecha_cita = time.strptime(fecha_cita, "%Y-%m-%d")
        temp_fecha_actual = time.strptime(fecha_actual, "%Y-%m-%d")


        if len(formulario['task']) < 2:
            flash("Todos los campos deben tener valores", "cita")
            es_valido = False 

        if formulario['date'] == "":
            flash("Ingrese una fecha", "cita")
            es_valido = False
        
        if temp_fecha_cita < temp_fecha_actual:
            flash("No se permiten fechas pasadas", "cita")
            es_valido = False
        
        return es_valido

    @classmethod
    def citas_pasadas(cls, data):
        query = "SELECT * FROM citas WHERE user_id = %(id)s"
        results = connectToMySQL('esquema_citas_2').query_db(query, data)
        if len(results) < 1:
                return False
        else :
            citas = []
            for i in results:
                citas.append(cls(i))
            fecha_actual=time.strftime("%Y-%m-%d")
            print("PROBANDO ===========")
            past_citas=[]
            for j in citas:
                date_str = j.date.date()
                solo_fecha_str = date_str.strftime('%Y-%m-%d')
                print(solo_fecha_str)

                if(solo_fecha_str<fecha_actual):
                    # print(f' J. DATE: {j.date}')
                    past_citas.append(j)
            return past_citas

        



    @classmethod
    def save(cls, data):
        query = "INSERT INTO citas (task, date, status, user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s);"
        nuevoId = connectToMySQL('esquema_citas_2').query_db(query, data)
        return nuevoId
    
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM citas WHERE user_id = %(id)s"
        results = connectToMySQL('esquema_citas_2').query_db(query, data)
        print(f'Resultados del id: {results}')
        if len(results) < 1:
            return False
        else :
            citas = []
            for i in results:
                citas.append(cls(i))
            fecha_actual=time.strftime("%Y-%m-%d")
            print("PROBANDO ===========")

            new_citas=[]
            for j in citas:
                date_str = j.date.date()
                solo_fecha_str = date_str.strftime('%Y-%m-%d')
                print(solo_fecha_str)
                if(solo_fecha_str>=fecha_actual):
                    # print(f' J. DATE: {j.date}')
                    new_citas.append(j)
            return new_citas

    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM citas WHERE id = %(id)s"
        result = connectToMySQL('esquema_citas_2').query_db(query, data)
        cita = cls(result[0])
        return cita

    @classmethod
    def update(cls, data):
        query = "UPDATE citas SET task = %(task)s, status = %(status)s, date = %(date)s WHERE (id = %(id)s);"
        result = connectToMySQL('esquema_citas_2').query_db(query, data)
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM citas WHERE id = %(id)s"
        return connectToMySQL('esquema_citas_2').query_db(query, data)

