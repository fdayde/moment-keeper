"""Module d'analyse et de statistiques pour MomentKeeper."""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image, ImageOps

from .config import CHART_CONFIG, INSIGHTS_THRESHOLDS
from .organizer import OrganisateurPhotos
from .theme import BAR_CHART_GRADIENT, COLORS, HEATMAP_COLORSCALE
from .translations import Translator


def extract_photo_data(organiseur: OrganisateurPhotos) -> pd.DataFrame:
    """Extrait les données des photos pour l'analyse."""
    photos_data = []

    # Parcourir tous les dossiers du projet (source + dossiers mensuels)
    for dossier in organiseur.dossier_racine.iterdir():
        if dossier.is_dir():
            for fichier in dossier.iterdir():
                if (
                    fichier.is_file()
                    and fichier.suffix.lower() in organiseur.extensions_actives
                ):
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


def calculate_metrics(df: pd.DataFrame, type_fichiers: str = None) -> dict:
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
    if type_fichiers == "📸🎬 Photos et Vidéos" and "type" in df.columns:
        total_photos = len(df[df["type"] == "photo"])
        total_videos = len(df[df["type"] == "video"])
        total_fichiers = total_photos + total_videos
    else:
        total_fichiers = len(df)
        total_photos = (
            total_fichiers if type_fichiers and "Photos" in type_fichiers else 0
        )
        total_videos = (
            total_fichiers if type_fichiers and "Vidéos" in type_fichiers else 0
        )

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
    df: pd.DataFrame, min_gap_days: int = None
) -> list[tuple[datetime, datetime, int]]:
    """Trouve les gaps temporels dans les photos."""
    if min_gap_days is None:
        min_gap_days = INSIGHTS_THRESHOLDS["min_gap_days"]

    if df.empty:
        return []

    dates_uniques = sorted(df["date"].dt.date.unique())
    gaps = []

    for i in range(1, len(dates_uniques)):
        gap_days = (dates_uniques[i] - dates_uniques[i - 1]).days
        if gap_days >= min_gap_days:
            gaps.append((dates_uniques[i - 1], dates_uniques[i], gap_days))

    return gaps


def age_to_month_name(
    age_mois: int, date_naissance: datetime, language: str = "fr"
) -> str:
    """Convertit un âge en mois vers le nom du mois calendaire correspondant."""
    mois_cible = date_naissance + timedelta(
        days=age_mois * 30.44  # 30.44 jours par mois en moyenne
    )

    if language == "fr":
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
    else:
        mois_noms = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
    return mois_noms[mois_cible.month - 1]


