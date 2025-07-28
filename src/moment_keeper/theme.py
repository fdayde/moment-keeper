"""Thème et styles pour MomentKeeper."""

# 🎨 Palette couleurs T-Rex Pastel
COLORS = {
    "primary": "#E8F4F8",  # Bleu pastel doux (ciel préhistorique)
    "secondary": "#F9F2E7",  # Beige/crème chaleureux (sable ancien)
    "accent": "#D4C5B9",  # Taupe rosé (terre préhistorique)
    "success": "#C8E6C9",  # Vert pastel (T-Rex amical)
    "warning": "#FFE0B2",  # Orange pastel
    "error": "#FFCDD2",  # Rose pastel
    "text_dark": "#2C3E50",  # Bleu marine doux
    "text_light": "#7F8C8D",  # Gris élégant
    # Couleurs additionnelles pour graphiques
    "chart_purple": "#E1D5E7",  # Violet pastel
    "chart_mint": "#D5F4E6",  # Menthe pastel
    "chart_peach": "#FFE5D9",  # Pêche pastel
    "chart_lavender": "#E6E6FA",  # Lavande pastel
    "chart_coral": "#FFB3BA",  # Corail pastel
    "dark_red_pastel": "#F8BBD9",  # Rouge pastel plus foncé
}

# Couleurs pour les graphiques Plotly
CHART_COLORS = [
    COLORS["success"],
    COLORS["chart_mint"],
    COLORS["primary"],
    COLORS["chart_peach"],
    COLORS["warning"],
    COLORS["chart_purple"],
    COLORS["chart_lavender"],
    COLORS["chart_coral"],
]

# Gradient pour le graphique en barres
BAR_CHART_GRADIENT = [
    [0, COLORS["success"]],
    [0.3, COLORS["chart_mint"]],
    [0.6, COLORS["primary"]],
    [1, COLORS["chart_purple"]],
]

# Colorscale pour la heatmap
HEATMAP_COLORSCALE = [
    [0.0, "#F0F8FF"],  # Blanc cassé pour zéro
    [0.2, COLORS["chart_mint"]],  # Menthe pour faible activité
    [0.4, COLORS["success"]],  # Vert pastel pour activité modérée
    [0.6, COLORS["chart_peach"]],  # Pêche pour bonne activité
    [0.8, COLORS["warning"]],  # Orange pour forte activité
    [1.0, COLORS["chart_coral"]],  # Corail pour activité maximale
]


def get_css_styles() -> str:
    """Retourne les styles CSS personnalisés pour l'application."""
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Variables CSS pour cohérence */
:root {{
    --primary: {COLORS['primary']};
    --secondary: {COLORS['secondary']};
    --accent: {COLORS['accent']};
    --success: {COLORS['success']};
    --warning: {COLORS['warning']};
    --error: {COLORS['error']};
    --text-dark: {COLORS['text_dark']};
    --text-light: {COLORS['text_light']};
}}

/* Styles globaux */
.main {{
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    min-height: 100vh;
}}

/* Header principal T-Rex */
.main-header {{
    font-family: 'Poppins', sans-serif;
    color: {COLORS['text_dark']};
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}}

.main-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: {COLORS['text_dark']};
}}

.main-header p {{
    font-size: 1.1rem;
    color: {COLORS['text_light']};
    margin: 0;
}}

/* Cards métriques */
.metric-card {{
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-left: 4px solid {COLORS['accent']};
    margin: 0.5rem 0;
    transition: transform 0.2s ease;
}}

.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

/* Bulles d'insights */
.insight-bubble {{
    background: {COLORS['secondary']};
    padding: 1rem 1.5rem;
    border-radius: 20px;
    margin: 0.5rem 0;
    border: 1px solid {COLORS['primary']};
    font-family: 'Poppins', sans-serif;
    position: relative;
}}

.insight-bubble::before {{
    content: '';
    position: absolute;
    left: 15px;
    top: -5px;
    width: 10px;
    height: 10px;
    background: {COLORS['secondary']};
    border: 1px solid {COLORS['primary']};
    border-bottom: none;
    border-right: none;
    transform: rotate(45deg);
}}

