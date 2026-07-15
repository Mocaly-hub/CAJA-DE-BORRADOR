import tkinter as tk
from tkinter import ttk, messagebox
from crud_clientes import agregar_cliente, obtener_clientes, actualizar_cliente, eliminar_cliente

class VentanaClientes:
    def __init__(self, ventana, db):
        self.ventana = ventana
        self.db = db
        self.ventana.title("Gestión de Clientes - ComercioTech")
        self.ventana.geometry("850x600")
        
        self.id_seleccionado = None
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_telefono = tk.StringVar()

        frame_form = tk.LabelFrame(self.ventana, text="Datos del Cliente", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        lbl_info = tk.Label(frame_form, text="Luego de ocupar un ID no puede ser \n Actualizado, a menos que lo Elimine", fg="gray", font=("Arial", 8))
        lbl_info.grid(row=0, column=4, padx=10, sticky="e")
        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        self.ent_id = tk.Entry(frame_form)
        self.ent_id.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="w")
        self.ent_nombre = tk.Entry(frame_form, textvariable=self.var_nombre)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(frame_form, text="Apellido:").grid(row=1, column=0, sticky="w")
        self.ent_apellido = tk.Entry(frame_form, textvariable=self.var_apellido)
        self.ent_apellido.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="Correo:").grid(row=1, column=2, sticky="w")
        self.ent_correo = tk.Entry(frame_form, textvariable=self.var_correo)
        self.ent_correo.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, sticky="w")
        self.ent_telefono = tk.Entry(frame_form, textvariable=self.var_telefono)
        self.ent_telefono.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Calle:").grid(row=2, column=2, sticky="w")
        self.ent_calle = tk.Entry(frame_form)
        self.ent_calle.grid(row=2, column=3, padx=5, pady=2)
        
        tk.Label(frame_form, text="Número:").grid(row=3, column=0, sticky="w")
        self.ent_numero = tk.Entry(frame_form)
        self.ent_numero.grid(row=3, column=1, padx=5, pady=2)
        
        tk.Label(frame_form, text="Comuna:").grid(row=3, column=2, sticky="w")
        self.ent_comuna = tk.Entry(frame_form)
        self.ent_comuna.grid(row=3, column=3, padx=5, pady=2)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(fill="x", padx=10, pady=5)
        
        tk.Button(frame_botones, text="Agregar", command=self.agregar, bg="green", fg="white").pack(side="left", padx=5)
        tk.Button(frame_botones, text="Actualizar", command=self.actualizar, bg="blue", fg="white").pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar, bg="red", fg="white").pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.ventana, columns=("ID", "Nombre", "Apellido", "Correo", "Teléfono"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)
        self.cargar_clientes()

    def seleccionar_registro(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            if valores:
                self.id_seleccionado = str(valores[0])
                self.ent_id.delete(0, tk.END)
                self.ent_id.insert(0, valores[0])
                self.var_nombre.set(valores[1])
                self.var_apellido.set(valores[2])
                self.var_correo.set(valores[3])
                self.var_telefono.set(valores[4])
                
                cliente = self.db["clientes"].find_one({"_id": self.id_seleccionado})
                if cliente and "domicilio" in cliente:
                    dom = cliente["domicilio"]
                    self.ent_calle.delete(0, tk.END)
                    self.ent_calle.insert(0, dom.get("calle", ""))
                    self.ent_numero.delete(0, tk.END)
                    self.ent_numero.insert(0, dom.get("numero", ""))
                    self.ent_comuna.delete(0, tk.END)
                    self.ent_comuna.insert(0, dom.get("comuna", ""))

    def cargar_clientes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in obtener_clientes(self.db):
            self.tree.insert("", "end", values=(
                str(c.get("_id", "")), c.get("nombre", ""), c.get("apellido", ""),
                c.get("correo", ""), c.get("telefono", "")
            ))

    def agregar(self):
        id_c = self.ent_id.get().strip()
        nom = self.var_nombre.get().strip()
        ape = self.var_apellido.get().strip()
        corr = self.var_correo.get().strip()
        tel = self.var_telefono.get().strip()
        calle = self.ent_calle.get().strip()
        num = self.ent_numero.get().strip()
        com = self.ent_comuna.get().strip()

        #  atributos vacíos
        if not (id_c and nom and ape and corr and tel and calle and num and com):
            messagebox.showwarning("Campos vacíos", "Todos los atributos son obligatorios.")
            return

        exito, mensaje = agregar_cliente(self.db, id_c, nom, ape, corr, tel, calle, num, com)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_campos()
            self.cargar_clientes()
        else:
            messagebox.showerror("Error", mensaje)

    def actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un cliente de la tabla.")
            return
            
        nom = self.var_nombre.get().strip()
        ape = self.var_apellido.get().strip()
        corr = self.var_correo.get().strip()
        tel = self.var_telefono.get().strip()
        calle = self.ent_calle.get().strip()
        num = self.ent_numero.get().strip()
        com = self.ent_comuna.get().strip()

     
        if not (nom and ape and corr and tel and calle and num and com):
            messagebox.showwarning("Campos vacíos", "No se permiten atributos vacíos al actualizar.")
            return

        actualizar_cliente(self.db, self.id_seleccionado, nom, ape, corr, tel, calle, num, com)
        messagebox.showinfo("Éxito", "Cliente actualizado con éxito.")
        self.limpiar_campos()
        self.cargar_clientes()

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Selección", "Selecciona un cliente de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este cliente de forma permanente?"):
            exito, mensaje = eliminar_cliente(self.db, self.id_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_campos()
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", mensaje)

    def limpiar_campos(self):
        self.id_seleccionado = None
        self.ent_id.delete(0, tk.END)
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_correo.set("")
        self.var_telefono.set("")
        self.ent_calle.delete(0, tk.END)
        self.ent_numero.delete(0, tk.END)
        self.ent_comuna.delete(0, tk.END)