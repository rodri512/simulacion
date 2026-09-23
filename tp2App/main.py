import tkinter as tk
from tkinter import ttk, messagebox
import pruebas_estadisticas as pe  # Importación del módulo separado

numeros_generados = []

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
        x = int(x_str[inicio:fin])
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

# --- Gestión de la GUI y Módulo de Pruebas ---

def evaluar_prueba():
    global numeros_generados
    if not numeros_generados:
        messagebox.showwarning("Faltan Datos", "Primero debes generar la secuencia de números.")
        return

    prueba = combo_pruebas.get()
    txt_resultados.insert(tk.END, f"\n--- {prueba.upper()} ---\n")

    if prueba == "Prueba de los Promedios":
        media, z0, aceptado = pe.prueba_promedios(numeros_generados)
        txt_resultados.insert(tk.END, f"Media Muestral: {media:.5f}\nEstadístico Z0: {z0:.5f}\n")
        msg = ">>> SE ACEPTA H0 (Distribución Uniforme).\n" if aceptado else ">>> SE RECHAZA H0 (Sesgado).\n"
        txt_resultados.insert(tk.END, msg)

    elif prueba == "Test de las Rachas":
        rachas, z0, aceptado = pe.prueba_rachas(numeros_generados)
        txt_resultados.insert(tk.END, f"Total de Rachas (R): {rachas}\nEstadístico Z0: {z0:.5f}\n")
        msg = ">>> SE ACEPTA H0 (Independencia aprobada).\n" if aceptado else ">>> SE RECHAZA H0.\n"
        txt_resultados.insert(tk.END, msg)

    elif prueba == "Prueba del Póker":
        chi_cuadrado, aceptado = pe.prueba_poker(numeros_generados)
        txt_resultados.insert(tk.END, f"Estadístico X2_0: {chi_cuadrado:.5f}\n")
        msg = ">>> SE ACEPTA H0 (Distribución Uniforme).\n" if aceptado else ">>> SE RECHAZA H0.\n"
        txt_resultados.insert(tk.END, msg)

    elif prueba == "Prueba de Series":
        chi_cuadrado, aceptado = pe.prueba_series(numeros_generados)
        txt_resultados.insert(tk.END, f"Estadístico X2_0: {chi_cuadrado:.5f}\n")
        msg = ">>> SE ACEPTA H0 (Independencia confirmada).\n" if aceptado else ">>> SE RECHAZA H0.\n"
        txt_resultados.insert(tk.END, msg)

def actualizar_campos(event=None):
    metodo = combo_metodo.get()
    lbl_multiplicador.grid_remove()
    entry_multiplicador.grid_remove()
    lbl_constante.grid_remove()
    entry_constante.grid_remove()
    lbl_modulo.grid_remove()
    entry_modulo.grid_remove()
    lbl_semilla.config(text="X0 (Semilla):")

    if metodo == "Lehmer":
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
    global numeros_generados
    txt_resultados.delete(1.0, tk.END)
    try:
        metodo = combo_metodo.get()
        n = int(entry_n.get())
        
        if metodo == "Cuadrados Medios":
            x0 = int(entry_semilla.get())
            numeros_generados = generador_cuadrados_medios(x0, n)
        elif metodo == "Lehmer":
            x0 = int(entry_semilla.get())
            y = int(entry_multiplicador.get())
            numeros_generados = generador_lehmer(x0, y, n)
        elif metodo == "Congruencial Aditivo":
            semillas_str = entry_semilla.get().split(',')
            semillas = [int(s.strip()) for s in semillas_str]
            m = int(entry_modulo.get())
            numeros_generados = generador_aditivo(semillas, m, n)
        elif metodo == "Congruencial Multiplicativo":
            x0 = int(entry_semilla.get())
            a = int(entry_multiplicador.get())
            m = int(entry_modulo.get())
            numeros_generados = generador_multiplicativo(x0, a, m, n)
        elif metodo == "Congruencial Mixto":
            x0 = int(entry_semilla.get())
            a = int(entry_multiplicador.get())
            c = int(entry_constante.get())
            m = int(entry_modulo.get())
            numeros_generados = generador_mixto(x0, a, c, m, n)
            
        for i, val in enumerate(numeros_generados):
            txt_resultados.insert(tk.END, f"U_{i+1} = {val:.5f}\n")
            
    except ValueError:
        messagebox.showerror("Error", "Verifica que todos los campos visibles tengan datos válidos.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Generador y Evaluador de Pseudoaleatorios")
root.geometry("500x750")

frame_inputs = tk.LabelFrame(root, text="Generación de Números", padx=10, pady=10)
frame_inputs.pack(padx=10, pady=5, fill="x")

tk.Label(frame_inputs, text="N (Cantidad):").grid(row=0, column=0, sticky="w", pady=2)
entry_n = tk.Entry(frame_inputs)
entry_n.grid(row=0, column=1, pady=2)

tk.Label(frame_inputs, text="Método:").grid(row=1, column=0, sticky="w", pady=2)
combo_metodo = ttk.Combobox(frame_inputs, values=["Cuadrados Medios", "Lehmer", "Congruencial Aditivo", "Congruencial Multiplicativo", "Congruencial Mixto"], state="readonly", width=25)
combo_metodo.grid(row=1, column=1, pady=2)
combo_metodo.bind("<<ComboboxSelected>>", actualizar_campos)

lbl_semilla = tk.Label(frame_inputs, text="X0 (Semilla):")
lbl_semilla.grid(row=2, column=0, sticky="w", pady=2)
entry_semilla = tk.Entry(frame_inputs)
entry_semilla.grid(row=2, column=1, pady=2)

lbl_multiplicador = tk.Label(frame_inputs, text="Multiplicador (Y o a):")
entry_multiplicador = tk.Entry(frame_inputs)

lbl_constante = tk.Label(frame_inputs, text="Constante aditiva (c):")
entry_constante = tk.Entry(frame_inputs)

lbl_modulo = tk.Label(frame_inputs, text="Módulo (M):")
entry_modulo = tk.Entry(frame_inputs)

combo_metodo.current(0)
actualizar_campos()

tk.Button(frame_inputs, text="Generar Números", command=calcular, bg="lightblue").grid(row=6, column=0, columnspan=2, pady=10)

frame_pruebas = tk.LabelFrame(root, text="Pruebas Estadísticas", padx=10, pady=10)
frame_pruebas.pack(padx=10, pady=5, fill="x")

tk.Label(frame_pruebas, text="Seleccionar Prueba:").grid(row=0, column=0, sticky="w")
combo_pruebas = ttk.Combobox(frame_pruebas, values=["Prueba de los Promedios", "Test de las Rachas", "Prueba del Póker", "Prueba de Series"], state="readonly", width=23)
combo_pruebas.grid(row=0, column=1, padx=5)
combo_pruebas.current(0)

tk.Button(frame_pruebas, text="Aplicar Prueba", command=evaluar_prueba, bg="lightgreen").grid(row=0, column=2, padx=5)

frame_resultados = tk.LabelFrame(root, text="Consola de Resultados", padx=10, pady=10)
frame_resultados.pack(padx=10, pady=5, fill="both", expand=True)

txt_resultados = tk.Text(frame_resultados, width=50, height=15)
txt_resultados.pack(fill="both", expand=True)

if __name__ == "__main__":
    root.mainloop()