/* Messages T-Rex */
.trex-message {{
    background: linear-gradient(135deg, {COLORS['success']} 0%, {COLORS['primary']} 100%);
    padding: 1rem 1.5rem;
    border-radius: 15px;
    border-left: 4px solid {COLORS['accent']};
    margin: 1rem 0;
    font-weight: 500;
}}

.trex-success {{
    background: linear-gradient(135deg, {COLORS['success']} 0%, {COLORS['primary']} 100%);
    border-left-color: #4CAF50;
}}

.trex-warning {{
    background: linear-gradient(135deg, {COLORS['dark_red_pastel']} 0%, {COLORS['primary']} 100%);
    border-left-color: #E91E63;
}}

.trex-error {{
    background: linear-gradient(135deg, {COLORS['error']} 0%, {COLORS['primary']} 100%);
    border-left-color: #F44336;
}}

/* Sidebar style */
.css-1d391kg {{
    background: linear-gradient(180deg, {COLORS['secondary']} 0%, {COLORS['primary']} 100%);
}}

/* Onglets personnalisés */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 0.5rem;
}}

.stTabs [data-baseweb="tab"] {{
    height: 50px;
    background: rgba(255,255,255,0.7);
    border-radius: 10px;
    color: {COLORS['text_dark']};
    font-weight: 500;
    border: none;
    transition: all 0.3s ease;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['primary']} 100%);
    color: {COLORS['text_dark']};
    font-weight: 600;
}}

/* Footer T-Rex */
.trex-footer {{
    text-align: center;
    padding: 2rem 0;
    background: {COLORS['secondary']};
    border-radius: 15px;
    margin-top: 2rem;
    color: {COLORS['text_light']};
    font-size: 0.9rem;
}}

.trex-footer a {{
    color: {COLORS['accent']};
    text-decoration: none;
    font-weight: 600;
}}

.trex-footer a:hover {{
    color: {COLORS['primary']};
    text-decoration: underline;
}}

/* Buttons personnalisés */
.stButton > button {{
    background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['primary']} 100%);
    color: {COLORS['text_dark']};
    border: none;
    border-radius: 10px;
    font-weight: 500;
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}}

/* Métriques Streamlit personnalisées */
[data-testid="metric-container"] {{
    background: white;
    border: 1px solid {COLORS['primary']};
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}}

/* Forcer le texte sombre dans les zones pastels */
.insight-bubble,
.insight-bubble p,
.insight-bubble span,
.insight-bubble div {{
    color: {COLORS['text_dark']} !important;
}}

.metric-card,
.metric-card p,
.metric-card span,
.metric-card div,
.metric-card h1,
.metric-card h2,
.metric-card h3 {{
    color: {COLORS['text_dark']} !important;
}}

.main-header,
.main-header h1,
.main-header p {{
    color: {COLORS['text_dark']} !important;
}}

.trex-message,
.trex-message p,
.trex-message span,
.trex-message div {{
    color: {COLORS['text_dark']} !important;
}}

/* Cibler les éléments Streamlit dans les zones pastels */
.insight-bubble .stMarkdown,
.insight-bubble .stText,
.metric-card .stMarkdown,
.metric-card .stText,
.trex-message .stMarkdown,
.trex-message .stText {{
    color: {COLORS['text_dark']} !important;
}}

/* Zone de contenu principale plus claire */
.main .block-container {{
    background: rgba(255, 255, 255, 0.7);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 1rem;
}}

/* Forcer le texte sombre sur tous les contenus markdown dans les zones pastels */
.main .block-container .stMarkdown p,
.main .block-container .stMarkdown div,
.main .block-container .stMarkdown span,
.main .block-container .stText {{
    color: {COLORS['text_dark']} !important;
}}

/* Sélecteur de langue moderne */
.language-selector {{
    margin-bottom: 1rem;
}}

.language-selector .stButton > button {{
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.2s ease;
    border: 2px solid transparent;
}}

.language-selector .stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}}

/* Style pour le bouton actif */
.language-selector .stButton > button[data-testid="baseButton-primary"] {{
    background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['primary']} 100%);
    border: 2px solid {COLORS['accent']};
    color: {COLORS['text_dark']};
}}

/* Style pour le bouton inactif */
.language-selector .stButton > button[data-testid="baseButton-secondary"] {{
    background: rgba(255,255,255,0.7);
    border: 2px solid {COLORS['primary']};
    color: {COLORS['text_light']};
}}
</style>
"""
