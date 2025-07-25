"""Application Streamlit pour MomentKeeper."""

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

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

            tab1, tab2 = st.tabs(["📋 Simulation", "🚀 Organisation"])

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
