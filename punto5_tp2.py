import tkinter as tk
from tkinter import ttk, messagebox

# --- Lógica de los Métodos de Generación ---

def generador_cuadrados_medios(x0, n_iter):
    resultados = []
    x = x0
    l_cifras = len(str(x0))
    for _ in range(n_iter):
        x_cuad = x ** 2
        x_str = str(x_cuad).zfill(2 * l_cifras)
        inicio = l_cifras // 2
        fin = inicio + l_cifras
        x_str_centro = x_str[inicio:fin]
        x = int(x_str_centro)
        ui = round(x / (10 ** l_cifras), 5)
        resultados.append(ui)
    return resultados

def generador_lehmer(x0, y, n_iter):
    resultados = []
    x = x0
    N_digitos = len(str(x0))
    K_digitos = len(str(y))
    for _ in range(n_iter):
        z = x * y
        z_str = str(z).zfill(N_digitos + K_digitos)
        izq = int(z_str[:K_digitos])
        der = int(z_str[K_digitos:])
        x = der - izq
        ui = round(x / (10**N_digitos), 5)
        resultados.append(ui)
    return resultados

def generador_aditivo(semillas, m, n_iter):
    resultados = []
    secuencia = semillas.copy()
    k = len(semillas)
    for _ in range(n_iter):
        nuevo_x = (secuencia[-1] + secuencia[-k]) % m
        secuencia.append(nuevo_x)
        ui = round(nuevo_x / (m - 1), 5) 
        resultados.append(ui)
    return resultados

def generador_multiplicativo(x0, a, m, n_iter):
    resultados = []
    x = x0
    for _ in range(n_iter):
        x = (a * x) % m
        ui = round(x / (m - 1), 5)
        resultados.append(ui)
    return resultados

def generador_mixto(x0, a, c, m, n_iter):
    resultados = []
    x = x0
    for _ in range(n_iter):
        x = (a * x + c) % m
        ui = round(x / (m - 1), 5)
        resultados.append(ui)
    return resultados

# --- Interfaz Gráfica (GUI) ---

def actualizar_campos(event=None):
    """Muestra u oculta los campos dinámicamente según el método elegido."""
    metodo = combo_metodo.get()
    
    # Ocultar todos los campos condicionales primero
    lbl_multiplicador.grid_remove()
    entry_multiplicador.grid_remove()
    lbl_constante.grid_remove()
    entry_constante.grid_remove()
    lbl_modulo.grid_remove()
    entry_modulo.grid_remove()
    
    # Configuración por defecto del label de la semilla
    lbl_semilla.config(text="X0 (Semilla):")

    # Mostrar solo lo necesario según el método
    if metodo == "Cuadrados Medios":
        pass # Solo usa N y X0 (ya visibles)
        
    elif metodo == "Lehmer":
        lbl_multiplicador.config(text="Multiplicador (Y):")
        lbl_multiplicador.grid()
        entry_multiplicador.grid()
        
    elif metodo == "Congruencial Aditivo":
        lbl_semilla.config(text="Semillas (separadas por coma):")
        lbl_modulo.grid()
        entry_modulo.grid()
        
    elif metodo == "Congruencial Multiplicativo":
        lbl_multiplicador.config(text="Multiplicador (a):")
        lbl_multiplicador.grid()
        entry_multiplicador.grid()
        lbl_modulo.grid()
        entry_modulo.grid()
        
    elif metodo == "Congruencial Mixto":
        lbl_multiplicador.config(text="Multiplicador (a):")
        lbl_multiplicador.grid()
        entry_multiplicador.grid()
        lbl_constante.grid()
        entry_constante.grid()
        lbl_modulo.grid()
        entry_modulo.grid()

