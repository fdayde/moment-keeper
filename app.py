"""Application Streamlit pour MomentKeeper."""

import tkinter as tk
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog
from typing import Dict, List, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.moment_keeper.organizer import OrganisateurPhotos

# 🎨 Palette couleurs T-Rex Pastel
PRIMARY = "#E8F4F8"  # Bleu pastel doux (ciel préhistorique)
SECONDARY = "#F9F2E7"  # Beige/crème chaleureux (sable ancien)
ACCENT = "#D4C5B9"  # Taupe rosé (terre préhistorique)
SUCCESS = "#C8E6C9"  # Vert pastel (T-Rex amical)
WARNING = "#FFE0B2"  # Orange pastel
ERROR = "#FFCDD2"  # Rose pastel
TEXT_DARK = "#2C3E50"  # Bleu marine doux
TEXT_LIGHT = "#7F8C8D"  # Gris élégant

# 🎮 T-Rex Achievements
TREX_ACHIEVEMENTS = {
    "🦖 Baby T-Rex": "Première photo organisée",
    "🦖 T-Rex Adolescent": "100 photos organisées",
    "🦖 T-Rex Adulte": "1000 photos organisées",
    "🦖 T-Rex Légendaire": "365 jours consécutifs",
    "🦖 Roi des T-Rex": "5000 photos organisées",
    "🦖 T-Rex Flamboyant": "10000 photos organisées",
}

# 🎨 CSS Custom T-Rex Pastel
TREX_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Variables CSS pour cohérence */
:root {{
    --primary: {PRIMARY};
    --secondary: {SECONDARY};
    --accent: {ACCENT};
    --success: {SUCCESS};
    --warning: {WARNING};
    --error: {ERROR};
    --text-dark: {TEXT_DARK};
    --text-light: {TEXT_LIGHT};
}}

/* Styles globaux */
.main {{
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    min-height: 100vh;
}}

/* Header principal T-Rex */
.main-header {{
    font-family: 'Poppins', sans-serif;
    color: {TEXT_DARK};
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, {PRIMARY} 0%, {SECONDARY} 100%);
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}}

.main-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: {TEXT_DARK};
}}

.main-header p {{
    font-size: 1.1rem;
    color: {TEXT_LIGHT};
    margin: 0;
}}

/* Cards métriques */
.metric-card {{
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-left: 4px solid {ACCENT};
    margin: 0.5rem 0;
    transition: transform 0.2s ease;
}}

.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

/* Bulles d'insights */
.insight-bubble {{
    background: {SECONDARY};
    padding: 1rem 1.5rem;
    border-radius: 20px;
    margin: 0.5rem 0;
    border: 1px solid {PRIMARY};
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
    background: {SECONDARY};
    border: 1px solid {PRIMARY};
    border-bottom: none;
    border-right: none;
    transform: rotate(45deg);
}}

/* Messages T-Rex */
.trex-message {{
    background: linear-gradient(135deg, {SUCCESS} 0%, {PRIMARY} 100%);
    padding: 1rem 1.5rem;
    border-radius: 15px;
    border-left: 4px solid {ACCENT};
    margin: 1rem 0;
    font-weight: 500;
}}

.trex-success {{
    background: linear-gradient(135deg, {SUCCESS} 0%, {PRIMARY} 100%);
    border-left-color: #4CAF50;
}}

.trex-warning {{
    background: linear-gradient(135deg, {WARNING} 0%, {PRIMARY} 100%);
    border-left-color: #FF9800;
}}

.trex-error {{
    background: linear-gradient(135deg, {ERROR} 0%, {PRIMARY} 100%);
    border-left-color: #F44336;
}}

/* Sidebar style */
.css-1d391kg {{
    background: linear-gradient(180deg, {SECONDARY} 0%, {PRIMARY} 100%);
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
    color: {TEXT_DARK};
    font-weight: 500;
    border: none;
    transition: all 0.3s ease;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {ACCENT} 0%, {PRIMARY} 100%);
    color: {TEXT_DARK};
    font-weight: 600;
}}

/* Footer T-Rex */
.trex-footer {{
    text-align: center;
    padding: 2rem 0;
    background: {SECONDARY};
    border-radius: 15px;
    margin-top: 2rem;
    color: {TEXT_LIGHT};
    font-size: 0.9rem;
}}

/* Buttons personnalisés */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT} 0%, {PRIMARY} 100%);
    color: {TEXT_DARK};
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
    border: 1px solid {PRIMARY};
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}}

