"""Application Streamlit pour MomentKeeper."""

import base64
import re
import tkinter as tk
from datetime import datetime
from io import BytesIO
from pathlib import Path
from tkinter import filedialog

import streamlit as st

from src.moment_keeper import __version__
from src.moment_keeper.analytics import (
    calculate_metrics,
    create_charts,
    find_gaps,
    generate_insights,
    get_gallery_data_cached,
    get_image_with_correct_orientation,
    get_photo_caption_with_age,
    get_photo_data_cached,
    get_photos_by_mode,
    photos_grouped_by_age,
)
from src.moment_keeper.config import (
    ALL_MONTHS_SENTINEL,
    FILE_TYPES,
    GALLERY_MODES,
    GITHUB_REPO,
    MAX_FILES_EXPANDER,
    MAX_FILES_PREVIEW,
    MAX_IGNORED_FILES_DISPLAY,
    PAGE_CONFIG,
    UNSORTED_SENTINEL,
    includes_photos,
    is_both,
)
from src.moment_keeper.config_manager import ConfigManager
from src.moment_keeper.organizer import OrganisateurPhotos
from src.moment_keeper.theme import get_css_styles
from src.moment_keeper.translations import Translator
from src.moment_keeper.utils import extract_month_number

_MONTH_FOLDER_RE = re.compile(r"^(\d+)-(\d+)months$")


def selectionner_dossier():
    """Ouvre une fenêtre de sélection de dossier avec gestion d'erreur robuste."""
    try:
        import queue
        import threading

        # Utiliser une queue pour récupérer le résultat du thread
        result_queue = queue.Queue()

        def _select_folder():
            try:
                root = tk.Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                dossier = filedialog.askdirectory(
                    title="Sélectionnez le dossier contenant vos photos"
                )
                root.destroy()
                result_queue.put(dossier if dossier else "")
            except Exception as e:
                result_queue.put(f"ERROR:{str(e)}")

        # Exécuter dans un thread séparé pour éviter les conflits avec Streamlit
        thread = threading.Thread(target=_select_folder)
        thread.start()
        # 60s : couvre la lenteur des gros dossiers (miniatures vidéos, disques externes)
        # tout en gardant un garde-fou si Tk se bloque vraiment.
        thread.join(timeout=60)

        if thread.is_alive():
            # Le thread n'a pas fini dans le temps imparti
            return "TIMEOUT"

        # Récupérer le résultat
        try:
            result = result_queue.get_nowait()
            if result.startswith("ERROR:"):
                return result
            return result if result else None
        except queue.Empty:
            return "EMPTY"

    except Exception as e:
        # Erreur lors de l'import ou autre problème
        return f"ERROR:{str(e)}"


