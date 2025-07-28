"""Application Streamlit pour MomentKeeper."""

import importlib
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

import streamlit as st

# Force reload des modules en développement
if "src.moment_keeper.analytics" in sys.modules:
    importlib.reload(sys.modules["src.moment_keeper.analytics"])
if "src.moment_keeper.translations" in sys.modules:
    importlib.reload(sys.modules["src.moment_keeper.translations"])

from src.moment_keeper import __version__
from src.moment_keeper.analytics import (
    calculate_metrics,
    create_charts,
    extract_photo_data,
    find_gaps,
    generate_insights,
    get_gallery_data,
    get_photo_caption_with_age,
    get_photos_by_mode,
)
from src.moment_keeper.config import (
    FILE_TYPES,
    GITHUB_REPO,
    MAX_FILES_EXPANDER,
    MAX_FILES_PREVIEW,
    MAX_IGNORED_FILES_DISPLAY,
    PAGE_CONFIG,
)
from src.moment_keeper.config_manager import ConfigManager
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


def save_configuration(config_manager: ConfigManager):
    """Sauvegarde la configuration actuelle."""
    config = {
        "dossier_path": st.session_state.get("dossier_path", ""),
        "sous_dossier_photos": st.session_state.get("sous_dossier_photos", "photos"),
        "language": st.session_state.get("language", "fr"),
        "baby_name": st.session_state.get("baby_name", ""),
        "photos_selected": st.session_state.get("photos_selected", True),
        "videos_selected": st.session_state.get("videos_selected", True),
    }

    # Ajouter la date de naissance si elle existe
    if "date_naissance" in st.session_state:
        config["date_naissance"] = datetime.combine(
            st.session_state.date_naissance, datetime.min.time()
        )

    config_manager.save_config(config)


