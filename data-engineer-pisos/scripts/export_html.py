"""Export analysis charts to a single standalone HTML file for GitHub Pages."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import duckdb
import plotly.express as px
import plotly.graph_objects as go
import polars as pl

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pisos.duckdb"
OUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "index.html"


def query(sql):
    con = duckdb.connect(str(DB_PATH), read_only=True)
    df = con.execute(sql).pl()
    con.close()
    return df


DISTRITOS_MADRID = {
    "2807901": "Centro", "2807902": "Arganzuela", "2807903": "Retiro",
    "2807904": "Salamanca", "2807905": "Chamartin", "2807906": "Tetuan",
    "2807907": "Chamberi", "2807908": "Fuencarral-El Pardo", "2807909": "Moncloa-Aravaca",
    "2807910": "Latina", "2807911": "Carabanchel", "2807912": "Usera",
    "2807913": "Puente de Vallecas", "2807914": "Moratalaz", "2807915": "Ciudad Lineal",
    "2807916": "Hortaleza", "2807917": "Villaverde", "2807918": "Villa de Vallecas",
    "2807919": "Vicalvaro", "2807920": "San Blas-Canillejas", "2807921": "Barajas",
}

NAN_FILTER = "AND name IS NOT NULL AND name != ''"
NUM_FILTER = "IS NOT NULL AND NOT isnan"


def fig1_ccaa_evolution():
    top_ccaa = query(f"""
        SELECT name FROM rentals
        WHERE level = 'ccaa' AND year = 2024
            AND monthly_rent_median_collective {NUM_FILTER}(monthly_rent_median_collective)
            {NAN_FILTER}
        ORDER BY monthly_rent_median_collective DESC LIMIT 8
    """)["name"].to_list()

    df = query(f"""
        SELECT name, year, monthly_rent_median_collective as alquiler_mediano
        FROM rentals
        WHERE level = 'ccaa'
            AND alquiler_mediano {NUM_FILTER}(alquiler_mediano)
            {NAN_FILTER}
        ORDER BY name, year
    """)
    df = df.filter(pl.col("name").is_in(top_ccaa))

    return px.line(
        df.to_pandas(), x="year", y="alquiler_mediano", color="name",
        title="Alquiler mensual mediano por CCAA (vivienda colectiva)",
        labels={"year": "Año", "alquiler_mediano": "Alquiler mediano (EUR/mes)", "name": "CCAA"},
        markers=True,
    ).update_layout(hovermode="x unified", width=900, height=500)


def fig2_ccaa_ranking():
    df = query(f"""
        SELECT name, rent_m2_median_collective as eur_m2
        FROM rentals
        WHERE level = 'ccaa' AND year = 2024
            AND eur_m2 {NUM_FILTER}(eur_m2)
            {NAN_FILTER}
        ORDER BY eur_m2 DESC
    """)
    return px.bar(
        df.to_pandas(), x="eur_m2", y="name", orientation="h",
        title="Precio alquiler por m2 en 2024 (mediana, vivienda colectiva)",
        labels={"eur_m2": "EUR/m2/mes", "name": "CCAA"},
        text_auto=".1f", color="eur_m2", color_continuous_scale="RdYlGn_r",
    ).update_layout(yaxis=dict(autorange="reversed"), width=900, height=500, showlegend=False)


def fig3_madrid_band():
    df = query("""
        SELECT year,
            monthly_rent_median_collective as mediana,
            monthly_rent_p25_collective as p25,
            monthly_rent_p75_collective as p75
        FROM rentals
        WHERE level = 'municipio' AND name = 'Madrid'
        ORDER BY year
    """).to_pandas()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["year"], y=df["p75"], mode="lines", name="P75", line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=df["year"], y=df["p25"], mode="lines", name="Banda P25-P75", fill="tonexty", fillcolor="rgba(99,110,250,0.2)", line=dict(width=0)))
    fig.add_trace(go.Scatter(x=df["year"], y=df["mediana"], mode="lines+markers", name="Mediana", line=dict(color="rgb(99,110,250)", width=3)))
    fig.update_layout(title="Alquiler mensual en Madrid (municipio) 2011-2024", xaxis_title="Año", yaxis_title="EUR/mes", hovermode="x unified", width=900, height=450)
    return fig


def fig4_madrid_districts_change():
    codes_sql = ",".join(f"'{c}'" for c in DISTRITOS_MADRID)
    df = query(f"""
        SELECT code, year, monthly_rent_median_collective as alquiler
        FROM rentals
        WHERE level = 'distrito' AND code IN ({codes_sql}) AND year IN (2011, 2024)
            AND alquiler {NUM_FILTER}(alquiler)
        ORDER BY code, year
    """).to_pandas()
    df["distrito"] = df["code"].map(DISTRITOS_MADRID)
    pivot = df.pivot(index="distrito", columns="year", values="alquiler").reset_index()
    pivot.columns = ["distrito", "alquiler_2011", "alquiler_2024"]
    pivot["incremento_pct"] = (pivot["alquiler_2024"] - pivot["alquiler_2011"]) / pivot["alquiler_2011"] * 100
    pivot = pivot.dropna().sort_values("incremento_pct", ascending=True)

    return px.bar(
        pivot, x="incremento_pct", y="distrito", orientation="h",
        title="Incremento del alquiler 2011-2024 por distrito de Madrid (%)",
        labels={"incremento_pct": "Incremento (%)", "distrito": ""},
        text_auto=".0f", color="incremento_pct", color_continuous_scale="RdYlGn_r",
    ).update_layout(yaxis=dict(autorange="reversed"), width=900, height=600, showlegend=False)


def fig5_madrid_heatmap():
    codes_sql = ",".join(f"'{c}'" for c in DISTRITOS_MADRID)
    df = query(f"""
        SELECT code, year, rent_m2_median_collective as eur_m2
        FROM rentals
        WHERE level = 'distrito' AND code IN ({codes_sql})
            AND eur_m2 {NUM_FILTER}(eur_m2)
        ORDER BY code, year
    """).to_pandas()
    df["distrito"] = df["code"].map(DISTRITOS_MADRID)
    heatmap = df.pivot(index="distrito", columns="year", values="eur_m2")

    return px.imshow(
        heatmap, aspect="auto",
        title="EUR/m2 alquiler por distrito de Madrid (2011-2024)",
        labels=dict(x="Año", y="Distrito", color="EUR/m2"),
        color_continuous_scale="YlOrRd",
    ).update_layout(width=900, height=600)


def fig6_ipv():
    df = query("SELECT category, period, value FROM ipv WHERE value IS NOT NULL ORDER BY category, period").to_pandas()
    cat_labels = {"ipv_general": "General", "ipv_nueva": "Vivienda nueva", "ipv_segunda_mano": "Segunda mano"}
    df["tipo"] = df["category"].map(cat_labels)
    return px.line(
        df, x="period", y="value", color="tipo",
        title="Indice de Precios de Vivienda (IPV) — Nacional",
        labels={"period": "Periodo", "value": "Indice (base 2015=100)", "tipo": "Tipo"},
        markers=True,
    ).update_layout(hovermode="x unified", width=900, height=450, xaxis_tickangle=-45)


def fig7_top_municipios():
    df = query(f"""
        SELECT name, rent_m2_median_collective as eur_m2,
            monthly_rent_median_collective as alquiler,
            num_properties_collective as num_pisos
        FROM rentals
        WHERE level = 'municipio' AND year = 2024
            AND eur_m2 {NUM_FILTER}(eur_m2)
            AND alquiler {NUM_FILTER}(alquiler)
            AND num_pisos {NUM_FILTER}(num_pisos)
            AND num_pisos > 500
        ORDER BY eur_m2 DESC LIMIT 20
    """)
    return px.bar(
        df.to_pandas(), x="eur_m2", y="name", orientation="h",
        title="Top 20 municipios mas caros (EUR/m2, >500 viviendas en alquiler, 2024)",
        labels={"eur_m2": "EUR/m2/mes", "name": "Municipio"},
        text_auto=".1f", color="alquiler", color_continuous_scale="Viridis",
        hover_data=["alquiler", "num_pisos"],
    ).update_layout(yaxis=dict(autorange="reversed"), width=900, height=600, coloraxis_colorbar_title="Alquiler<br>(EUR/mes)")


def fig8_volume():
    top = query(f"""
        SELECT name FROM rentals
        WHERE level = 'ccaa' AND year = 2024
            AND monthly_rent_median_collective {NUM_FILTER}(monthly_rent_median_collective)
            {NAN_FILTER}
        ORDER BY monthly_rent_median_collective DESC LIMIT 8
    """)["name"].to_list()

    df = query(f"""
        SELECT name, year, num_properties_collective as viviendas
        FROM rentals
        WHERE level = 'ccaa'
            AND viviendas {NUM_FILTER}(viviendas) AND viviendas > 0
            {NAN_FILTER}
        ORDER BY name, year
    """)
    df = df.filter(pl.col("name").is_in(top))
    return px.area(
        df.to_pandas(), x="year", y="viviendas", color="name",
        title="Viviendas en alquiler (colectivas) por CCAA",
        labels={"year": "Año", "viviendas": "Num. viviendas", "name": "CCAA"},
    ).update_layout(hovermode="x unified", width=900, height=500)


def build_html():
    figures = [
        ("Evolucion del alquiler por CCAA", fig1_ccaa_evolution()),
        ("Ranking CCAA por EUR/m2 (2024)", fig2_ccaa_ranking()),
        ("Madrid: alquiler con banda P25-P75", fig3_madrid_band()),
        ("Distritos de Madrid: incremento 2011 vs 2024", fig4_madrid_districts_change()),
        ("Heatmap distritos de Madrid", fig5_madrid_heatmap()),
        ("Indice de Precios de Vivienda (IPV)", fig6_ipv()),
        ("Top 20 municipios mas caros", fig7_top_municipios()),
        ("Crecimiento del mercado de alquiler", fig8_volume()),
    ]

    charts_html = ""
    for title, fig in figures:
        chart = fig.to_html(full_html=False, include_plotlyjs=False)
        charts_html += f'<section><h2>{title}</h2>{chart}</section>\n'

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mercado de alquiler en España (2011-2024)</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 960px; margin: 0 auto; padding: 2rem; background: #fafafa; color: #333; }}
        h1 {{ border-bottom: 3px solid #333; padding-bottom: 0.5rem; }}
        h2 {{ color: #555; margin-top: 2.5rem; }}
        section {{ margin-bottom: 1rem; }}
        .meta {{ color: #888; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>Mercado de alquiler en España (2011-2024)</h1>
    <p class="meta">Datos: SERPAVI (Ministerio de Vivienda) + INE (Indice de Precios de Vivienda)<br>
    Generado con <a href="https://github.com/kroloxmcg/casitas/tree/main/data-engineer-pisos">pisos-etl</a></p>
    {charts_html}
</body>
</html>"""

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(html)
    print(f"Written to {OUT_PATH} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    build_html()
