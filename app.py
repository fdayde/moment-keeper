"""Application Streamlit pour MomentKeeper."""

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

import streamlit as st

from src.moment_keeper.analytics import (
    calculate_metrics,
    create_charts,
    extract_photo_data,
    find_gaps,
    generate_insights,
)
from src.moment_keeper.config import (
    FILE_TYPES,
    MAX_FILES_EXPANDER,
    MAX_FILES_PREVIEW,
    MAX_IGNORED_FILES_DISPLAY,
    PAGE_CONFIG,
)
from src.moment_keeper.organizer import OrganisateurPhotos
from src.moment_keeper.theme import get_css_styles
from src.moment_keeper.translations import Translator




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






def main():
    # 🦖 Configuration T-Rex Pastel
    st.set_page_config(**PAGE_CONFIG)

    # 🎨 Appliquer le CSS custom
    st.markdown(get_css_styles(), unsafe_allow_html=True)

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
            type_fichiers = FILE_TYPES["both"]
        elif photos_selected:
            type_fichiers = FILE_TYPES["photos_only"]
        elif videos_selected:
            type_fichiers = FILE_TYPES["videos_only"]
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
                        tr.t("files_reset", count=nb_fichiers)
                    )
                if erreurs:
                    st.error(tr.t("errors_encountered"))
                    for erreur in erreurs:
                        st.error(erreur)

    if dossier_racine and Path(dossier_racine).exists():
        dossier_photos_complet = Path(dossier_racine) / sous_dossier_photos
        if dossier_photos_complet.exists():
            if type_fichiers is None:
                st.error(tr.t("select_file_type"))
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
                        
                        if type_fichiers == FILE_TYPES["both"]:
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
                            if type_fichiers == FILE_TYPES["both"]:
                                # Séparer photos et vidéos
                                photos = [f for f in fichiers if organiseur.get_file_type(f) == "photo"]
                                videos = [f for f in fichiers if organiseur.get_file_type(f) == "video"]
                                
                                with st.expander(f"📁 {dossier} ({len(photos)} 📸 + {len(videos)} 🎬)"):
                                    if photos:
                                        st.write("📸 **Photos:**")
                                        for photo in photos[:MAX_FILES_EXPANDER]:
                                            st.text(f"  📸 {photo.name}")
                                        if len(photos) > MAX_FILES_EXPANDER:
                                            st.text(f"  ... et {len(photos) - MAX_FILES_EXPANDER} autres photos")
                                    
                                    if videos:
                                        st.write("🎬 **Vidéos:**")
                                        for video in videos[:MAX_FILES_EXPANDER]:
                                            st.text(f"  🎬 {video.name}")
                                        if len(videos) > MAX_FILES_EXPANDER:
                                            st.text(f"  ... et {len(videos) - MAX_FILES_EXPANDER} autres vidéos")
                            else:
                                # Affichage normal pour un seul type
                                type_emoji = "📸" if "Photos" in type_fichiers else "🎬"
                                type_nom = tr.t("photos_unit") if "Photos" in type_fichiers else tr.t("videos_unit")
                                
                                with st.expander(f"📁 {dossier} ({len(fichiers)} {type_nom})"):
                                    for fichier in fichiers[:MAX_FILES_PREVIEW]:
                                        st.text(f"  {type_emoji} {fichier.name}")
                                    if len(fichiers) > MAX_FILES_PREVIEW:
                                        st.text(tr.t("and_more", count=len(fichiers) - MAX_FILES_PREVIEW))
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
                                for nom, raison in organiseur._fichiers_ignores[:MAX_IGNORED_FILES_DISPLAY]:
                                    st.text(f"  - {nom}: {raison}")

                                if len(organiseur._fichiers_ignores) > MAX_IGNORED_FILES_DISPLAY:
                                    st.text(
                                        f"  ... et {len(organiseur._fichiers_ignores) - MAX_IGNORED_FILES_DISPLAY} autres"
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
                            if type_fichiers == FILE_TYPES["both"]:
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
                        if type_fichiers == FILE_TYPES["both"]:
                            st.metric(
                                "📸 Photos" if tr.language == "fr" else "📸 Photos",
                                metrics["total_photos"],
                                delta=(
                                    f"{metrics['total_photos'] / metrics['total_fichiers'] * 100:.0f}% du total" if tr.language == "fr"
                                    else f"{metrics['total_photos'] / metrics['total_fichiers'] * 100:.0f}% of total"
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
                        if type_fichiers == FILE_TYPES["both"]:
                            st.metric(
                                "🎬 Vidéos" if tr.language == "fr" else "🎬 Videos",
                                metrics["total_videos"],
                                delta=(
                                    f"{metrics['total_videos'] / metrics['total_fichiers'] * 100:.0f}% du total" if tr.language == "fr"
                                    else f"{metrics['total_videos'] / metrics['total_fichiers'] * 100:.0f}% of total"
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
                            st.subheader(tr.t("temporal_alerts"))
                            for gap_start, gap_end, gap_days in gaps:
                                if gap_days >= 5:
                                    st.warning(
                                        tr.t("gap_alert", days=gap_days, start=gap_start.strftime('%d/%m/%Y'), end=gap_end.strftime('%d/%m/%Y'))
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
                        st.subheader(tr.t("detailed_analysis"))

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(tr.t("monthly_distribution"))
                            photos_par_mois = df_photos.groupby("age_mois").size()
                            for mois, nb in photos_par_mois.head(5).items():
                                st.write(tr.t("months_pattern", start=mois, end=mois+1, count=nb))
                            if len(photos_par_mois) > 5:
                                st.write(
                                    tr.t("and_other_months", count=len(photos_par_mois) - 5)
                                )

                        with col2:
                            st.write(tr.t("favorite_days"))
                            if tr.language == "fr":
                                jours_map = {
                                    "Monday": "Lundi",
                                    "Tuesday": "Mardi",
                                    "Wednesday": "Mercredi",
                                    "Thursday": "Jeudi",
                                    "Friday": "Vendredi",
                                    "Saturday": "Samedi",
                                    "Sunday": "Dimanche",
                                }
                            else:
                                jours_map = {
                                    "Monday": "Monday",
                                    "Tuesday": "Tuesday",
                                    "Wednesday": "Wednesday",
                                    "Thursday": "Thursday",
                                    "Friday": "Friday",
                                    "Saturday": "Saturday",
                                    "Sunday": "Sunday",
                                }
                            photos_par_jour = (
                                df_photos.groupby("jour_semaine")
                                .size()
                                .sort_values(ascending=False)
                            )
                            for jour_en, nb in photos_par_jour.head(3).items():
                                jour_localized = jours_map.get(jour_en, jour_en)
                                st.write(tr.t("photos_count", day=jour_localized, count=nb))

                        # Suggestions d'amélioration
                        st.subheader(tr.t("suggestions"))

                        gaps = find_gaps(df_photos, min_gap_days=7)
                        if gaps:
                            st.write(tr.t("not_to_miss"))
                            st.write(tr.t("think_weekday_photos"))
                            st.write(tr.t("capture_daily_moments"))

                        if metrics["moyenne_par_mois"] < 10:
                            st.write(tr.t("enrich_memories"))
                            st.write(tr.t("more_photos_evolution"))
                            st.write(tr.t("small_moments_matter"))
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