def detect_special_moments(
    df: pd.DataFrame, jour_record_existant: int, tr: Translator
) -> list[str]:
    """Détecte les moments spéciaux basés sur les pics de photos."""
    special_insights = []

    if df.empty:
        return special_insights

    # Analyser les pics de photos par jour
    photos_par_jour = df.groupby(df["date"].dt.date).size()
    moyenne_quotidienne = photos_par_jour.mean()
    seuil_pic = max(
        moyenne_quotidienne * INSIGHTS_THRESHOLDS["special_event_multiplier"],
        INSIGHTS_THRESHOLDS["special_event_min"],
    )

    pics = photos_par_jour[photos_par_jour >= seuil_pic]

    if len(pics) > 1:  # Plusieurs événements spéciaux détectés
        # Afficher quelques dates d'exemple (max 3)
        dates_exemples = sorted(pics.index)[:3]
        dates_str = ", ".join([d.strftime("%d/%m") for d in dates_exemples])
        if len(pics) > 3:
            dates_str += "..."

        special_insights.append(
            f"🎉 {len(pics)} événements spéciaux détectés ({dates_str})"
            if tr.language == "fr"
            else f"🎉 {len(pics)} special events detected ({dates_str})"
        )

        # Suggestions d'événements selon les pics
        pic_max = pics.max()
        date_pic_max = pics.idxmax()

        if pic_max >= INSIGHTS_THRESHOLDS["major_event_threshold"]:
            special_insights.append(
                f"🎊 Événement majeur le {date_pic_max.strftime('%d/%m/%Y')} - Premières vacances ? Visite famille ?"
                if tr.language == "fr"
                else f"🎊 Major event on {date_pic_max.strftime('%d/%m/%Y')} - First vacation? Family visit?"
            )
        elif pic_max >= INSIGHTS_THRESHOLDS["nice_event_threshold"]:
            special_insights.append(
                f"🎈 Belle journée le {date_pic_max.strftime('%d/%m/%Y')} - Sortie familiale ? Premier anniversaire ?"
                if tr.language == "fr"
                else f"🎈 Great day on {date_pic_max.strftime('%d/%m/%Y')} - Family outing? First birthday?"
            )

    # Détection de séries de photos
    dates_pics = sorted(pics.index)
    if len(dates_pics) >= 2:
        for i in range(1, len(dates_pics)):
            if (dates_pics[i] - dates_pics[i - 1]).days <= INSIGHTS_THRESHOLDS[
                "intensive_period_gap"
            ]:
                date_debut = dates_pics[i - 1]
                date_fin = dates_pics[i]
                special_insights.append(
                    f"🏖️ Période intensive {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')} - Vacances ou événement ?"
                    if tr.language == "fr"
                    else f"🏖️ Intensive period {date_debut.strftime('%d/%m')} - {date_fin.strftime('%d/%m')} - Vacation or event?"
                )
                break

    return special_insights


def generate_temporal_comparisons(
    df: pd.DataFrame, date_naissance: datetime, tr: Translator
) -> list[str]:
    """Génère des comparaisons temporelles."""
    comparisons = []

    if df.empty:
        return comparisons

    # 1. Comparaisons mois par mois
    photos_par_mois = df.groupby("age_mois").size()

    if len(photos_par_mois) >= 2:
        # Évolution entre premier et dernier mois
        premier_mois = photos_par_mois.index.min()
        dernier_mois = photos_par_mois.index.max()

        if dernier_mois - premier_mois >= 2:
            photos_premier = photos_par_mois.loc[premier_mois]
            photos_dernier = photos_par_mois.loc[dernier_mois]

            premier_nom = age_to_month_name(premier_mois, date_naissance, tr.language)
            dernier_nom = age_to_month_name(dernier_mois, date_naissance, tr.language)

            if photos_premier > 0:
                evolution = ((photos_dernier - photos_premier) / photos_premier) * 100
                if evolution > INSIGHTS_THRESHOLDS["evolution_significant"]:
                    comparisons.append(
                        f"📈 Évolution croissante : +{evolution:.0f}% entre {premier_nom} et {dernier_nom}"
                        if tr.language == "fr"
                        else f"📈 Growing evolution: +{evolution:.0f}% between {premier_nom} and {dernier_nom}"
                    )
                elif evolution < INSIGHTS_THRESHOLDS["evolution_decrease"]:
                    comparisons.append(
                        f"📉 Évolution : {evolution:.0f}% entre {premier_nom} et {dernier_nom}"
                        if tr.language == "fr"
                        else f"📉 Evolution: {evolution:.0f}% between {premier_nom} and {dernier_nom}"
                    )

        # Comparaison des 2 mois les plus contrastés
        if len(photos_par_mois) >= 3:
            mois_min = photos_par_mois.idxmin()
            mois_max = photos_par_mois.idxmax()
            photos_min = photos_par_mois.min()
            photos_max = photos_par_mois.max()

            mois_min_nom = age_to_month_name(mois_min, date_naissance, tr.language)
            mois_max_nom = age_to_month_name(mois_max, date_naissance, tr.language)

            if photos_min > 0 and mois_min != mois_max:
                ratio = photos_max / photos_min
                if ratio >= INSIGHTS_THRESHOLDS["contrast_ratio_min"]:
                    comparisons.append(
                        tr.t(
                            "contrast_months",
                            max_month=mois_max_nom,
                            min_month=mois_min_nom,
                            ratio=f"{ratio:.1f}",
                        )
                    )

    # 2. Comparaison week-end vs semaine
    photos_weekends = df[df["jour_semaine"].isin(["Saturday", "Sunday"])].shape[0]
    photos_semaine = df[~df["jour_semaine"].isin(["Saturday", "Sunday"])].shape[0]

    if photos_weekends > 0 and photos_semaine > 0:
        # Ratio par jour
        ratio_weekend_par_jour = photos_weekends / 2
        ratio_semaine_par_jour = photos_semaine / 5

        if ratio_semaine_par_jour > 0:
            multiplicateur = ratio_weekend_par_jour / ratio_semaine_par_jour

            if multiplicateur >= INSIGHTS_THRESHOLDS["weekend_intensity_high"]:
                comparisons.append(
                    tr.t("intense_weekend", ratio=f"{multiplicateur:.1f}")
                )
            elif multiplicateur <= INSIGHTS_THRESHOLDS["weekend_intensity_low"]:
                comparisons.append(
                    tr.t("active_weekdays", ratio=f"{1/multiplicateur:.1f}")
                )

    # 3. Tendance sur les derniers mois
    if len(photos_par_mois) >= 3:
        derniers_3_mois = photos_par_mois.tail(3)

        # Calculer la tendance
        valeurs = list(derniers_3_mois.values)
        if len(valeurs) == 3:
            tendance = (valeurs[2] - valeurs[0]) / 2
            if tendance > INSIGHTS_THRESHOLDS["trend_increase_threshold"]:
                comparisons.append(tr.t("trend_increasing"))
            elif tendance < INSIGHTS_THRESHOLDS["trend_decrease_threshold"]:
                comparisons.append(tr.t("trend_decreasing"))

    return comparisons


