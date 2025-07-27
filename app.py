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
from src.moment_keeper.translations import Translator

# 🎨 Palette couleurs T-Rex Pastel
PRIMARY = "#E8F4F8"  # Bleu pastel doux (ciel préhistorique)
SECONDARY = "#F9F2E7"  # Beige/crème chaleureux (sable ancien)
ACCENT = "#D4C5B9"  # Taupe rosé (terre préhistorique)
SUCCESS = "#C8E6C9"  # Vert pastel (T-Rex amical)
WARNING = "#FFE0B2"  # Orange pastel
ERROR = "#FFCDD2"  # Rose pastel
TEXT_DARK = "#2C3E50"  # Bleu marine doux
TEXT_LIGHT = "#7F8C8D"  # Gris élégant

# 🎨 Couleurs pastels additionnelles pour graphiques
CHART_PURPLE = "#E1D5E7"  # Violet pastel
CHART_MINT = "#D5F4E6"    # Menthe pastel
CHART_PEACH = "#FFE5D9"   # Pêche pastel
CHART_LAVENDER = "#E6E6FA" # Lavande pastel
CHART_CORAL = "#FFB3BA"   # Corail pastel
DARK_RED_PASTEL = "#F8BBD9" # Rouge pastel plus foncé

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
    background: linear-gradient(135deg, {DARK_RED_PASTEL} 0%, {PRIMARY} 100%);
    border-left-color: #E91E63;
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
    background: linear-gradient(135deg, {ACCENT} 0%, {PRIMARY} 100%);
    border: 2px solid {ACCENT};
    color: {TEXT_DARK};
}}

