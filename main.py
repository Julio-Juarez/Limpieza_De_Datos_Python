
# ========================================
# LIMPIEZA DE DATOS - 
# ========================================

# 1 Importación de librerías
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

# 2 Cargar datos
# Lectura del archivo CSV original que contiene los datos a limpiar
df = pd.read_csv("Limpiezadedatos.csv")
print("Vista inicial:")
print(df.head(), "\n")

# 3 Exploración inicial
# Esta etapa nos permite entender la estructura de los datos y detectar problemas
# como valores faltantes, tipos de datos incorrectos o inconsistencias
print("Información general:")
print(df.info(), "\n")

# Contabilización de valores nulos por columna para identificar datos faltantes
print("Valores faltantes:")
print(df.isnull().sum(), "\n")

# Análisis de valores únicos en la columna género para detectar inconsistencias
print("Valores únicos en 'gender':", df['gender'].unique(), "\n")

# 4 Limpieza de formato en la columna 'Ventas'
# Eliminación de caracteres no numéricos (símbolos de dinero y comas)
# para convertir los datos de texto a formato numérico float
df['Ventas'] = df['Ventas'].replace(r'[\$,]', '', regex=True).astype(float)

# 5 Manejo de valores faltantes
# Eliminación de registros donde faltan datos críticos como nombre o email
# ya que estos campos son identificadores únicos y no pueden ser imputados
df = df.dropna(subset=['Nombre', 'email'])

# Para valores faltantes en ventas, utilizamos imputación con la media
# Esto permite mantener los registros sin distorsionar la distribución general
df['Ventas'] = df['Ventas'].fillna(df['Ventas'].mean())

print("Después de manejar NaN:")
print(df.isnull().sum(), "\n")

# 6 Corrección de formato de género
# Estandarización del texto: conversión a mayúsculas y eliminación de espacios
# para uniformizar los valores categóricos
df['gender'] = df['gender'].str.upper().str.strip()

# Mapeo de valores abreviados a categorías completas y consistentes
# Los valores vacíos se convierten a NaN para un manejo apropiado
df['gender'] = df['gender'].replace({'M': 'Masculino', 'F': 'Femenino', '': np.nan})

# Asignación de una categoría explícita para valores no especificados
# en lugar de dejar valores nulos en datos categóricos
df['gender'] = df['gender'].fillna('No especificado')

print("Valores únicos en género normalizados:", df['gender'].unique(), "\n")

# 7 Eliminación de duplicados
# Remoción de registros duplicados basados en la combinación de nombre y email
# que deberían ser únicos para cada individuo en el dataset
df = df.drop_duplicates(subset=['Nombre', 'email'])
print(f"Registros después de eliminar duplicados: {len(df)}\n")

# 8 Detección de valores atípicos
# Cálculo del rango intercuartílico (IQR) para identificar outliers estadísticos
# que pueden afectar negativamente los análisis posteriores
Q1 = df['Ventas'].quantile(0.25)  # Primer cuartil (percentil 25)
Q3 = df['Ventas'].quantile(0.75)  # Tercer cuartil (percentil 75)
IQR = Q3 - Q1  # Rango intercuartílico

# Definición de límites inferior y superior para valores normales
# utilizando el criterio estándar de 1.5 veces el IQR
rango_bajo = Q1 - 1.5 * IQR
rango_alto = Q3 + 1.5 * IQR

# Identificación de registros que caen fuera del rango normal
outliers = df[(df['Ventas'] < rango_bajo) | (df['Ventas'] > rango_alto)]
print(f"Valores atípicos detectados: {len(outliers)}")

# Eliminación de los valores atípicos para obtener un dataset más robusto
# y representativo de la distribución central de los datos
df = df[(df['Ventas'] >= rango_bajo) & (df['Ventas'] <= rango_alto)]
print(f"Registros después de limpiar outliers: {len(df)}\n")

# 9 Estandarización (normalización de 'Ventas')
# Aplicación de normalización Min-Max para escalar los valores de ventas
# al rango [0, 1], lo que facilita la comparación y el uso en algoritmos

scaler = MinMaxScaler()
df['Ventas_normalizadas'] = scaler.fit_transform(df[['Ventas']])

# 10 Validación final
# Verificación integral del dataset limpio para asegurar que cumple
# con los estándares de calidad requeridos para el análisis
print("Resumen final:")
print(df.describe())
print(df.info())

# Guardar el archivo limpio
# Exportación del dataset procesado para su uso en análisis posteriores
df.to_csv("datos_limpios.csv", index=False)
print("\nArchivo 'datos_limpios.csv' guardado correctamente.")