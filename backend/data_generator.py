import pandas as pd
import numpy as np

def generate_real_estate_data(n_samples=500):
    """
    Genera un dataset sintético pero realista de propiedades inmobiliarias.
    """
    np.random.seed(42)
    
    # Generar características
    area_m2 = np.random.normal(loc=120, scale=40, size=n_samples) # Media 120m2
    area_m2 = np.clip(area_m2, 40, 500) # Limitar entre 40 y 500
    
    habitaciones = np.round(area_m2 / 40 + np.random.normal(0, 0.5, size=n_samples))
    habitaciones = np.clip(habitaciones, 1, 8)
    
    banos = np.round(habitaciones / 2 + np.random.normal(0, 0.5, size=n_samples))
    banos = np.clip(banos, 1, 5)
    
    distancia_centro_km = np.random.exponential(scale=5, size=n_samples)
    distancia_centro_km = np.clip(distancia_centro_km, 0.1, 30)
    
    antiguedad_anos = np.random.uniform(0, 50, size=n_samples)
    
    tiene_piscina = np.where(area_m2 > 150, np.random.choice([0, 1], p=[0.4, 0.6], size=n_samples), 
                             np.random.choice([0, 1], p=[0.9, 0.1], size=n_samples))
    
    # Calcular precio (Lógica oculta real)
    # Precio base + 2000 por m2 + 10000 por hab + 8000 por baño - 5000 por km - 500 por año + 25000 por piscina
    precio_real = (
        30000 + 
        (area_m2 * 2000) + 
        (habitaciones * 10000) + 
        (banos * 8000) - 
        (distancia_centro_km * 5000) - 
        (antiguedad_anos * 500) + 
        (tiene_piscina * 25000)
    )
    
    # Añadir ruido estadístico para que el modelo no sea 100% perfecto
    ruido = np.random.normal(0, 20000, size=n_samples)
    precio_lista = precio_real + ruido
    precio_lista = np.clip(precio_lista, 20000, None)
    
    # Coordenadas falsas (simulando una ciudad)
    lat_centro = 40.7128 # Ej. New York, pero vamos a esparcir en base a distancia
    lon_centro = -74.0060
    
    angulos = np.random.uniform(0, 2*np.pi, size=n_samples)
    latitudes = lat_centro + (distancia_centro_km / 111.0) * np.cos(angulos)
    longitudes = lon_centro + (distancia_centro_km / (111.0 * np.cos(np.radians(lat_centro)))) * np.sin(angulos)

    df = pd.DataFrame({
        'id': range(1, n_samples + 1),
        'latitud': latitudes,
        'longitud': longitudes,
        'area_m2': area_m2.round(2),
        'habitaciones': habitaciones.astype(int),
        'banos': banos.astype(int),
        'distancia_centro_km': distancia_centro_km.round(2),
        'antiguedad_anos': antiguedad_anos.round(1),
        'tiene_piscina': tiene_piscina,
        'precio_lista': precio_lista.round(2)
    })
    
    return df

dataset = generate_real_estate_data()
