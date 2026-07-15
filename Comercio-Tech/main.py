import tkinter as tk
from tkinter import messagebox
from clientes import VentanaClientes
from productos import VentanaProductos
from pedidos import VentanaPedidos
from conexion import crear_conexion

# Login
class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - ComercioTech")
        self.root.geometry("350x250")
        

        frame_usr_lbl = tk.Frame(root)
        frame_usr_lbl.pack(pady=5)
        tk.Label(frame_usr_lbl, text="Usuario : ", font=("Arial", 10)).pack(side="left")

        
        self.txt_usuario = tk.Entry(root, width=30)
        self.txt_usuario.pack()

        frame_pwd_lbl = tk.Frame(root)
        frame_pwd_lbl.pack(pady=5)
        tk.Label(frame_pwd_lbl, text="Contraseña : ", font=("Arial", 10)).pack(side="left")
        
        self.txt_password = tk.Entry(root, width=30, show="*")
        self.txt_password.pack()

        tk.Button(root, text="Iniciar Sesión", command=self.conectar, bg="#4CAF50", fg="white").pack(pady=20)
    def conectar(self):
        usr = self.txt_usuario.get().strip()
        pwd = self.txt_password.get().strip()

        if not usr or not pwd:
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")
            return

        try:
            db = crear_conexion(usr, pwd)
            messagebox.showinfo("Éxito", "Conectado a MongoDB Atlas.")
            
            self.root.destroy()
            root_menu = tk.Tk()
            MenuPrincipal(root_menu, db)
            
        except Exception:
            messagebox.showerror(
                "Error de Conexión", 
                "No se pudo conectar a MongoDB Atlas. Por favor, intente nuevamente."
            )

# Menú Principal
class MenuPrincipal:
    def __init__(self, root, db):
        self.root = root
        self.db = db 
        self.root.title("Panel Control - ComercioTech")
        self.root.geometry("400x300")

        tk.Label(root, text="SISTEMA COMERCIOTECH", font=("Arial", 16, "bold"), pady=15).pack()

        tk.Button(root, text="👤 Gestionar Clientes", width=25, height=2, command=self.abrir_clientes).pack(pady=5)
        tk.Button(root, text="📦 Gestionar Productos", width=25, height=2, command=self.abrir_productos).pack(pady=5)
        tk.Button(root, text="🛒 Registrar Pedidos", width=25, height=2, command=self.abrir_pedidos).pack(pady=5)

    def abrir_clientes(self):
        VentanaClientes(tk.Toplevel(), self.db)

    def abrir_productos(self):
        VentanaProductos(tk.Toplevel(), self.db)

    def abrir_pedidos(self):
        VentanaPedidos(tk.Toplevel(), self.db)

if __name__ == "__main__":
    root = tk.Tk()
    VentanaLogin(root)
    root.mainloop()