
from tkinter import *
import sqlite3
import funciones as fn
import os
import json

class GestorTareas:
    def __init__(self, ventana_principal):
        
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Gestor de Tareas")
        self.ventana_principal.resizable(0, 0)
        self.ventana_principal.geometry("850x650")
        ancho_pantalla = self.ventana_principal.winfo_screenwidth()
        altura_pantalla = self.ventana_principal.winfo_screenheight()
        x = (ancho_pantalla - 850) // 2
        y = (altura_pantalla - 650) // 2
        self.ventana_principal.geometry(f"850x650+{x}+{y}")
        self.ventana_principal.configure(bg="white")
        
        icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check.ico")

        self.ventana_principal.iconbitmap(icono)
        
        self.frame_botones = Frame(self.ventana_principal, bg="white")
        
        self.boton_fondo = Button(self.ventana_principal, text="FONDO", command=lambda: fn.cambiar_fondo(self.ventana_principal, self.frame_botones), bg="white", width=20)
        self.boton_fondo.pack(pady=5)

        self.conexion = sqlite3.connect("tareas.db")
        self.conexion.execute("CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY, descripcion TEXT, estado TEXT)")

        self.lista_tareas = Listbox(self.ventana_principal, width=75, height=24, font=("Arial", 12))

        agregar_boton = Button(self.ventana_principal, text="AGREGAR TAREA", command=lambda: fn.agregar_tarea(self.conexion, self.lista_tareas), bg="#65B2F5", width=96)

        agregar_boton.pack(side=TOP, pady=5)

        self.lista_tareas.pack(pady=10)

        self.frame_botones.pack(side=BOTTOM, pady=15)

        completar_boton = Button(self.frame_botones, text="MARCAR REALIZADA", command=lambda: fn.completar_tarea(self.conexion, self.lista_tareas), bg="#21C600", width=20)
        completar_boton.grid(row=0, column=0, padx=5, pady=5)

        cambiar_pendiente_boton = Button(self.frame_botones, text="CAMBIAR A PENDIENTE", command=lambda: fn.cambiar_a_pendiente(self.conexion, self.lista_tareas), bg="#FFD700", width=20)
        cambiar_pendiente_boton.grid(row=0, column=1, padx=5, pady=5)

        eliminar_boton = Button(self.frame_botones, text="ELIMINAR TAREA", command=lambda: fn.confirmar_eliminar_tarea(self.conexion, self.lista_tareas), bg="#FF5733", width=20)
        eliminar_boton.grid(row=1, column=0, padx=5, pady=5)

        eliminar_todas_boton = Button(self.frame_botones, text="ELIMINAR TODAS", command=lambda: fn.eliminar_todas(self.conexion, self.lista_tareas), bg="#F83737", width=20)
        eliminar_todas_boton.grid(row=1, column=1, padx=5, pady=5)

        crear_pdf_boton = Button(self.frame_botones, text="CREAR Y ABRIR PDF", command=lambda: fn.crear_lista_pdf(self.lista_tareas), bg="#9ed231", width=20)
        crear_pdf_boton.grid(row=1, column=2, padx=5, pady=5)

        editar_boton = Button(self.frame_botones, text="EDITAR TAREA", command=lambda: fn.editar_tarea(self.conexion, self.lista_tareas), bg="#65F5EE", width=20)
        editar_boton.grid(row=0, column=2, padx=5, pady=5)

        fn.actualizar_lista(self.conexion, self.lista_tareas)    

        self.cargar_configuracion()

    def cargar_configuracion(self):
            try:
                with open("configuracion.json", "r") as archivo_config:
                    configuracion = json.load(archivo_config)
                    color_fondo = configuracion.get("color_fondo")
                    if color_fondo:
                        self.ventana_principal.configure(bg=color_fondo)
                        self.frame_botones.configure(bg=color_fondo)
            except FileNotFoundError:
                pass 

ventana = Tk()
gestor_tareas = GestorTareas(ventana)
ventana.mainloop()