def calcular():
    txt_resultados.delete(1.0, tk.END)
    try:
        metodo = combo_metodo.get()
        n = int(entry_n.get())
        
        if metodo == "Cuadrados Medios":
            x0 = int(entry_semilla.get())
            res = generador_cuadrados_medios(x0, n)
            
        elif metodo == "Lehmer":
            x0 = int(entry_semilla.get())
            y = int(entry_multiplicador.get())
            res = generador_lehmer(x0, y, n)
            
        elif metodo == "Congruencial Aditivo":
            semillas_str = entry_semilla.get().split(',')
            semillas = [int(s.strip()) for s in semillas_str]
            m = int(entry_modulo.get())
            res = generador_aditivo(semillas, m, n)
            
        elif metodo == "Congruencial Multiplicativo":
            x0 = int(entry_semilla.get())
            a = int(entry_multiplicador.get())
            m = int(entry_modulo.get())
            res = generador_multiplicativo(x0, a, m, n)
            
        elif metodo == "Congruencial Mixto":
            x0 = int(entry_semilla.get())
            a = int(entry_multiplicador.get())
            c = int(entry_constante.get())
            m = int(entry_modulo.get())
            res = generador_mixto(x0, a, c, m, n)
            
        for i, val in enumerate(res):
            txt_resultados.insert(tk.END, f"U_{i+1} = {val:.5f}\n")
            
    except ValueError:
        messagebox.showerror("Error de Entrada", "Por favor, verifica que todos los campos visibles tengan datos válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Generador de Variables Pseudoaleatorias")
root.geometry("450x550")

# Contenedores
frame_inputs = tk.LabelFrame(root, text="Parámetros de Entrada", padx=10, pady=10)
frame_inputs.pack(padx=10, pady=10, fill="x")

# N (Cantidad a generar)
tk.Label(frame_inputs, text="N (Cantidad de números):").grid(row=0, column=0, sticky="w", pady=2)
entry_n = tk.Entry(frame_inputs)
entry_n.grid(row=0, column=1, pady=2)

# Selección de Método
tk.Label(frame_inputs, text="Método de Generación:").grid(row=1, column=0, sticky="w", pady=2)
combo_metodo = ttk.Combobox(frame_inputs, values=["Cuadrados Medios", "Lehmer", "Congruencial Aditivo", "Congruencial Multiplicativo", "Congruencial Mixto"], state="readonly", width=25)
combo_metodo.grid(row=1, column=1, pady=2)
# Vincular el evento de cambio en el combobox a nuestra función de actualización
combo_metodo.bind("<<ComboboxSelected>>", actualizar_campos)

# Campos base y dinámicos (Se guardan las referencias de los Labels para poder ocultarlos)
lbl_semilla = tk.Label(frame_inputs, text="X0 (Semilla):")
lbl_semilla.grid(row=2, column=0, sticky="w", pady=2)
entry_semilla = tk.Entry(frame_inputs)
entry_semilla.grid(row=2, column=1, pady=2)

lbl_multiplicador = tk.Label(frame_inputs, text="Multiplicador (Y o a):")
entry_multiplicador = tk.Entry(frame_inputs)
# No usamos .grid() aquí directamente para los dinámicos, lo hará la función actualizar_campos()

lbl_constante = tk.Label(frame_inputs, text="Constante aditiva (c):")
entry_constante = tk.Entry(frame_inputs)

lbl_modulo = tk.Label(frame_inputs, text="Módulo (M):")
entry_modulo = tk.Entry(frame_inputs)

# Inicializar los campos dinámicos mostrando el estado para el primer método de la lista
combo_metodo.current(0)
actualizar_campos()

# Botón Calcular
btn_calcular = tk.Button(root, text="Generar Números", command=calcular, bg="lightblue")
btn_calcular.pack(pady=10)

# Resultados
frame_resultados = tk.LabelFrame(root, text="Resultados (máx 5 decimales)", padx=10, pady=10)
frame_resultados.pack(padx=10, pady=10, fill="both", expand=True)

txt_resultados = tk.Text(frame_resultados, width=40, height=15)
txt_resultados.pack()

root.mainloop()