
from tkinter import *
from tkinter import colorchooser, simpledialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import json

class Tarea:
    def __init__(self, id, descripcion, estado):
        self.id = id
        self.descripcion = descripcion
        self.estado = estado

def actualizar_lista(conexion, lista_tareas):
        lista_tareas.delete(0, "end")
        for fila in conexion.execute("SELECT * FROM tareas WHERE estado != 'eliminada'"):
            tarea = Tarea(id=fila[0], descripcion=fila[1], estado=fila[2])
            lista_tareas.insert("end", f"N°: {tarea.id}, Tarea: {tarea.descripcion}, Estado: {tarea.estado}")    

import json

def cambiar_fondo(ventana_principal, frame_botones):
    color_seleccionado = colorchooser.askcolor()[1]
    if color_seleccionado:
        ventana_principal.configure(bg=color_seleccionado)
        frame_botones.configure(bg=color_seleccionado)
        
        # Guardar el color seleccionado en un archivo JSON
        with open("configuracion.json", "w") as archivo_config:
            json.dump({"color_fondo": color_seleccionado}, archivo_config)










"""def cambiar_fondo(ventana_principal, frame_botones):
        # Abrir el selector de color y obtener el color seleccionado
        color_seleccionado = colorchooser.askcolor()[1] #abre el selector de color, permite que el usuario seleccione un color y 
                                                    #almacena el color seleccionado en formato hexadecimal en la variable color_seleccionado.
        if color_seleccionado:  # Si el usuario selecciona un color
            ventana_principal.configure(bg=color_seleccionado)  # Cambiamos c. de fondo de v. princ. y el frame de botones 
            frame_botones.configure(bg=color_seleccionado)"""










def agregar_tarea(conexion, lista_tareas):  # esta funcion debe irse al otro archivo...
        tarea_descripcion = simpledialog.askstring("Agregar Tarea", "Ingrese la descripción de la tarea:")
        if tarea_descripcion:
            conexion.execute("INSERT INTO tareas (descripcion, estado) VALUES (?, ?)", (tarea_descripcion, "PENDIENTE"))
            conexion.commit()
            actualizar_lista(conexion, lista_tareas)

def completar_tarea(conexion, lista_tareas):
        seleccion = lista_tareas.curselection()
        if seleccion:
            tarea_index = seleccion[0]
            tarea_texto = lista_tareas.get(tarea_index)
            tarea_id = int(tarea_texto.split(",")[0].split(":")[1].strip())
            conexion.execute("UPDATE tareas SET estado='REALIZADA' WHERE id=?", (tarea_id,))
            conexion.commit()
            actualizar_lista(conexion, lista_tareas)

def cambiar_a_pendiente(conexion, lista_tareas):
        seleccion = lista_tareas.curselection()
        if seleccion:
            tarea_index = seleccion[0]
            tarea_texto = lista_tareas.get(tarea_index)
            tarea_id = int(tarea_texto.split(",")[0].split(":")[1].strip())
            conexion.execute("UPDATE tareas SET estado='PENDIENTE' WHERE id=?", (tarea_id,))
            conexion.commit()
            actualizar_lista(conexion, lista_tareas)

def eliminar_tarea(conexion, lista_tareas):
        seleccion = lista_tareas.curselection()
        if seleccion:
            tarea_index = seleccion[0]
            tarea_texto = lista_tareas.get(tarea_index)
            tarea_id = int(tarea_texto.split(",")[0].split(":")[1].strip())
            conexion.execute("UPDATE tareas SET estado='eliminada' WHERE id=?", (tarea_id,))
            conexion.commit()
            actualizar_lista(conexion, lista_tareas)

def confirmar_eliminar_tarea(conexion, lista_tareas):
        seleccion = lista_tareas.curselection()
        if seleccion:
            confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar esta tarea?")
            if confirmar:
                eliminar_tarea(conexion, lista_tareas)

def editar_tarea(conexion, lista_tareas):
        seleccion = lista_tareas.curselection()
        if seleccion:
            tarea_index = seleccion[0]
            tarea_texto = lista_tareas.get(tarea_index)
            tarea_id = int(tarea_texto.split(",")[0].split(":")[1].strip())
            tarea_actual = conexion.execute("SELECT descripcion FROM tareas WHERE id=?", (tarea_id,)).fetchone()[0]

            nueva_descripcion = simpledialog.askstring("Editar Tarea", "Editar descripción de la tarea:", initialvalue=tarea_actual)
            if nueva_descripcion:
                conexion.execute("UPDATE tareas SET descripcion=? WHERE id=?", (nueva_descripcion, tarea_id))
                conexion.commit()
                actualizar_lista(conexion, lista_tareas)

def eliminar_todas(conexion, lista_tareas):
        confirmar_eliminar = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar todas las tareas?")
        if confirmar_eliminar:
            conexion.execute("DELETE FROM tareas")
            conexion.commit()
            actualizar_lista(conexion, lista_tareas)
        else:
            messagebox.showinfo("Operación Cancelada", "No se eliminaron las tareas.")

def crear_lista_pdf(lista_tareas):
        seleccion = lista_tareas.get(0, END)
        if seleccion:
            ruta_escritorio = os.path.expanduser("~/Desktop")
            archivo_pdf = os.path.join(ruta_escritorio, "Lista de tareas.pdf")
            pdf = canvas.Canvas(archivo_pdf, pagesize=letter)
            y = 750
            for tarea_texto in seleccion:
                pdf.drawString(100, y, tarea_texto)
                y -= 20
            pdf.save()
            messagebox.showinfo("PDF Creado", f"Se ha creado 'Lista de tareas.pdf' en el escritorio.")
            os.startfile(archivo_pdf)