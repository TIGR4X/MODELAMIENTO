import tkinter as tk
from tkinter import ttk, filedialog, Text, Scrollbar, END
import subprocess
import os

#funcion que convierte el archivo txt en un archivo dzn para ser utilizado por minizinc
def convert_txt_to_dzn(txt_file_path, dzn_file_path):
    with open(txt_file_path, 'r') as txt_file:
        lines = txt_file.readlines()

    n = lines[0].strip()
    m = lines[1].strip()
    f = lines[2].strip().split(',')
    c = lines[3].strip().split(',')
    d = lines[4].strip().split(',')
    b = [lines[i].strip().split(',') for i in range(5, 5 + int(n))]

    with open(dzn_file_path, 'w') as dzn_file:
        dzn_file.write(f"n = {n};\n")
        dzn_file.write(f"m = {m};\n")
        dzn_file.write(f"f = [{','.join(f)}];\n")
        dzn_file.write(f"c = [{','.join(c)}];\n")
        dzn_file.write(f"d = [{','.join(d)}];\n")
        b_flat = ', '.join([f"| {', '.join(row)}" for row in b])
        b_flat += " |"
        dzn_file.write(f"b = [{b_flat}];\n")

#ventana emergente para seleccionar texto
def select_txt_file():
    global dzn_file_path
    txt_file_path = filedialog.askopenfilename(title="Seleccionar archivo TXT", filetypes=(("Archivos de texto", "*.txt"),))
    if txt_file_path:
        with open(txt_file_path, 'r') as file:
            input_text.delete(1.0, END)
            input_text.insert(END, file.read())
        dzn_file_path = os.path.join(os.path.dirname(txt_file_path), "DatosPUICA.dzn")
        convert_txt_to_dzn(txt_file_path, dzn_file_path)
        print(f"Convertido {txt_file_path} a {dzn_file_path}")

def encontrar_ejecutable(nombre_ejecutable):
    # Separar las rutas del PATH usando el delimitador adecuado según el sistema operativo
    paths = os.environ["PATH"].split(os.pathsep)

    # Iterar sobre cada ruta en el PATH
    for path in paths:
        # Combinar la ruta con el nombre del archivo ejecutable
        ruta_completa = os.path.join(path, nombre_ejecutable)
        # Verificar si el archivo existe y es ejecutable
        if os.path.isfile(ruta_completa) and os.access(ruta_completa, os.X_OK):
            return ruta_completa

    # Si no se encontró el ejecutable, devolver None
    return None

# Nombre del ejecutable 
nombre_ejecutable = "minizinc.exe"

# Llamado de función para encontrar el ejecutable
ruta_ejecutable = encontrar_ejecutable(nombre_ejecutable)

if ruta_ejecutable:
    print(f"Se encontró el ejecutable en: {ruta_ejecutable}")
else:
    print("No se encontró el ejecutable en el PATH.")

#funcion que soluciona el problema
def solve_problem():
    global dzn_file_path
    if dzn_file_path:
        model_path = 'PUICA.mzn'  # ruta al archivo del modelo MiniZinc // debe estar en el mismo directorio
        minizinc_executable = encontrar_ejecutable("minizinc.exe")  # Búsqueda del ejecutable de MiniZinc en el PATH
        if minizinc_executable and os.path.exists(minizinc_executable):  # Verificar si la ruta devuelta es válida
            print(f"Running MiniZinc with model {model_path} and data {dzn_file_path}")
            command = [minizinc_executable, '--solver', 'coin-bc', model_path, dzn_file_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            output_text.delete(1.0, END)
            output_text.insert(END, stdout.decode())
        else:
            output_text.delete(1.0, END)
            output_text.insert(END, "Ejecutable de Minizinc no se encontró en el PATH.")
    else:
        output_text.delete(1.0, END)
        output_text.insert(END, "Selecciona un archivo TXT.")

############################# ui #############################
root = tk.Tk()
root.title("Modelo PUICA")
root.geometry("620x680")

style = ttk.Style()
style.configure('TButton', padding=6, relief="flat", background="#ccc", foreground="#333", font=("Arial", 12))
style.map('TButton', background=[('active', '#999'), ('disabled', '#ccc')])

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

btn_select_file = ttk.Button(frame, text="Seleccionar TXT", command=select_txt_file)
btn_select_file.grid(row=0, column=0, padx=5, pady=5)

input_text_frame = ttk.LabelFrame(frame, text="Entrada")
input_text_frame.grid(row=1, column=0, padx=5, pady=5)

input_text = Text(input_text_frame, wrap='word', width=80, height=15, padx=5, pady=5, font=("Arial", 10))
input_text.grid(row=0, column=0)

input_scrollbar = Scrollbar(input_text_frame, command=input_text.yview)
input_scrollbar.grid(row=0, column=1, sticky='nsew')
input_text['yscrollcommand'] = input_scrollbar.set

btn_solve = ttk.Button(frame, text="Solucionar", command=solve_problem)
btn_solve.grid(row=2, column=0, padx=5, pady=5)

output_text_frame = ttk.LabelFrame(frame, text="Salida")
output_text_frame.grid(row=3, column=0, padx=5, pady=5)

output_text = Text(output_text_frame, wrap='word', width=80, height=15, padx=5, pady=5, font=("Arial", 10))
output_text.grid(row=0, column=0)

output_scrollbar = Scrollbar(output_text_frame, command=output_text.yview)
output_scrollbar.grid(row=0, column=1, sticky='nsew')
output_text['yscrollcommand'] = output_scrollbar.set

dzn_file_path = None

root.mainloop()
