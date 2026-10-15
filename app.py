"""Interactive companion dashboard for browsing the same data without Power BI."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Tableau de bord commercial', page_icon='📊', layout='wide')
st.title('Tableau de bord commercial')
st.caption('Portfolio de data analytics • Données entièrement fictives • CA des commandes réalisées, remises déduites')
CSV = Path(__file__).parent / 'data/processed/ventes_nettoyees.csv'

@st.cache_data
def load():
    df = pd.read_csv(CSV, parse_dates=['order_date'])
    return df

if not CSV.exists():
    st.error('Données absentes. Exécuter `python scripts/generate_data.py` puis `python scripts/prepare_data.py`.')
    st.stop()
df = load()
with st.sidebar:
    st.header('Filtres')
    years = st.multiselect('Année', sorted(df.year.unique().tolist()), default=sorted(df.year.unique().tolist()))
    segments = st.multiselect('Segment', sorted(df.segment.unique()), default=sorted(df.segment.unique()))
    channels = st.multiselect('Canal', sorted(df.channel.unique()), default=sorted(df.channel.unique()))
    regions = st.multiselect('Région', sorted(df.region.unique()), default=sorted(df.region.unique()))
    categories = st.multiselect('Catégorie', sorted(df.category.unique()), default=sorted(df.category.unique()))
view = df[df.year.isin(years) & df.segment.isin(segments) & df.channel.isin(channels) & df.region.isin(regions) & df.category.isin(categories)].copy()
completed = view[view.status == 'Completed']
revenue = completed.revenue_eur.sum()
orders = completed.order_id.nunique()
customers = completed.customer_id.nunique()
euro = lambda v: f'{v:,.2f} €'.replace(',', ' ').replace('.', ',')
a,b,c,d = st.columns(4)
a.metric('Chiffre d’affaires', euro(revenue))
b.metric('Commandes réalisées', f'{orders:,}'.replace(',', ' '))
c.metric('Panier moyen', euro(revenue / orders if orders else 0))
d.metric('Clients actifs', f'{customers:,}'.replace(',', ' '))
if view.empty:
    st.info('Aucune donnée pour ces filtres.')
    st.stop()
left,right = st.columns(2)
with left:
    monthly = completed.groupby('month', as_index=False).revenue_eur.sum().sort_values('month')
    st.plotly_chart(px.line(monthly, x='month', y='revenue_eur', markers=True, title='Évolution du CA mensuel', labels={'month':'Mois', 'revenue_eur':'CA (€)'}), use_container_width=True)
    top = completed.groupby('product', as_index=False).revenue_eur.sum().sort_values('revenue_eur', ascending=False)
    st.plotly_chart(px.bar(top, x='revenue_eur', y='product', orientation='h', title='CA par produit', labels={'revenue_eur':'CA (€)', 'product':'Produit'}), use_container_width=True)
with right:
    geo = completed.groupby('region', as_index=False).revenue_eur.sum().sort_values('revenue_eur', ascending=False)
    st.plotly_chart(px.bar(geo, x='region', y='revenue_eur', title='CA par région', labels={'region':'Région', 'revenue_eur':'CA (€)'}), use_container_width=True)
    channel = completed.groupby('channel', as_index=False).revenue_eur.sum()
    st.plotly_chart(px.pie(channel, values='revenue_eur', names='channel', title='Contribution par canal', hole=.55), use_container_width=True)
st.subheader('Données filtrées')
st.dataframe(view.sort_values('order_date', ascending=False), use_container_width=True, hide_index=True)
st.download_button('Exporter les données filtrées (CSV)', view.to_csv(index=False).encode('utf-8-sig'), 'ventes_filtrees.csv', 'text/csv')
