# Tarea de Limpieza de Datos — Documentación completa

> **Propósito**: Documentar paso a paso el script de limpieza de datos `main.py` que lee un CSV con las columnas `id, Nombre, email, gender, Ventas`, detecta y corrige inconsistencias, maneja valores faltantes, outliers, normaliza una columna y guarda un CSV limpio listo para análisis.

---

## Contenido del repositorio (sugerido)

- `main.py` — Script principal de limpieza (ejecutable).
- `datos_originales.csv` — Archivo CSV original (tu entrada).
- `datos_limpios.csv` — Archivo resultado que genera el script.
- `requirements.txt` — Dependencias (opcional).
- `README.md` — Este archivo (documentación).

---

## Requisitos / Prerrequisitos

- Python 3.8+ (recomendado).
- Paquetes de Python:
  - `pandas`
  - `numpy`
  - `scikit-learn` (si usas `MinMaxScaler`, explicado abajo)
- Opcionalmente, un entorno virtual (recomendado) para instalar dependencias sin afectar el sistema.

### Instalación rápida (Windows / macOS / Linux)

Crear y activar virtualenv (opcional, pero recomendado):

```bash
# Crear entorno virtual
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (cmd)
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Instalar dependencias:

```bash
python -m pip install --upgrade pip
pip install pandas numpy scikit-learn
```

(O con `requirements.txt`):
```text
# requirements.txt
pandas
numpy
scikit-learn
```
```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar

Coloca tu CSV (por ejemplo `datos_originales.csv`) en la misma carpeta que `main.py`. Luego:

```bash
python main.py datos_originales.csv
```

El script leerá el archivo, ejecutará la limpieza y generará `datos_limpios.csv`.

---

## Estructura esperada del CSV de entrada

Columnas (cabeceras) esperadas:

```
id,Nombre,email,gender,Ventas
```

- `id`: identificador entero.
- `Nombre`: nombre completo (cadena).
- `email`: correo (cadena).
- `gender`: género (valores esperados 'M' o 'F', mayúsculas o minúsculas posibles).
- `Ventas`: valor monetario que puede incluir símbolo `$` y comas, o estar vacío.

---

## README: explicación paso a paso (línea por línea / bloque por bloque)

### Encabezado y comentarios
Proporciona contexto y explica el propósito y uso del script.

### Imports (librerías)
- `sys`: lee argumentos desde la línea de comandos.
- `pandas`: manipulación de datos.
- `numpy`: operaciones numéricas.
- `MinMaxScaler` de `sklearn`: normalización de datos.

### Función principal `main(path_csv)`
Contiene todo el flujo: carga, limpieza, validación y guardado.

#### 1️⃣ Cargar datos
Usa `pd.read_csv()` para leer el CSV y `df.head()` para mostrar las primeras filas.

#### 2️⃣ Exploración inicial
Muestra información general (`df.info()`) y valores faltantes (`df.isnull().sum()`).

#### 3️⃣ Revisión de valores únicos
Permite conocer las variaciones en la columna `gender`.

#### 4️⃣ Limpieza de formato en `Ventas`
Elimina símbolos de dinero usando una **expresión regular raw string (`r'...`)** y convierte a tipo `float` con `pd.to_numeric()`.

#### 5️⃣ Manejo de valores faltantes
- Elimina filas sin `Nombre` o `email`.
- Imputa valores faltantes en `Ventas` con la media.

#### 6️⃣ Normalización de género
Estandariza el texto (mayúsculas, sin espacios) y sustituye códigos por etiquetas:  
`M → Masculino`, `F → Femenino`, otros → `No especificado`.

#### 7️⃣ Eliminación de duplicados
Elimina duplicados basados en `Nombre` y `email` para evitar repeticiones.

#### 8️⃣ Detección y eliminación de outliers (IQR)
Calcula el rango intercuartílico y filtra valores fuera de los límites `[Q1 - 1.5IQR, Q3 + 1.5IQR]`.

#### 9️⃣ Estandarización (MinMaxScaler)
Escala los valores de `Ventas` a un rango de 0 a 1, utilizando `MinMaxScaler` o un método manual si `scikit-learn` no está instalado.

#### 🔟 Validación y guardado
Usa `df.describe()` para mostrar un resumen estadístico y guarda los datos limpios en `datos_limpios.csv`.

---

## Errores comunes y soluciones

### ⚠ SyntaxWarning: invalid escape sequence '\$'
Causa: `'\$'` no es una secuencia válida.  
Solución: usar una **raw string** → `r'[\$,]'`.

### ❌ ModuleNotFoundError: No module named 'sklearn'
Causa: no está instalado `scikit-learn`.  
Solución:
```bash
pip install scikit-learn
```

---

## Decisiones de limpieza

| Aspecto | Decisión | Justificación |
|----------|-----------|---------------|
| Faltantes en `Nombre`/`email` | Eliminar | Sin identificadores, los registros son irrelevantes. |
| Faltantes en `Ventas` | Reemplazar por media | Evita perder filas con información útil. |
| Duplicados | Eliminar por `Nombre+email` | Evita repetición de registros. |
| Outliers | Eliminar fuera de [Q1−1.5IQR, Q3+1.5IQR] | Evita distorsión de estadísticas. |
| Escalado | MinMaxScaler (0–1) | Normaliza la magnitud de los valores. |

---

## Mejoras sugeridas

- Exportar registros eliminados (duplicados, outliers) a archivos separados.
- Añadir `logging` para registrar cada paso de limpieza.
- Configurar opciones por línea de comandos (ej. método de imputación).
- Validar correos con expresiones regulares.
- Incluir pruebas unitarias (`pytest`) para garantizar reproducibilidad.

---

## Comandos útiles

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install pandas numpy scikit-learn

# Ejecutar script
python main.py datos_originales.csv
```

---

## Resultado final

El archivo `datos_limpios.csv` contendrá los datos depurados, con:
- Todos los valores de `Ventas` numéricos y sin símbolos.
- Géneros estandarizados (`Masculino`, `Femenino`, `No especificado`).
- Sin filas duplicadas.
- Sin valores faltantes.
- Sin outliers detectables según el rango intercuartílico.
- Una nueva columna `Ventas_normalizadas` escalada entre 0 y 1.

---

## Licencia y autoría

Proyecto creado con fines educativos para la **Tarea de Limpieza de Datos (INTECAP)**.  
Autor: *Julio Alejandro Juarez Enriquez*  
Lenguaje: Python 3  
Dependencias: pandas, numpy, scikit-learn

---
