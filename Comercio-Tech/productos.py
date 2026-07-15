import tkinter as tk
from tkinter import ttk, messagebox
from crud_productos import agregar_producto, obtener_productos, actualizar_producto, eliminar_producto

class VentanaProductos:
    def __init__(self, ventana, db):
        self.ventana = ventana
        self.db = db
        self.ventana.title("Gestión de Productos - ComercioTech")
        self.ventana.geometry("650x450")

        self.id_seleccionado = None
        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()

        frame_form = tk.LabelFrame(self.ventana, text="Datos del Producto", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        lbl_info = tk.Label(frame_form, text="Luego de ocupar un ID no puede ser \n Actualizado, a menos que lo Elimine", fg="gray", font=("Arial", 8))
        lbl_info.grid(row=0, column=4, padx=10, sticky="e")

        tk.Label(frame_form, text="ID:").grid(row=1, column=2, sticky="w")
        self.ent_id = tk.Entry(frame_form)
        self.ent_id.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_nombre).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Precio:").grid(row=0, column=2, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_precio).grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_form, text="Stock:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_stock).grid(row=1, column=1, padx=5, pady=2)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_botones, text="Agregar", command=self.agregar, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(frame_botones, text="Actualizar", command=self.actualizar, bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar, bg="#F44336", fg="white").pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.ventana, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)

        self.cargar_productos()

    def cargar_productos(self):
        for item in self.tree.get_children(): 
            self.tree.delete(item)
        for p in obtener_productos(self.db): 
            self.tree.insert("", "end", values=(
                str(p.get("_id", "")), p.get("nombre", ""), p.get("precio", ""), p.get("stock", "")
            ))

    def agregar(self):
        id_prod = self.ent_id.get().strip()
        nom = self.var_nombre.get().strip()
        pre = self.var_precio.get().strip()
        stk = self.var_stock.get().strip()

        #en caso de que también hayan atributos vacios
        if not (id_prod and nom and pre and stk):
            messagebox.showwarning("Campos vacíos", "Todos los atributos del producto son mandatorios.")
            return

        try:
            exito, mensaje = agregar_producto(self.db, id_prod, nom, float(pre), int(stk))
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showerror("Error", "Precio y stock deben ser numéricos.")

    def seleccionar_registro(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            self.id_seleccionado = str(valores[0])
            self.ent_id.delete(0, tk.END)
            self.ent_id.insert(0, valores[0])
            self.var_nombre.set(valores[1])
            self.var_precio.set(valores[2])
            self.var_stock.set(valores[3])

    def actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un producto de la tabla.")
            return
        nom = self.var_nombre.get().strip()
        pre = self.var_precio.get().strip()
        stk = self.var_stock.get().strip()

        # Validacion en ccaso de que el cliente deje los datos vacios
        if not (nom and pre and stk):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos para actualizar.")
            return

        try:
            actualizar_producto(self.db, self.id_seleccionado, nom, float(pre), int(stk))
            messagebox.showinfo("Éxito", "Producto actualizado.")
            self.limpiar()
            self.cargar_productos()
        except ValueError:
            messagebox.showerror("Error", "Datos numéricos no válidos.")

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un producto de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            exito, mensaje = eliminar_producto(self.db, self.id_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar(self):
        self.id_seleccionado = None
        self.ent_id.delete(0, tk.END)
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_stock.set("")