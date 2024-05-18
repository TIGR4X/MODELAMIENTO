Explicación del código:
Se crea una clase PUICAGUIApp que hereda de tk.Tk (la ventana principal de Tkinter).
En el método __init__, se crea la ventana principal y se configuran las pestañas ("Entrada" y "Salida").
En la pestaña "Entrada", se crean los widgets necesarios (etiquetas y campos de entrada) para que el usuario pueda ingresar los valores de n, m, fi, ci, dc y bci.
En la pestaña "Salida", se crea un área de texto (self.result_text) donde se mostrarán los resultados de la solución.
Se crea un botón "Ejecutar Modelo" que ejecuta el método run_model cuando se presiona.
El método generate_dzn_file recopila los valores ingresados por el usuario y genera el archivo DatosPUICA.dzn.
El método run_model llama a generate_dzn_file para generar el archivo DatosPUICA.dzn, luego ejecuta el modelo MiniZinc PUICA.mzn utilizando subprocess y pasa la salida al método show_output.
El método show_output muestra la salida del modelo MiniZinc en el área de texto self.result_text de la pestaña "Salida".