/* Style pour le bouton inactif */
.language-selector .stButton > button[data-testid="baseButton-secondary"] {{
    background: rgba(255,255,255,0.7);
    border: 2px solid {PRIMARY};
    color: {TEXT_LIGHT};
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
    
    # Parcourir tous les dossiers du projet (source + dossiers mensuels)
    for dossier in organiseur.dossier_racine.iterdir():
        if dossier.is_dir():
            for fichier in dossier.iterdir():
                if fichier.is_file() and fichier.suffix.lower() in organiseur.extensions_actives:
                    # Réutiliser la méthode existante pour extraire la date
                    date_photo = organiseur.extraire_date_nom_fichier(fichier.name)

                    if date_photo and date_photo >= organiseur.date_naissance:
                        # Réutiliser la méthode existante pour calculer l'âge
                        age_mois = organiseur.calculer_age_mois(date_photo)

                        photos_data.append(
                            {
                                "fichier": fichier.name,
                                "type": organiseur.get_file_type(fichier),
                                "date": date_photo,
                                "age_mois": age_mois,
                                "dossier": dossier.name,
                                "jour_semaine": date_photo.strftime("%A"),
                                "semaine": date_photo.isocalendar()[1],
                                "annee": date_photo.year,
                            }
                        )

    return pd.DataFrame(photos_data)


def calculate_metrics(df: pd.DataFrame, type_fichiers: str = None) -> Dict:
    """Calcule toutes les métriques pour l'onglet Analytics."""
    if df.empty:
        return {
            "total_photos": 0,
            "total_videos": 0,
            "periode_couverte": 0,
            "moyenne_par_mois": 0,
            "derniere_photo": None,
            "jour_record": 0,
            "max_gap": 0,
        }

    # Métriques de base avec distinction photo/vidéo si nécessaire
    if type_fichiers == "📸🎬 Photos et Vidéos" and 'type' in df.columns:
        total_photos = len(df[df['type'] == 'photo'])
        total_videos = len(df[df['type'] == 'video'])
        total_fichiers = total_photos + total_videos
    else:
        total_fichiers = len(df)
        total_photos = total_fichiers if type_fichiers and "Photos" in type_fichiers else 0
        total_videos = total_fichiers if type_fichiers and "Vidéos" in type_fichiers else 0
    
    periode_couverte = df["age_mois"].max() + 1 if not df.empty else 0
    moyenne_par_mois = total_fichiers / periode_couverte if periode_couverte > 0 else 0

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
        "total_videos": total_videos,
        "total_fichiers": total_fichiers,
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
    df: pd.DataFrame, metrics: Dict, date_naissance: datetime, type_fichiers: str = None, tr=None
) -> List[str]:
    """Génère les messages d'insights contextuels."""
    insights = []

    if df.empty:
        if tr:
            return [tr.t("analyze_first")]
        return ["Aucune photo analysée pour le moment 📸"]
    
    # Protection contre tr None
    if not tr:
        from src.moment_keeper.translations import Translator
        tr = Translator("fr")

    # Messages encourageants adaptés au type
    if type_fichiers == "📸🎬 Photos et Vidéos":
        total = metrics.get("total_fichiers", 0)
        if total > 100:
            insights.append(
                tr.t("magnificent_collection_mixed", photos=metrics['total_photos'], videos=metrics['total_videos'])
            )
        
        # Ratio photos/vidéos
        if metrics["total_videos"] > 0:
            ratio = metrics["total_photos"] / metrics["total_videos"]
            if ratio > 5:
                insights.append(
                    "📸 Vous préférez clairement les photos aux vidéos!" if tr.language == "fr" 
                    else "📸 You clearly prefer photos to videos!"
                )
            elif ratio < 0.2:
                insights.append("🎬 Un vrai vidéaste ! Vous capturez surtout en vidéo")
            elif 0.8 < ratio < 1.2:
                insights.append("⚖️ Équilibre parfait entre photos et vidéos!")
    else:
        # Messages pour un seul type
        total = metrics.get("total_fichiers", metrics.get("total_photos", 0))
        type_nom = "photos" if type_fichiers and "Photos" in type_fichiers else "vidéos"
        type_emoji = "📸" if type_fichiers and "Photos" in type_fichiers else "🎬"
        
        if total > 100:
            insights.append(
                tr.t("magnificent_collection", total=total, type=type_nom)
            )
        elif total > 50:
            insights.append(f"{type_emoji} Belle collection de {total} {type_nom}!")

    # Analyse des mois les plus photographiés
    photos_par_mois = df.groupby("age_mois").size()
    if not photos_par_mois.empty:
        mois_champion = photos_par_mois.idxmax()
        nb_photos_champion = photos_par_mois.max()

        # Convertir l'âge en nom de mois calendaire
        mois_nom = age_to_month_name(mois_champion, date_naissance)

        insights.append(
            tr.t("record_period", start=mois_champion, end=mois_champion+1, month=mois_nom, count=nb_photos_champion)
        )

    # Analyse des jours de la semaine
    photos_par_jour_semaine = df.groupby("jour_semaine").size()
    if not photos_par_jour_semaine.empty:
        jour_favori = photos_par_jour_semaine.idxmax()
        if jour_favori in ["Saturday", "Sunday"]:
            insights.append(
                "📅 Vous capturez bien les week-ends en famille!" if tr.language == "fr" 
                else "📅 You capture family weekends well!"
            )
        elif jour_favori == "Sunday":
            insights.append("🌅 Champion du dimanche!")

    # Record de photos en une journée
    if metrics["jour_record"] >= 10:
        # Trouver la date du record
        photos_par_jour = df.groupby(df["date"].dt.date).size()
        date_record = photos_par_jour.idxmax()

        insights.append(
            tr.t("burst_mode_activated", count=metrics['jour_record'], date=date_record.strftime('%d/%m/%Y'))
        )
    elif metrics["jour_record"] >= 5:
        # Trouver la date du record
        photos_par_jour = df.groupby(df["date"].dt.date).size()
        date_record = photos_par_jour.idxmax()

        insights.append(
            tr.t("productive_day", count=metrics['jour_record'], date=date_record.strftime('%d/%m/%Y'))
        )

    # Analyse des gaps
    gaps = find_gaps(df)
    if gaps:
        gap_le_plus_long = max(gaps, key=lambda x: x[2])
        if gap_le_plus_long[2] >= 10:
            insights.append(
                tr.t("longest_silence", days=gap_le_plus_long[2], start=gap_le_plus_long[0].strftime('%d/%m'), end=gap_le_plus_long[1].strftime('%d/%m'))
            )

    # Régularité récente
    if not df.empty:
        photos_recentes = df[df["date"] >= (datetime.now() - timedelta(days=30))]
        if len(photos_recentes) == 0:
            insights.append(tr.t("think_recent_photos"))
        elif len(photos_recentes) >= 20:
            insights.append(tr.t("very_active_month"))

    # Projection future
    if metrics["moyenne_par_mois"] > 0:
        projection_annuelle = metrics["moyenne_par_mois"] * 12
        insights.append(
            f"📈 À ce rythme, vous aurez ~{int(projection_annuelle)} photos par an!" if tr.language == "fr"
            else f"📈 At this rate, you'll have ~{int(projection_annuelle)} photos per year!"
        )

    # 2. Détection de moments spéciaux 🎉 (sans doublons avec jour_record)
    special_moments = detect_special_moments(df, metrics["jour_record"], tr)
    insights.extend(special_moments)

    # 3. Comparaisons temporelles 📊 (sans doublons avec analyse weekends existante)
    temporal_comparisons = generate_temporal_comparisons(df, date_naissance, tr)
    insights.extend(temporal_comparisons)

    return insights


def detect_special_moments(df: pd.DataFrame, jour_record_existant: int, tr) -> List[str]:
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
            f"🎉 {len(pics)} événements spéciaux détectés ({dates_str})" if tr.language == "fr"
            else f"🎉 {len(pics)} special events detected ({dates_str})"
        )

        # Suggestions d'événements selon les pics avec date du pic maximum
        pic_max = pics.max()
        date_pic_max = pics.idxmax()

        if pic_max >= 25:
            special_insights.append(
                f"🎊 Événement majeur le {date_pic_max.strftime('%d/%m/%Y')} - Premières vacances ? Visite famille ?" if tr.language == "fr"
                else f"🎊 Major event on {date_pic_max.strftime('%d/%m/%Y')} - First vacation? Family visit?"
            )
        elif pic_max >= 15:
            special_insights.append(
                f"🎈 Belle journée le {date_pic_max.strftime('%d/%m/%Y')} - Sortie familiale ? Premier anniversaire ?" if tr.language == "fr"
                else f"🎈 Great day on {date_pic_max.strftime('%d/%m/%Y')} - Family outing? First birthday?"
            )

    # Détection de séries de photos (plusieurs jours consécutifs avec beaucoup de photos)
    dates_pics = sorted(pics.index)
    if len(dates_pics) >= 2:
        for i in range(1, len(dates_pics)):
            if (dates_pics[i] - dates_pics[i - 1]).days <= 3:  # 3 jours max
                date_debut = dates_pics[i - 1]
                date_fin = dates_pics[i]
                special_insights.append(
                    f"🏖️ Période intensive {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')} - Vacances ou événement ?" if tr.language == "fr"
                    else f"🏖️ Intensive period {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')} - Vacation or event?"
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
    df: pd.DataFrame, date_naissance: datetime, tr=None
) -> List[str]:
    """Génère des comparaisons temporelles (évite doublons avec analyse weekends existante)."""
    comparisons = []
    
    # Protection contre tr None
    if not tr:
        from src.moment_keeper.translations import Translator
        tr = Translator("fr")

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
                        f"📉 Évolution : {evolution:.0f}% entre {premier_nom} et {dernier_nom}" if tr.language == "fr"
                        else f"📉 Evolution: {evolution:.0f}% between {premier_nom} and {dernier_nom}"
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
                        tr.t("contrast_months", max_month=mois_max_nom, min_month=mois_min_nom, ratio=f"{ratio:.1f}")
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
                    tr.t("intense_weekend", ratio=f"{multiplicateur:.1f}")
                )
            elif multiplicateur <= 0.4:
                comparisons.append(
                    tr.t("active_weekdays", ratio=f"{1/multiplicateur:.1f}")
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


def create_charts(df: pd.DataFrame, tr):
    """Crée tous les graphiques pour l'onglet Analytics avec palette T-Rex Pastel."""
    charts = {}

    if df.empty:
        return charts

    # 🎨 Configuration T-Rex Pastel pour Plotly avec couleurs différenciées
    trex_colors = [SUCCESS, CHART_MINT, PRIMARY, CHART_PEACH, WARNING, CHART_PURPLE, CHART_LAVENDER, CHART_CORAL]

    # 1. Graphique en barres : Photos par mois d'âge avec dégradé amélioré
    photos_par_mois = df.groupby("age_mois").size().reset_index(name="nb_photos")
    fig_barres = px.bar(
        photos_par_mois,
        x="age_mois",
        y="nb_photos",
        title="🦖 Évolution des photos par mois d'âge" if tr.language == "fr" else "🦖 Photo evolution by age in months",
        labels={
            "age_mois": "Âge du T-Rex (mois)" if tr.language == "fr" else "T-Rex age (months)",
            "nb_photos": "Nombre de photos" if tr.language == "fr" else "Number of photos"
        },
        color="nb_photos",
        color_continuous_scale=[[0, SUCCESS], [0.3, CHART_MINT], [0.6, PRIMARY], [1, CHART_PURPLE]],
    )
    fig_barres.update_layout(
        showlegend=False,
        font=dict(family="Poppins, sans-serif", color=TEXT_DARK),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig_barres.update_xaxes(
        title="Âge du bébé (mois)" if tr.language == "fr" else "Baby age (months)", 
        gridcolor=PRIMARY
    )
    fig_barres.update_yaxes(
        title="Nombre de photos" if tr.language == "fr" else "Number of photos", 
        gridcolor=PRIMARY
    )
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
        title="🦖 Timeline : Activité hebdomadaire" if tr.language == "fr" else "🦖 Timeline: Weekly activity",
        labels={
            "semaine_annee": "Semaine" if tr.language == "fr" else "Week",
            "nb_photos": "Nombre de photos" if tr.language == "fr" else "Number of photos"
        },
        color_discrete_sequence=[CHART_PURPLE],
    )
    fig_timeline.update_layout(
        font=dict(family="Poppins, sans-serif", color=TEXT_DARK),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig_timeline.update_xaxes(
        tickangle=45, 
        title="Semaine" if tr.language == "fr" else "Week", 
        gridcolor=PRIMARY
    )
    fig_timeline.update_yaxes(
        title="Nombre de photos" if tr.language == "fr" else "Number of photos", 
        gridcolor=PRIMARY
    )
    fig_timeline.update_traces(
        line_width=4,
        line_color=CHART_PURPLE,
        marker=dict(size=8, color=CHART_CORAL, line=dict(width=2, color=TEXT_DARK))
    )
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

    # Créer une colorscale T-Rex pastel custom avec meilleur contraste
    trex_colorscale = [
        [0.0, "#F0F8FF"],      # Blanc cassé pour zéro
        [0.2, CHART_MINT],     # Menthe pour faible activité
        [0.4, SUCCESS],        # Vert pastel pour activité modérée
        [0.6, CHART_PEACH],    # Pêche pour bonne activité
        [0.8, WARNING],        # Orange pour forte activité
        [1.0, CHART_CORAL]     # Corail pour activité maximale
    ]

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=[photos_par_jour.values],
            x=jours_fr,
            y=["🦖 Activité"],
            colorscale=trex_colorscale,
            showscale=True,
            text=[photos_par_jour.values],
            texttemplate="%{text}",
            textfont={"size": 14, "color": TEXT_DARK, "family": "Poppins"},
        )
    )
    fig_heatmap.update_layout(
        title="🦖 Heatmap : Jours favoris" if tr.language == "fr" else "🦖 Heatmap: Favorite days",
        xaxis_title="Jour de la semaine" if tr.language == "fr" else "Day of the week",
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
    # Traducteur temporaire pour le header (avant la sidebar)
    temp_lang = st.session_state.get("language", "fr") 
    temp_tr = Translator(temp_lang)
    
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{temp_tr.t("app_title")}</h1>
            <p><strong>{temp_tr.t("tagline")}</strong></p>
            <p>{temp_tr.t("subtitle")}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialiser la session state
    if "dossier_path" not in st.session_state:
        st.session_state.dossier_path = ""
    if "language" not in st.session_state:
        st.session_state.language = "fr"

    with st.sidebar:
        # Sélecteur de langue ultra-compact
        current_lang = st.session_state.language
        
        col1, col2, col3 = st.columns([1, 0.2, 1])
        with col1:
            if st.button("FR", key="lang_fr_mini", 
                        type="primary" if current_lang == "fr" else "secondary",
                        help="Français"):
                if current_lang != "fr":
                    st.session_state.language = "fr"
                    st.rerun()
        
        with col2:
            st.markdown("<p style='text-align: center; margin: 0.5rem 0; color: #7F8C8D;'>|</p>", 
                       unsafe_allow_html=True)
        
        with col3:
            if st.button("EN", key="lang_en_mini",
                        type="primary" if current_lang == "en" else "secondary", 
                        help="English"):
                if current_lang != "en":
                    st.session_state.language = "en"
                    st.rerun()
        
        # Initialiser le traducteur
        tr = Translator(st.session_state.language)
        
        st.header(tr.t("config_header"))

        st.subheader(tr.t("main_folder"))
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📁", help=tr.t("browse"), key="browse_root"):
                dossier_selectionne = selectionner_dossier()
                if dossier_selectionne:
                    st.session_state.dossier_path = dossier_selectionne
                    st.rerun()

        with col2:
            dossier_racine = st.text_input(
                tr.t("main_folder"),
                placeholder=tr.t("main_folder_placeholder"),
                value=st.session_state.dossier_path,
                label_visibility="collapsed",
                help=tr.t("main_folder_help")
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if dossier_racine != st.session_state.dossier_path:
                st.session_state.dossier_path = dossier_racine

        st.subheader(tr.t("source_folder"))
        col3, col4 = st.columns([1, 3])
        with col3:
            if st.button("📁", help=tr.t("browse_subfolder"), key="browse_sub"):
                if dossier_racine and Path(dossier_racine).exists():
                    dossier_selectionne = selectionner_dossier()
                    if dossier_selectionne:
                        # Extraire seulement le nom du sous-dossier relatif au dossier principal
                        try:
                            chemin_relatif = Path(dossier_selectionne).relative_to(
                                Path(dossier_racine)
                            )
                            st.session_state.sous_dossier_photos = str(chemin_relatif)
                            st.rerun()
                        except ValueError:
                            st.error(tr.t("folder_must_be_in_root"))
                else:
                    st.error(tr.t("select_root_first"))

        with col4:
            # Initialiser la session state pour le sous-dossier
            if "sous_dossier_photos" not in st.session_state:
                st.session_state.sous_dossier_photos = "photos"

            sous_dossier_photos = st.text_input(
                tr.t("source_folder"),
                value=st.session_state.sous_dossier_photos,
                help=tr.t("source_folder_help"),
                label_visibility="collapsed",
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if sous_dossier_photos != st.session_state.sous_dossier_photos:
                st.session_state.sous_dossier_photos = sous_dossier_photos

        date_naissance = st.date_input(
            tr.t("birth_date"),
            min_value=datetime(2000, 1, 1).date(),
            max_value=datetime.now().date(),
        )

        st.subheader(tr.t("file_types"))
        
        # Checkboxes pour photos et vidéos
        photos_selected = st.checkbox(tr.t("photos"), value=True)
        videos_selected = st.checkbox(tr.t("videos"), value=True)
        
        # Déterminer le type de fichiers basé sur les checkboxes
        if photos_selected and videos_selected:
            type_fichiers = "📸🎬 Photos et Vidéos"
        elif photos_selected:
            type_fichiers = "📸 Photos uniquement"
        elif videos_selected:
            type_fichiers = "🎬 Vidéos uniquement"
        else:
            type_fichiers = None
            st.warning(tr.t("no_type_selected"))

        if st.button(
            tr.t("reset_button"), help=tr.t("reset_help")
        ):
            if dossier_racine and Path(dossier_racine).exists():
                organiseur = OrganisateurPhotos(
                    Path(dossier_racine),
                    sous_dossier_photos,
                    datetime.combine(date_naissance, datetime.min.time()),
                    type_fichiers
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
            if type_fichiers is None:
                st.error("❌ Veuillez sélectionner au moins un type de fichier (Photos et/ou Vidéos)")
            else:
                organiseur = OrganisateurPhotos(
                    Path(dossier_racine),
                    sous_dossier_photos,
                    datetime.combine(date_naissance, datetime.min.time()),
                    type_fichiers
                )

                tab1, tab2, tab3, tab4 = st.tabs(
                [
                    tr.t("tab_simulation"),
                    tr.t("tab_organization"),
                    tr.t("tab_analytics"),
                    tr.t("tab_insights"),
                ]
            )

            with tab1:
                st.markdown(
                    f'<div class="trex-message">{tr.t("simulation_title")}</div>',
                    unsafe_allow_html=True,
                )

                if st.button(tr.t("analyze_button")):
                    with st.spinner(tr.t("analyzing")):
                        repartition, erreurs = organiseur.simuler_organisation()

                    if repartition:
                        total_photos = sum(len(f) for f in repartition.values())
                        
                        if type_fichiers == "📸🎬 Photos et Vidéos":
                            # Compter photos et vidéos séparément
                            total_photos_count = sum(len([f for f in fichiers if organiseur.get_file_type(f) == "photo"]) for fichiers in repartition.values())
                            total_videos_count = sum(len([f for f in fichiers if organiseur.get_file_type(f) == "video"]) for fichiers in repartition.values())
                            message = tr.t("success_simulation_mixed", photos=total_photos_count, videos=total_videos_count)
                        elif "Photos" in type_fichiers:
                            message = tr.t("success_simulation", photos=total_photos)
                        else:
                            message = tr.t("success_simulation", photos=total_photos)
                        
                        st.markdown(
                            f'<div class="trex-success">{message}</div>',
                            unsafe_allow_html=True,
                        )

                        for dossier, fichiers in sorted(repartition.items()):
                            if type_fichiers == "📸🎬 Photos et Vidéos":
                                # Séparer photos et vidéos
                                photos = [f for f in fichiers if organiseur.get_file_type(f) == "photo"]
                                videos = [f for f in fichiers if organiseur.get_file_type(f) == "video"]
                                
                                with st.expander(f"📁 {dossier} ({len(photos)} 📸 + {len(videos)} 🎬)"):
                                    if photos:
                                        st.write("📸 **Photos:**")
                                        for photo in photos[:5]:
                                            st.text(f"  📸 {photo.name}")
                                        if len(photos) > 5:
                                            st.text(f"  ... et {len(photos) - 5} autres photos")
                                    
                                    if videos:
                                        st.write("🎬 **Vidéos:**")
                                        for video in videos[:5]:
                                            st.text(f"  🎬 {video.name}")
                                        if len(videos) > 5:
                                            st.text(f"  ... et {len(videos) - 5} autres vidéos")
                            else:
                                # Affichage normal pour un seul type
                                type_emoji = "📸" if "Photos" in type_fichiers else "🎬"
                                type_nom = tr.t("photos_unit") if "Photos" in type_fichiers else tr.t("videos_unit")
                                
                                with st.expander(f"📁 {dossier} ({len(fichiers)} {type_nom})"):
                                    for fichier in fichiers[:10]:
                                        st.text(f"  {type_emoji} {fichier.name}")
                                    if len(fichiers) > 10:
                                        st.text(tr.t("and_more", count=len(fichiers) - 10))
                    else:
                        st.info(tr.t("no_files_found"))

                        # Afficher des informations de débogage
                        if (
                            hasattr(organiseur, "_fichiers_ignores")
                            and organiseur._fichiers_ignores
                        ):
                            with st.expander(tr.t("debug_details")):
                                st.write(
                                    f"{tr.t('birth_date_configured')}{date_naissance}"
                                )
                                st.write(
                                    f"{tr.t('ignored_files_count')}{len(organiseur._fichiers_ignores)}"
                                )

                                # Afficher quelques exemples
                                for nom, raison in organiseur._fichiers_ignores[:5]:
                                    st.text(f"  - {nom}: {raison}")

                                if len(organiseur._fichiers_ignores) > 5:
                                    st.text(
                                        f"  ... et {len(organiseur._fichiers_ignores) - 5} autres"
                                    )

                    if erreurs:
                        st.warning(tr.t("warnings"))
                        for erreur in erreurs:
                            st.warning(erreur)

            with tab2:
                st.markdown(
                    f'<div class="trex-message">{tr.t("organization_title")}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="trex-warning">{tr.t("organization_warning")}</div>',
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)
                with col1:
                    type_text = tr.t("photos_unit") if "Photos" in type_fichiers else tr.t("videos_unit") if "Vidéos" in type_fichiers else tr.t("files_unit")
                    confirmer = st.checkbox(tr.t("confirm_organize", type=type_text))

                with col2:
                    if st.button(tr.t("organize_button"), disabled=not confirmer):
                        with st.spinner(tr.t("organizing")):
                            nb_fichiers, erreurs = organiseur.organiser()

                        if nb_fichiers > 0:
                            if type_fichiers == "📸🎬 Photos et Vidéos":
                                type_text = tr.t("files_unit")
                            elif "Photos" in type_fichiers:
                                type_text = tr.t("photos_unit")
                            else:
                                type_text = tr.t("videos_unit")
                            
                            message = tr.t("success_organize", count=nb_fichiers, type=type_text)
                            st.markdown(
                                f'<div class="trex-success">{message}</div>',
                                unsafe_allow_html=True,
                            )

                        if erreurs:
                            st.error(tr.t("errors_occurred"))
                            for erreur in erreurs:
                                st.error(erreur)

            with tab3:
                st.markdown(
                    f'<div class="trex-message">{tr.t("analytics_title")}</div>',
                    unsafe_allow_html=True,
                )

                # Extraire les données des photos
                with st.spinner(tr.t("calculating_stats")):
                    df_photos = extract_photo_data(organiseur)
                    metrics = calculate_metrics(df_photos, type_fichiers)

                if df_photos.empty:
                    st.info(tr.t("no_data_analytics"))
                else:
                    # Métriques principales en colonnes (3x2 layout)
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if type_fichiers == "📸🎬 Photos et Vidéos":
                            st.metric(
                                "📸 Photos",
                                metrics["total_photos"],
                                delta=(
                                    f"{metrics['total_photos'] / metrics['total_fichiers'] * 100:.0f}% du total"
                                    if metrics["total_fichiers"] > 0
                                    else None
                                ),
                            )
                        else:
                            label = tr.t("photos_kept") if "Photos" in type_fichiers else tr.t("videos_kept")
                            st.metric(
                                label,
                                metrics["total_fichiers"],
                                delta=(
                                    tr.t("precious_memories")
                                    if metrics["total_fichiers"] > 0
                                    else None
                                ),
                            )
                        st.metric(
                            tr.t("last_capture"),
                            (
                                metrics["derniere_photo"].strftime("%d/%m/%Y")
                                if metrics["derniere_photo"]
                                else "N/A"
                            ),
                            delta=tr.t("recent") if metrics["derniere_photo"] else None,
                        )

                    with col2:
                        if type_fichiers == "📸🎬 Photos et Vidéos":
                            st.metric(
                                "🎬 Vidéos",
                                metrics["total_videos"],
                                delta=(
                                    f"{metrics['total_videos'] / metrics['total_fichiers'] * 100:.0f}% du total"
                                    if metrics["total_fichiers"] > 0
                                    else None
                                ),
                            )
                        else:
                            st.metric(
                                tr.t("growth_period"),
                                f"{metrics['periode_couverte']} mois",
                                delta=(
                                    tr.t("growing_fast")
                                    if metrics["periode_couverte"] > 6
                                    else None
                                ),
                            )
                        st.metric(
                            tr.t("daily_record"),
                            f"{metrics['jour_record']} photos",
                            delta=(
                                tr.t("burst_mode")
                                if metrics["jour_record"] >= 10
                                else None
                            ),
                        )

                    with col3:
                        st.metric(
                            tr.t("average_rhythm"),
                            f"{metrics['moyenne_par_mois']:.1f}/mois",
                            delta=(
                                tr.t("regular")
                                if metrics["moyenne_par_mois"] >= 20
                                else tr.t("can_do_better")
                            ),
                        )
                        st.metric(
                            tr.t("longest_gap"),
                            f"{metrics['max_gap']} jours",
                            delta=(
                                tr.t("trex_sleeping")
                                if metrics["max_gap"] >= 7
                                else tr.t("well_followed")
                            ),
                        )

                    st.divider()

                    # Graphiques
                    charts = create_charts(df_photos, tr)

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
                    f'<div class="trex-message">{tr.t("insights_title")}</div>',
                    unsafe_allow_html=True,
                )

                # Réutiliser les données déjà extraites si possible
                if "df_photos" not in locals():
                    with st.spinner(tr.t("searching_data")):
                        df_photos = extract_photo_data(organiseur)
                        metrics = calculate_metrics(df_photos, type_fichiers)

                # Messages d'insights
                insights = generate_insights(
                    df_photos, metrics, organiseur.date_naissance, type_fichiers, tr
                )

                if insights:
                    st.markdown(tr.t("discoveries"))
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
                        st.info(tr.t("analyze_first"))
        else:
            st.error(tr.t("folder_not_exist", folder=sous_dossier_photos, root=dossier_racine))
    else:
        if dossier_racine:
            st.error(tr.t("root_not_exist"))
        else:
            st.info(tr.t("configure_root"))

    # 🦖 Footer T-Rex avec personnalité
    st.markdown(
        f"""
        <div class="trex-footer">
            <p>{temp_tr.t("footer_love")}</p>
            <p><strong>{temp_tr.t("footer_version")}</strong></p>
            <p><em>{temp_tr.t("footer_tagline")}</em></p>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
