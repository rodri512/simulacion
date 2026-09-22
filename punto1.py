import tkinter as tk
from tkinter import ttk, scrolledtext

def iniciar_simulacion():
    # 1. Limpiar el área de texto
    consola.configure(state='normal')
    consola.delete('1.0', tk.END)
    
    # 2. Variables Exógenas 
    tasa_llegada = 5             
    capacidad_procesamiento = 8  
    minutos_simulacion = 10
    
    # Variables de Estado 
    entregas_totales = 0
    ocioso_total = 0
    
    consola.insert(tk.END, f"--- INICIANDO SIMULACIÓN ({minutos_simulacion} MINUTOS) ---\n")
    consola.insert(tk.END, f"Tasa de llegada: {tasa_llegada} entregas/min | Capacidad: {capacidad_procesamiento} entregas/min\n\n")
    
    # 3.  (Avance del Reloj)
    for minuto in range(1, minutos_simulacion + 1):
        # Lógica de operación
        procesadas = min(tasa_llegada, capacidad_procesamiento)#busco el numero mas chico con la fun min()
        ocioso = capacidad_procesamiento - procesadas#luego hago la diferencia
        
        # Actualización de estado
        entregas_totales += procesadas
        ocioso_total += ocioso
        
        # Imprimir registro en la interfaz
        consola.insert(tk.END, f"Minuto {minuto:02d} ➔ Recibidas: {tasa_llegada} | Procesadas: {procesadas} | Ocioso: {ocioso}\n")
        
    # 4. Resultados Finales (Variables Endógenas)
    consola.insert(tk.END, "\n--- RESULTADOS ENDÓGENOS FINALES ---\n")
    consola.insert(tk.END, f"Total de entregas procesadas: {entregas_totales}\n")
    consola.insert(tk.END, f"Espacios de procesamiento ociosos desperdiciados: {ocioso_total}\n")
    
  
    consola.configure(state='disabled')

# ==========================================
# CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# ==========================================
ventana = tk.Tk()
ventana.title("Simulador Campus Virtual - Ejercicio 1")
ventana.geometry("500x450")
ventana.configure(padx=20, pady=20)

# Título y Descripción
tk.Label(ventana, text="Modelo de Servidor E-Learning", font=("Arial", 14, "bold")).pack(pady=(0, 5))
tk.Label(ventana, text="Simulación Determinística: 10 minutos", fg="grey").pack(pady=(0, 15))

# Botón de ejecución
btn_simular = ttk.Button(ventana, text="▶ Ejecutar Simulación", command=iniciar_simulacion)
btn_simular.pack(pady=(0, 15))

# Consola de texto con Scroll
consola = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=55, height=15, font=("Courier New", 10))
consola.pack()
consola.insert(tk.END, "Presione 'Ejecutar Simulación' para comenzar...")
consola.configure(state='disabled')

# Iniciar aplicación
ventana.mainloop()