/* Forcer le texte sombre dans les zones pastels */
.insight-bubble,
.insight-bubble p,
.insight-bubble span,
.insight-bubble div {{
    color: {TEXT_DARK} !important;
}}

.metric-card,
.metric-card p,
.metric-card span,
.metric-card div,
.metric-card h1,
.metric-card h2,
.metric-card h3 {{
    color: {TEXT_DARK} !important;
}}

.main-header,
.main-header h1,
.main-header p {{
    color: {TEXT_DARK} !important;
}}

.trex-message,
.trex-message p,
.trex-message span,
.trex-message div {{
    color: {TEXT_DARK} !important;
}}

/* Cibler les éléments Streamlit dans les zones pastels */
.insight-bubble .stMarkdown,
.insight-bubble .stText,
.metric-card .stMarkdown,
.metric-card .stText,
.trex-message .stMarkdown,
.trex-message .stText {{
    color: {TEXT_DARK} !important;
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
    color: {TEXT_DARK} !important;
}}
</style>
"""


def selectionner_dossier():
    """Ouvre une fenêtre de sélection de dossier."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    dossier = filedialog.askdirectory(
        title="Sélectionnez le dossier contenant vos photos"
    )
    root.destroy()
    return dossier


def extract_photo_data(organiseur: OrganisateurPhotos) -> pd.DataFrame:
    """Extrait les données des photos."""
    photos_data = []
    extensions = {".jpg", ".jpeg", ".png"}

    # Parcourir tous les dossiers du projet (source + dossiers mensuels)
    for dossier in organiseur.dossier_racine.iterdir():
        if dossier.is_dir():
            for fichier in dossier.iterdir():
                if fichier.is_file() and fichier.suffix.lower() in extensions:
                    # Réutiliser la méthode existante pour extraire la date
                    date_photo = organiseur.extraire_date_nom_fichier(fichier.name)

                    if date_photo and date_photo >= organiseur.date_naissance:
                        # Réutiliser la méthode existante pour calculer l'âge
                        age_mois = organiseur.calculer_age_mois(date_photo)

                        photos_data.append(
                            {
                                "fichier": fichier.name,
                                "date": date_photo,
                                "age_mois": age_mois,
                                "dossier": dossier.name,
                                "jour_semaine": date_photo.strftime("%A"),
                                "semaine": date_photo.isocalendar()[1],
                                "annee": date_photo.year,
                            }
                        )

    return pd.DataFrame(photos_data)


def calculate_metrics(df: pd.DataFrame) -> Dict:
    """Calcule toutes les métriques pour l'onglet Analytics."""
    if df.empty:
        return {
            "total_photos": 0,
            "periode_couverte": 0,
            "moyenne_par_mois": 0,
            "derniere_photo": None,
            "jour_record": 0,
            "max_gap": 0,
        }

    # Métriques de base
    total_photos = len(df)
    periode_couverte = df["age_mois"].max() + 1 if not df.empty else 0
    moyenne_par_mois = total_photos / periode_couverte if periode_couverte > 0 else 0

    # Date de la dernière photo
    derniere_photo = df["date"].max()

    # Jour record
    photos_par_jour = df.groupby(df["date"].dt.date).size()
    jour_record = photos_par_jour.max() if not photos_par_jour.empty else 0

    # Plus long gap
    dates_uniques = sorted(df["date"].dt.date.unique())
    max_gap = 0
    if len(dates_uniques) > 1:
        for i in range(1, len(dates_uniques)):
            gap = (dates_uniques[i] - dates_uniques[i - 1]).days
            max_gap = max(max_gap, gap)

    return {
        "total_photos": total_photos,
        "periode_couverte": periode_couverte,
        "moyenne_par_mois": moyenne_par_mois,
        "derniere_photo": derniere_photo,
        "jour_record": jour_record,
        "max_gap": max_gap,
    }


def find_gaps(
    df: pd.DataFrame, min_gap_days: int = 5
) -> List[Tuple[datetime, datetime, int]]:
    """Trouve les gaps temporels dans les photos."""
    if df.empty:
        return []

    dates_uniques = sorted(df["date"].dt.date.unique())
    gaps = []

    for i in range(1, len(dates_uniques)):
        gap_days = (dates_uniques[i] - dates_uniques[i - 1]).days
        if gap_days >= min_gap_days:
            gaps.append((dates_uniques[i - 1], dates_uniques[i], gap_days))

    return gaps


