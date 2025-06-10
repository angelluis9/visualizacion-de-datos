import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('/workspaces/visualizacion-de-datos/world all university rank and rank score.csv')

# Preprocesamiento
df['rank'] = pd.to_numeric(df['rank'], errors='coerce')

indicators = [
    'Overall scores', 'Research Quality Score', 'Industry Score',
    'International Outlook', 'Research Environment Score', 'Teaching Score'
]

# Convertir columnas a numéricas
for col in indicators:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Agrupar por país (todas las universidades)
grouped = df.groupby('location')[indicators].mean().reset_index()

# Visualización con Plotly
fig = go.Figure()
for var in indicators:
    fig.add_trace(go.Choropleth(
        locations=grouped['location'],
        z=grouped[var],
        locationmode='country names',
        colorscale='Reds',
        colorbar_title=var,
        visible=(var == indicators[0]),
        name=var
    ))

# Botones de selección de indicador
buttons = []
for i, var in enumerate(indicators):
    visibility = [False]*len(indicators)
    visibility[i] = True
    buttons.append(dict(
        label=var,
        method='update',
        args=[{'visible': visibility},
              {'title': f'Media por país: {var}',
               'coloraxis.colorbar.title': var}]
    ))

fig.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=0.1, y=1.15,
        xanchor='left', yanchor='top'
    )],
    title=f'Media por país: {indicators[0]}',
    geo=dict(showframe=False, showcoastlines=True)
)

fig.show()
