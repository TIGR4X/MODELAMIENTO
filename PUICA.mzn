%Parámetros
int: n; % Número de clientes
int: m; % Número de sitios posibles para instalaciones
array[1..m] of float: f; % Costos fijos de abrir cada instalación
array[1..m] of int: c; % Capacidades máximas de producción de cada instalación
array[1..n] of float: d; % Demandas de los clientes
array[1..n, 1..m] of float: b; % Beneficios por vender a cada cliente desde cada instalación

% Variables de decisión
array[1..n, 1..m] of var 0.0..50000: x; % Cantidad a enviar de cada instalación a cada cliente
array[1..m] of var 0..1: a; % 1 si la instalación se abre, 0 en caso contrario

% Restricciones
% 1. Satisfacer la demanda de cada cliente
constraint forall(j in 1..n)(sum(i in 1..m)(x[j, i]) == d[j]);

% 2. No exceder la capacidad de cada instalación
constraint forall(i in 1..m)(sum(j in 1..n)(x[j, i]) <= c[i] * a[i]);

% 3. Si no se abre una instalación, no se puede enviar productos desde ella
constraint forall(i in 1..m, j in 1..n)(x[j, i] <= c[i] * a[i]);

% 4. No negatividad de Matriz
constraint forall(j in 1..n, i in 1..m)(x[j,i] >= 0);

% 5. Cota superior Matriz
constraint forall(j in 1..n, i in 1..m)(x[j,i] <= max(c));

% Función objetivo: maximizar el beneficio total
solve maximize sum(i in 1..m, j in 1..n)(b[j, i] * x[j, i]) - sum(i in 1..m)(f[i] * a[i]);

    
% Mostrar los valores de las variables de decisión
%output ["Cantidad a enviar de cada instalación a cada cliente (x):"]
  %++ [show(x[j, i]) ++ if j == n /\ i == m then "" else " " endif | i in 1..m, j in 1..n];

%output ["Instalaciones abiertas (a):"]
  %++ [show(a[i]) ++ if i == m then "" else ", " endif | i in 1..m];
  
% Mostrar el valor de la función objetivo (utilidad máxima)
output ["\nUtilidad máxima: ", show(sum(i in 1..m, j in 1..n)(b[j, i] * x[j, i]) - sum(i in 1..m)(f[i] * a[i]))];

% Mostrar las cantidades a enviar de cada instalación a cada cliente
% Mostrar las cantidades a enviar de cada instalación a cada cliente
output ["Productos que se enviarán al cliente c desde la instalación i:"]
  ++ [if fix(x[j, i]) > 0 then
       "\nx[" ++ show(j) ++ ", " ++ show(i) ++ "] = " ++ show_float(6, 2, x[j, i]) ++ " (enviar " ++ show_float(6, 2, x[j, i]) ++ " unidades al cliente " ++ show(j) ++ " desde la instalación " ++ show(i) ++ ")"
     else
       ""
     endif | i in 1..m, j in 1..n]
  ++ ["\n"]

% Mostrar las instalaciones que se abrirán
++ ["Instalaciones que se abrirán:"]
++ [if fix(a[i]) == 1 then
     "\na[" ++ show(i) ++ "] = 1 (abrir la instalación " ++ show(i) ++ ")"
   else
     "\na[" ++ show(i) ++ "] = 0 (no abrir la instalación " ++ show(i) ++ ")"
   endif | i in 1..m];