def generate_insights(
    df: pd.DataFrame,
    metrics: dict,
    date_naissance: datetime,
    type_fichiers: str = None,
    tr: Translator = None,
) -> list[str]:
    """Génère les messages d'insights contextuels."""
    insights = []

    if df.empty:
        if tr:
            return [tr.t("analyze_first")]
        return ["Aucune photo analysée pour le moment 📸"]

    # Protection contre tr None
    if not tr:
        tr = Translator("fr")

    # Messages encourageants adaptés au type
    if type_fichiers == "📸🎬 Photos et Vidéos":
        total = metrics.get("total_fichiers", 0)
        if total > INSIGHTS_THRESHOLDS["large_collection"]:
            insights.append(
                tr.t(
                    "magnificent_collection_mixed",
                    photos=metrics["total_photos"],
                    videos=metrics["total_videos"],
                )
            )

        # Ratio photos/vidéos
        if metrics["total_videos"] > 0:
            ratio = metrics["total_photos"] / metrics["total_videos"]
            if ratio > 5:
                insights.append(tr.t("prefer_photos"))
            elif ratio < 0.2:
                insights.append(tr.t("true_videographer"))
            elif 0.8 < ratio < 1.2:
                insights.append(tr.t("perfect_balance"))
    else:
        # Messages pour un seul type
        total = metrics.get("total_fichiers", metrics.get("total_photos", 0))
        if tr.language == "fr":
            type_nom = (
                "photos" if type_fichiers and "Photos" in type_fichiers else "vidéos"
            )
        else:
            type_nom = (
                "photos" if type_fichiers and "Photos" in type_fichiers else "videos"
            )
        type_emoji = "📸" if type_fichiers and "Photos" in type_fichiers else "🎬"

        if total > INSIGHTS_THRESHOLDS["large_collection"]:
            insights.append(tr.t("magnificent_collection", total=total, type=type_nom))
        elif total > INSIGHTS_THRESHOLDS["medium_collection"]:
            insights.append(
                f"{type_emoji} Belle collection de {total} {type_nom}!"
                if tr.language == "fr"
                else f"{type_emoji} Nice collection of {total} {type_nom}!"
            )

    # Analyse des mois les plus photographiés
    photos_par_mois = df.groupby("age_mois").size()
    if not photos_par_mois.empty:
        mois_champion = photos_par_mois.idxmax()
        nb_photos_champion = photos_par_mois.max()

        # Convertir l'âge en nom de mois calendaire
        mois_nom = age_to_month_name(mois_champion, date_naissance, tr.language)

        insights.append(
            tr.t(
                "record_period",
                start=mois_champion,
                end=mois_champion + 1,
                month=mois_nom,
                count=nb_photos_champion,
            )
        )

    # Analyse des jours de la semaine
    photos_par_jour_semaine = df.groupby("jour_semaine").size()
    if not photos_par_jour_semaine.empty:
        jour_favori = photos_par_jour_semaine.idxmax()
        if jour_favori in ["Saturday", "Sunday"]:
            insights.append(tr.t("capture_weekends"))
        elif jour_favori == "Sunday":
            insights.append(tr.t("sunday_champion"))

    # Record de photos en une journée
    if metrics["jour_record"] >= INSIGHTS_THRESHOLDS["burst_mode_threshold"]:
        # Trouver la date du record
        photos_par_jour = df.groupby(df["date"].dt.date).size()
        date_record = photos_par_jour.idxmax()

        insights.append(
            tr.t(
                "burst_mode_activated",
                count=metrics["jour_record"],
                date=date_record.strftime("%d/%m/%Y"),
            )
        )
    elif metrics["jour_record"] >= INSIGHTS_THRESHOLDS["productive_day_threshold"]:
        # Trouver la date du record
        photos_par_jour = df.groupby(df["date"].dt.date).size()
        date_record = photos_par_jour.idxmax()

        insights.append(
            tr.t(
                "productive_day",
                count=metrics["jour_record"],
                date=date_record.strftime("%d/%m/%Y"),
            )
        )

    # Analyse des gaps
    gaps = find_gaps(df)
    if gaps:
        gap_le_plus_long = max(gaps, key=lambda x: x[2])
        if gap_le_plus_long[2] >= INSIGHTS_THRESHOLDS["very_long_gap"]:
            insights.append(
                tr.t(
                    "longest_silence",
                    days=gap_le_plus_long[2],
                    start=gap_le_plus_long[0].strftime("%d/%m"),
                    end=gap_le_plus_long[1].strftime("%d/%m"),
                )
            )

    # Régularité récente
    if not df.empty:
        photos_recentes = df[
            df["date"]
            >= (datetime.now() - timedelta(days=INSIGHTS_THRESHOLDS["recent_days"]))
        ]
        if len(photos_recentes) == 0:
            insights.append(tr.t("think_recent_photos"))
        elif len(photos_recentes) >= INSIGHTS_THRESHOLDS["recent_active_threshold"]:
            insights.append(tr.t("very_active_month"))

    # Projection future
    if metrics["moyenne_par_mois"] > 0:
        projection_annuelle = metrics["moyenne_par_mois"] * 12
        insights.append(tr.t("yearly_projection", count=int(projection_annuelle)))

    # Détection de moments spéciaux
    special_moments = detect_special_moments(df, metrics["jour_record"], tr)
    insights.extend(special_moments)

    # Comparaisons temporelles
    temporal_comparisons = generate_temporal_comparisons(df, date_naissance, tr)
    insights.extend(temporal_comparisons)

    return insights