def main():
    # 🦖 Configuration T-Rex Pastel
    st.set_page_config(**PAGE_CONFIG)

    # 🎨 Appliquer le CSS custom
    st.markdown(get_css_styles(), unsafe_allow_html=True)

    # Forcer l'ouverture de la sidebar au premier lancement
    if "sidebar_state" not in st.session_state:
        st.session_state.sidebar_state = "expanded"

    # Initialiser le gestionnaire de configuration
    config_manager = ConfigManager()

    # Charger la configuration sauvegardée au premier chargement
    if "config_loaded" not in st.session_state:
        saved_config = config_manager.load_config()
        if saved_config:
            st.session_state.dossier_path = saved_config.get("dossier_path", "")
            st.session_state.sous_dossier_photos = saved_config.get(
                "sous_dossier_photos", "photos"
            )
            st.session_state.language = saved_config.get("language", "fr")
            if "date_naissance" in saved_config:
                st.session_state.date_naissance = saved_config["date_naissance"]
            if "baby_name" in saved_config:
                st.session_state.baby_name = saved_config.get("baby_name", "")
            if "photos_selected" in saved_config:
                st.session_state.photos_selected = saved_config.get(
                    "photos_selected", True
                )
            if "videos_selected" in saved_config:
                st.session_state.videos_selected = saved_config.get(
                    "videos_selected", True
                )
        st.session_state.config_loaded = True

    # Initialiser la session state avec les valeurs par défaut si nécessaire
    if "dossier_path" not in st.session_state:
        st.session_state.dossier_path = ""
    if "sous_dossier_photos" not in st.session_state:
        st.session_state.sous_dossier_photos = "photos"
    if "language" not in st.session_state:
        st.session_state.language = "fr"
    if "page_loaded" not in st.session_state:
        st.session_state.page_loaded = False
    if "baby_name" not in st.session_state:
        st.session_state.baby_name = ""
    if "photos_selected" not in st.session_state:
        st.session_state.photos_selected = True
    if "videos_selected" not in st.session_state:
        st.session_state.videos_selected = True

    # Traducteur temporaire pour le header et footer
    temp_lang = st.session_state.get("language", "fr")
    temp_tr = Translator(temp_lang)

    # Le header principal sera maintenant dans l'onglet Accueil

    with st.sidebar:
        # Titre compact dans la sidebar
        st.markdown(
            "<h3 style='text-align: center;'>🦖 MomentKeeper</h3>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Initialiser le traducteur
        tr = Translator(st.session_state.language)

        st.subheader(tr.t("main_folder"))
        col1, col2 = st.columns([1, 5], gap="small")
        with col1:
            if st.button("📁", help=tr.t("browse"), key="browse_root"):
                st.session_state.page_loaded = True
                dossier_selectionne = selectionner_dossier()
                if dossier_selectionne:
                    st.session_state.dossier_path = dossier_selectionne
                    save_configuration(config_manager)
                    st.rerun()

        with col2:
            dossier_racine = st.text_input(
                tr.t("main_folder"),
                placeholder=tr.t("main_folder_placeholder"),
                value=st.session_state.dossier_path,
                label_visibility="collapsed",
                help=tr.t("main_folder_help"),
                key="dossier_racine_input",
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if dossier_racine != st.session_state.dossier_path:
                st.session_state.dossier_path = dossier_racine
                save_configuration(config_manager)

        st.subheader(tr.t("source_folder"))
        col3, col4 = st.columns([1, 5], gap="small")
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
                            save_configuration(config_manager)
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
                key="sous_dossier_input",
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if sous_dossier_photos != st.session_state.sous_dossier_photos:
                st.session_state.sous_dossier_photos = sous_dossier_photos
                save_configuration(config_manager)

        # Champ prénom du bébé
        baby_name = st.text_input(
            tr.t("baby_name"),
            placeholder=tr.t("baby_name_placeholder"),
            help="Optionnel : permet de personnaliser l'affichage",
            value=st.session_state.baby_name,
            key="baby_name_input",
        )
        if baby_name != st.session_state.baby_name:
            st.session_state.baby_name = baby_name
            save_configuration(config_manager)

        date_naissance = st.date_input(
            tr.t("birth_date"),
            min_value=datetime(2000, 1, 1).date(),
            max_value=datetime.now().date(),
            value=st.session_state.get("date_naissance", datetime.now().date()),
            key="date_naissance_input",
        )
        if date_naissance != st.session_state.get("date_naissance"):
            st.session_state.date_naissance = date_naissance
            save_configuration(config_manager)

        st.subheader(tr.t("file_types"))

        # Checkboxes pour photos et vidéos
        photos_selected = st.checkbox(
            tr.t("photos"),
            value=st.session_state.photos_selected,
            key="photos_checkbox",
        )
        if photos_selected != st.session_state.photos_selected:
            st.session_state.photos_selected = photos_selected
            save_configuration(config_manager)

        videos_selected = st.checkbox(
            tr.t("videos"),
            value=st.session_state.videos_selected,
            key="videos_checkbox",
        )
        if videos_selected != st.session_state.videos_selected:
            st.session_state.videos_selected = videos_selected
            save_configuration(config_manager)

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

        # Séparateur avant le bouton de réinitialisation
        st.markdown("---")

        if st.button(
            tr.t("reset_button"),
            help=tr.t("reset_help"),
            type="secondary",
            use_container_width=True,
        ):
            if dossier_racine and Path(dossier_racine).exists():
                organiseur = OrganisateurPhotos(
                    Path(dossier_racine),
                    sous_dossier_photos,
                    datetime.combine(date_naissance, datetime.min.time()),
                    type_fichiers,
                )
                nb_fichiers, erreurs = organiseur.reinitialiser()

                if nb_fichiers > 0:
                    st.success(tr.t("files_reset", count=nb_fichiers))
                if erreurs:
                    st.error(tr.t("errors_encountered"))
                    for erreur in erreurs:
                        st.error(erreur)

        # Séparateur avant les boutons de langue
        st.markdown("---")

        # Sélecteur de langue ultra-compact
        current_lang = st.session_state.language

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "FR",
                key="lang_fr_mini",
                type="primary" if current_lang == "fr" else "secondary",
                help="Français",
                use_container_width=True,
            ):
                if current_lang != "fr":
                    st.session_state.language = "fr"
                    save_configuration(config_manager)
                    st.rerun()

        with col2:
            if st.button(
                "EN",
                key="lang_en_mini",
                type="primary" if current_lang == "en" else "secondary",
                help="English",
                use_container_width=True,
            ):
                if current_lang != "en":
                    st.session_state.language = "en"
                    save_configuration(config_manager)
                    st.rerun()

    # Toujours afficher tous les onglets
    tab_list = [
        tr.t("tab_home"),
        tr.t("tab_simulation"),
        tr.t("tab_organization"),
        tr.t("tab_analytics"),
        tr.t("tab_insights"),
        tr.t("tab_gallery"),
    ]

    tabs = st.tabs(tab_list)

    # Onglet Accueil
    with tabs[0]:
        # 🦖 Header principal avec style T-Rex
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

        # Zone d'explication de l'application
        st.markdown(
            f"""
            <div style="background-color: #f0f8ff; padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;">
                <h3 style="color: #2C3E50; margin-bottom: 0.5rem;">🤔 {temp_tr.t("welcome_title")}</h3>
                <p style="color: #7F8C8D; margin-bottom: 0.8rem;">{temp_tr.t("welcome_description")}</p>
                <ul style="color: #7F8C8D; margin-left: 1.5rem;">
                    <li>{temp_tr.t("welcome_feature_1")}</li>
                    <li>{temp_tr.t("welcome_feature_2")}</li>
                    <li>{temp_tr.t("welcome_feature_3")}</li>
                    <li>{temp_tr.t("welcome_feature_4")}</li>
                    <li>{temp_tr.t("welcome_feature_5")}</li>
                </ul>
            </div>

            <div style="background-color: #e8f4f8; padding: 1.2rem; border-radius: 10px; margin-top: 1rem;">
                <h4 style="color: #2C3E50; margin-bottom: 0.8rem;">{temp_tr.t("welcome_steps_title")}</h4>
                <div style="color: #7F8C8D; line-height: 1.8;">
                    <p style="margin: 0.3rem 0;">{temp_tr.t("welcome_step_1")}</p>
                    <p style="margin: 0.3rem 0;">{temp_tr.t("welcome_step_2")}</p>
                    <p style="margin: 0.3rem 0;">{temp_tr.t("welcome_step_3")}</p>
                    <p style="margin: 0.3rem 0;">{temp_tr.t("welcome_step_4")}</p>
                    <p style="margin: 0.3rem 0;">{temp_tr.t("welcome_step_5")}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not dossier_racine:
            st.info(tr.t("configure_root"))
        elif not Path(dossier_racine).exists():
            st.error(tr.t("root_not_exist"))
        elif not (Path(dossier_racine) / sous_dossier_photos).exists():
            st.error(
                tr.t(
                    "folder_not_exist",
                    folder=sous_dossier_photos,
                    root=dossier_racine,
                )
            )
        elif type_fichiers is None:
            st.error(tr.t("select_file_type"))

        # Vérifier si la configuration est complète
        config_complete = (
            dossier_racine
            and Path(dossier_racine).exists()
            and (Path(dossier_racine) / sous_dossier_photos).exists()
            and type_fichiers is not None
        )

        if config_complete:
            organiseur = OrganisateurPhotos(
                Path(dossier_racine),
                sous_dossier_photos,
                datetime.combine(date_naissance, datetime.min.time()),
                type_fichiers,
            )

        with tabs[1]:
            st.markdown(
                f'<div class="trex-message">{tr.t("simulation_title")}</div>',
                unsafe_allow_html=True,
            )

            if not config_complete:
                st.info(tr.t("configure_settings_first"))
            else:
                if st.button(tr.t("analyze_button")):
                    # Marquer la page comme chargée après la première interaction
                    st.session_state.page_loaded = True
                    with st.spinner(tr.t("analyzing")):
                        repartition, erreurs = organiseur.simuler_organisation()

                    if repartition:
                        total_photos = sum(len(f) for f in repartition.values())

                        if type_fichiers == FILE_TYPES["both"]:
                            # Compter photos et vidéos séparément
                            total_photos_count = sum(
                                len(
                                    [
                                        f
                                        for f in fichiers
                                        if organiseur.get_file_type(f) == "photo"
                                    ]
                                )
                                for fichiers in repartition.values()
                            )
                            total_videos_count = sum(
                                len(
                                    [
                                        f
                                        for f in fichiers
                                        if organiseur.get_file_type(f) == "video"
                                    ]
                                )
                                for fichiers in repartition.values()
                            )
                            message = tr.t(
                                "success_simulation_mixed",
                                photos=total_photos_count,
                                videos=total_videos_count,
                            )
                        elif "Photos" in type_fichiers:
                            message = tr.t("success_simulation", photos=total_photos)
                        else:
                            message = tr.t("success_simulation", photos=total_photos)

                        st.markdown(
                            f'<div class="trex-success">{message}</div>',
                            unsafe_allow_html=True,
                        )

                        # Fonction pour extraire le nombre du début du nom de dossier
                        def extract_month_number(folder_name):
                            # Extrait le premier nombre du nom du dossier (ex: "0-1months" -> 0)
                            try:
                                return int(folder_name.split("-")[0])
                            except:
                                return 999  # Valeur par défaut pour les dossiers non standards

                        for dossier, fichiers in sorted(
                            repartition.items(),
                            key=lambda x: extract_month_number(x[0]),
                        ):
                            if type_fichiers == FILE_TYPES["both"]:
                                # Séparer photos et vidéos
                                photos = [
                                    f
                                    for f in fichiers
                                    if organiseur.get_file_type(f) == "photo"
                                ]
                                videos = [
                                    f
                                    for f in fichiers
                                    if organiseur.get_file_type(f) == "video"
                                ]

                                with st.expander(
                                    f"📁 {dossier} ({len(photos)} 📸 + {len(videos)} 🎬)"
                                ):
                                    if photos:
                                        st.write("📸 **Photos:**")
                                        for photo in photos[:MAX_FILES_EXPANDER]:
                                            st.text(f"  📸 {photo.name}")
                                        if len(photos) > MAX_FILES_EXPANDER:
                                            st.text(
                                                f"  ... et {len(photos) - MAX_FILES_EXPANDER} autres photos"
                                            )

                                    if videos:
                                        st.write("🎬 **Vidéos:**")
                                        for video in videos[:MAX_FILES_EXPANDER]:
                                            st.text(f"  🎬 {video.name}")
                                        if len(videos) > MAX_FILES_EXPANDER:
                                            st.text(
                                                f"  ... et {len(videos) - MAX_FILES_EXPANDER} autres vidéos"
                                            )
                            else:
                                # Affichage normal pour un seul type
                                type_emoji = "📸" if "Photos" in type_fichiers else "🎬"
                                type_nom = (
                                    tr.t("photos_unit")
                                    if "Photos" in type_fichiers
                                    else tr.t("videos_unit")
                                )

                                with st.expander(
                                    f"📁 {dossier} ({len(fichiers)} {type_nom})"
                                ):
                                    for fichier in fichiers[:MAX_FILES_PREVIEW]:
                                        st.text(f"  {type_emoji} {fichier.name}")
                                    if len(fichiers) > MAX_FILES_PREVIEW:
                                        st.text(
                                            tr.t(
                                                "and_more",
                                                count=len(fichiers) - MAX_FILES_PREVIEW,
                                            )
                                        )
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
                                for nom, raison in organiseur._fichiers_ignores[
                                    :MAX_IGNORED_FILES_DISPLAY
                                ]:
                                    st.text(f"  - {nom}: {raison}")

                                if (
                                    len(organiseur._fichiers_ignores)
                                    > MAX_IGNORED_FILES_DISPLAY
                                ):
                                    st.text(
                                        f"  ... et {len(organiseur._fichiers_ignores) - MAX_IGNORED_FILES_DISPLAY} autres"
                                    )

                    if erreurs:
                        st.warning(tr.t("warnings"))
                        for erreur in erreurs:
                            st.warning(erreur)

        with tabs[2]:
            st.markdown(
                f'<div class="trex-message">{tr.t("organization_title")}</div>',
                unsafe_allow_html=True,
            )

            if not config_complete:
                st.info(tr.t("configure_settings_first"))
            else:
                st.markdown(
                    f'<div class="trex-warning">{tr.t("organization_warning")}</div>',
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)
                with col1:
                    type_text = (
                        tr.t("photos_unit")
                        if "Photos" in type_fichiers
                        else (
                            tr.t("videos_unit")
                            if "Vidéos" in type_fichiers
                            else tr.t("files_unit")
                        )
                    )
                    confirmer = st.checkbox(tr.t("confirm_organize", type=type_text))

                with col2:
                    if st.button(tr.t("organize_button"), disabled=not confirmer):
                        st.session_state.page_loaded = True
                        with st.spinner(tr.t("organizing")):
                            nb_fichiers, erreurs = organiseur.organiser()

                        if nb_fichiers > 0:
                            if type_fichiers == FILE_TYPES["both"]:
                                type_text = tr.t("files_unit")
                            elif "Photos" in type_fichiers:
                                type_text = tr.t("photos_unit")
                            else:
                                type_text = tr.t("videos_unit")

                            message = tr.t(
                                "success_organize", count=nb_fichiers, type=type_text
                            )
                            st.markdown(
                                f'<div class="trex-success">{message}</div>',
                                unsafe_allow_html=True,
                            )

                        if erreurs:
                            st.error(tr.t("errors_occurred"))
                            for erreur in erreurs:
                                st.error(erreur)

        with tabs[3]:
            st.markdown(
                f'<div class="trex-message">{tr.t("analytics_title")}</div>',
                unsafe_allow_html=True,
            )

            if not config_complete:
                st.info(tr.t("configure_settings_first"))
            else:
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
                                    f"{metrics['total_photos'] / metrics['total_fichiers'] * 100:.0f}% du total"
                                    if tr.language == "fr"
                                    else (
                                        f"{metrics['total_photos'] / metrics['total_fichiers'] * 100:.0f}% of total"
                                        if metrics["total_fichiers"] > 0
                                        else None
                                    )
                                ),
                            )
                        else:
                            label = (
                                tr.t("photos_kept")
                                if "Photos" in type_fichiers
                                else tr.t("videos_kept")
                            )
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
                                    f"{metrics['total_videos'] / metrics['total_fichiers'] * 100:.0f}% du total"
                                    if tr.language == "fr"
                                    else (
                                        f"{metrics['total_videos'] / metrics['total_fichiers'] * 100:.0f}% of total"
                                        if metrics["total_fichiers"] > 0
                                        else None
                                    )
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
                                        tr.t(
                                            "gap_alert",
                                            days=gap_days,
                                            start=gap_start.strftime("%d/%m/%Y"),
                                            end=gap_end.strftime("%d/%m/%Y"),
                                        )
                                    )

        with tabs[4]:
            st.markdown(
                f'<div class="trex-message">{tr.t("insights_title")}</div>',
                unsafe_allow_html=True,
            )

            if not config_complete:
                st.info(tr.t("configure_settings_first"))
            else:
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
                                st.write(
                                    tr.t(
                                        "months_pattern",
                                        start=mois,
                                        end=mois + 1,
                                        count=nb,
                                    )
                                )
                            if len(photos_par_mois) > 5:
                                st.write(
                                    tr.t(
                                        "and_other_months",
                                        count=len(photos_par_mois) - 5,
                                    )
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
                                st.write(
                                    tr.t("photos_count", day=jour_localized, count=nb)
                                )

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

        with tabs[5]:
            st.markdown(
                f'<div class="trex-message">{tr.t("gallery_title")}</div>',
                unsafe_allow_html=True,
            )

            if not config_complete:
                st.info(tr.t("configure_settings_first"))
            else:
                # Obtenir les données de la galerie
                with st.spinner(tr.t("searching_data")):
                    gallery_data = get_gallery_data(organiseur)

                if not gallery_data:
                    st.info(tr.t("no_photos_month"))
                else:
                    # Contrôles de l'interface
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

                    with col1:
                        # Fonction pour extraire le nombre du début du nom de dossier
                        def extract_month_number(folder_name):
                            try:
                                return int(folder_name.split("-")[0])
                            except:
                                return 999  # Pour "Photos non triées" et autres

                        # Trier les mois disponibles
                        months_available = ["Tous les mois"] + sorted(
                            gallery_data.keys(), key=extract_month_number
                        )

                        selected_month = st.selectbox(
                            tr.t("select_month"), months_available, index=0
                        )

                    with col2:
                        # Sélecteur de mode d'affichage
                        view_modes = [
                            tr.t("mode_random"),
                            tr.t("mode_chronological"),
                            tr.t("mode_highlights"),
                            tr.t("mode_timeline"),
                        ]

                        view_mode = st.selectbox(
                            tr.t("view_mode"),
                            view_modes,
                            index=0,
                            help=tr.t("view_mode_help"),
                        )

                    with col3:
                        # Calculer l'âge actuel du bébé pour définir le max
                        age_actuel_mois = organiseur.calculer_age_mois(datetime.now())
                        max_photos = max(
                            6, age_actuel_mois
                        )  # Minimum 6 pour les très jeunes bébés

                        num_photos = st.slider(
                            tr.t("photos_to_show"),
                            min_value=1,
                            max_value=max_photos,
                            value=min(6, max_photos),
                            step=1,
                        )

                    with col4:
                        if st.button(tr.t("refresh_gallery"), type="secondary"):
                            st.rerun()

                    # Afficher le nombre de photos trouvées
                    if view_mode == tr.t("mode_timeline"):
                        # Pour le mode timeline, afficher le nombre de mois disponibles
                        monthly_folders = {
                            k: v
                            for k, v in gallery_data.items()
                            if k != "Photos non triées" and "-" in k
                        }
                        if baby_name.strip():
                            message = tr.t(
                                "months_growth_available",
                                count=len(monthly_folders),
                                name=baby_name.strip(),
                            )
                            st.info(f"📈 {message}")
                        else:
                            message = tr.t(
                                "months_growth_available_no_name",
                                count=len(monthly_folders),
                            )
                            st.info(f"📈 {message}")
                    elif selected_month == "Tous les mois":
                        total_photos = sum(
                            len(photos) for photos in gallery_data.values()
                        )
                        if baby_name.strip():
                            message = tr.t(
                                "photos_found_with_name",
                                count=total_photos,
                                name=baby_name.strip(),
                            )
                            st.info(message)
                        else:
                            st.info(tr.t("photos_found", count=total_photos))
                    else:
                        month_photos = len(gallery_data.get(selected_month, []))
                        if baby_name.strip():
                            message = tr.t(
                                "photos_found_with_name",
                                count=month_photos,
                                name=baby_name.strip(),
                            )
                            st.info(message)
                        else:
                            st.info(tr.t("photos_found", count=month_photos))

                    # Obtenir et afficher les photos selon le mode sélectionné
                    selected_photos = get_photos_by_mode(
                        gallery_data, organiseur, view_mode, selected_month, num_photos
                    )

                    if selected_photos:
                        # Afficher les photos in une grille
                        cols_per_row = 3
                        rows = [
                            selected_photos[i : i + cols_per_row]
                            for i in range(0, len(selected_photos), cols_per_row)
                        ]

                        for row in rows:
                            cols = st.columns(cols_per_row)
                            for idx, photo_path in enumerate(row):
                                with cols[idx]:
                                    try:
                                        # Afficher l'image sans caption par défaut
                                        st.image(
                                            str(photo_path),
                                            use_container_width=True,
                                        )
                                        # Afficher la légende personnalisée avec badge d'âge
                                        caption_html = get_photo_caption_with_age(
                                            photo_path, organiseur, tr
                                        )
                                        st.markdown(
                                            caption_html, unsafe_allow_html=True
                                        )
                                    except Exception as e:
                                        st.error(
                                            f"Erreur lors du chargement de {photo_path.name}: {str(e)}"
                                        )

                            # Remplir les colonnes vides s'il y en a moins que cols_per_row
                            for idx in range(len(row), cols_per_row):
                                with cols[idx]:
                                    st.empty()

                            # Ajouter un espace entre les rangées
                            st.markdown(
                                "<div style='margin-bottom: 1rem;'></div>",
                                unsafe_allow_html=True,
                            )
                    else:
                        st.warning(tr.t("no_photos_month"))

    # 🦖 Footer T-Rex avec personnalité
    st.markdown(
        f"""
        <div class="trex-footer">
            <p><a href="{GITHUB_REPO}" target="_blank">MomentKeeper 🦖</a> • v{__version__} • <a href="{GITHUB_REPO}" target="_blank">GitHub</a></p>
            <p>{temp_tr.t("footer_new_tagline")}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