def generate_insights(
    df: pd.DataFrame, metrics: Dict, date_naissance: datetime
) -> List[str]:
    """Génère les messages d'insights contextuels."""
    insights = []

    if df.empty:
        return ["Aucune photo analysée pour le moment 📸"]

    # Messages encourageants
    if metrics["total_photos"] > 100:
        insights.append(
            f"🎉 Magnifique collection de {metrics['total_photos']} photos!"
        )
    elif metrics["total_photos"] > 50:
        insights.append(f"📸 Belle collection de {metrics['total_photos']} photos!")

    # Analyse des mois les plus photographiés
    photos_par_mois = df.groupby("age_mois").size()
    if not photos_par_mois.empty:
        mois_champion = photos_par_mois.idxmax()
        nb_photos_champion = photos_par_mois.max()

        # Convertir l'âge en nom de mois calendaire
        mois_nom = age_to_month_name(mois_champion, date_naissance)

        insights.append(
            f"🏆 Période record : {mois_champion}-{mois_champion+1} mois ({mois_nom}) avec {nb_photos_champion} photos!"
        )

    # Analyse des jours de la semaine
    photos_par_jour_semaine = df.groupby("jour_semaine").size()
    if not photos_par_jour_semaine.empty:
        jour_favori = photos_par_jour_semaine.idxmax()
        if jour_favori in ["Saturday", "Sunday"]:
            insights.append("📅 Vous capturez bien les week-ends en famille!")
        elif jour_favori == "Sunday":
            insights.append("🌅 Champion du dimanche!")

    # Record de photos en une journée
    if metrics["jour_record"] >= 10:
        # Trouver la date du record
        photos_par_jour = df.groupby(df["date"].dt.date).size()
        date_record = photos_par_jour.idxmax()

        insights.append(
            f"📸 Mode rafale activé ! Record : {metrics['jour_record']} photos le {date_record.strftime('%d/%m/%Y')}!"
        )
    elif metrics["jour_record"] >= 5:
        # Trouver la date du record
        photos_par_jour = df.groupby(df["date"].dt.date).size()
        date_record = photos_par_jour.idxmax()

        insights.append(
            f"📷 Journée productive : {metrics['jour_record']} photos le {date_record.strftime('%d/%m/%Y')}!"
        )

    # Analyse des gaps
    gaps = find_gaps(df)
    if gaps:
        gap_le_plus_long = max(gaps, key=lambda x: x[2])
        if gap_le_plus_long[2] >= 10:
            insights.append(
                f"⚠️ Plus long silence : {gap_le_plus_long[2]} jours entre le {gap_le_plus_long[0].strftime('%d/%m')} et le {gap_le_plus_long[1].strftime('%d/%m')}"
            )

    # Régularité récente
    if not df.empty:
        photos_recentes = df[df["date"] >= (datetime.now() - timedelta(days=30))]
        if len(photos_recentes) == 0:
            insights.append("💡 Pensez à prendre quelques photos récentes!")
        elif len(photos_recentes) >= 20:
            insights.append("🔥 Très actif ce mois-ci!")

    # Projection future
    if metrics["moyenne_par_mois"] > 0:
        projection_annuelle = metrics["moyenne_par_mois"] * 12
        insights.append(
            f"📈 À ce rythme, vous aurez ~{int(projection_annuelle)} photos par an!"
        )

    # 2. Détection de moments spéciaux 🎉 (sans doublons avec jour_record)
    special_moments = detect_special_moments(df, metrics["jour_record"])
    insights.extend(special_moments)

    # 3. Comparaisons temporelles 📊 (sans doublons avec analyse weekends existante)
    temporal_comparisons = generate_temporal_comparisons(df, date_naissance)
    insights.extend(temporal_comparisons)

    return insights


