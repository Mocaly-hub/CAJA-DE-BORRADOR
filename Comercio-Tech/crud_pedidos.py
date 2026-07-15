from bson import ObjectId

def agregar_pedido(db, id_cliente, nombre_cliente, lista_productos, total):

    for item in lista_productos:
        producto = db["productos"].find_one({"_id": item["id_producto"]})
        if not producto:
            return False, f"Error: El producto '{item['nombre']}' ya no existe."
        if producto["stock"] < item["cantidad"]:
            return False, f"Stock insuficiente para {item['nombre']}. Disponibles: {producto['stock']}"
    

    for item in lista_productos:
        db["productos"].update_one(
            {"_id": item["id_producto"]},
            {"$inc": {"stock": -int(item["cantidad"])}}
        )
    
    # Guardar pedido en Atlas
    pedido = {
        "id_cliente": id_cliente,
        "nombre_cliente": nombre_cliente,
        "productos": lista_productos, 
        "total": float(total)
    }
    db["pedidos"].insert_one(pedido)
    return True, "Pedido registrado con éxito."

def obtener_pedidos(db):
    return list(db["pedidos"].find())

def eliminar_pedido(db, id_pedido):
    id_limpio = str(id_pedido).strip()
    try:
        filtro = {"_id": ObjectId(id_limpio)}
    except:
        filtro = {"_id": id_limpio}
        
    pedido = db["pedidos"].find_one(filtro)
    if not pedido:
        return False, "El pedido no existe."

    for item in pedido.get("productos", []):
        db["productos"].update_one(
            {"_id": item["id_producto"]},
            {"$inc": {"stock": int(item["cantidad"])}}
        )
        
    db["pedidos"].delete_one(filtro)
    return True, "Pedido cancelado. El stock ha sido devuelto a los productos."