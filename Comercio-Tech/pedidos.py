import tkinter as tk
from tkinter import ttk, messagebox
from crud_pedidos import agregar_pedido, obtener_pedidos, eliminar_pedido
from crud_clientes import obtener_clientes
from crud_productos import obtener_productos

class VentanaPedidos:
    def __init__(self, ventana, db): 
        self.ventana = ventana
        self.db = db
        self.ventana.title("Gestión de Pedidos - ComercioTech")
        self.ventana.geometry("750x550")

        self.lista_items_pedido = []
        self.total_pedido = 0.0

        self.clientes_db = obtener_clientes(self.db) 
        self.productos_db = obtener_productos(self.db)

        # Ventana  Cliente
        frame_cli = tk.LabelFrame(self.ventana, text="1. Seleccionar Cliente")
        frame_cli.pack(fill="x", padx=10, pady=5)
        self.combo_clientes = ttk.Combobox(frame_cli, values=[f"{c['nombre']} {c['apellido']} ({c['_id']})" for c in self.clientes_db], width=50, state="readonly")
        self.combo_clientes.pack(padx=10, pady=10)

        # VentanaProductos
        frame_prod = tk.LabelFrame(self.ventana, text="2. Agregar Productos al Carrito")
        frame_prod.pack(fill="x", padx=10, pady=5)
        self.combo_productos = ttk.Combobox(frame_prod, values=[f"{p['nombre']} - ${p['precio']} ({p['_id']})" for p in self.productos_db], width=40, state="readonly")
        self.combo_productos.pack(side="left", padx=10, pady=10)

        tk.Label(frame_prod, text="Cant:").pack(side="left")
        self.txt_cantidad = tk.Entry(frame_prod, width=5)
        self.txt_cantidad.pack(side="left", padx=5)
        self.txt_cantidad.insert(0, "1")

        tk.Button(frame_prod, text="Añadir", command=self.anadir_carrito, bg="#2196F3", fg="white").pack(side="left", padx=5)

        self.lbl_total = tk.Label(self.ventana, text="Total Carrito: $0.0", font=("Arial", 12, "bold"))
        self.lbl_total.pack(pady=2)

        tk.Button(self.ventana, text="🛒 Confirmar y Registrar Pedido", command=self.guardar_pedido, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=5)


        frame_hist = tk.LabelFrame(self.ventana, text="Historial de Pedidos en Sistema")
        frame_hist.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_pedidos = ttk.Treeview(frame_hist, columns=("ID Pedido", "Cliente", "Total"), show="headings")
        self.tree_pedidos.heading("ID Pedido", text="ID Pedido")
        self.tree_pedidos.heading("Cliente", text="Cliente")
        self.tree_pedidos.heading("Total", text="Total")
        self.tree_pedidos.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Button(frame_hist, text="❌ Eliminar Pedido Seleccionado", command=self.eliminar_pedido_ui, bg="#F44336", fg="white").pack(pady=5)

        self.cargar_pedidos()

    def anadir_carrito(self):
        idx_p = self.combo_productos.current()
        if idx_p == -1: return
        prod = self.productos_db[idx_p]
        try:
            cant = int(self.txt_cantidad.get())
            if cant <= 0:
                messagebox.showwarning("Cantidad", "La cantidad debe ser mayor a 0.")
                return
            subtotal = prod["precio"] * cant
            self.lista_items_pedido.append({
                "id_producto": str(prod["_id"]),
                "nombre": prod["nombre"],
                "cantidad": cant
            })
            self.total_pedido += subtotal
            self.lbl_total.config(text=f"Total Carrito: ${self.total_pedido}")
            messagebox.showinfo("Carrito", f"Agregado {prod['nombre']} x{cant}")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero entero.")

    def guardar_pedido(self):
        idx_c = self.combo_clientes.current()
        if idx_c == -1 or not self.lista_items_pedido:
            messagebox.showwarning("Incompleto", "Seleccione un cliente y añada productos.")
            return
        
        cliente = self.clientes_db[idx_c]
        exito, mensaje = agregar_pedido(self.db, str(cliente["_id"]), 
                                       f"{cliente['nombre']} {cliente['apellido']}", 
                                       self.lista_items_pedido, self.total_pedido)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.lista_items_pedido = []
            self.total_pedido = 0.0
            self.lbl_total.config(text="Total Carrito: $0.0")

            self.productos_db = obtener_productos(self.db)
            self.combo_productos['values'] = [f"{p['nombre']} - ${p['precio']} ({p['_id']})" for p in self.productos_db]
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_pedido_ui(self):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            messagebox.showwarning("Selección", "Selecciona un pedido del historial para eliminar.")
            return
        
        item = self.tree_pedidos.item(seleccion[0])
        id_pedido = item["values"][0]
        
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar el pedido? El stock se devolverá automáticamente."):
            exito, mensaje = eliminar_pedido(self.db, id_pedido)
            if exito:
                messagebox.showinfo("Éxito", mensaje)

                self.productos_db = obtener_productos(self.db)
                self.combo_productos['values'] = [f"{p['nombre']} - ${p['precio']} ({p['_id']})" for p in self.productos_db]
                self.cargar_pedidos()
            else:
                messagebox.showerror("Error", mensaje)

    def cargar_pedidos(self):
        for item in self.tree_pedidos.get_children(): 
            self.tree_pedidos.delete(item)
        for ped in obtener_pedidos(self.db):
            self.tree_pedidos.insert("", "end", values=(str(ped["_id"]), ped["nombre_cliente"], f"${ped['total']}"))