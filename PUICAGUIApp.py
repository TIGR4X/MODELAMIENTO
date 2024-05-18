import tkinter as tk
from tkinter import ttk, filedialog
import subprocess

class PUICAGUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PUICA GUI")
        self.geometry("800x600")

        # Crear pestañas
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", padx=10, pady=10)

        # Pestaña de entrada
        self.input_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.input_tab, text="Entrada")
        self.create_input_widgets()

        # Pestaña de salida
        self.output_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.output_tab, text="Salida")
        self.result_text = tk.Text(self.output_tab, height=20, width=70)
        self.result_text.pack(pady=10)

        # Botón para seleccionar archivo de entrada
        self.input_button = tk.Button(self.input_tab, text="Seleccionar archivo de entrada", command=self.select_input_file)
        self.input_button.pack(pady=10)

        # Botón para ejecutar el modelo
        self.run_button = tk.Button(self, text="Ejecutar Modelo", command=self.run_model)
        self.run_button.pack(pady=10)

    def create_input_widgets(self):
        input_frame = ttk.Frame(self.input_tab)
        input_frame.pack(padx=10, pady=10)

        self.input_label = ttk.Label(input_frame, text="Archivo de entrada seleccionado:")
        self.input_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.input_entry = ttk.Entry(input_frame, state="readonly")
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo de entrada", filetypes=[("Archivos de texto", "*.txt")])
        self.input_entry.configure(state="normal")
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)
        self.input_entry.configure(state="readonly")

    def generate_dzn_file(self, file_path):
        with open(file_path, "r") as input_file:
            lines = input_file.readlines()

        n = int(lines[0].strip())
        m = int(lines[1].strip())
        fi = [float(x) for x in lines[2].strip().split(",")]
        ci = [int(x) for x in lines[3].strip().split(",")]
        dc = [float(x) for x in lines[4].strip().split(",")]
        bci = []
        for row in lines[5:5+n]:
            bci.append([float(x) for x in row.strip().split(",")])

        with open("DatosPUICA.dzn", "w") as file:
            file.write(f"n = {n}; % Número de clientes\n")
            file.write(f"m = {m}; % Número de sitios posibles para instalaciones\n")
            file.write(f"f = [{','.join(map(str, fi))}]; % Costos fijos de abrir cada instalación\n")
            file.write(f"c = [{','.join(map(str, ci))}]; % Capacidades máximas de producción de cada instalación\n")
            file.write(f"d = [{','.join(map(str, dc))}]; % Demandas de los clientes\n")
            file.write("b = [| ")
            for row in bci:
                file.write(",".join(map(str, row)) + ", | ")
            file.write("|]; % Beneficios\n")

    def run_model(self):
        input_file_path = self.input_entry.get()
        if input_file_path:
            self.generate_dzn_file(input_file_path)
            result = subprocess.run(["minizinc", "PUICA.mzn", "DatosPUICA.dzn"], capture_output=True, text=True)
            self.show_output(result.stdout)
        else:
            messagebox.showerror("Error", "Debe seleccionar un archivo de entrada válido.")

    def show_output(self, output):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, output)

if __name__ == "__main__":
    app = PUICAGUIApp()
    app.mainloop()