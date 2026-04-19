import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import date

# ── CONFIG ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Matriz de Kraljic – Elymar Estévez",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── ESTILOS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #f0f4f8; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
h1 { color: #1e3a5f; font-weight: 800; }
h2, h3 { color: #2563eb; font-weight: 700; }
.stButton>button { border-radius: 8px; font-weight: 600; }
.stButton>button:first-child { background: linear-gradient(135deg,#2563eb,#0284c7); color: white; border: none; }
.metric-card { background: white; border: 1px solid #b8d0e8; border-radius: 12px; padding: 16px 20px; text-align: center; box-shadow: 0 2px 8px rgba(37,99,235,.07); }
.metric-value { font-size: 2rem; font-weight: 800; color: #1e3a5f; }
.metric-label { font-size: 0.75rem; color: #4a6fa5; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
.metric-sub { font-size: 0.72rem; color: #4a6fa5; margin-top: 2px; }
.quadrant-pill { display: inline-block; padding: 3px 10px; border-radius: 10px; font-size: 0.75rem; font-weight: 700; }
.rec-box { border-radius: 10px; padding: 16px; margin-bottom: 12px; }
.footer { text-align: center; color: #4a6fa5; font-size: 0.75rem; padding: 20px 0; border-top: 1px solid #b8d0e8; margin-top: 30px; }
.header-box { background: linear-gradient(135deg,#1e3a6e,#2563eb); border-radius: 14px; padding: 22px 28px; margin-bottom: 24px; color: white; display: flex; justify-content: space-between; align-items: center; }
</style>
""", unsafe_allow_html=True)

# ── TEXTOS BILINGÜE ───────────────────────────────────────────────
LANG = {
    'es': {
        'title': 'Matriz de Kraljic',
        'subtitle': 'Herramienta de Análisis de Compras Estratégicas',
        'client': 'Nombre del Cliente / Empresa',
        'sector': 'Sector de la Empresa',
        'analyst': 'Analista / Consultor',
        'date': 'Fecha del Análisis',
        'mode': 'Modo de Entrada',
        'by_cat': 'Por Categoría',
        'by_sup': 'Por Proveedor',
        'add_data': 'Introduce tus datos',
        'name_col': 'Categoría / Proveedor',
        'spend_col': 'Gasto Anual (€)',
        'generate': '🔲 Generar Matriz',
        'download_tpl': '⬇ Descargar plantilla Excel',
        'upload': '📤 Cargar Excel',
        'autoscore': '💡 La app calcula automáticamente el Impacto y el Riesgo. Solo introduce el nombre y el gasto.',
        'total_spend': 'Gasto Total',
        'strategic': 'Estratégico',
        'leverage': 'Apalancamiento',
        'bottleneck': 'Cuello de Botella',
        'noncritical': 'No Crítico',
        'matrix_title': '🔲 Matriz de Kraljic',
        'scatter_title': '📈 Gráfico de Dispersión – Gasto vs Riesgo & Complejidad',
        'score_table': '📊 Detalle de Puntuaciones',
        'recs_title': '💡 Recomendaciones y Planes de Acción',
        'inferred': 'Categoría Inferida',
        'impact': 'Impacto Negocio',
        'risk': 'Riesgo Suministro',
        'quadrant': 'Cuadrante',
        'high_risk': 'Alto riesgo',
        'low_risk': 'Bajo riesgo',
        'high_impact': 'Alto impacto',
        'low_impact': 'Bajo impacto',
        'analyst_lbl': 'Analista',
        'sector_lbl': 'Sector',
        'items': 'elementos',
        'urgent': 'URGENTE',
        'short': 'CORTO PLAZO',
        'mid': 'MEDIO PLAZO',
        'no_items': 'Sin categorías en este cuadrante',
        'footer': 'Matriz de Kraljic · Herramienta de Análisis de Compras Estratégicas · Creado por Elymar Estévez',
        'select_sector': '-- Seleccionar sector --',
        'x_axis': 'GASTO ANUAL (€)',
        'y_axis': 'RIESGO & COMPLEJIDAD',
    },
    'en': {
        'title': 'Kraljic Matrix',
        'subtitle': 'Strategic Purchasing Analysis Tool',
        'client': 'Client / Company Name',
        'sector': 'Business Sector',
        'analyst': 'Analyst / Consultant',
        'date': 'Analysis Date',
        'mode': 'Input Mode',
        'by_cat': 'By Category',
        'by_sup': 'By Supplier',
        'add_data': 'Enter your data',
        'name_col': 'Category / Supplier',
        'spend_col': 'Annual Spend (€)',
        'generate': '🔲 Generate Matrix',
        'download_tpl': '⬇ Download Excel template',
        'upload': '📤 Upload Excel',
        'autoscore': '💡 The app automatically calculates Impact and Risk. Just enter the name and spend.',
        'total_spend': 'Total Spend',
        'strategic': 'Strategic',
        'leverage': 'Leverage',
        'bottleneck': 'Bottleneck',
        'noncritical': 'Non-Critical',
        'matrix_title': '🔲 Kraljic Matrix',
        'scatter_title': '📈 Scatter Chart – Spend vs Risk & Complexity',
        'score_table': '📊 Score Detail',
        'recs_title': '💡 Recommendations & Action Plans',
        'inferred': 'Inferred Category',
        'impact': 'Business Impact',
        'risk': 'Supply Risk',
        'quadrant': 'Quadrant',
        'high_risk': 'High risk',
        'low_risk': 'Low risk',
        'high_impact': 'High impact',
        'low_impact': 'Low impact',
        'analyst_lbl': 'Analyst',
        'sector_lbl': 'Sector',
        'items': 'items',
        'urgent': 'URGENT',
        'short': 'SHORT-TERM',
        'mid': 'MID-TERM',
        'no_items': 'No categories in this quadrant',
        'footer': 'Kraljic Matrix · Strategic Purchasing Analysis Tool · Created by Elymar Estévez',
        'select_sector': '-- Select sector --',
        'x_axis': 'ANNUAL SPEND (€)',
        'y_axis': 'RISK & COMPLEXITY',
    }
}

SECTORS = {
    'es': {
        '': '-- Seleccionar sector --',
        'manufactura': 'Manufactura / Industria',
        'retail': 'Retail / Comercio',
        'salud': 'Salud / Farmacia',
        'it': 'Tecnología / IT',
        'construccion': 'Construcción / Infraestructura',
        'servicios': 'Servicios / Consultoría',
        'alimentacion': 'Alimentación / Agroindustria',
        'energia': 'Energía / Utilities',
    },
    'en': {
        '': '-- Select sector --',
        'manufactura': 'Manufacturing / Industry',
        'retail': 'Retail / Commerce',
        'salud': 'Health / Pharma',
        'it': 'Technology / IT',
        'construccion': 'Construction / Infrastructure',
        'servicios': 'Services / Consulting',
        'alimentacion': 'Food / Agro-industry',
        'energia': 'Energy / Utilities',
    }
}

# ── SCORING ENGINE ────────────────────────────────────────────────
RULES = [
    (['materia prima','insumo','commodity','mineral','metal','acero','aluminio','cobre','plastico','resina','raw material'], 9, 7, 'Materia Prima', 'Raw Material'),
    (['medicamento','fármaco','vacuna','reactivo','reagent','biologico','diagnóstico','diagnostic','drug','pharma'], 10, 9, 'Medicamento / Reactivo', 'Drug / Reagent'),
    (['maquinaria','equipamiento','equipo','machinery','equipment','turbina','generador','generator','cnc','robot','automatización'], 8, 7, 'Maquinaria / Equipo', 'Machinery / Equipment'),
    (['software','licencia','license','saas','erp','crm','cloud','nube','plataforma','sistema'], 8, 8, 'Software / Tecnología', 'Software / Technology'),
    (['ciberseguridad','cybersecurity','seguridad it','firewall','antivirus','siem'], 9, 9, 'Ciberseguridad', 'Cybersecurity'),
    (['hardware','servidor','server','ordenador','computer','dispositivo','network','telecomunicaciones'], 7, 6, 'Hardware / Infraestructura', 'Hardware / Infrastructure'),
    (['logística','logistic','transporte','transport','flete','freight','distribución','warehouse','courier'], 6, 5, 'Logística / Transporte', 'Logistics / Transport'),
    (['energía','energia','electricidad','electricity','gas natural','combustible','fuel','utilities'], 7, 7, 'Energía / Utilities', 'Energy / Utilities'),
    (['embalaje','packaging','envase','container','caja','botella','etiqueta'], 5, 4, 'Embalaje / Packaging', 'Packaging'),
    (['mantenimiento','maintenance','mro','repuesto','spare','pieza','reparación'], 5, 6, 'Mantenimiento / MRO', 'Maintenance / MRO'),
    (['consultoría','consulting','asesoría','advisory','outsourcing','servicios profesionales'], 6, 5, 'Servicios Profesionales', 'Professional Services'),
    (['talento','talent','personal','staff','rrhh','hr','recursos humanos','formación','training'], 7, 6, 'Talento / RRHH', 'Talent / HR'),
    (['marketing','publicidad','advertising','comunicación','marca','brand','digital','campaña'], 5, 3, 'Marketing / Publicidad', 'Marketing / Advertising'),
    (['construcción','construction','obra','hormigón','concrete','cemento','cement'], 8, 7, 'Construcción / Infraestructura', 'Construction / Infrastructure'),
    (['producto','product','mercancía','merchandise','artículo','sku','inventario','stock'], 7, 5, 'Producto Comercial', 'Commercial Product'),
    (['equipo médico','medical equipment','instrumental','medical device','implante','ortopedia'], 9, 8, 'Equipo Médico', 'Medical Equipment'),
    (['alimento','food','ingrediente','ingredient','cereal','trigo','maíz','soja','carne','leche','fruta','verdura'], 8, 7, 'Alimentación / Ingrediente', 'Food / Ingredient'),
    (['scada','plc','instrumentación','instrumentation','sensor','automatización industrial'], 9, 8, 'Automatización Industrial', 'Industrial Automation'),
    (['suministro','supply','oficina','office','papelería','tóner','papel','limpieza','higiene'], 2, 1, 'Suministros Generales', 'General Supplies'),
    (['seguridad','safety','epi','ppe','protección','señalización'], 4, 2, 'Seguridad / EPIs', 'Safety / PPE'),
]

SECTOR_MOD = {
    'manufactura': {'materia': 1, 'machinery': 1, 'mro': 1, 'energy': 1},
    'retail':      {'product': 2, 'logistics': 1, 'packaging': 1},
    'salud':       {'drug': 1, 'medical': 1, 'reagent': 1, 'cyber': 1},
    'it':          {'software': 1, 'cyber': 2, 'hardware': 1},
    'construccion':{'construction': 1, 'machinery': 1, 'steel': 1},
    'servicios':   {'talent': 2, 'consulting': 1, 'software': 1},
    'alimentacion':{'food': 2, 'packaging': 1, 'logistics': 1, 'ingredient': 1},
    'energia':     {'scada': 1, 'machinery': 1, 'energy': 1, 'automation': 1},
}

def score_item(name, spend, total_spend, sector):
    nl = (name or '').lower()
    impact, risk, ies, ien = 4, 4, 'Otros', 'Others'
    for kws, bi, br, les, len_ in RULES:
        if any(k in nl for k in kws):
            impact, risk, ies, ien = bi, br, les, len_
            break
    mods = SECTOR_MOD.get(sector, {})
    inf = ies.lower()
    for k, b in mods.items():
        if k in inf or k in nl:
            risk = min(10, risk + b)
            impact = min(10, impact + (b + 1) // 2)
    if total_spend > 0:
        pct = spend / total_spend
        if pct > 0.3:   impact = min(10, impact + 2)
        elif pct > 0.2: impact = min(10, impact + 1)
        elif pct < 0.02: impact = max(1, impact - 1)
    return round(impact), round(risk), ies, ien

def get_quadrant(impact, risk):
    hi, hr = impact >= 5.5, risk >= 5.5
    if hi and hr:   return 'strategic'
    if not hi and hr: return 'bottleneck'
    if hi and not hr: return 'leverage'
    return 'noncritical'

def fmt_spend(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M€"
    if n >= 1_000:     return f"{n/1_000:.0f}K€"
    return f"{n:.0f}€"

# ── EJEMPLOS POR SECTOR ───────────────────────────────────────────
EXAMPLES = {
    'manufactura': [('Materia prima principal',500000),('Componentes mecánicos',250000),('Maquinaria CNC',300000),('Mantenimiento MRO',120000),('Embalaje',80000),('Logística',150000),('Suministros oficina',20000)],
    'retail':      [('Producto estrella A',400000),('Producto estrella B',300000),('Packaging premium',100000),('Sistemas POS',80000),('Merchandising',50000),('Suministros tienda',25000)],
    'salud':       [('Medicamentos críticos',600000),('Equipos médicos',400000),('Reactivos diagnóstico',200000),('Desechables médicos',150000),('Servicios limpieza',80000),('Material administrativo',15000)],
    'it':          [('Licencias software crítico',500000),('Infraestructura cloud',400000),('Hardware especializado',300000),('Ciberseguridad',200000),('Soporte técnico',150000),('Material oficina',30000)],
    'construccion':[('Acero estructural',800000),('Cemento y hormigón',600000),('Maquinaria pesada',500000),('Servicios especializados',300000),('Materiales acabado',200000),('EPIs seguridad',80000)],
    'servicios':   [('Talento especializado',700000),('Software gestión',200000),('Formación',100000),('Marketing digital',150000),('Suministros oficina',30000)],
    'alimentacion':[('Materias primas críticas',700000),('Envases alimentarios',200000),('Maquinaria proceso',400000),('Aditivos conservantes',150000),('Logística refrigerada',180000),('Material limpieza',40000)],
    'energia':     [('Turbinas / Generadores',1000000),('Cableado especializado',500000),('Sistemas SCADA',400000),('Mantenimiento predictivo',300000),('EPIs seguridad',100000),('Suministros generales',40000)],
}

# ── RECOMENDACIONES ───────────────────────────────────────────────
RECS = {
    'es': {
        'strategic':   {'color':'#1d4ed8','bg':'#eff6ff','border':'#bfdbfe','icon':'⭐','title':'Estratégico',
            'recs':[('Desarrollar alianzas estratégicas a largo plazo con proveedores clave','URGENTE','#fecaca','#b91c1c'),
                    ('Implementar planes de continuidad de suministro (BCP)','URGENTE','#fecaca','#b91c1c'),
                    ('Evaluar integración vertical o co-inversión','CORTO PLAZO','#fef08a','#92400e'),
                    ('Negociar contratos plurianuales con revisión de precios','MEDIO PLAZO','#bbf7d0','#065f46')]},
        'leverage':    {'color':'#065f46','bg':'#f0fdf4','border':'#bbf7d0','icon':'💪','title':'Apalancamiento',
            'recs':[('Consolidar volúmenes para obtener mejores precios','CORTO PLAZO','#fef08a','#92400e'),
                    ('Desarrollar base de proveedores alternativa','CORTO PLAZO','#fef08a','#92400e'),
                    ('Implementar subastas inversas y RFQ competitivos','MEDIO PLAZO','#bbf7d0','#065f46'),
                    ('Aprovechar poder de negociación contractual','CORTO PLAZO','#fef08a','#92400e')]},
        'bottleneck':  {'color':'#92400e','bg':'#fffbeb','border':'#fde68a','icon':'⚠️','title':'Cuello de Botella',
            'recs':[('Crear stock de seguridad para mitigar interrupciones','URGENTE','#fecaca','#b91c1c'),
                    ('Buscar y homologar proveedores alternativos urgentemente','URGENTE','#fecaca','#b91c1c'),
                    ('Establecer acuerdos de suministro garantizado','CORTO PLAZO','#fef08a','#92400e'),
                    ('Implementar sistema de alerta temprana','CORTO PLAZO','#fef08a','#92400e')]},
        'noncritical': {'color':'#374151','bg':'#f9fafb','border':'#e5e7eb','icon':'📦','title':'No Crítico',
            'recs':[('Automatizar compras con catálogos y e-procurement','MEDIO PLAZO','#bbf7d0','#065f46'),
                    ('Consolidar proveedores para reducir complejidad','MEDIO PLAZO','#bbf7d0','#065f46'),
                    ('Simplificar procesos y reducir carga administrativa','MEDIO PLAZO','#bbf7d0','#065f46'),
                    ('Revisar frecuencias de pedido y tamaños de lote','MEDIO PLAZO','#bbf7d0','#065f46')]},
    },
    'en': {
        'strategic':   {'color':'#1d4ed8','bg':'#eff6ff','border':'#bfdbfe','icon':'⭐','title':'Strategic',
            'recs':[('Develop long-term strategic alliances with key suppliers','URGENT','#fecaca','#b91c1c'),
                    ('Implement supply continuity plans (BCP)','URGENT','#fecaca','#b91c1c'),
                    ('Evaluate vertical integration or co-investment','SHORT-TERM','#fef08a','#92400e'),
                    ('Negotiate multi-year contracts with price review clauses','MID-TERM','#bbf7d0','#065f46')]},
        'leverage':    {'color':'#065f46','bg':'#f0fdf4','border':'#bbf7d0','icon':'💪','title':'Leverage',
            'recs':[('Consolidate volumes for better pricing','SHORT-TERM','#fef08a','#92400e'),
                    ('Develop alternative supplier base','SHORT-TERM','#fef08a','#92400e'),
                    ('Implement reverse auctions and competitive RFQs','MID-TERM','#bbf7d0','#065f46'),
                    ('Leverage negotiating power for better contract terms','SHORT-TERM','#fef08a','#92400e')]},
        'bottleneck':  {'color':'#92400e','bg':'#fffbeb','border':'#fde68a','icon':'⚠️','title':'Bottleneck',
            'recs':[('Create safety stock to mitigate supply disruption','URGENT','#fecaca','#b91c1c'),
                    ('Urgently identify and qualify alternative suppliers','URGENT','#fecaca','#b91c1c'),
                    ('Establish guaranteed supply agreements','SHORT-TERM','#fef08a','#92400e'),
                    ('Implement early warning and monitoring system','SHORT-TERM','#fef08a','#92400e')]},
        'noncritical': {'color':'#374151','bg':'#f9fafb','border':'#e5e7eb','icon':'📦','title':'Non-Critical',
            'recs':[('Automate purchasing with catalogs and e-procurement','MID-TERM','#bbf7d0','#065f46'),
                    ('Consolidate suppliers to reduce complexity','MID-TERM','#bbf7d0','#065f46'),
                    ('Simplify processes and reduce admin burden','MID-TERM','#bbf7d0','#065f46'),
                    ('Review order frequencies and batch sizes','MID-TERM','#bbf7d0','#065f46')]},
    }
}

# ── MAIN APP ──────────────────────────────────────────────────────
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("## ⬡ Matriz de Kraljic")
        st.markdown("---")
        lang = st.radio("🌐 Idioma / Language", ['ES', 'EN'], horizontal=True)
        L = lang.lower()
        t = LANG[L]
        st.markdown("---")
        st.markdown("**" + t['client'] + "**")
        client_name = st.text_input(t['client'], label_visibility="collapsed", placeholder="Ej: Empresa ABC")
        sector_opts = list(SECTORS[L].values())
        sector_keys = list(SECTORS[L].keys())
        sector_label = st.selectbox(t['sector'], sector_opts)
        sector = sector_keys[sector_opts.index(sector_label)]
        analyst = st.text_input(t['analyst'], value="Elymar Estévez")
        analysis_date = st.date_input(t['date'], value=date.today())
        st.markdown("---")
        mode = st.radio(t['mode'], [t['by_cat'], t['by_sup']], horizontal=True)
        st.markdown("---")
        st.markdown(f"<div style='font-size:0.72rem;color:#4a6fa5;text-align:center'>Creado por<br><strong>Elymar Estévez</strong></div>", unsafe_allow_html=True)

    # Header
    st.markdown(f"""
    <div class="header-box">
        <div>
            <div style="font-size:1.4rem;font-weight:800;color:white">⬡ {t['title']}</div>
            <div style="font-size:0.85rem;color:rgba(255,255,255,0.8);margin-top:4px">{t['subtitle']}</div>
        </div>
        <div style="text-align:right;font-size:0.75rem;color:rgba(255,255,255,0.75)">
            {t['analyst_lbl']}: <strong style="color:white">{analyst}</strong><br>
            {client_name} · {analysis_date.strftime('%d/%m/%Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TAB DATA ENTRY ────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📊 " + t['add_data'], "🔲 " + t['matrix_title']])

    with tab1:
        st.info(t['autoscore'])

        # Plantilla descargable
        ex = EXAMPLES.get(sector, [('Categoría 1', 100000), ('Categoría 2', 50000)])
        df_tpl = pd.DataFrame(ex, columns=[t['name_col'], t['spend_col']])
        excel_bytes = df_tpl.to_csv(index=False).encode('utf-8')
        st.download_button(t['download_tpl'], excel_bytes, file_name=f"Kraljic_{sector}.csv", mime='text/csv')

        # Carga de Excel/CSV
        uploaded = st.file_uploader(t['upload'], type=['xlsx','xls','csv'], label_visibility="collapsed")
        if uploaded:
            try:
                if uploaded.name.endswith('.csv'):
                    df_up = pd.read_csv(uploaded)
                else:
                    df_up = pd.read_excel(uploaded)
                df_up.columns = [t['name_col'], t['spend_col']][:len(df_up.columns)]
                st.session_state['uploaded_df'] = df_up
                st.success(f"✅ {len(df_up)} filas cargadas correctamente.")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

        # Editor de datos
        if 'uploaded_df' in st.session_state:
            df_input = st.session_state['uploaded_df']
        else:
            df_input = pd.DataFrame({t['name_col']: [''] * 6, t['spend_col']: [0] * 6})

        st.markdown("#### ✏️ " + t['add_data'])
        edited = st.data_editor(
            df_input,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                t['name_col']: st.column_config.TextColumn(t['name_col'], width="large"),
                t['spend_col']: st.column_config.NumberColumn(t['spend_col'], min_value=0, format="%.0f €"),
            }
        )

        if st.button(t['generate'], type="primary", use_container_width=True):
            if not sector:
                st.error("⚠️ " + ("Selecciona el sector primero." if L=='es' else "Please select a sector first."))
            else:
                rows = edited.dropna(subset=[t['name_col']])
                rows = rows[rows[t['name_col']].astype(str).str.strip() != '']
                if len(rows) == 0:
                    st.error("⚠️ " + ("Añade al menos un elemento." if L=='es' else "Add at least one item."))
                else:
                    total = rows[t['spend_col']].sum()
                    results = []
                    for _, row in rows.iterrows():
                        name = str(row[t['name_col']])
                        spend = float(row[t['spend_col']] or 0)
                        imp, risk, ies, ien = score_item(name, spend, total, sector)
                        q = get_quadrant(imp, risk)
                        inferred = ies if L == 'es' else ien
                        results.append({'name': name, 'spend': spend, 'impact': imp, 'risk': risk,
                                        'inferredEs': ies, 'inferredEn': ien, 'inferred': inferred, 'quadrant': q})
                    st.session_state['results'] = results
                    st.session_state['meta'] = {'client': client_name, 'sector': sector, 'analyst': analyst,
                                                 'date': analysis_date.strftime('%d/%m/%Y'), 'lang': L}
                    st.success("✅ " + ("Matriz generada. Ve a la pestaña 🔲 Matriz." if L=='es' else "Matrix generated. Go to 🔲 Matrix tab."))

    with tab2:
        if 'results' not in st.session_state:
            st.info("📊 " + ("Genera la matriz primero en la pestaña de Datos." if lang=='ES' else "Generate the matrix first in the Data tab."))
            return

        results = st.session_state['results']
        meta = st.session_state['meta']
        L2 = meta['lang']
        t2 = LANG[L2]
        df = pd.DataFrame(results)

        Q_LABELS = {
            'strategic':   t2['strategic'],
            'leverage':    t2['leverage'],
            'bottleneck':  t2['bottleneck'],
            'noncritical': t2['noncritical'],
        }
        Q_COLORS = {'strategic':'#2563eb','leverage':'#059669','bottleneck':'#d97706','noncritical':'#64748b'}

        # KPIs
        total = df['spend'].sum()
        c1, c2, c3, c4 = st.columns(4)
        for col, q, label, color in [
            (c1, None, t2['total_spend'], '#1e3a5f'),
            (c2, 'strategic', t2['strategic'], '#1d4ed8'),
            (c3, 'leverage',  t2['leverage'],  '#065f46'),
            (c4, 'bottleneck',t2['bottleneck'],'#92400e'),
        ]:
            subset = df[df['quadrant']==q] if q else df
            val = subset['spend'].sum() if q else total
            cnt = len(subset)
            with col:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="color:{color}">{fmt_spend(val)}</div>
                    <div class="metric-sub">{cnt} {t2['items']}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── MATRIZ VISUAL ─────────────────────────────────────────
        st.markdown(f"### {t2['matrix_title']} – <span style='color:#d97706'>{meta['client']}</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.78rem;color:#4a6fa5;margin-bottom:12px'>{t2['sector_lbl']}: <strong>{SECTORS[L2].get(meta['sector'],meta['sector'])}</strong> · {t2['analyst_lbl']}: {meta['analyst']} · {meta['date']}</div>", unsafe_allow_html=True)

        q_order = [('bottleneck','#92400e','#fef3c7'), ('strategic','#1d4ed8','#dbeafe'),
                   ('noncritical','#374151','#f1f5f9'), ('leverage','#065f46','#d1fae5')]
        row1 = st.columns(2)
        row2 = st.columns(2)
        cols_map = {'bottleneck': row1[0], 'strategic': row1[1], 'noncritical': row2[0], 'leverage': row2[1]}
        icons = {'strategic':'⭐','leverage':'💪','bottleneck':'⚠️','noncritical':'📦'}
        subtitles = {
            'strategic':   f"{t2['high_risk']} · {t2['high_impact']}",
            'leverage':    f"{t2['low_risk']} · {t2['high_impact']}",
            'bottleneck':  f"{t2['high_risk']} · {t2['low_impact']}",
            'noncritical': f"{t2['low_risk']} · {t2['low_impact']}",
        }
        cell_bg = {'strategic':'#1e40af','leverage':'#065f46','bottleneck':'#92400e','noncritical':'#334155'}

        for q, color, bg in q_order:
            items = df[df['quadrant']==q].sort_values('spend', ascending=False)
            with cols_map[q]:
                items_html = ''.join([f"<div style='background:rgba(255,255,255,0.18);border-radius:5px;padding:4px 8px;margin-bottom:4px;font-size:0.72rem;color:white;display:flex;justify-content:space-between'><span>{r['name']}</span><span style='color:rgba(255,255,255,0.7)'>{fmt_spend(r['spend'])}</span></div>" for _, r in items.iterrows()]) if len(items) > 0 else f"<div style='font-size:0.72rem;color:rgba(255,255,255,0.4);font-style:italic'>{t2['no_items']}</div>"
                st.markdown(f"""
                <div style="background:{cell_bg[q]};border-radius:10px;padding:14px;min-height:160px;border:1px solid rgba(255,255,255,0.2)">
                    <div style="font-size:1.4rem;margin-bottom:4px">{icons[q]}</div>
                    <div style="font-size:0.95rem;font-weight:800;color:white">{Q_LABELS[q]}</div>
                    <div style="font-size:0.68rem;color:rgba(255,255,255,0.65);margin-bottom:8px">{subtitles[q]}</div>
                    {items_html}
                </div>""", unsafe_allow_html=True)

        st.markdown("<div style='text-align:center;color:#4a6fa5;font-size:0.72rem;margin-top:8px'>◄── {low} ─────── {xlabel} ────── {high} ──►</div>".format(
            low=t2['low_impact'], xlabel=t2['x_axis'], high=t2['high_impact']), unsafe_allow_html=True)

        # ── SCATTER ───────────────────────────────────────────────
        st.markdown(f"### {t2['scatter_title']}")

        # Agrupar por categoría inferida
        cat_map = {}
        for r in results:
            k = r['inferredEs']
            if k not in cat_map:
                cat_map[k] = {'name': r['inferred'], 'spend': 0, 'impact': 0, 'risk': 0, 'n': 0, 'quadrant': r['quadrant']}
            cat_map[k]['spend']  += r['spend']
            cat_map[k]['impact'] += r['impact']
            cat_map[k]['risk']   += r['risk']
            cat_map[k]['n']      += 1
        plot_rows = []
        for v in cat_map.values():
            imp = round(v['impact'] / v['n'])
            risk = round(v['risk'] / v['n'])
            q = get_quadrant(imp, risk)
            plot_rows.append({'name': v['name'], 'spend': v['spend'], 'impact': imp, 'risk': risk, 'quadrant': q})

        fig = go.Figure()

        # Cuadrantes de fondo
        max_spend = max(r['spend'] for r in plot_rows) if plot_rows else 1
        mid_spend = max_spend / 2
        fig.add_shape(type="rect", x0=0, x1=mid_spend, y0=5.5, y1=10.5, fillcolor="rgba(217,119,6,0.07)", line_width=0, layer="below")
        fig.add_shape(type="rect", x0=mid_spend, x1=max_spend*1.05, y0=5.5, y1=10.5, fillcolor="rgba(37,99,235,0.08)", line_width=0, layer="below")
        fig.add_shape(type="rect", x0=0, x1=mid_spend, y0=0.5, y1=5.5, fillcolor="rgba(100,116,139,0.05)", line_width=0, layer="below")
        fig.add_shape(type="rect", x0=mid_spend, x1=max_spend*1.05, y0=0.5, y1=5.5, fillcolor="rgba(5,150,105,0.07)", line_width=0, layer="below")

        # Líneas divisorias
        fig.add_shape(type="line", x0=mid_spend, x1=mid_spend, y0=0.5, y1=10.5, line=dict(color="rgba(37,99,235,0.25)", width=1.5, dash="dash"))
        fig.add_shape(type="line", x0=0, x1=max_spend*1.05, y0=5.5, y1=5.5, line=dict(color="rgba(37,99,235,0.25)", width=1.5, dash="dash"))

        # Etiquetas cuadrantes
        for lbl, x, y in [
            (t2['bottleneck'].upper(), mid_spend*0.5, 8),
            (t2['strategic'].upper(),  mid_spend*1.5, 8),
            (t2['noncritical'].upper(),mid_spend*0.5, 3),
            (t2['leverage'].upper(),   mid_spend*1.5, 3),
        ]:
            fig.add_annotation(x=x, y=y, text=lbl, showarrow=False,
                font=dict(size=11, color='rgba(30,58,95,0.3)', family='Arial Black'), xanchor='center')

        # Puntos
        for row in plot_rows:
            q = row['quadrant']
            color = Q_COLORS[q]
            size = 20 + (row['spend'] / max_spend) * 40
            fig.add_trace(go.Scatter(
                x=[row['spend']], y=[row['risk']],
                mode='markers+text',
                name=Q_LABELS[q],
                marker=dict(size=size, color=color, opacity=0.85, line=dict(color=color, width=2)),
                text=[row['name']],
                textposition='top center',
                textfont=dict(size=11, color='#1e3a5f', family='Arial'),
                hovertemplate=f"<b>{row['name']}</b><br>{t2['risk']}: {row['risk']}/10<br>Gasto: {fmt_spend(row['spend'])}<br>{Q_LABELS[q]}<extra></extra>",
                showlegend=False,
            ))

        fig.update_layout(
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title=t2['x_axis'], showgrid=True, gridcolor='rgba(0,0,0,0.05)',
                       zeroline=False, tickfont=dict(color='#4a6fa5', size=10)),
            yaxis=dict(title=t2['y_axis'], range=[0.5, 10.5], showgrid=True,
                       gridcolor='rgba(0,0,0,0.05)', zeroline=False,
                       tickfont=dict(color='#4a6fa5', size=10), tickvals=list(range(1,11))),
            margin=dict(l=60, r=30, t=30, b=60),
            font=dict(family='Arial', color='#1e3a5f'),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── SCORE TABLE ───────────────────────────────────────────
        st.markdown(f"### {t2['score_table']}")
        df_show = df[['name','inferred','spend','impact','risk','quadrant']].copy()
        df_show['spend'] = df_show['spend'].apply(fmt_spend)
        df_show['impact'] = df_show['impact'].apply(lambda x: f"{x}/10")
        df_show['risk']   = df_show['risk'].apply(lambda x: f"{x}/10")
        df_show['quadrant'] = df_show['quadrant'].map(Q_LABELS)
        df_show.columns = [t2['name_col'], t2['inferred'], t2['spend_col'], t2['impact'], t2['risk'], t2['quadrant']]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

        # ── RECOMMENDATIONS ───────────────────────────────────────
        st.markdown(f"### {t2['recs_title']}")
        recs_data = RECS[L2]
        col_a, col_b = st.columns(2)
        for i, (q, col) in enumerate([('strategic', col_a), ('bottleneck', col_b), ('leverage', col_a), ('noncritical', col_b)]):
            r = recs_data[q]
            items_in_q = df[df['quadrant']==q]['name'].tolist()
            tags_html = ''.join([f"<span style='background:{r[\"color\"]}18;color:{r[\"color\"]};border-radius:4px;padding:2px 8px;font-size:0.68rem;font-weight:600;margin:2px;display:inline-block'>{n}</span>" for n in items_in_q])
            if not tags_html:
                tags_html = f"<span style='font-size:0.73rem;color:#4a6fa5;font-style:italic'>{t2['no_items']}</span>"
            recs_html = ''.join([f"<div style='padding:5px 0 5px 14px;border-bottom:1px solid #e5e7eb;font-size:0.78rem;color:#374151;position:relative'><span style='position:absolute;left:0;color:{r[\"color\"]}'>→</span>{rec} <span style='background:{bg};color:{tc};font-size:0.62rem;font-weight:700;padding:1px 6px;border-radius:8px;margin-left:4px'>{badge}</span></div>" for rec, badge, bg, tc in r['recs']])
            with col:
                st.markdown(f"""<div style="background:{r['bg']};border:1px solid {r['border']};border-radius:10px;padding:16px;margin-bottom:14px">
                    <div style="font-size:0.9rem;font-weight:700;color:{r['color']};margin-bottom:8px">{r['icon']} {r['title']}</div>
                    <div style="margin-bottom:10px">{tags_html}</div>
                    {recs_html}
                </div>""", unsafe_allow_html=True)

        # ── EXPORT CSV ────────────────────────────────────────────
        st.markdown("---")
        export_df = df[['name','inferred','spend','impact','risk','quadrant']].copy()
        export_df['quadrant'] = export_df['quadrant'].map(Q_LABELS)
        csv = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇ " + ("Exportar resultados CSV" if L2=='es' else "Export results CSV"),
            data=csv,
            file_name=f"Kraljic_{meta['client']}_{meta['date']}.csv",
            mime='text/csv',
            use_container_width=True
        )

    # Footer
    st.markdown(f"<div class='footer'>{LANG[lang.lower()]['footer']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
