"""
FlockLedger - Aplicación de Gestión de Registro Ganadero
Versión Base con funcionalidades fundamentales
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from pathlib import Path
from models import Explotacion, Oveja, Alta, Baja, RepositorioExplotaciones
from pdf_export import ExportadorPDF


class WelcomeWindow:
    """Ventana de bienvenida con opciones principales"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FlockLedger - Bienvenido")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.result = None
        self.create_ui()
    
    def create_ui(self):
        """Crear interfaz de bienvenida"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title = ttk.Label(
            main_frame,
            text="FlockLedger",
            font=("Helvetica", 28, "bold")
        )
        title.pack(pady=20)
        
        # Subtítulo
        subtitle = ttk.Label(
            main_frame,
            text="Gestor de Registro Ganadero",
            font=("Helvetica", 12),
            foreground="gray"
        )
        subtitle.pack(pady=10)
        
        # Descripción
        description = ttk.Label(
            main_frame,
            text="Seleccione una opción para comenzar",
            font=("Helvetica", 10)
        )
        description.pack(pady=20)
        
        # Botones de opciones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30, fill='x', expand=True)
        
        btn_new = ttk.Button(
            button_frame,
            text="📝 Crear Nuevo Libro",
            command=self.create_new,
            width=30
        )
        btn_new.pack(pady=10, ipady=10)
        
        btn_open = ttk.Button(
            button_frame,
            text="📂 Abrir Libro Existente",
            command=self.open_existing,
            width=30
        )
        btn_open.pack(pady=10, ipady=10)
        
        btn_exit = ttk.Button(
            button_frame,
            text="❌ Salir",
            command=self.root.quit,
            width=30
        )
        btn_exit.pack(pady=10, ipady=10)
    
    def create_new(self):
        """Crear nuevo libro"""
        self.result = 'new'
        self.root.destroy()
    
    def open_existing(self):
        """Abrir libro existente"""
        self.result = 'open'
        self.root.destroy()


class FlockLedgerApp:
    """Aplicación principal de gestión de registro ganadero"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FlockLedger - Gestor de Registro Ganadero")
        self.root.geometry("1200x700")
        self.root.minsize(900, 500)
        
        # Modelos de datos
        self.repositorio = RepositorioExplotaciones()
        self.explotacion_actual = None
        self.current_file = None
        self.df = None
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear interfaz
        self.create_menu_bar()
        self.create_toolbar()
        self.create_main_layout()
    
    def setup_styles(self):
        """Configurar estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_menu_bar(self):
        """Crear barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir CSV", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar Como", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Edición
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edición", menu=edit_menu)
        edit_menu.add_command(label="Agregar Fila", command=self.add_row)
        edit_menu.add_command(label="Eliminar Fila", command=self.delete_row)
        edit_menu.add_separator()
        edit_menu.add_command(label="Limpiar Filtros", command=self.clear_filters)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=view_menu)
        view_menu.add_command(label="Refrescar", command=self.refresh_table)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        
    def create_toolbar(self):
        """Crear barra de herramientas"""
        toolbar = ttk.Frame(self.root, relief='raised', borderwidth=1)
        toolbar.pack(side='top', fill='x', padx=5, pady=5)
        
        ttk.Button(toolbar, text="📂 Abrir", command=self.open_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="💾 Guardar", command=self.save_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="📄 PDF", command=self.export_to_pdf).pack(side='left', padx=2)
        ttk.Button(toolbar, text="➕ Nueva Fila", command=self.add_row).pack(side='left', padx=2)
        ttk.Button(toolbar, text="🗑️ Eliminar", command=self.delete_row).pack(side='left', padx=2)
        ttk.Separator(toolbar, orient='vertical').pack(side='left', fill='y', padx=5)
        ttk.Button(toolbar, text="🔄 Refrescar", command=self.refresh_table).pack(side='left', padx=2)
        
    def create_main_layout(self):
        """Crear diseño principal"""
        # Frame de información del archivo
        info_frame = ttk.LabelFrame(self.root, text="Información del Archivo", padding=5)
        info_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="No hay archivo cargado", foreground="red")
        self.info_label.pack(side='left')
        
        # Frame de búsqueda y filtros
        filter_frame = ttk.LabelFrame(self.root, text="Búsqueda y Filtros", padding=5)
        filter_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Buscar:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<Return>', lambda e: self.search_data())
        
        ttk.Button(filter_frame, text="Buscar", command=self.search_data).pack(side='left', padx=2)
        ttk.Button(filter_frame, text="Limpiar", command=self.clear_filters).pack(side='left', padx=2)
        
        # Frame de tabla
        table_frame = ttk.LabelFrame(self.root, text="Datos del Registro", padding=5)
        table_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Crear Treeview con scrollbars
        self.create_treeview(table_frame)
        
        # Frame de estado
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Listo", relief='sunken')
        self.status_label.pack(side='left', fill='x', expand=True)
        
    def create_treeview(self, parent):
        """Crear tabla de datos con Treeview"""
        # Frame para scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbar vertical
        vsb = ttk.Scrollbar(tree_frame, orient='vertical')
        vsb.pack(side='right', fill='y')
        
        # Scrollbar horizontal
        hsb = ttk.Scrollbar(tree_frame, orient='horizontal')
        hsb.pack(side='bottom', fill='x')
        
        # Crear Treeview
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill='both', expand=True)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Menú contextual
        self.tree.bind("<Button-3>", self.show_context_menu)
        
    def open_file(self):
        """Abrir archivo CSV"""
        file_path = filedialog.askopenfilename(
            title="Abrir archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Leer CSV como texto puro para evitar conversiones automáticas
            self.df = pd.read_csv(file_path, dtype=str, na_filter=False)
            self.current_file = file_path
            
            # Crear explotación desde el CSV
            codigo_explotacion = os.path.splitext(os.path.basename(file_path))[0]
            self.explotacion_actual = Explotacion.from_dataframe(
                self.df, 
                codigo=codigo_explotacion,
                nombre=codigo_explotacion
            )
            
            self.repositorio.agregar_explotacion(self.explotacion_actual)
            self.update_info_label()
            self.display_data()
            self.status_label.config(text=f"Archivo cargado: {os.path.basename(file_path)}")
            
            messagebox.showinfo(
                "Éxito", 
                f"Archivo cargado correctamente.\n"
                f"Explotación: {codigo_explotacion}\n"
                f"Total ovejas: {self.explotacion_actual.total_ovejas()}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
    
    def save_file(self):
        """Guardar archivo CSV actual"""
        if not self.explotacion_actual:
            messagebox.showwarning("Advertencia", "No hay datos para guardar")
            return
        
        if not self.current_file:
            self.save_as_file()
        else:
            self._guardar_csv(self.current_file)
    
    def save_as_file(self):
        """Guardar archivo con nuevo nombre"""
        if not self.explotacion_actual:
            messagebox.showwarning("Advertencia", "No hay datos para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            self._guardar_csv(file_path)
    
    def _guardar_csv(self, file_path):
        """Helper para guardar CSV"""
        try:
            df = self.explotacion_actual.to_dataframe()
            df.to_csv(file_path, index=False)
            self.update_info_label()
            self.status_label.config(text=f"Archivo guardado: {os.path.basename(file_path)}")
            messagebox.showinfo("Éxito", "Archivo guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def display_data(self):
        """Mostrar datos en la tabla"""
        if not self.explotacion_actual:
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener datos del modelo
        df = self.explotacion_actual.to_dataframe()
        
        if df.empty:
            self.status_label.config(text="No hay datos para mostrar")
            return
        
        # Configurar columnas
        columns = list(df.columns)
        self.tree['columns'] = columns
        self.tree.column('#0', width=30, anchor='center')
        self.tree.heading('#0', text='#')
        
        for col in columns:
            self.tree.column(col, width=100, anchor='w')
            self.tree.heading(col, text=col)
        
        # Agregar datos
        for idx, oveja in enumerate(self.explotacion_actual.ovejas, 1):
            row_data = oveja.to_dict()
            values = [row_data[col] for col in columns]
            self.tree.insert('', 'end', text=str(idx), values=values)
        
        self.status_label.config(text=f"Total ovejas: {self.explotacion_actual.total_ovejas()}")
    
    def add_row(self):
        """Agregar nueva fila"""
        if not self.explotacion_actual:
            messagebox.showwarning("Advertencia", "Primero debe abrir un archivo")
            return
        
        # Calcular número de orden siguiente
        numero_orden = max(
            [o.numero_orden for o in self.explotacion_actual.ovejas], 
            default=0
        ) + 1
        
        # Crear nueva oveja vacía
        nueva_oveja = Oveja(
            numero_orden=numero_orden,
            identificacion='',
            ano_nacimiento=0,
            fecha_identificacion='',
            raza='',
            sexo=''
        )
        
        self.explotacion_actual.agregar_oveja(nueva_oveja)
        self.display_data()
        self.status_label.config(text="Nueva oveja agregada")
    
    def delete_row(self):
        """Eliminar fila seleccionada"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una fila para eliminar")
            return
        
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar la fila seleccionada?"):
            return
        
        for item in selected:
            index = int(self.tree.item(item, 'text')) - 1
            if index < len(self.explotacion_actual.ovejas):
                oveja_a_eliminar = self.explotacion_actual.ovejas[index]
                self.explotacion_actual.eliminar_oveja(oveja_a_eliminar.numero_orden)
        
        self.display_data()
        self.status_label.config(text="Fila eliminada")
    
    def search_data(self):
        """Buscar en los datos"""
        search_term = self.search_var.get()
        
        if not search_term or not self.explotacion_actual:
            self.display_data()
            return
        
        # Buscar en DataFrame
        df = self.explotacion_actual.to_dataframe()
        mask = df.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        
        filtered_df = df[mask]
        
        if len(filtered_df) == 0:
            messagebox.showinfo("Búsqueda", "No se encontraron resultados")
            return
        
        # Mostrar resultados filtrados
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        columns = list(filtered_df.columns)
        for idx, (_, row) in enumerate(filtered_df.iterrows(), 1):
            values = [row[col] for col in columns]
            self.tree.insert('', 'end', text=str(idx), values=values)
        
        self.status_label.config(text=f"Búsqueda: {len(filtered_df)} resultados encontrados")
    
    def clear_filters(self):
        """Limpiar filtros y mostrar todos los datos"""
        self.search_var.set('')
        self.display_data()
        self.status_label.config(text="Filtros limpios")
    
    def refresh_table(self):
        """Refrescar tabla"""
        self.display_data()
    
    def update_info_label(self):
        """Actualizar etiqueta de información"""
        if self.current_file and self.explotacion_actual:
            file_name = os.path.basename(self.current_file)
            file_size = os.path.getsize(self.current_file) / 1024  # KB
            self.info_label.config(
                text=f"Archivo: {file_name} | Tamaño: {file_size:.2f} KB | "
                     f"Explotación: {self.explotacion_actual.codigo} | "
                     f"Ovejas: {self.explotacion_actual.total_ovejas()}",
                foreground="green"
            )
    
    def show_context_menu(self, event):
        """Mostrar menú contextual"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Editar", command=lambda: messagebox.showinfo("Info", "Función de edición en desarrollo"))
        menu.add_command(label="Copiar", command=lambda: self.copy_cell(event))
        menu.add_separator()
        menu.add_command(label="Eliminar fila", command=self.delete_row)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def copy_cell(self, event):
        """Copiar celda seleccionada"""
        try:
            item = self.tree.selection()[0]
            messagebox.showinfo("Info", "Función de copiar en desarrollo")
        except:
            messagebox.showwarning("Advertencia", "Seleccione una celda")
    
    def export_to_pdf(self):
        """Exportar explotación actual a PDF"""
        if not self.explotacion_actual:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        # Pedir ubicación del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"Explotacion_{self.explotacion_actual.codigo}.pdf"
        )
        
        if not file_path:
            return
        
        try:
            exportador = ExportadorPDF(self.explotacion_actual)
            exitoso, mensaje = exportador.generar_pdf(file_path)
            
            if exitoso:
                messagebox.showinfo("Éxito", f"PDF generado correctamente\n\n{mensaje}")
                self.status_label.config(text=f"PDF exportado: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Error", f"Error al generar PDF:\n\n{mensaje}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar a PDF:\n\n{str(e)}")
    
    def show_about(self):
        """Mostrar ventana Acerca de"""
        messagebox.showinfo(
            "Acerca de FlockLedger",
            "FlockLedger v1.0\n\n"
            "Gestor de Registro Ganadero\n"
            "Aplicación para gestionar datos de ganado y contabilidad\n\n"
            "© 2025"
        )


def main():
    """Función principal - Mostrar ventana de bienvenida primero"""
    # Crear ventana de bienvenida
    welcome_root = tk.Tk()
    welcome = WelcomeWindow(welcome_root)
    welcome_root.mainloop()
    
    # Si el usuario no cerró explícitamente, abrir la aplicación principal
    if welcome.result is not None:
        root = tk.Tk()
        app = FlockLedgerApp(root)
        
        # Si eligió abrir existente, abrir diálogo de archivo
        if welcome.result == 'open':
            app.root.after(100, app.open_file)
        
        app.root.mainloop()


if __name__ == "__main__":
    main()
