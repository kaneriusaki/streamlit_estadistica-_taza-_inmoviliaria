from fpdf import FPDF
import pandas as pd


def generate_pdf_report(df: pd.DataFrame, stats: dict) -> bytes:
    """Genera el reporte PDF a partir de los datos y estadísticas."""
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 15, 'Reporte de Preferencias de Mercado', new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font('helvetica', 'I', 12)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 10, 'Generado por IA Real Estate Analytics', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 10, '1. Preferencias de Mercado Mas Comunes', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    hab_comun = df['habitaciones'].mode()[0]
    area_promedio = df['area_m2'].mean()
    pdf.multi_cell(0, 8, f"- Habitaciones mas solicitadas: {int(hab_comun)} habitaciones.\n- Area promedio del mercado: {area_promedio:.1f} metros cuadrados.")
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 10, '2. Preferencias Menos Comunes (Atipicas)', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    banos_menos_comun = df['banos'].value_counts().idxmin()
    pdf.multi_cell(0, 8, f"- La cantidad de banos menos frecuente es: {int(banos_menos_comun)} banos.\n- Propiedades muy grandes (>6 habs): {len(df[df['habitaciones'] > 6])}\n- Propiedades antiguas (>40 anios): {len(df[df['antiguedad_anos'] > 40])}\n- Propiedades pequenas con piscina: {len(df[(df['area_m2'] < 80) & (df['tiene_piscina'] == 1)])}")
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 10, '3. Analisis Economico: Impacto en Precio', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    coefs = stats.get('feature_importance', {})
    mas_caras = sorted(coefs.items(), key=lambda x: x[1], reverse=True)[:2]
    mas_baratas = sorted(coefs.items(), key=lambda x: x[1])[:2]
    
    format_names = {
        "area_m2": "Area (m2)",
        "habitaciones": "Habitaciones",
        "banos": "Banos",
        "distancia_centro_km": "Distancia al Centro (km)",
        "antiguedad_anos": "Antiguedad (anios)",
        "tiene_piscina": "Tiene Piscina"
    }
    
    n_cara = format_names.get(mas_caras[0][0], mas_caras[0][0]) if mas_caras else "Desconocido"
    v_cara = mas_caras[0][1] if mas_caras else 0
    n_barata = format_names.get(mas_baratas[0][0], mas_baratas[0][0]) if mas_baratas else "Desconocido"
    v_barata = mas_baratas[0][1] if mas_baratas else 0
    
    pdf.multi_cell(0, 8, f"Caracteristica mas cara: {n_cara} (+${v_cara:,.0f})\nCaracteristica que mas devalua: {n_barata} (${v_barata:,.0f})")
    pdf.ln(5)
    
    pdf.multi_cell(0, 8, f"Desglose de costos principales:\n- Cada m2 extra suma: ${coefs.get('area_m2', 0):,.0f}\n- Cada km lejos del centro resta: ${abs(coefs.get('distancia_centro_km', 0)):,.0f}\n- Cada anio de antiguedad resta: ${abs(coefs.get('antiguedad_anos', 0)):,.0f}")
    
    pdf.ln(15)
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, 'Documento generado de forma automatizada por IA.', new_x="LMARGIN", new_y="NEXT", align='C')
    
    return bytes(pdf.output())