def detect_special_moments(df: pd.DataFrame, jour_record_existant: int) -> List[str]:
    """Détecte les moments spéciaux basés sur les pics de photos (évite doublons avec jour_record)."""
    special_insights = []

    if df.empty:
        return special_insights

    # Analyser les pics de photos par jour (éviter doublon avec jour_record déjà traité)
    photos_par_jour = df.groupby(df["date"].dt.date).size()
    moyenne_quotidienne = photos_par_jour.mean()
    seuil_pic = max(moyenne_quotidienne * 2, 8)  # Seuil adaptatif

    pics = photos_par_jour[photos_par_jour >= seuil_pic]

    if len(pics) > 1:  # Plusieurs événements spéciaux détectés
        # Afficher quelques dates d'exemple (max 3)
        dates_exemples = sorted(pics.index)[:3]
        dates_str = ", ".join([d.strftime("%d/%m") for d in dates_exemples])
        if len(pics) > 3:
            dates_str += "..."

        special_insights.append(
            f"🎉 {len(pics)} événements spéciaux détectés ({dates_str})"
        )

        # Suggestions d'événements selon les pics avec date du pic maximum
        pic_max = pics.max()
        date_pic_max = pics.idxmax()

        if pic_max >= 25:
            special_insights.append(
                f"🎊 Événement majeur le {date_pic_max.strftime('%d/%m/%Y')} - Premières vacances ? Visite famille ?"
            )
        elif pic_max >= 15:
            special_insights.append(
                f"🎈 Belle journée le {date_pic_max.strftime('%d/%m/%Y')} - Sortie familiale ? Premier anniversaire ?"
            )

    # Détection de séries de photos (plusieurs jours consécutifs avec beaucoup de photos)
    dates_pics = sorted(pics.index)
    if len(dates_pics) >= 2:
        for i in range(1, len(dates_pics)):
            if (dates_pics[i] - dates_pics[i - 1]).days <= 3:  # 3 jours max
                date_debut = dates_pics[i - 1]
                date_fin = dates_pics[i]
                special_insights.append(
                    f"🏖️ Période intensive {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')} - Vacances ou événement ?"
                )
                break  # Une seule fois

    return special_insights


def age_to_month_name(age_mois: int, date_naissance: datetime) -> str:
    """Convertit un âge en mois vers le nom du mois calendaire correspondant."""
    mois_cible = date_naissance + timedelta(
        days=age_mois * 30.44
    )  # 30.44 jours par mois en moyenne
    mois_noms = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ]
    return mois_noms[mois_cible.month - 1]


def generate_temporal_comparisons(
    df: pd.DataFrame, date_naissance: datetime
) -> List[str]:
    """Génère des comparaisons temporelles (évite doublons avec analyse weekends existante)."""
    comparisons = []

    if df.empty:
        return comparisons

    # 1. Comparaisons mois par mois (évolution)
    photos_par_mois = df.groupby("age_mois").size()

    if len(photos_par_mois) >= 2:
        # Évolution entre premier et dernier mois
        premier_mois = photos_par_mois.index.min()
        dernier_mois = photos_par_mois.index.max()

        if dernier_mois - premier_mois >= 2:  # Au moins 2 mois d'écart
            photos_premier = photos_par_mois.loc[premier_mois]
            photos_dernier = photos_par_mois.loc[dernier_mois]

            premier_nom = age_to_month_name(premier_mois, date_naissance)
            dernier_nom = age_to_month_name(dernier_mois, date_naissance)

            if photos_premier > 0:
                evolution = ((photos_dernier - photos_premier) / photos_premier) * 100
                if evolution > 50:
                    comparisons.append(
                        f"📈 Évolution croissante : +{evolution:.0f}% entre {premier_nom} et {dernier_nom}"
                    )
                elif evolution < -40:
                    comparisons.append(
                        f"📉 Évolution : {evolution:.0f}% entre {premier_nom} et {dernier_nom}"
                    )

        # Comparaison des 2 mois les plus contrastés
        if len(photos_par_mois) >= 3:
            mois_min = photos_par_mois.idxmin()
            mois_max = photos_par_mois.idxmax()
            photos_min = photos_par_mois.min()
            photos_max = photos_par_mois.max()

            mois_min_nom = age_to_month_name(mois_min, date_naissance)
            mois_max_nom = age_to_month_name(mois_max, date_naissance)

            if photos_min > 0 and mois_min != mois_max:
                ratio = photos_max / photos_min
                if ratio >= 2:
                    comparisons.append(
                        f"📊 Contraste : {mois_max_nom} vs {mois_min_nom} = {ratio:.1f}x plus de photos"
                    )

    # 2. Comparaison week-end vs semaine avec RATIOS PRÉCIS (complément de l'existant)
    photos_weekends = df[df["jour_semaine"].isin(["Saturday", "Sunday"])].shape[0]
    photos_semaine = df[~df["jour_semaine"].isin(["Saturday", "Sunday"])].shape[0]

    if photos_weekends > 0 and photos_semaine > 0:
        # Ratio par jour (weekend = 2 jours, semaine = 5 jours)
        ratio_weekend_par_jour = photos_weekends / 2
        ratio_semaine_par_jour = photos_semaine / 5

        if ratio_semaine_par_jour > 0:
            multiplicateur = ratio_weekend_par_jour / ratio_semaine_par_jour

            # Seulement si très marqué (éviter doublon avec message existant)
            if multiplicateur >= 3:
                comparisons.append(
                    f"🎯 Weekend intense : {multiplicateur:.1f}x plus de photos par jour le weekend"
                )
            elif multiplicateur <= 0.4:
                comparisons.append(
                    f"💼 Semaine active : {1/multiplicateur:.1f}x plus de photos par jour en semaine"
                )

    # 3. Tendance sur les derniers mois
    if len(photos_par_mois) >= 3:
        derniers_3_mois = photos_par_mois.tail(3)

        # Calculer la tendance (régression simple)
        valeurs = list(derniers_3_mois.values)
        if len(valeurs) == 3:
            tendance = (valeurs[2] - valeurs[0]) / 2  # Pente moyenne
            if tendance > 8:
                comparisons.append(
                    "📈 Tendance récente : Vous photographiez de plus en plus votre 🦖"
                )
            elif tendance < -8:
                comparisons.append(
                    "📉 Tendance récente : Moins de photos - normal quand 🦖 grandit!"
                )

    return comparisons