def create_charts(df: pd.DataFrame, tr: Translator) -> dict:
    """Crée tous les graphiques pour l'onglet Analytics."""
    charts = {}

    if df.empty:
        return charts

    # 1. Graphique en barres : Photos par mois d'âge
    photos_par_mois = df.groupby("age_mois").size().reset_index(name="nb_photos")
    fig_barres = px.bar(
        photos_par_mois,
        x="age_mois",
        y="nb_photos",
        title=(
            "🦖 Évolution des photos par mois d'âge"
            if tr.language == "fr"
            else "🦖 Photo evolution by age in months"
        ),
        labels={
            "age_mois": (
                "Âge du T-Rex (mois)" if tr.language == "fr" else "T-Rex age (months)"
            ),
            "nb_photos": (
                "Nombre de photos" if tr.language == "fr" else "Number of photos"
            ),
        },
        color="nb_photos",
        color_continuous_scale=BAR_CHART_GRADIENT,
    )
    fig_barres.update_layout(
        showlegend=False,
        font=dict(family="Poppins, sans-serif", color=COLORS["text_dark"]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig_barres.update_xaxes(
        title="Âge du bébé (mois)" if tr.language == "fr" else "Baby age (months)",
        gridcolor=COLORS["primary"],
    )
    fig_barres.update_yaxes(
        title="Nombre de photos" if tr.language == "fr" else "Number of photos",
        gridcolor=COLORS["primary"],
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
        title=(
            "🦖 Timeline : Activité hebdomadaire"
            if tr.language == "fr"
            else "🦖 Timeline: Weekly activity"
        ),
        labels={
            "semaine_annee": "Semaine" if tr.language == "fr" else "Week",
            "nb_photos": (
                "Nombre de photos" if tr.language == "fr" else "Number of photos"
            ),
        },
        color_discrete_sequence=[COLORS["chart_purple"]],
    )
    fig_timeline.update_layout(
        font=dict(family="Poppins, sans-serif", color=COLORS["text_dark"]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig_timeline.update_xaxes(
        tickangle=CHART_CONFIG["tick_angle"],
        title="Semaine" if tr.language == "fr" else "Week",
        gridcolor=COLORS["primary"],
    )
    fig_timeline.update_yaxes(
        title="Nombre de photos" if tr.language == "fr" else "Number of photos",
        gridcolor=COLORS["primary"],
    )
    fig_timeline.update_traces(
        line_width=CHART_CONFIG["line_width"],
        line_color=COLORS["chart_purple"],
        marker=dict(
            size=CHART_CONFIG["marker_size"],
            color=COLORS["chart_coral"],
            line=dict(
                width=CHART_CONFIG["marker_line_width"], color=COLORS["text_dark"]
            ),
        ),
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
    if tr.language == "fr":
        jours_display = [
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche",
        ]
    else:
        jours_display = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

    photos_par_jour = (
        df.groupby("jour_semaine").size().reindex(jours_ordre, fill_value=0)
    )

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=[photos_par_jour.values],
            x=jours_display,
            y=["🦖 Activité"],
            colorscale=HEATMAP_COLORSCALE,
            showscale=True,
            text=[photos_par_jour.values],
            texttemplate="%{text}",
            textfont={"size": 14, "color": COLORS["text_dark"], "family": "Poppins"},
        )
    )
    fig_heatmap.update_layout(
        title=(
            "🦖 Heatmap : Jours favoris"
            if tr.language == "fr"
            else "🦖 Heatmap: Favorite days"
        ),
        xaxis_title="Jour de la semaine" if tr.language == "fr" else "Day of the week",
        yaxis_title="",
        height=CHART_CONFIG["height_heatmap"],
        font=dict(family="Poppins, sans-serif", color=COLORS["text_dark"]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    charts["heatmap"] = fig_heatmap

    return charts


def get_gallery_data(organiseur: OrganisateurPhotos) -> dict[str, list[Path]]:
    """Obtient les photos organisées par mois pour la galerie."""
    gallery_data = {}

    # Parcourir tous les dossiers du projet
    for dossier in organiseur.dossier_racine.iterdir():
        if dossier.is_dir():
            photos = []
            for fichier in dossier.iterdir():
                if (
                    fichier.is_file()
                    and fichier.suffix.lower() in organiseur.extensions_actives
                    and organiseur.get_file_type(fichier)
                    == "photo"  # Seulement les photos pour la galerie
                ):
                    # Vérifier que c'est une photo avec une date valide
                    date_photo = organiseur.extraire_date_nom_fichier(fichier.name)
                    if date_photo and date_photo >= organiseur.date_naissance:
                        photos.append(fichier)

            if photos:
                # Utiliser le nom du dossier comme clé, ou calculer l'âge pour le dossier source
                if dossier.name == organiseur.dossier_source.name:
                    # Photos non organisées dans le dossier source
                    gallery_data["Photos non triées"] = photos
                else:
                    # Photos déjà organisées dans les dossiers mensuels
                    gallery_data[dossier.name] = photos

    return gallery_data


def get_photos_by_mode(
    gallery_data: dict[str, list[Path]],
    organiseur: OrganisateurPhotos,
    mode: str,
    selected_month: str,
    num_photos: int = 6,
) -> list[Path]:
    """Obtient les photos selon le mode sélectionné."""
    if mode == "🎲 Aléatoire" or mode == "🎲 Random":
        return get_random_photos_for_month(gallery_data, selected_month, num_photos)
    elif mode == "⏰ Chronologique" or mode == "⏰ Chronological":
        return get_chronological_photos(
            gallery_data, organiseur, selected_month, num_photos
        )
    elif mode == "📸 Moments forts" or mode == "📸 Highlights":
        return get_highlight_photos(
            gallery_data, organiseur, selected_month, num_photos
        )
    elif mode == "📈 Timeline croissance" or mode == "📈 Growth timeline":
        return get_timeline_photos(gallery_data, organiseur, num_photos)
    else:
        return get_random_photos_for_month(gallery_data, selected_month, num_photos)


def get_random_photos_for_month(
    gallery_data: dict[str, list[Path]], selected_month: str, num_photos: int = 6
) -> list[Path]:
    """Obtient un échantillon aléatoire de photos pour un mois donné."""
    if selected_month == "Tous les mois":
        # Mélanger toutes les photos de tous les mois
        all_photos = []
        for photos in gallery_data.values():
            all_photos.extend(photos)
        return (
            random.sample(all_photos, min(num_photos, len(all_photos)))
            if all_photos
            else []
        )

    photos = gallery_data.get(selected_month, [])
    return random.sample(photos, min(num_photos, len(photos))) if photos else []


def get_chronological_photos(
    gallery_data: dict[str, list[Path]],
    organiseur: OrganisateurPhotos,
    selected_month: str,
    num_photos: int = 6,
) -> list[Path]:
    """Obtient les photos triées chronologiquement (plus récent → plus ancien)."""
    if selected_month == "Tous les mois":
        # Collecter toutes les photos avec leur date
        all_photos_with_dates = []
        for photos in gallery_data.values():
            for photo in photos:
                date_photo = organiseur.extraire_date_nom_fichier(photo.name)
                if date_photo:
                    all_photos_with_dates.append((photo, date_photo))

        # Trier par date décroissante (plus récent en premier)
        all_photos_with_dates.sort(key=lambda x: x[1], reverse=True)
        return [photo for photo, _ in all_photos_with_dates[:num_photos]]

    # Pour un mois spécifique
    photos = gallery_data.get(selected_month, [])
    photos_with_dates = []
    for photo in photos:
        date_photo = organiseur.extraire_date_nom_fichier(photo.name)
        if date_photo:
            photos_with_dates.append((photo, date_photo))

    # Trier par date décroissante
    photos_with_dates.sort(key=lambda x: x[1], reverse=True)
    return [photo for photo, _ in photos_with_dates[:num_photos]]


def get_highlight_photos(
    gallery_data: dict[str, list[Path]],
    organiseur: OrganisateurPhotos,
    selected_month: str,
    num_photos: int = 6,
) -> list[Path]:
    """Obtient les photos des journées avec le plus de photos (moments forts)."""
    if selected_month == "Tous les mois":
        # Collecter toutes les photos avec leur date
        all_photos_with_dates = []
        for photos in gallery_data.values():
            for photo in photos:
                date_photo = organiseur.extraire_date_nom_fichier(photo.name)
                if date_photo:
                    all_photos_with_dates.append((photo, date_photo.date()))
    else:
        # Pour un mois spécifique
        photos = gallery_data.get(selected_month, [])
        all_photos_with_dates = []
        for photo in photos:
            date_photo = organiseur.extraire_date_nom_fichier(photo.name)
            if date_photo:
                all_photos_with_dates.append((photo, date_photo.date()))

    if not all_photos_with_dates:
        return []

    # Grouper par jour et compter les photos
    from collections import defaultdict

    photos_par_jour = defaultdict(list)
    for photo, date in all_photos_with_dates:
        photos_par_jour[date].append(photo)

    # Trier les jours par nombre de photos (moments forts)
    jours_tries = sorted(photos_par_jour.items(), key=lambda x: len(x[1]), reverse=True)

    # Sélectionner des photos des jours les plus actifs
    selected_photos = []
    for _, photos_du_jour in jours_tries:
        if len(selected_photos) >= num_photos:
            break
        # Prendre une photo aléatoire de ce jour fort
        selected_photos.append(random.choice(photos_du_jour))

    return selected_photos[:num_photos]


def get_timeline_photos(
    gallery_data: dict[str, list[Path]],
    organiseur: OrganisateurPhotos,
    num_photos: int = 6,
) -> list[Path]:
    """Obtient une photo aléatoire par mois pour montrer la timeline de croissance."""
    # Ignorer "Photos non triées" et ne prendre que les dossiers mensuels
    monthly_folders = {
        k: v for k, v in gallery_data.items() if k != "Photos non triées" and "-" in k
    }

    if not monthly_folders:
        return []

    # Fonction pour extraire le nombre du début du nom de dossier
    def extract_month_number(folder_name):
        try:
            return int(folder_name.split("-")[0])
        except:
            return 999

    # Trier les mois par ordre chronologique
    sorted_months = sorted(monthly_folders.keys(), key=extract_month_number)

    # Prendre une photo aléatoire par mois (limité par num_photos)
    timeline_photos = []
    for month in sorted_months[:num_photos]:
        month_photos = monthly_folders[month]
        if month_photos:
            timeline_photos.append(random.choice(month_photos))

    return timeline_photos


def get_photo_caption_with_age(
    photo_path: Path, organiseur: OrganisateurPhotos, tr
) -> str:
    """Génère une légende de photo avec badge d'âge."""
    # Extraire la date de la photo
    date_photo = organiseur.extraire_date_nom_fichier(photo_path.name)

    if not date_photo or date_photo < organiseur.date_naissance:
        return photo_path.name

    # Calculer l'âge en mois
    age_mois = organiseur.calculer_age_mois(date_photo)

    # Créer le badge d'âge
    if age_mois < 1:
        # Pour les photos de moins d'1 mois, afficher en jours
        age_jours = (date_photo.date() - organiseur.date_naissance.date()).days
        age_text = tr.t("age_days", age=age_jours)
    else:
        age_text = tr.t("age_months", age=age_mois)

    # Créer la légende HTML avec badge
    caption_html = f"""
    <div class="photo-caption">
        <span>{photo_path.name}</span>
        <span class="age-badge">🦖 {age_text}</span>
    </div>
    """

    return caption_html


@st.cache_data
def get_image_with_correct_orientation(image_path: str) -> Image.Image:
    """
    Charge une image en appliquant automatiquement la rotation EXIF.

    Args:
        image_path: Chemin vers l'image

    Returns:
        Image PIL avec l'orientation corrigée
    """
    try:
        # Ouvrir l'image
        image = Image.open(image_path)

        # Appliquer la rotation EXIF automatiquement
        # ImageOps.exif_transpose gère tous les cas d'orientation EXIF
        image = ImageOps.exif_transpose(image)

        return image
    except Exception as e:
        # En cas d'erreur, retourner l'image sans transformation
        print(f"Erreur lors du chargement de l'image {image_path}: {e}")
        return Image.open(image_path)
