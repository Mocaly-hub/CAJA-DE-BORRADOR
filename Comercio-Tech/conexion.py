from pymongo import MongoClient

def crear_conexion(usuario, password):
    # URI con variables dinámicas recibida desde el Login
    uri_dinamica = f"mongodb+srv://{usuario}:{password}@cluster0.oafqndq.mongodb.net/?appName=Cluster0"
    

    cliente = MongoClient(uri_dinamica, serverSelectionTimeoutMS=4000)
    

    cliente.admin.command("ping")
    
    return cliente["ComercioTech"]