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
    """Extrait les données des photos en réutilisant les méthodes existantes."""
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


def generate_insights(df: pd.DataFrame, metrics: Dict) -> List[str]:
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
        insights.append(
            f"🏆 Période record : {mois_champion}-{mois_champion+1} mois avec {nb_photos_champion} photos!"
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
        insights.append(
            f"📸 Mode rafale activé ! Record : {metrics['jour_record']} photos en une journée!"
        )
    elif metrics["jour_record"] >= 5:
        insights.append(f"📷 Journée productive : {metrics['jour_record']} photos!")

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

    return insights


def create_charts(df: pd.DataFrame):
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
        title="📊 Nombre de photos par mois d'âge",
        labels={"age_mois": "Âge (mois)", "nb_photos": "Nombre de photos"},
        color="nb_photos",
        color_continuous_scale="Viridis",
    )
    fig_barres.update_layout(showlegend=False)
    fig_barres.update_xaxes(title="Âge du bébé (mois)")
    fig_barres.update_yaxes(title="Nombre de photos")
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
        title="📈 Évolution hebdomadaire du nombre de photos",
        labels={"semaine_annee": "Semaine", "nb_photos": "Nombre de photos"},
    )
    fig_timeline.update_xaxes(tickangle=45, title="Semaine")
    fig_timeline.update_yaxes(title="Nombre de photos")
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

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=[photos_par_jour.values],
            x=jours_fr,
            y=["Photos"],
            colorscale="Viridis",
            showscale=True,
            text=[photos_par_jour.values],
            texttemplate="%{text}",
            textfont={"size": 14},
        )
    )
    fig_heatmap.update_layout(
        title="🗓️ Répartition des photos par jour de la semaine",
        xaxis_title="Jour de la semaine",
        yaxis_title="",
        height=200,
    )
    charts["heatmap"] = fig_heatmap

    return charts


def main():
    st.set_page_config(page_title="MomentKeeper", page_icon="🦖", layout="wide")

    st.title("🦖🍼 MomentKeeper - Organisateur de Photos")
    st.markdown("Organisez automatiquement vos photos par mois depuis la naissance")

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
                ["📋 Simulation", "🚀 Organisation", "📊 Analytics", "💡 Insights"]
            )

            with tab1:
                st.header("Simulation de l'organisation")

                if st.button("🔍 Analyser les photos"):
                    with st.spinner("Analyse en cours..."):
                        repartition, erreurs = organiseur.simuler_organisation()

                    if repartition:
                        st.success(
                            f"✅ {sum(len(f) for f in repartition.values())} photos analysées"
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
                st.header("Organisation réelle")
                st.warning("⚠️ Cette action déplacera réellement vos fichiers!")

                col1, col2 = st.columns(2)
                with col1:
                    confirmer = st.checkbox("Je confirme vouloir organiser mes photos")

                with col2:
                    if st.button("🚀 Organiser", disabled=not confirmer):
                        with st.spinner("Organisation en cours..."):
                            nb_fichiers, erreurs = organiseur.organiser()

                        if nb_fichiers > 0:
                            st.success(
                                f"✅ {nb_fichiers} photos organisées avec succès!"
                            )

                        if erreurs:
                            st.error("❌ Erreurs rencontrées:")
                            for erreur in erreurs:
                                st.error(erreur)

            with tab3:
                st.header("📊 Analytics - Métriques et Graphiques")

                # Extraire les données des photos
                with st.spinner("Analyse des photos en cours..."):
                    df_photos = extract_photo_data(organiseur)
                    metrics = calculate_metrics(df_photos)

                if df_photos.empty:
                    st.info("ℹ️ Aucune photo trouvée pour l'analyse")
                else:
                    # Métriques principales en colonnes (3x2 layout)
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("📸 Photos totales", metrics["total_photos"])
                        st.metric(
                            "📅 Dernière photo",
                            (
                                metrics["derniere_photo"].strftime("%d/%m/%Y")
                                if metrics["derniere_photo"]
                                else "N/A"
                            ),
                        )

                    with col2:
                        st.metric(
                            "🗓️ Période couverte", f"{metrics['periode_couverte']} mois"
                        )
                        st.metric("🏆 Jour record", f"{metrics['jour_record']} photos")

                    with col3:
                        st.metric(
                            "📈 Moyenne/mois", f"{metrics['moyenne_par_mois']:.1f}"
                        )
                        st.metric("⏱️ Plus long gap", f"{metrics['max_gap']} jours")

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
                st.header("💡 Insights - Découvertes et Messages")

                # Réutiliser les données déjà extraites si possible
                if "df_photos" not in locals():
                    with st.spinner("Analyse des photos en cours..."):
                        df_photos = extract_photo_data(organiseur)
                        metrics = calculate_metrics(df_photos)

                # Messages d'insights
                insights = generate_insights(df_photos, metrics)

                if insights:
                    st.subheader("🎯 Découvertes principales")
                    for insight in insights:
                        st.info(insight)

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


if __name__ == "__main__":
    main()