def _open_reset_dialog(
    racine_str: str,
    sous_dossier: str,
    date_naissance_iso: str,
    type_fichiers: str,
) -> None:
    """Ouvre un modal de confirmation et exécute le reset si confirmé.

    Les arguments sont des primitives (str, iso) pour éviter les soucis de
    sérialisation avec Streamlit lors de l'ouverture du modal.
    """
    tr_dlg = Translator(st.session_state.get("language", "fr"))

    @st.dialog(tr_dlg.t("reset_dialog_title"))
    def _dialog():
        st.write(tr_dlg.t("reset_dialog_body"))
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(
                "✕ " + tr_dlg.t("cancel"),
                key="reset_dlg_cancel",
                width="stretch",
            ):
                st.rerun()
        with col_b:
            if st.button(
                "⚠️ " + tr_dlg.t("confirm_reset"),
                key="reset_dlg_confirm",
                type="primary",
                width="stretch",
            ):
                organiseur = OrganisateurPhotos(
                    Path(racine_str),
                    sous_dossier,
                    datetime.fromisoformat(date_naissance_iso),
                    type_fichiers,
                )
                nb_fichiers, erreurs = organiseur.reinitialiser()
                st.session_state["reset_result"] = (nb_fichiers, erreurs)
                st.rerun()

    _dialog()


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

        col1, col2 = st.columns([1, 8])
        with col1:
            if st.button("📁", help=tr.t("browse"), key="browse_root", width="stretch"):
                st.session_state.page_loaded = True
                with st.spinner(tr.t("opening_folder_dialog")):
                    dossier_selectionne = selectionner_dossier()

                if dossier_selectionne:
                    if dossier_selectionne.startswith("ERROR:"):
                        st.session_state.root_folder_messages = [
                            (
                                "error",
                                "❌ "
                                + tr.t("folder_selection_error")
                                + f" ({dossier_selectionne[6:]})",
                            ),
                            ("info", "💡 " + tr.t("folder_selection_tip")),
                        ]
                        st.rerun()
                    elif dossier_selectionne == "TIMEOUT":
                        st.session_state.root_folder_messages = [
                            ("warning", "⏱️ " + tr.t("folder_selection_timeout")),
                            ("info", "💡 " + tr.t("folder_selection_tip")),
                        ]
                        st.rerun()
                    elif dossier_selectionne == "EMPTY":
                        st.session_state.root_folder_messages = [
                            ("warning", "⚠️ " + tr.t("folder_selection_cancelled"))
                        ]
                        st.rerun()
                    else:
                        st.session_state.dossier_path = dossier_selectionne
                        st.session_state.root_folder_messages = []  # Effacer les anciens messages
                        save_configuration(config_manager)
                        st.rerun()

        with col2:
            dossier_racine = st.text_input(
                tr.t("main_folder"),
                placeholder=tr.t("main_folder_placeholder"),
                value=st.session_state.dossier_path,
                label_visibility="collapsed",
                help=tr.t("main_folder_help"),
            )
            # Mettre à jour la session state si l'utilisateur tape directement
            if dossier_racine != st.session_state.dossier_path:
                st.session_state.dossier_path = dossier_racine
                # Réinitialiser le sous-dossier si on change de racine
                if dossier_racine and Path(dossier_racine).exists():
                    # Vérifier si l'ancien sous-dossier existe dans le nouveau dossier
                    nouveau_chemin_photos = (
                        Path(dossier_racine) / st.session_state.sous_dossier_photos
                    )
                    if not nouveau_chemin_photos.exists():
                        # Réinitialiser à "photos" par défaut
                        st.session_state.sous_dossier_photos = "photos"
                save_configuration(config_manager)

        # Afficher les messages du dossier racine en dehors des colonnes
        if (
            "root_folder_messages" in st.session_state
            and st.session_state.root_folder_messages
        ):
            for msg_type, msg_text in st.session_state.root_folder_messages:
                if msg_type == "error":
                    st.error(msg_text)
                elif msg_type == "warning":
                    st.warning(msg_text)
                elif msg_type == "info":
                    st.info(msg_text)
            # Effacer les messages après affichage pour éviter qu'ils persistent
            st.session_state.root_folder_messages = []

        st.subheader(tr.t("source_folder"))

        col3, col4 = st.columns([1, 8])
        with col3:
            if st.button(
                "📁",
                help=tr.t("browse_subfolder"),
                key="browse_sub",
                width="stretch",
            ):
                if dossier_racine and Path(dossier_racine).exists():
                    with st.spinner(tr.t("opening_folder_dialog")):
                        dossier_selectionne = selectionner_dossier()
                    if dossier_selectionne:
                        if dossier_selectionne.startswith("ERROR:"):
                            st.session_state.subfolder_messages = [
                                (
                                    "error",
                                    "❌ "
                                    + tr.t("folder_selection_error")
                                    + f" ({dossier_selectionne[6:]})",
                                ),
                                ("info", "💡 " + tr.t("folder_selection_tip")),
                            ]
                            st.rerun()
                        elif dossier_selectionne == "TIMEOUT":
                            st.session_state.subfolder_messages = [
                                ("warning", "⏱️ " + tr.t("folder_selection_timeout")),
                                ("info", "💡 " + tr.t("folder_selection_tip")),
                            ]
                            st.rerun()
                        elif dossier_selectionne == "EMPTY":
                            st.session_state.subfolder_messages = [
                                ("warning", "⚠️ " + tr.t("folder_selection_cancelled"))
                            ]
                            st.rerun()
                        else:
                            # Extraire seulement le nom du sous-dossier relatif au dossier principal
                            try:
                                chemin_relatif = Path(dossier_selectionne).relative_to(
                                    Path(dossier_racine)
                                )
                                st.session_state.sous_dossier_photos = str(
                                    chemin_relatif
                                )
                                st.session_state.subfolder_messages = []  # Effacer les anciens messages
                                save_configuration(config_manager)
                                st.rerun()
                            except ValueError:
                                st.session_state.subfolder_messages = [
                                    ("error", tr.t("folder_must_be_in_root"))
                                ]
                                st.rerun()
                else:
                    st.session_state.subfolder_messages = [
                        ("error", "⚠️ " + tr.t("select_root_first"))
                    ]
                    st.rerun()

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
                save_configuration(config_manager)

        # Afficher les messages du sous-dossier en dehors des colonnes
        if (
            "subfolder_messages" in st.session_state
            and st.session_state.subfolder_messages
        ):
            for msg_type, msg_text in st.session_state.subfolder_messages:
                if msg_type == "error":
                    st.error(msg_text)
                elif msg_type == "warning":
                    st.warning(msg_text)
                elif msg_type == "info":
                    st.info(msg_text)
            # Effacer les messages après affichage pour éviter qu'ils persistent
            st.session_state.subfolder_messages = []

        # Champ prénom du bébé
        baby_name = st.text_input(
            tr.t("baby_name"),
            placeholder=tr.t("baby_name_placeholder"),
            help="Optionnel : permet de personnaliser l'affichage",
            value=st.session_state.baby_name,
        )
        if baby_name != st.session_state.baby_name:
            st.session_state.baby_name = baby_name
            save_configuration(config_manager)

        date_naissance = st.date_input(
            tr.t("birth_date"),
            min_value=datetime(1980, 1, 1).date(),
            max_value=datetime.now().date(),
            value=st.session_state.get("date_naissance", datetime.now().date()),
        )
        if date_naissance != st.session_state.get("date_naissance"):
            st.session_state.date_naissance = date_naissance
            save_configuration(config_manager)

        st.subheader(tr.t("file_types"))

        # Checkboxes pour photos et vidéos
        photos_selected = st.checkbox(
            tr.t("photos"),
            value=st.session_state.photos_selected,
        )
        if photos_selected != st.session_state.photos_selected:
            st.session_state.photos_selected = photos_selected
            save_configuration(config_manager)

        videos_selected = st.checkbox(
            tr.t("videos"),
            value=st.session_state.videos_selected,
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
            width="stretch",
        ):
            if dossier_racine and Path(dossier_racine).exists():
                date_dt = datetime.combine(date_naissance, datetime.min.time())
                _open_reset_dialog(
                    dossier_racine,
                    sous_dossier_photos,
                    date_dt.isoformat(),
                    type_fichiers,
                )

        # Résultat affiché après fermeture du modal
        if "reset_result" in st.session_state:
            nb_fichiers, erreurs = st.session_state.pop("reset_result")
            if nb_fichiers > 0:
                st.success(tr.t("files_reset", count=nb_fichiers))
            if erreurs:
                st.error(tr.t("errors_encountered"))
                for erreur in erreurs:
                    st.error(erreur)

        # Bouton pour charger la configuration de test
        if st.button(
            "🦖 " + tr.t("load_test_config"),
            help=tr.t("load_test_config_help"),
            type="secondary",
            width="stretch",
        ):
            test_config_path = (
                Path(__file__).parent
                / "data"
                / "user-config"
                / "test"
                / "test_config.json"
            )
            if test_config_path.exists():
                # Charger directement le fichier JSON de test
                import json

                with open(test_config_path, encoding="utf-8") as f:
                    test_config = json.load(f)
                if test_config:
                    # Résoudre les chemins relatifs par rapport au répertoire du projet
                    project_root = Path(__file__).parent
                    dossier_path = test_config.get("dossier_path", "")
                    if dossier_path and not Path(dossier_path).is_absolute():
                        dossier_path = str(project_root / dossier_path)

                    # Créer la configuration de test complète
                    test_config_to_save = {
                        "dossier_path": dossier_path,
                        "sous_dossier_photos": test_config.get(
                            "sous_dossier_photos", "photos"
                        ),
                        "language": test_config.get("language", "fr"),
                        "baby_name": test_config.get("baby_name", "TestRex"),
                        "photos_selected": test_config.get("photos_selected", True),
                        "videos_selected": test_config.get("videos_selected", True),
                    }

                    if "date_naissance" in test_config:
                        test_config_to_save["date_naissance"] = datetime.combine(
                            datetime.fromisoformat(
                                test_config["date_naissance"]
                            ).date(),
                            datetime.min.time(),
                        )

                    # Sauvegarder directement la config sur disque
                    config_manager.save_config(test_config_to_save)

                    # Marquer qu'on vient de charger la config de test
                    st.session_state.test_config_just_loaded = True
                    st.rerun()
            else:
                st.error(tr.t("test_config_not_found"))

        # Afficher le message de succès si la config de test vient d'être chargée
        if st.session_state.get("test_config_just_loaded", False):
            st.success("✅ " + tr.t("test_config_loaded"))
            st.info(
                "🔄 Rechargez la page (F5 ou Ctrl+R) pour appliquer tous les changements."
            )
            st.session_state.test_config_just_loaded = False  # Réinitialiser le flag

        # Sélecteur de langue ultra-compact
        current_lang = st.session_state.language

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "FR",
                key="lang_fr_mini",
                type="primary" if current_lang == "fr" else "secondary",
                help="Français",
                width="stretch",
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
                width="stretch",
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
            and date_naissance is not None
        )

        if config_complete:
            # Valider que les chemins existent avant de créer l'organisateur
            try:
                chemin_racine = Path(dossier_racine)
                chemin_photos = chemin_racine / sous_dossier_photos

                if not chemin_racine.exists():
                    st.error(f"Le dossier racine n'existe pas : {dossier_racine}")
                    config_complete = False
                elif not chemin_photos.exists():
                    st.error(f"Le dossier source n'existe pas : {chemin_photos}")
                    config_complete = False
                else:
                    organiseur = OrganisateurPhotos(
                        chemin_racine,
                        sous_dossier_photos,
                        datetime.combine(date_naissance, datetime.min.time()),
                        type_fichiers,
                    )
            except Exception as e:
                st.error(f"Erreur lors de la validation des chemins : {str(e)}")
                config_complete = False

    with tabs[1]:
        st.markdown(
            f'<div class="trex-message">{tr.t("simulation_title")}</div>',
            unsafe_allow_html=True,
        )

        if not config_complete:
            st.caption(tr.t("config_needed_short"))
        else:
            if st.button(tr.t("analyze_button")):
                # Marquer la page comme chargée après la première interaction
                st.session_state.page_loaded = True
                try:
                    with st.spinner(tr.t("analyzing")):
                        repartition, erreurs = organiseur.simuler_organisation()
                        taille_dossier_gb = (
                            organiseur.calculer_taille_fichiers_organises(repartition)
                            if repartition
                            else 0
                        )
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse : {str(e)}")
                    st.info(
                        "Vérifiez que les dossiers existent et contiennent des photos au bon format (YYYYMMDD_*.jpg)"
                    )
                    repartition = None
                    erreurs = []

                if repartition:
                    total_photos = sum(len(f) for f in repartition.values())

                    if is_both(type_fichiers):
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
                            "success_simulation_mixed_with_size",
                            photos=total_photos_count,
                            videos=total_videos_count,
                            size=taille_dossier_gb,
                        )
                    else:
                        # photos_only ou videos_only : même clé de traduction
                        message = tr.t(
                            "success_simulation_with_size",
                            photos=total_photos,
                            size=taille_dossier_gb,
                        )

                    st.markdown(
                        f'<div class="trex-success">{message}</div>',
                        unsafe_allow_html=True,
                    )

                    for dossier, fichiers in sorted(
                        repartition.items(),
                        key=lambda x: extract_month_number(x[0]),
                    ):
                        if is_both(type_fichiers):
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
                            has_photos = includes_photos(type_fichiers)
                            type_emoji = "📸" if has_photos else "🎬"
                            type_nom = (
                                tr.t("photos_unit")
                                if has_photos
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
                            st.write(f"{tr.t('birth_date_configured')}{date_naissance}")
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
            st.caption(tr.t("config_needed_short"))
        else:
            st.markdown(
                f'<div class="trex-warning">{tr.t("organization_warning")}</div>',
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if is_both(type_fichiers):
                    type_text = tr.t("files_unit")
                elif includes_photos(type_fichiers):
                    type_text = tr.t("photos_unit")
                else:
                    type_text = tr.t("videos_unit")
                confirmer = st.checkbox(tr.t("confirm_organize", type=type_text))

            with col2:
                if st.button(tr.t("organize_button"), disabled=not confirmer):
                    st.session_state.page_loaded = True
                    with st.spinner(tr.t("organizing")):
                        nb_fichiers, erreurs = organiseur.organiser()

                    if nb_fichiers > 0:
                        if is_both(type_fichiers):
                            type_text = tr.t("files_unit")
                        elif includes_photos(type_fichiers):
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
            st.caption(tr.t("config_needed_short"))
        else:
            # Extraire les données des photos
            with st.spinner(tr.t("calculating_stats")):
                df_photos = get_photo_data_cached(organiseur)
                metrics = calculate_metrics(df_photos, type_fichiers)

            if df_photos.empty:
                st.info(tr.t("no_data_analytics"))
            else:
                # Métriques principales en colonnes (3x2 layout)
                col1, col2, col3 = st.columns(3)

                with col1:
                    if is_both(type_fichiers):
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
                            if includes_photos(type_fichiers)
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
                    if is_both(type_fichiers):
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
                            tr.t("burst_mode") if metrics["jour_record"] >= 10 else None
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
                        st.plotly_chart(charts["barres"], width="stretch")

                    # Timeline et heatmap en colonnes
                    col1, col2 = st.columns(2)

                    with col1:
                        if "timeline" in charts:
                            st.plotly_chart(charts["timeline"], width="stretch")

                    with col2:
                        if "heatmap" in charts:
                            st.plotly_chart(charts["heatmap"], width="stretch")

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
            st.caption(tr.t("config_needed_short"))
        else:
            # Réutiliser les données déjà extraites si possible
            if "df_photos" not in locals():
                with st.spinner(tr.t("searching_data")):
                    df_photos = get_photo_data_cached(organiseur)
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

    with tabs[5]:
        st.markdown(
            f'<div class="trex-message">{tr.t("gallery_title")}</div>',
            unsafe_allow_html=True,
        )

        if not config_complete:
            st.caption(tr.t("config_needed_short"))
        else:
            # Obtenir les données de la galerie
            with st.spinner(tr.t("searching_data")):
                gallery_data = get_gallery_data_cached(organiseur)

            if not gallery_data:
                st.info(tr.t("no_photos_month"))
            else:
                # Contrôles de l'interface
                col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

                with col1:
                    # Trier les mois disponibles (sentinelle interne + dossiers triés)
                    months_available = [ALL_MONTHS_SENTINEL] + sorted(
                        gallery_data.keys(), key=extract_month_number
                    )

                    def _format_month(m):
                        if m == ALL_MONTHS_SENTINEL:
                            return tr.t("all_months")
                        if m == UNSORTED_SENTINEL:
                            return tr.t("unsorted_label")
                        match = _MONTH_FOLDER_RE.match(m)
                        if match:
                            return tr.t(
                                "month_pattern",
                                start=match.group(1),
                                end=match.group(2),
                            )
                        return m

                    selected_month = st.selectbox(
                        tr.t("select_month"),
                        months_available,
                        index=0,
                        format_func=_format_month,
                    )

                with col2:
                    # Sélecteur de mode d'affichage (clés internes stables,
                    # libellés traduits via format_func)
                    view_mode = st.selectbox(
                        tr.t("view_mode"),
                        GALLERY_MODES,
                        index=0,
                        format_func=lambda m: tr.t(f"mode_{m}"),
                        help=tr.t("view_mode_help"),
                    )

                with col3:
                    # Max basé sur le nombre de médias disponibles, capé à 50
                    # (au-delà, la galerie devient trop lourde à rendre)
                    total_available = sum(
                        len(photos) for photos in gallery_data.values()
                    )
                    max_photos = max(6, min(50, total_available))

                    num_photos = st.slider(
                        tr.t("photos_to_show"),
                        min_value=1,
                        max_value=max_photos,
                        value=min(6, max_photos),
                        step=1,
                    )

                with col4:
                    if st.button(tr.t("refresh_gallery"), type="secondary"):
                        # Bust les caches @st.cache_data pour relire le disque
                        st.cache_data.clear()
                        # Incrémenter le compteur invalide la sélection en session
                        # (sinon, en mode aléatoire, on retomberait sur la même)
                        st.session_state["gallery_refresh_counter"] = (
                            st.session_state.get("gallery_refresh_counter", 0) + 1
                        )
                        # Replier toutes les vidéos qui étaient en cours de lecture
                        for k in list(st.session_state.keys()):
                            if k.startswith("play_video::"):
                                del st.session_state[k]
                        st.rerun()

                # Afficher le nombre de photos trouvées
                if view_mode == "timeline":
                    # Pour le mode timeline, afficher le nombre de mois disponibles
                    monthly_folders = {
                        k: v
                        for k, v in gallery_data.items()
                        if k != UNSORTED_SENTINEL and "-" in k
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
                elif selected_month == ALL_MONTHS_SENTINEL:
                    total_photos = sum(len(photos) for photos in gallery_data.values())
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

                # Mode Time-lapse : slider d'âge + une grande photo médiane du mois
                if view_mode == "timelapse":
                    photos_par_age = photos_grouped_by_age(gallery_data, organiseur)
                    if not photos_par_age:
                        st.warning(tr.t("no_photos_month"))
                    else:
                        ages_dispo = sorted(photos_par_age.keys())
                        selected_age = st.select_slider(
                            tr.t("age_slider_label"),
                            options=ages_dispo,
                            value=ages_dispo[0],
                            format_func=lambda a: tr.t("age_months", age=a),
                        )

                        # Choisir une photo "médiane par date" pour ce mois
                        candidates = sorted(
                            photos_par_age[selected_age],
                            key=lambda p: organiseur.extraire_date(p) or datetime.min,
                        )
                        photo = candidates[len(candidates) // 2]

                        try:
                            if organiseur.get_file_type(photo) == "video":
                                st.video(str(photo))
                            else:
                                image = get_image_with_correct_orientation(
                                    str(photo), max_size=(900, 900)
                                )
                                buffered = BytesIO()
                                image.save(buffered, format="JPEG", quality=90)
                                img_str = base64.b64encode(buffered.getvalue()).decode()
                                st.markdown(
                                    f'<div style="text-align:center; margin: 1rem 0;">'
                                    f'<img src="data:image/jpeg;base64,{img_str}" '
                                    f'style="max-width:100%; max-height:600px; '
                                    f"border-radius:12px; "
                                    f'box-shadow:0 4px 20px rgba(0,0,0,0.15);" />'
                                    f"</div>",
                                    unsafe_allow_html=True,
                                )
                            caption_html = get_photo_caption_with_age(
                                photo, organiseur, tr
                            )
                            st.markdown(caption_html, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(
                                f"Erreur lors du chargement de {photo.name}: {str(e)}"
                            )
                    # Stop ici pour ne pas exécuter la grille classique
                    selected_photos = None
                else:
                    # Stabiliser la sélection en session_state : sinon les modes
                    # aléatoire/highlights/timeline retirent au sort à chaque rerun
                    # (notamment quand on clique ▶ Lire sur une vidéo), ce qui peut
                    # faire disparaître l'élément cliqué et générer des 500
                    # MediaFileStorageError sur les anciennes URLs.
                    refresh_counter = st.session_state.get("gallery_refresh_counter", 0)
                    selection_key = (
                        f"gallery_sel::{view_mode}::{selected_month}::"
                        f"{num_photos}::{refresh_counter}"
                    )
                    if selection_key in st.session_state:
                        selected_photos = st.session_state[selection_key]
                    else:
                        selected_photos = get_photos_by_mode(
                            gallery_data,
                            organiseur,
                            view_mode,
                            selected_month,
                            num_photos,
                        )
                        st.session_state[selection_key] = selected_photos

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
                                    if organiseur.get_file_type(photo_path) == "video":
                                        # Carte cliquable : st.video n'est appelé qu'après clic
                                        # (évite le préchargement de N lecteurs HTML5 + les 500
                                        # logs Streamlit quand des fichiers sont déplacés)
                                        state_key = f"play_video::{photo_path}"
                                        if st.session_state.get(state_key, False):
                                            st.video(str(photo_path))
                                        else:
                                            st.markdown(
                                                f"""
                                                <div class="video-card">
                                                    <div class="video-card-icon">🎬</div>
                                                    <div class="video-card-filename">{photo_path.name}</div>
                                                </div>
                                                """,
                                                unsafe_allow_html=True,
                                            )
                                            if st.button(
                                                tr.t("play_video"),
                                                key=f"btn_{state_key}",
                                                width="stretch",
                                            ):
                                                st.session_state[state_key] = True
                                                st.rerun()
                                    else:
                                        # Image en RGB + thumbnail 600x600, déjà mis en cache
                                        image = get_image_with_correct_orientation(
                                            str(photo_path), max_size=(600, 600)
                                        )

                                        # Convertir l'image PIL en base64 pour l'intégrer dans le HTML
                                        buffered = BytesIO()
                                        image.save(buffered, format="JPEG", quality=85)
                                        img_str = base64.b64encode(
                                            buffered.getvalue()
                                        ).decode()

                                        # Créer le HTML pour l'image avec le style carré
                                        image_html = f"""
                                        <div class="gallery-image-container">
                                            <img src="data:image/jpeg;base64,{img_str}"
                                                 class="gallery-image"
                                                 alt="{photo_path.name}"
                                                 loading="lazy">
                                        </div>
                                        """
                                        st.markdown(image_html, unsafe_allow_html=True)

                                    # Légende avec badge d'âge (commune photo/vidéo)
                                    caption_html = get_photo_caption_with_age(
                                        photo_path, organiseur, tr
                                    )
                                    st.markdown(caption_html, unsafe_allow_html=True)
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
                elif view_mode != "timelapse":
                    # Pas de warning en mode time-lapse (rendu inline plus haut)
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
