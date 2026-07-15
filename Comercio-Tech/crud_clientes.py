from bson import ObjectId
from bson.errors import InvalidId

def agregar_cliente(db, id_cliente, nombre, apellido, correo, telefono, calle, numero, comuna):

    if db["clientes"].find_one({"_id": id_cliente.strip()}):
        return False, "El código de cliente ya existe en el sistema."
    
    cliente = {
        "_id": id_cliente.strip(),
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "correo": correo.strip(),
        "telefono": telefono.strip(),
        "domicilio": {
            "calle": calle.strip(),
            "numero": numero.strip(),
            "comuna": comuna.strip()
        }
    }
    db["clientes"].insert_one(cliente)
    return True, "Cliente registrado con éxito."

def obtener_clientes(db):
    return list(db["clientes"].find())

def actualizar_cliente(db, id_cliente, nombre, apellido, correo, telefono, calle, numero, comuna):
    id_limpio = str(id_cliente).strip()
    return db["clientes"].update_one(
        {"_id": id_limpio},
        {"$set": {
            "nombre": nombre.strip(),
            "apellido": apellido.strip(),
            "correo": correo.strip(),
            "telefono": telefono.strip(),
            "domicilio": {
                "calle": calle.strip(), 
                "numero": numero.strip(), 
                "comuna": comuna.strip()
            }
        }}
    )

def eliminar_cliente(db, id_cliente):
    id_limpio = str(id_cliente).strip()

    if db["pedidos"].find_one({"id_cliente": id_limpio}):
        return False, "No se puede eliminar: El cliente tiene pedidos asociados en el historial."
        
    resultado = db["clientes"].delete_one({"_id": id_limpio})
    if resultado.deleted_count > 0:
        return True, "Cliente eliminado con éxito."
    return False, "El cliente no pudo ser encontrado."