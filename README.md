**Simulador de Clima con Cadenas de Márkov**

Este proyecto es una aplicación de escritorio desarrollada en Python y PyQt6 que simula patrones climáticos usando cadenas de Márkov. Permite al usuario generar una secuencia histórica de estados del clima, calcular la matriz de transición, pronosticar días futuros y visualizar la distribución estacionaria.

---

## 📁 Estructura del proyecto

```
simulador_clima/
├─ main.py                  # Punto de entrada de la aplicación
├─ ui/                      # Interfaz de usuario (PyQt6)
│  ├─ icons/                # Imágenes de iconos y logos
│  │   ├─ soleado.png
│  │   ├─ parcialmente-soleado.png
│  │   ├─ parcialmente-nublado.png
│  │   ├─ nublado.png
│  │   └─ UPC_logo_transparente.png
│  ├─ icon_map.py           # Mapa de rutas absolutas a iconos y textos
│  ├─ FlowLayout.py         # Layout personalizado para iconos flotantes
│  ├─ main_window.py        # Ventana principal y navegación por páginas
│  └─ pages/                # Módulos de cada página de la UI
│     ├─ menu.py            # Página de menú principal
│     ├─ input.py           # Página de ingreso de número de días
│     ├─ sequence.py        # Página de secuencia histórica
│     ├─ matrix.py          # Página de matriz de transición
│     ├─ forecast.py        # Página de configuración de pronóstico
│     ├─ results.py         # Página de resultados por día
│     └─ detail.py          # Página de detalle (matriz A^n y vector)
│
├─ core/                    # Lógica de negocio y algoritmos
│  ├─ __init__.py
│  ├─ CadenaMarkov.py       # Implementación de la cadena de Márkov
│  ├─ Estado.py             # Definición de estados y utilidades
│  ├─ Calculos.py           # Funciones matemáticas (multiplicaciones, vector estacionario)
│  ├─ HistorialClima.py     # Generación de secuencia histórica
│  └─ MatrizTransicion.py   # Construcción de la matriz de transición
```

---

## 🛠 Requisitos

* Python 3.8 o superior
* PyQt6

Instalar dependencias:

```bash
pip install PyQt6
```

---

## 🚀 Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

La aplicación se abrirá mostrando el menú principal. Luego:

1. **Nueva simulación**: Ingresar un valor entre 20 y 40 para los días históricos.
2. **Visualizar secuencia**: Ver iconos con la secuencia generada.
3. **Matriz de transición**: Calcular y mostrar la matriz.
4. **Pronóstico**: Elegir cuántos días pronosticar.
5. **Resultados por día**: Ver iconos para cada día pronosticado.
6. **Detalle y estado estacionario**: Consultar la matriz A^n, vector de probabilidades y distribución estacionaria.

---

## 📦 Paquetes y módulos

* **ui/**: Todo lo relacionado a la interfaz gráfica.
* **core/**: Algoritmos y lógica de la simulación.
* **ui/icons/**: Recursos de imágenes.

