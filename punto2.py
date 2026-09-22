import tkinter as tk
from tkinter import ttk, scrolledtext

def ejecutar_simulacion():
    # 1. Habilitar la consola de texto y limpiarla
    consola.configure(state='normal')
    consola.delete('1.0', tk.END)
    
    try:
        # 2. Leer los parámetros ingresados
        vol_inicial = float(entry_vol_inicial.get())
        capacidad_max = float(entry_capacidad_max.get())
        flujo_in = float(entry_flujo_in.get())
        flujo_out = float(entry_flujo_out.get())
        tiempo_sim = int(entry_tiempo.get())
    except ValueError:
        consola.insert(tk.END, "Error: Por favor, ingrese solo números válidos.\n")
        consola.configure(state='disabled')
        return

    # Validación lógica inicial
    if vol_inicial > capacidad_max:
        consola.insert(tk.END, "Advertencia: El volumen inicial supera la capacidad máxima del tanque.\n\n")

    volumen_actual = vol_inicial
    
    consola.insert(tk.END, "--- INICIANDO SIMULACIÓN CONTINUA ---\n")
    consola.insert(tk.END, f"Volumen inicial: {vol_inicial} L | Capacidad Máxima: {capacidad_max} L\n")
    consola.insert(tk.END, f"Entrada: {flujo_in} L/min | Salida: {flujo_out} L/min\n\n")
    
    # 3. Bucle iterativo (Avance del Reloj)
    for minuto in range(1, tiempo_sim + 1):
        # Ecuación de balance por cada minuto
        volumen_actual = volumen_actual + flujo_in - flujo_out
        
        # Condición física 1: Control de desborde (si supera la capacidad máxima)
        if volumen_actual > capacidad_max:
            volumen_actual = capacidad_max
            consola.insert(tk.END, f"▶ Minuto {minuto:02d}: ¡El tanque ha alcanzado su capacidad máxima (Desborde)!\n")
            break #---
            
        # Condición física 2: Control de vaciamiento (si baja de 0)
        if volumen_actual < 0:
            volumen_actual = 0
            consola.insert(tk.END, f"▶ Minuto {minuto:02d}: ¡El tanque se ha vaciado por completo!\n")
            break 
            
        # Imprimir resultados cada 10 minutos para no saturar la pantalla
        if minuto % 1 == 0 or minuto == tiempo_sim:
            consola.insert(tk.END, f"Minuto {minuto:02d} -> Nivel del tanque: {volumen_actual} Litros\n")

    # 4. Comprobación Matemática Teórica (sin límites físicos)
    nivel_teorico = vol_inicial + (flujo_in - flujo_out) * tiempo_sim
    if nivel_teorico < 0: nivel_teorico = 0
    if nivel_teorico > capacidad_max: nivel_teorico = capacidad_max
        
    consola.insert(tk.END, "\n--- RESULTADOS FINALES ---\n")
    consola.insert(tk.END, f"Nivel final (por Simulación Iterativa con límites): {volumen_actual} Litros\n")
    consola.insert(tk.END, f"Nivel teórico sin tope de capacidad: {nivel_teorico} Litros\n")
    
    
    consola.configure(state='disabled')

# ==========================================
# CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# ==========================================
ventana = tk.Tk()
ventana.title("Simulador: Tanque de Agua ")
ventana.geometry("580x580")
ventana.configure(padx=20, pady=20)

# Título
tk.Label(ventana, text="Modelo Continuo: Tanque de Agua", font=("Arial", 14, "bold")).pack(pady=(0, 10))

# Marco para agrupar los parámetros
frame_parametros = tk.LabelFrame(ventana, text="Parámetros del Sistema", padx=10, pady=10)
frame_parametros.pack(fill="x", pady=10)

# Fila 1: Volumen Inicial y Capacidad Máxima
tk.Label(frame_parametros, text="Volumen Inicial (L):").grid(row=0, column=0, sticky="w", pady=5)
entry_vol_inicial = tk.Entry(frame_parametros, width=8)
entry_vol_inicial.insert(0, "500")
entry_vol_inicial.grid(row=0, column=1, padx=5, sticky="w")

tk.Label(frame_parametros, text="Capacidad Máx (L):").grid(row=0, column=2, sticky="w", pady=5)
entry_capacidad_max = tk.Entry(frame_parametros, width=8)
entry_capacidad_max.insert(0, "1000") # Le ponemos un límite por defecto de 1000L
entry_capacidad_max.grid(row=0, column=3, padx=5, sticky="w")

# Fila 2: Flujo Entrada y Salida
tk.Label(frame_parametros, text="Tasa Entrada (L/min):").grid(row=1, column=0, sticky="w", pady=5)
entry_flujo_in = tk.Entry(frame_parametros, width=8)
entry_flujo_in.insert(0, "10")
entry_flujo_in.grid(row=1, column=1, padx=5, sticky="w")

tk.Label(frame_parametros, text="Tasa Salida (L/min):").grid(row=1, column=2, sticky="w", pady=5)
entry_flujo_out = tk.Entry(frame_parametros, width=8)
entry_flujo_out.insert(0, "12")
entry_flujo_out.grid(row=1, column=3, padx=5, sticky="w")

# Fila 3: Tiempo de Simulación
tk.Label(frame_parametros, text="Tiempo Sim. (min):").grid(row=2, column=0, sticky="w", pady=5)
entry_tiempo = tk.Entry(frame_parametros, width=8)
entry_tiempo.insert(0, "60")
entry_tiempo.grid(row=2, column=1, padx=5, sticky="w")

# Botón de ejecución
btn_simular = ttk.Button(ventana, text="▶ Ejecutar Simulación", command=ejecutar_simulacion)
btn_simular.pack(pady=15)

# Consola de salida
tk.Label(ventana, text="Registro del Sistema:", anchor="w").pack(fill="x")
consola = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=65, height=12, font=("Courier New", 10))
consola.pack(pady=5)
consola.insert(tk.END, "Modifique los parámetros y presione 'Ejecutar'...")
consola.configure(state='disabled')

# Iniciar aplicación
ventana.mainloop()