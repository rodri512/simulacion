import tkinter as tk
from tkinter import ttk, scrolledtext

def simular_migracion_cloud():
    import tkinter as tk
from tkinter import ttk, scrolledtext

def ejecutar_migracion():
    # 1. Habilitar y limpiar la consola gráfica
    consola.configure(state='normal')
    consola.delete('1.0', tk.END)
    
    try:
        # 2. Leer las Variables Exógenas desde la interfaz
        volumen_total = float(entry_volumen.get())
        tasa_subida = float(entry_subida.get())
        tasa_fondo = float(entry_fondo.get())
    except ValueError:
        consola.insert(tk.END, "Error: Por favor, ingrese solo números válidos.\n")
        consola.configure(state='disabled')
        return

    # Validar que la migración sea físicamente posible
    tasa_efectiva = tasa_subida - tasa_fondo
    if tasa_efectiva <= 0:
        consola.insert(tk.END, "❌ Error: El consumo de fondo es igual o mayor a la subida.\nLa migración nunca avanzará.\n")
        consola.configure(state='disabled')
        return

    # Variables de Estado
    datos_migrados = 0.0
    minuto = 0
    
    consola.insert(tk.END, "--- INICIANDO MIGRACIÓN CONTINUA A LA NUBE ---\n")
    consola.insert(tk.END, f"Objetivo: {volumen_total} GB | Tasa Efectiva Neta: {tasa_efectiva} GB/min\n\n")
    
    # 3. Iterador: Avanza el reloj de a 1 minuto usando un bucle while
    while datos_migrados < volumen_total:
        minuto += 1
        
        # Aplicación de la ecuación de balance
        datos_migrados += tasa_efectiva
        
        # Límite físico: no podemos migrar más del 100%
        if datos_migrados > volumen_total:
            datos_migrados = volumen_total
            
        # Mostrar progreso cada 10 minutos
        if minuto % 10 == 0 or datos_migrados == volumen_total:
            porcentaje = (datos_migrados / volumen_total) * 100
            consola.insert(tk.END, f"Minuto {minuto:03d} ➔ Transferidos: {datos_migrados:.1f} GB ({porcentaje:.1f}%)\n")
            
    # 4. Reporte Final (Variables Endógenas)
    consola.insert(tk.END, "\n--- MIGRACIÓN COMPLETADA ---\n")
    consola.insert(tk.END, f"✅ Tiempo total demorado: {minuto} minutos ({(minuto/60):.2f} horas)\n")
    
    consola.configure(state='disabled')

# ==========================================
# CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# ==========================================
ventana = tk.Tk()
ventana.title("Simulador: Migración Cloud (Ejercicio 5)")
ventana.geometry("550x550")
ventana.configure(padx=20, pady=20)

# Título
tk.Label(ventana, text="Modelo Continuo: Migración de Base de Datos", font=("Arial", 13, "bold")).pack(pady=(0, 10))

# Marco de parámetros (Datos por defecto del TP)
frame_parametros = tk.LabelFrame(ventana, text="Parámetros de Red (Variables Exógenas)", padx=10, pady=10)
frame_parametros.pack(fill="x", pady=10)

# Fila 1: Volumen total
tk.Label(frame_parametros, text="Volumen Total (GB):").grid(row=0, column=0, sticky="w", pady=5)
entry_volumen = tk.Entry(frame_parametros, width=10)
entry_volumen.insert(0, "500") # Volumen según TP
entry_volumen.grid(row=0, column=1, padx=10)

# Fila 2: Tasa subida y Consumo fondo
tk.Label(frame_parametros, text="Tasa Subida (GB/min):").grid(row=1, column=0, sticky="w", pady=5)
entry_subida = tk.Entry(frame_parametros, width=10)
entry_subida.insert(0, "2.5") # Tasa según TP
entry_subida.grid(row=1, column=1, padx=10)

tk.Label(frame_parametros, text="Consumo Fondo (GB/min):").grid(row=1, column=2, sticky="w", pady=5)
entry_fondo = tk.Entry(frame_parametros, width=10)
entry_fondo.insert(0, "0.5") # Consumo según TP
entry_fondo.grid(row=1, column=3, padx=10)

# Botón
btn_simular = ttk.Button(ventana, text="▶ Iniciar Migración", command=ejecutar_migracion)
btn_simular.pack(pady=15)

# Consola de salida
tk.Label(ventana, text="Registro del Sistema (Bucle While):", anchor="w").pack(fill="x")
consola = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=65, height=14, font=("Courier New", 10))
consola.pack(pady=5)
consola.insert(tk.END, "Presione 'Iniciar Migración' para comenzar...")
consola.configure(state='disabled')

ventana.mainloop()