def create_charts(df: pd.DataFrame):
    """Crée tous les graphiques pour l'onglet Analytics avec palette T-Rex Pastel."""
    charts = {}

    if df.empty:
        return charts

    # 🎨 Configuration T-Rex Pastel pour Plotly
    trex_colors = [PRIMARY, ACCENT, SUCCESS, WARNING, SECONDARY]

    # 1. Graphique en barres : Photos par mois d'âge
    photos_par_mois = df.groupby("age_mois").size().reset_index(name="nb_photos")
    fig_barres = px.bar(
        photos_par_mois,
        x="age_mois",
        y="nb_photos",
        title="🦖 Évolution des photos par mois d'âge",
        labels={"age_mois": "Âge du T-Rex (mois)", "nb_photos": "Nombre de photos"},
        color="nb_photos",
        color_continuous_scale=[[0, SUCCESS], [0.5, PRIMARY], [1, ACCENT]],
    )
    fig_barres.update_layout(
        showlegend=False,
        font=dict(family="Poppins, sans-serif", color=TEXT_DARK),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig_barres.update_xaxes(title="Âge du bébé (mois)", gridcolor=PRIMARY)
    fig_barres.update_yaxes(title="Nombre de photos", gridcolor=PRIMARY)
    charts["barres"] = fig_barres

    # 2. Timeline : Évolution hebdomadaire
    df["semaine_annee"] = df["date"].dt.strftime("%Y-W%U")
    photos_par_semaine = (
        df.groupby("semaine_annee").size().reset_index(name="nb_photos")
    )

    fig_timeline = px.line(
        photos_par_semaine,
        x="semaine_annee",
        y="nb_photos",
        title="🦖 Timeline : Activité hebdomadaire",
        labels={"semaine_annee": "Semaine", "nb_photos": "Nombre de photos"},
        color_discrete_sequence=[ACCENT],
    )
    fig_timeline.update_layout(
        font=dict(family="Poppins, sans-serif", color=TEXT_DARK),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig_timeline.update_xaxes(tickangle=45, title="Semaine", gridcolor=PRIMARY)
    fig_timeline.update_yaxes(title="Nombre de photos", gridcolor=PRIMARY)
    fig_timeline.update_traces(line_width=3)
    charts["timeline"] = fig_timeline

    # 3. Heatmap : Répartition par jour de la semaine
    jours_ordre = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    photos_par_jour = (
        df.groupby("jour_semaine").size().reindex(jours_ordre, fill_value=0)
    )

    # Créer une colorscale T-Rex pastel custom
    trex_colorscale = [[0.0, SUCCESS], [0.5, PRIMARY], [1.0, ACCENT]]

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=[photos_par_jour.values],
            x=jours_fr,
            y=["🦖 Activité"],
            colorscale=trex_colorscale,
            showscale=True,
            text=[photos_par_jour.values],
            texttemplate="%{text}",
            textfont={"size": 14, "color": TEXT_DARK},
        )
    )
    fig_heatmap.update_layout(
        title="🦖 Heatmap : Jours favoris",
        xaxis_title="Jour de la semaine",
        yaxis_title="",
        height=200,
        font=dict(family="Poppins, sans-serif", color=TEXT_DARK),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    charts["heatmap"] = fig_heatmap

    return charts


def main():
    # 🦖 Configuration T-Rex Pastel
    st.set_page_config(
        page_title="🦖 MomentKeeper",
        page_icon="🦖",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # 🎨 Appliquer le CSS custom
    st.markdown(TREX_CSS, unsafe_allow_html=True)

    # 🦖 Header principal avec style T-Rex
    st.markdown(
        """
        <div class="main-header">
            <h1>🦖 MomentKeeper</h1>
            <p><strong>Du Chaos à la Chronologie</strong></p>
            <p>Organisez vos photos de 🦖 (bébé) par mois d'âge et découvrez vos habitudes photo</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialiser la session state
    if "dossier_path" not in st.session_state:
        st.session_state.dossier_path = ""

    with st.sidebar:
        st.header("Configuration")

        st.subheader("📁 Dossier racine")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📁", help="Parcourir", key="browse_root"):
                dossier_selectionne = selectionner_dossier()
                if dossier_selectionne:
                    st.session_state.dossier_path = dossier_selectionne
                    st.rerun()

        with col2:
            dossier_racine = st.text_input(
                "Dossier racine du projet",
                placeholder="C:/Users/Nom/ProjetPhotos",
                value=st.session_state.dossier_path,
                label_visibility="collapsed",
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if dossier_racine != st.session_state.dossier_path:
                st.session_state.dossier_path = dossier_racine

        st.subheader("📸 Sous-dossier photos")
        col3, col4 = st.columns([1, 3])
        with col3:
            if st.button("📁", help="Parcourir sous-dossier", key="browse_sub"):
                if dossier_racine and Path(dossier_racine).exists():
                    dossier_selectionne = selectionner_dossier()
                    if dossier_selectionne:
                        # Extraire seulement le nom du sous-dossier relatif au dossier racine
                        try:
                            chemin_relatif = Path(dossier_selectionne).relative_to(
                                Path(dossier_racine)
                            )
                            st.session_state.sous_dossier_photos = str(chemin_relatif)
                            st.rerun()
                        except ValueError:
                            st.error(
                                "Le dossier sélectionné doit être dans le dossier racine"
                            )
                else:
                    st.error("Sélectionnez d'abord le dossier racine")

        with col4:
            # Initialiser la session state pour le sous-dossier
            if "sous_dossier_photos" not in st.session_state:
                st.session_state.sous_dossier_photos = "photos"

            sous_dossier_photos = st.text_input(
                "Nom du sous-dossier contenant les photos",
                value=st.session_state.sous_dossier_photos,
                help="Nom du dossier dans le dossier racine qui contient les photos à organiser",
                label_visibility="collapsed",
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if sous_dossier_photos != st.session_state.sous_dossier_photos:
                st.session_state.sous_dossier_photos = sous_dossier_photos

        date_naissance = st.date_input(
            "🦖 Date de naissance",
            min_value=datetime(2000, 1, 1).date(),
            max_value=datetime.now().date(),
        )

        if st.button(
            "🔄 Réinitialiser", help="Remet toutes les photos dans le dossier photos"
        ):
            if dossier_racine and Path(dossier_racine).exists():
                organiseur = OrganisateurPhotos(
                    Path(dossier_racine),
                    sous_dossier_photos,
                    datetime.combine(date_naissance, datetime.min.time()),
                )
                nb_fichiers, erreurs = organiseur.reinitialiser()

                if nb_fichiers > 0:
                    st.success(
                        f"✅ {nb_fichiers} fichiers remis dans le dossier photos"
                    )
                if erreurs:
                    st.error("❌ Erreurs rencontrées:")
                    for erreur in erreurs:
                        st.error(erreur)

    if dossier_racine and Path(dossier_racine).exists():
        dossier_photos_complet = Path(dossier_racine) / sous_dossier_photos
        if dossier_photos_complet.exists():
            organiseur = OrganisateurPhotos(
                Path(dossier_racine),
                sous_dossier_photos,
                datetime.combine(date_naissance, datetime.min.time()),
            )

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "🔍 Simulation",
                    "🗂️ Organisation",
                    "📊 Analytics",
                    "🦖 Insights",  # T-Rex pour les découvertes
                ]
            )

            with tab1:
                st.markdown(
                    '<div class="trex-message">🦖 <strong>Simulation de l\'organisation</strong><br>Prévisualisez sans déplacer vos fichiers !</div>',
                    unsafe_allow_html=True,
                )

                if st.button("🦖 Analyser les photos"):
                    with st.spinner("🦖 Analyse vos photos..."):
                        repartition, erreurs = organiseur.simuler_organisation()

                    if repartition:
                        total_photos = sum(len(f) for f in repartition.values())
                        st.markdown(
                            f'<div class="trex-success">🦖 Rawr de satisfaction ! {total_photos} photos analysées et prêtes à être organisées !</div>',
                            unsafe_allow_html=True,
                        )

                        for dossier, fichiers in sorted(repartition.items()):
                            with st.expander(f"📁 {dossier} ({len(fichiers)} photos)"):
                                for fichier in fichiers[:10]:
                                    st.text(f"  📸 {fichier.name}")
                                if len(fichiers) > 10:
                                    st.text(f"  ... et {len(fichiers) - 10} autres")
                    else:
                        st.info("ℹ️ Aucune photo trouvée à organiser")

                        # Afficher des informations de débogage
                        if (
                            hasattr(organiseur, "_fichiers_ignores")
                            and organiseur._fichiers_ignores
                        ):
                            with st.expander("🔍 Détails de l'analyse"):
                                st.write(
                                    f"Date de naissance configurée : {date_naissance}"
                                )
                                st.write(
                                    f"Nombre de fichiers ignorés : {len(organiseur._fichiers_ignores)}"
                                )

                                # Afficher quelques exemples
                                for nom, raison in organiseur._fichiers_ignores[:5]:
                                    st.text(f"  - {nom}: {raison}")

                                if len(organiseur._fichiers_ignores) > 5:
                                    st.text(
                                        f"  ... et {len(organiseur._fichiers_ignores) - 5} autres"
                                    )

                    if erreurs:
                        st.warning("⚠️ Avertissements:")
                        for erreur in erreurs:
                            st.warning(erreur)

            with tab2:
                st.markdown(
                    '<div class="trex-message">🗂️ <strong>Organisation réelle</strong><br>Temps de passer à l\'action !</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="trex-warning">🦖 Attention petits bras ! Cette action déplacera réellement vos fichiers.</div>',
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)
                with col1:
                    confirmer = st.checkbox("Je confirme vouloir organiser mes photos")

                with col2:
                    if st.button("🦖 Organiser", disabled=not confirmer):
                        with st.spinner("🦖 Petits bras en action..."):
                            nb_fichiers, erreurs = organiseur.organiser()

                        if nb_fichiers > 0:
                            st.markdown(
                                f'<div class="trex-success">🦖 Rawr de victoire ! {nb_fichiers} photos parfaitement organisées !</div>',
                                unsafe_allow_html=True,
                            )

                        if erreurs:
                            st.error("❌ Erreurs rencontrées:")
                            for erreur in erreurs:
                                st.error(erreur)

            with tab3:
                st.markdown(
                    '<div class="trex-message">📊 <strong>Analytics</strong><br>🦖 Découvrez les statistiques de votre petit explorateur !</div>',
                    unsafe_allow_html=True,
                )

                # Extraire les données des photos
                with st.spinner("🦖 Calcul des statistiques en cours..."):
                    df_photos = extract_photo_data(organiseur)
                    metrics = calculate_metrics(df_photos)

                if df_photos.empty:
                    st.info("ℹ️ Aucune photo trouvée pour l'analyse")
                else:
                    # Métriques principales en colonnes (3x2 layout)
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "🦖 Photos gardées",
                            metrics["total_photos"],
                            delta=(
                                "Petits souvenirs précieux !"
                                if metrics["total_photos"] > 0
                                else None
                            ),
                        )
                        st.metric(
                            "📅 Dernière capture",
                            (
                                metrics["derniere_photo"].strftime("%d/%m/%Y")
                                if metrics["derniere_photo"]
                                else "N/A"
                            ),
                            delta="Récente !" if metrics["derniere_photo"] else None,
                        )

                    with col2:
                        st.metric(
                            "🗓️ Croissance",
                            f"{metrics['periode_couverte']} mois",
                            delta=(
                                "Ça grandit vite !"
                                if metrics["periode_couverte"] > 6
                                else None
                            ),
                        )
                        st.metric(
                            "🏆 Record quotidien",
                            f"{metrics['jour_record']} photos",
                            delta=(
                                "Mode rafale !"
                                if metrics["jour_record"] >= 10
                                else None
                            ),
                        )

                    with col3:
                        st.metric(
                            "📈 Rythme",
                            f"{metrics['moyenne_par_mois']:.1f}/mois",
                            delta=(
                                "Régulier !"
                                if metrics["moyenne_par_mois"] >= 20
                                else "On peut faire mieux"
                            ),
                        )
                        st.metric(
                            "⏱️ Plus long silence",
                            f"{metrics['max_gap']} jours",
                            delta=(
                                "T-Rex endormi ?"
                                if metrics["max_gap"] >= 7
                                else "Bien suivi !"
                            ),
                        )

                    st.divider()

                    # Graphiques
                    charts = create_charts(df_photos)

                    if charts:
                        # Graphique en barres
                        if "barres" in charts:
                            st.plotly_chart(charts["barres"], use_container_width=True)

                        # Timeline et heatmap en colonnes
                        col1, col2 = st.columns(2)

                        with col1:
                            if "timeline" in charts:
                                st.plotly_chart(
                                    charts["timeline"], use_container_width=True
                                )

                        with col2:
                            if "heatmap" in charts:
                                st.plotly_chart(
                                    charts["heatmap"], use_container_width=True
                                )

                        # Alertes visuelles pour les gaps
                        gaps = find_gaps(df_photos)
                        if gaps:
                            st.subheader("⚠️ Alertes temporelles")
                            for gap_start, gap_end, gap_days in gaps:
                                if gap_days >= 5:
                                    st.warning(
                                        f"Gap de {gap_days} jours : du {gap_start.strftime('%d/%m/%Y')} au {gap_end.strftime('%d/%m/%Y')}"
                                    )

            with tab4:
                st.markdown(
                    '<div class="trex-message">🦖 <strong>Insights</strong><br>Découvertes sur vos habitudes photo !</div>',
                    unsafe_allow_html=True,
                )

                # Réutiliser les données déjà extraites si possible
                if "df_photos" not in locals():
                    with st.spinner("🦖 Fouille dans vos données..."):
                        df_photos = extract_photo_data(organiseur)
                        metrics = calculate_metrics(df_photos)

                # Messages d'insights
                insights = generate_insights(
                    df_photos, metrics, organiseur.date_naissance
                )

                if insights:
                    st.markdown("### 🎯 Découvertes")
                    for insight in insights:
                        st.markdown(
                            f'<div class="insight-bubble">{insight}</div>',
                            unsafe_allow_html=True,
                        )

                    st.divider()

                    # Section détails si il y a des données
                    if not df_photos.empty:
                        st.subheader("📋 Analyse détaillée")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write("**🗓️ Répartition mensuelle**")
                            photos_par_mois = df_photos.groupby("age_mois").size()
                            for mois, nb in photos_par_mois.head(5).items():
                                st.write(f"• {mois}-{mois+1} mois : {nb} photos")
                            if len(photos_par_mois) > 5:
                                st.write(
                                    f"... et {len(photos_par_mois) - 5} autres mois"
                                )

                        with col2:
                            st.write("**📅 Jours favoris**")
                            jours_fr_map = {
                                "Monday": "Lundi",
                                "Tuesday": "Mardi",
                                "Wednesday": "Mercredi",
                                "Thursday": "Jeudi",
                                "Friday": "Vendredi",
                                "Saturday": "Samedi",
                                "Sunday": "Dimanche",
                            }
                            photos_par_jour = (
                                df_photos.groupby("jour_semaine")
                                .size()
                                .sort_values(ascending=False)
                            )
                            for jour_en, nb in photos_par_jour.head(3).items():
                                jour_fr = jours_fr_map.get(jour_en, jour_en)
                                st.write(f"• {jour_fr} : {nb} photos")

                        # Suggestions d'amélioration
                        st.subheader("💡 Suggestions")

                        gaps = find_gaps(df_photos, min_gap_days=7)
                        if gaps:
                            st.write("📸 **Pour ne rien rater :**")
                            st.write(
                                "• Pensez à prendre des photos pendant la semaine aussi"
                            )
                            st.write("• Essayez de capturer les moments du quotidien")

                        if metrics["moyenne_par_mois"] < 10:
                            st.write("📈 **Pour enrichir vos souvenirs :**")
                            st.write(
                                "• Quelques photos de plus par mois donneraient un bel aperçu de l'évolution"
                            )
                            st.write(
                                "• Les petits moments comptent autant que les grands!"
                            )
                else:
                    st.info("Analysez d'abord vos photos pour voir les insights!")
        else:
            st.error(
                f"❌ Le dossier photos '{sous_dossier_photos}' n'existe pas dans {dossier_racine}"
            )
    else:
        if dossier_racine:
            st.error("❌ Le dossier racine spécifié n'existe pas")
        else:
            st.info("👈 Configurez le dossier racine dans la barre latérale")

    # 🦖 Footer T-Rex avec personnalité
    st.markdown(
        """
        <div class="trex-footer">
            <p>Créé avec ❤️ pour un 🦖 aux petits bras mais au grand cœur</p>
            <p><strong>🦖 MomentKeeper v1.0</strong> - Organisateur T-Rex Pastel</p>
            <p><em>"Du Chaos à la Chronologie, une photo à la fois"</em></p>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
