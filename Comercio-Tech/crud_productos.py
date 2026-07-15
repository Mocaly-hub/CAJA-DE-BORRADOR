from bson import ObjectId
from bson.errors import InvalidId

def agregar_producto(db, id_producto, nombre, precio, stock):
    if db["productos"].find_one({"_id": id_producto.strip()}):
        return False, "El código de producto ya existe en el sistema."
        
    producto = {
        "_id": id_producto.strip(),
        "nombre": nombre.strip(),
        "precio": float(precio),
        "stock": int(stock)
    }
    db["productos"].insert_one(producto)
    return True, "Producto registrado con éxito."

def obtener_productos(db):
    return list(db["productos"].find())

def actualizar_producto(db, id_producto, nombre, precio, stock):
    id_limpio = str(id_producto).strip()
    filtro = {"_id": id_limpio}
    nuevos_valores = {
        "$set": {
            "nombre": nombre.strip(),
            "precio": float(precio),
            "stock": int(stock)
        }
    }
    return db["productos"].update_one(filtro, nuevos_valores)

def eliminar_producto(db, id_producto):
    id_limpio = str(id_producto).strip()
    
    # (No borrar producto si está en algún pedido)
    if db["pedidos"].find_one({"productos.id_producto": id_limpio}):
        return False, "No se puede eliminar: El producto forma parte de pedidos registrados."
        
    resultado = db["productos"].delete_one({"_id": id_limpio})
    if resultado.deleted_count > 0:
        return True, "Producto eliminado con éxito."
    return False, "El producto no pudo ser encontrado."