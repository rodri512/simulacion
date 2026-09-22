import tkinter as tk
from tkinter import ttk, scrolledtext
import random

def simular_caja_supermercado():
    # Habilitar y limpiar la consola gráfica
    consola.configure(state='normal')
    consola.delete('1.0', tk.END)
    
    num_clientes = 10 # Cantidad a simular 
    
    # Variables de Estado iniciales
    fin_atencion_anterior = 0
    reloj_absoluto = 0
    
    consola.insert(tk.END, "--- INICIO SIMULACIÓN CAJA SUPERMERCADO ---\n\n")
    
    for cliente in range(1, num_clientes + 1):
        # 1. Generar un tiempo de llegada aleatorio (entre 1 y 5 min)
        intervalo_llegada = random.randint(1, 5)
        # El tiempo absoluto en que llega el cliente es el tiempo actual + el intervalo
        reloj_absoluto += intervalo_llegada 
        
        # 2. Generar un tiempo de atención aleatorio (entre 2 y 6 min)
        tiempo_atencion = random.randint(2, 6)
        
        # 3. Lógica para calcular la espera:
        # Si el cajero se libera después de que el cliente llega -> el cliente ESPERA.
        # Si el cajero se libera antes de que el cliente llegue -> NO ESPERA (se atiende apenas llega).
        inicio_atencion = max(reloj_absoluto, fin_atencion_anterior)
        
        # 3. Calcular el tiempo exacto que esperó en la fila
        tiempo_espera = inicio_atencion - reloj_absoluto
        
        # Actualizar la variable de estado: ¿Cuándo termina de atender a este cliente?
        fin_atencion_anterior = inicio_atencion + tiempo_atencion
        
        # Mostrar en pantalla los datos de este cliente
        consola.insert(tk.END, f"👤 CLIENTE {cliente}:\n")
        consola.insert(tk.END, f"   ➤ Llegó en el minuto: {reloj_absoluto} (Tardó {intervalo_llegada} min respecto al anterior)\n")
        consola.insert(tk.END, f"   ➤ Tiempo que le lleva al cajero: {tiempo_atencion} min\n")
        consola.insert(tk.END, f"   ⏳ TIEMPO ESPERANDO EN FILA: {tiempo_espera} minutos\n")
        consola.insert(tk.END, "-"*50 + "\n")

    # Deshabilitar edición
    consola.configure(state='disabled')

# ==========================================
# CONFIGURACIÓN DE LA VENTANA PRINCIPAL
# ==========================================
ventana = tk.Tk()
ventana.title("Simulador Discreto: Caja de Supermercado")
ventana.geometry("550x550")
ventana.configure(padx=50, pady=50)
#ventana.attributes("-alpha", 0.95) 

# Título
tk.Label(ventana, text="Fila del Supermercado", font=("Arial", 14, "bold")).pack(pady=(0, 10))
tk.Label(ventana, text="Variables estocásticas: Llegadas (1-5m) | Atención (2-6m)", fg="grey").pack(pady=(0, 15))

# Botón de ejecución
btn_simular = ttk.Button(ventana, text="▶ Simular Llegada de 10 Clientes", command=simular_caja_supermercado)
btn_simular.pack(pady=5)

# Consola de salida
tk.Label(ventana, text="Registro de la caja:", anchor="w").pack(fill="x", pady=(10, 0))
consola = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=65, height=20, font=("Courier New", 10))
consola.pack(pady=5)
consola.insert(tk.END, "Presione el botón para generar la simulación estocástica...")
consola.configure(state='disabled')

# Iniciar aplicación
ventana.mainloop()