"""Module de traductions pour MomentKeeper."""

TRANSLATIONS = {
    "fr": {
        # App principale
        "app_title": "🦖 MomentKeeper",
        "tagline": "Du Chaos à la Chronologie",
        "subtitle": "Organisez vos photos de 🦖 (bébé) par mois d'âge et découvrez vos habitudes photo",
        # Sidebar - Configuration
        "config_header": "Configuration",
        "main_folder": "📁 Dossier principal",
        "main_folder_placeholder": "C:/Users/Nom/ProjetPhotos",
        "main_folder_help": "Dossier qui contiendra les sous-dossiers par mois",
        "browse": "Parcourir",
        "source_folder": "📂 Dossier source",
        "source_folder_help": "Dossier contenant les fichiers non triés",
        "browse_subfolder": "Parcourir sous-dossier",
        "birth_date": "🦖 Date de naissance",
        "file_types": "📹 Type de fichiers",
        "photos": "📸 Photos",
        "videos": "🎬 Vidéos",
        "no_type_selected": "⚠️ Veuillez sélectionner au moins un type de fichier",
        "reset_button": "🔄 Réinitialiser",
        "reset_help": "Remet tous les fichiers dans le dossier source",
        # Tabs
        "tab_home": "🏠 Accueil",
        "tab_simulation": "🔍 Simulation",
        "tab_organization": "🗂️ Organisation",
        "tab_analytics": "📊 Analytics",
        "tab_insights": "🦖 Insights",
        # Simulation
        "simulation_title": "🦖 <strong>Simulation de l'organisation</strong><br>Prévisualisez sans déplacer vos fichiers !",
        "analyze_button": "🦖 Analyser les photos",
        "analyzing": "🦖 Analyse vos photos...",
        "no_files_found": "ℹ️ Aucune photo trouvée à organiser",
        "debug_details": "🔍 Détails de l'analyse",
        "birth_date_configured": "Date de naissance configurée : ",
        "ignored_files_count": "Nombre de fichiers ignorés : ",
        "warnings": "⚠️ Avertissements:",
        # Organisation
        "organization_title": "🗂️ <strong>Organisation réelle</strong><br>Temps de passer à l'action !",
        "organization_warning": "🦖 Attention petits bras ! Cette action déplacera réellement vos fichiers.",
        "confirm_organize": "Je confirme vouloir organiser mes {type}",
        "organize_button": "🦖 Organiser",
        "organizing": "🦖 Petits bras en action...",
        "errors_occurred": "❌ Erreurs rencontrées:",
        # Analytics
        "analytics_title": "📊 <strong>Analytics</strong><br>🦖 Découvrez les statistiques de votre petit explorateur !",
        "calculating_stats": "🦖 Calcul des statistiques en cours...",
        "no_data_analytics": "ℹ️ Aucune photo trouvée pour l'analyse",
        # Métriques
        "photos_kept": "📸 Photos gardées",
        "videos_kept": "🎬 Vidéos gardées",
        "last_capture": "📅 Dernière capture",
        "growth_period": "🗓️ Croissance",
        "daily_record": "🏆 Record quotidien",
        "average_rhythm": "📈 Rythme",
        "longest_gap": "⏱️ Plus long silence",
        # Insights
        "insights_title": "🦖 <strong>Insights</strong><br>Découvertes sur vos habitudes photo !",
        "searching_data": "🦖 Fouille dans vos données...",
        "discoveries": "### 🎯 Découvertes",
        "analyze_first": "Analysez d'abord vos photos pour voir les insights!",
        # Messages d'erreur
        "folder_not_exist": "❌ Le dossier photos '{folder}' n'existe pas dans {root}",
        "root_not_exist": "❌ Le dossier principal spécifié n'existe pas",
        "configure_root": "👈 Configurez le dossier principal dans la barre latérale",
        "folder_must_be_in_root": "Le dossier sélectionné doit être dans le dossier principal",
        "select_root_first": "Sélectionnez d'abord le dossier principal",
        # Page d'accueil
        "welcome_title": "Comment ça marche ?",
        "welcome_description": "MomentKeeper organise automatiquement vos photos de bébé par mois d'âge :",
        "welcome_feature_1": "📸 Lit la date dans le nom de vos fichiers (format obligatoire : YYYYMMDD_...)",
        "welcome_feature_2": "🗓️ Calcule l'âge de votre bébé à cette date",
        "welcome_feature_3": "📁 Classe les photos dans des dossiers mensuels (0-1mois, 1-2mois, etc.)",
        "welcome_feature_4": "📊 Analyse vos habitudes photo avec des statistiques détaillées",
        "welcome_feature_5": "🦖 Fournit des insights personnalisés sur vos tendances de capture",
        "welcome_start": "👈 Commencez par configurer le dossier principal dans la barre latérale !",
        "welcome_steps_title": "🚀 Étapes pour commencer :",
        "welcome_step_1": "1️⃣ Configurez vos dossiers et la date de naissance dans la barre latérale",
        "welcome_step_2": "2️⃣ Allez dans l'onglet Simulation pour prévisualiser l'organisation",
        "welcome_step_3": "3️⃣ Utilisez l'onglet Organisation pour déplacer réellement vos fichiers",
        "welcome_step_4": "4️⃣ Explorez Analytics pour découvrir vos statistiques de capture",
        "welcome_step_5": "5️⃣ Consultez Insights pour des analyses personnalisées de vos habitudes",
        # Footer
        "footer_love": "Créé avec ❤️ pour un 🦖 aux petits bras mais au grand cœur",
        "footer_version": "🦖 MomentKeeper v1.0",
        "footer_tagline": '"Du Chaos à la Chronologie, une photo à la fois"',
        "footer_new_tagline": "Fait avec ❤️ pour organiser les souvenirs qui comptent",
        # Messages dynamiques
        "success_simulation": "🦖 Rawr de satisfaction ! {photos} photos analysées et prêtes à être organisées !",
        "success_simulation_mixed": "🦖 Rawr de satisfaction ! {photos} 📸 photos et {videos} 🎬 vidéos analysées !",
        "success_organize": "🦖 Rawr de victoire ! {count} {type} parfaitement organisées !",
        "reset_success": "✅ {count} fichiers remis dans le dossier photos",
        # Unités
        "months": "mois",
        "photos_unit": "photos",
        "videos_unit": "vidéos",
        "files_unit": "fichiers",
        "and_more": "... et {count} autres",
        # Analytics - textes additionnels
        "precious_memories": "Souvenirs précieux !",
        "recent": "Récente !",
        "growing_fast": "Ça grandit vite !",
        "burst_mode": "Mode rafale !",
        "regular": "Régulier !",
        "can_do_better": "On peut faire mieux",
        "trex_sleeping": "T-Rex endormi ?",
        "well_followed": "Bien suivi !",
        # Insights - messages d'analyse
        "magnificent_collection_mixed": "🎉 Magnifique collection de {photos} 📸 photos et {videos} 🎬 vidéos!",
        "magnificent_collection": "🎉 Magnifique collection de {total} {type}!",
        "record_period": "🏆 Période record : {start}-{end} mois ({month}) avec {count} photos!",
        "burst_mode_activated": "📸 Mode rafale activé ! Record : {count} photos le {date}!",
        "productive_day": "📷 Journée productive : {count} photos le {date}!",
        "longest_silence": "⚠️ Plus long silence : {days} jours entre le {start} et le {end}",
        "think_recent_photos": "💡 Pensez à prendre quelques photos récentes!",
        "very_active_month": "🔥 Très actif ce mois-ci!",
        "contrast_months": "📊 Contraste : {max_month} vs {min_month} = {ratio}x plus de photos",
        "intense_weekend": "🎯 Weekend intense : {ratio}x plus de photos par jour le weekend",
        "active_weekdays": "💼 Semaine active : {ratio}x plus de photos par jour en semaine",
        "prefer_photos": "📸 Vous préférez clairement les photos aux vidéos!",
        "true_videographer": "🎬 Un vrai vidéaste ! Vous capturez surtout en vidéo",
        "perfect_balance": "⚖️ Équilibre parfait entre photos et vidéos!",
        "capture_weekends": "📅 Vous capturez bien les week-ends en famille!",
        "sunday_champion": "🌅 Champion du dimanche!",
        "yearly_projection": "📈 À ce rythme, vous aurez ~{count} photos par an!",
        "trend_increasing": "📈 Tendance récente : Vous photographiez de plus en plus votre 🦖",
        "trend_decreasing": "📉 Tendance récente : Moins de photos - normal quand 🦖 grandit!",
        # Analytics - Alertes
        "temporal_alerts": "⚠️ Alertes temporelles",
        "gap_alert": "Gap de {days} jours : du {start} au {end}",
        # Insights - Sections
        "detailed_analysis": "📋 Analyse détaillée",
        "monthly_distribution": "**🗓️ Répartition mensuelle**",
        "favorite_days": "**📅 Jours favoris**",
        "suggestions": "💡 Suggestions",
        "not_to_miss": "📸 **Pour ne rien rater :**",
        "enrich_memories": "📈 **Pour enrichir vos souvenirs :**",
        # Insights - Suggestions détaillées
        "think_weekday_photos": "• Pensez à prendre des photos pendant la semaine aussi",
        "capture_daily_moments": "• Essayez de capturer les moments du quotidien",
        "more_photos_evolution": "• Quelques photos de plus par mois donneraient un bel aperçu de l'évolution",
        "small_moments_matter": "• Les petits moments comptent autant que les grands!",
        # Insights - Répartition
        "months_pattern": "• {start}-{end} mois : {count} photos",
        "and_other_months": "... et {count} autres mois",
        "photos_count": "• {day} : {count} photos",
        # Messages additionnels
        "errors_encountered": "❌ Erreurs rencontrées:",
        "select_file_type": "❌ Veuillez sélectionner au moins un type de fichier (Photos et/ou Vidéos)",
        "files_reset": "✅ {count} fichiers remis dans le dossier photos",
    },
    "en": {
        # App principale
        "app_title": "🦖 MomentKeeper",
        "tagline": "From Chaos to Chronology",
        "subtitle": "Organize your 🦖 (baby) photos by age in months and discover your photo habits",
        # Sidebar - Configuration
        "config_header": "Configuration",
        "main_folder": "📁 Main folder",
        "main_folder_placeholder": "C:/Users/Name/PhotoProject",
        "main_folder_help": "Folder that will contain the monthly subfolders",
        "browse": "Browse",
        "source_folder": "📂 Source folder",
        "source_folder_help": "Folder containing unsorted files",
        "browse_subfolder": "Browse subfolder",
        "birth_date": "🦖 Birth date",
        "file_types": "📹 File types",
        "photos": "📸 Photos",
        "videos": "🎬 Videos",
        "no_type_selected": "⚠️ Please select at least one file type",
        "reset_button": "🔄 Reset",
        "reset_help": "Puts all files back in the source folder",
        # Tabs
        "tab_home": "🏠 Home",
        "tab_simulation": "🔍 Simulation",
        "tab_organization": "🗂️ Organization",
        "tab_analytics": "📊 Analytics",
        "tab_insights": "🦖 Insights",
        # Simulation
        "simulation_title": "🦖 <strong>Organization simulation</strong><br>Preview without moving your files!",
        "analyze_button": "🦖 Analyze photos",
        "analyzing": "🦖 Analyzing your photos...",
        "no_files_found": "ℹ️ No photos found to organize",
        "debug_details": "🔍 Analysis details",
        "birth_date_configured": "Configured birth date: ",
        "ignored_files_count": "Number of ignored files: ",
        "warnings": "⚠️ Warnings:",
        # Organisation
        "organization_title": "🗂️ <strong>Actual organization</strong><br>Time to take action!",
        "organization_warning": "🦖 Watch out tiny arms! This action will actually move your files.",
        "confirm_organize": "I confirm I want to organize my {type}",
        "organize_button": "🦖 Organize",
        "organizing": "🦖 Tiny arms in action...",
        "errors_occurred": "❌ Errors encountered:",
        # Analytics
        "analytics_title": "📊 <strong>Analytics</strong><br>🦖 Discover your little explorer's statistics!",
        "calculating_stats": "🦖 Calculating statistics...",
        "no_data_analytics": "ℹ️ No photos found for analysis",
        # Métriques
        "photos_kept": "📸 Photos kept",
        "videos_kept": "🎬 Videos kept",
        "last_capture": "📅 Last capture",
        "growth_period": "🗓️ Growth",
        "daily_record": "🏆 Daily record",
        "average_rhythm": "📈 Rhythm",
        "longest_gap": "⏱️ Longest gap",
        # Insights
        "insights_title": "🦖 <strong>Insights</strong><br>Discoveries about your photo habits!",
        "searching_data": "🦖 Digging through your data...",
        "discoveries": "### 🎯 Discoveries",
        "analyze_first": "Analyze your photos first to see insights!",
        # Messages d'erreur
        "folder_not_exist": "❌ The photos folder '{folder}' doesn't exist in {root}",
        "root_not_exist": "❌ The specified main folder doesn't exist",
        "configure_root": "👈 Configure the main folder in the sidebar",
        "folder_must_be_in_root": "The selected folder must be in the main folder",
        "select_root_first": "Select the main folder first",
        # Welcome page
        "welcome_title": "How does it work?",
        "welcome_description": "MomentKeeper automatically organizes your baby photos by age in months:",
        "welcome_feature_1": "📸 Reads the date from your file names (required format: YYYYMMDD_...)",
        "welcome_feature_2": "🗓️ Calculates your baby's age on that date",
        "welcome_feature_3": "📁 Sorts photos into monthly folders (0-1months, 1-2months, etc.)",
        "welcome_feature_4": "📊 Analyzes your photo habits with detailed statistics",
        "welcome_feature_5": "🦖 Provides personalized insights on your capture trends",
        "welcome_start": "👈 Start by configuring the main folder in the sidebar!",
        "welcome_steps_title": "🚀 Steps to get started:",
        "welcome_step_1": "1️⃣ Configure your folders and birth date in the sidebar",
        "welcome_step_2": "2️⃣ Go to the Simulation tab to preview the organization",
        "welcome_step_3": "3️⃣ Use the Organization tab to actually move your files",
        "welcome_step_4": "4️⃣ Explore Analytics to discover your capture statistics",
        "welcome_step_5": "5️⃣ Check Insights for personalized analysis of your habits",
        # Footer
        "footer_love": "Created with ❤️ for a 🦖 with tiny arms but a big heart",
        "footer_version": "🦖 MomentKeeper v1.0",
        "footer_tagline": '"From Chaos to Chronology, one photo at a time"',
        "footer_new_tagline": "Made with ❤️ to organize the memories that matter",
        # Messages dynamiques
        "success_simulation": "🦖 Satisfaction roar! {photos} photos analyzed and ready to be organized!",
        "success_simulation_mixed": "🦖 Satisfaction roar! {photos} 📸 photos and {videos} 🎬 videos analyzed!",
        "success_organize": "🦖 Victory roar! {count} {type} perfectly organized!",
        "reset_success": "✅ {count} files put back in the photos folder",
        # Units
        "months": "months",
        "photos_unit": "photos",
        "videos_unit": "videos",
        "files_unit": "files",
        "and_more": "... and {count} more",
        # Analytics - additional texts
        "precious_memories": "Precious memories!",
        "recent": "Recent!",
        "growing_fast": "Growing fast!",
        "burst_mode": "Burst mode!",
        "regular": "Regular!",
        "can_do_better": "Could do better",
        "trex_sleeping": "T-Rex sleeping?",
        "well_followed": "Well followed!",
        # Insights - analysis messages
        "magnificent_collection_mixed": "🎉 Magnificent collection of {photos} 📸 photos and {videos} 🎬 videos!",
        "magnificent_collection": "🎉 Magnificent collection of {total} {type}!",
        "record_period": "🏆 Record period: {start}-{end} months ({month}) with {count} photos!",
        "burst_mode_activated": "📸 Burst mode activated! Record: {count} photos on {date}!",
        "productive_day": "📷 Productive day: {count} photos on {date}!",
        "longest_silence": "⚠️ Longest silence: {days} days between {start} and {end}",
        "think_recent_photos": "💡 Think about taking some recent photos!",
        "very_active_month": "🔥 Very active this month!",
        "contrast_months": "📊 Contrast: {max_month} vs {min_month} = {ratio}x more photos",
        "intense_weekend": "🎯 Intense weekend: {ratio}x more photos per day on weekends",
        "active_weekdays": "💼 Active weekdays: {ratio}x more photos per day on weekdays",
        "prefer_photos": "📸 You clearly prefer photos to videos!",
        "true_videographer": "🎬 A true videographer! You mostly capture in video",
        "perfect_balance": "⚖️ Perfect balance between photos and videos!",
        "capture_weekends": "📅 You capture family weekends well!",
        "sunday_champion": "🌅 Sunday champion!",
        "yearly_projection": "📈 At this rate, you'll have ~{count} photos per year!",
        "trend_increasing": "📈 Recent trend: You're photographing your 🦖 more and more",
        "trend_decreasing": "📉 Recent trend: Fewer photos - normal as 🦖 grows!",
        # Analytics - Alerts
        "temporal_alerts": "⚠️ Temporal alerts",
        "gap_alert": "Gap of {days} days: from {start} to {end}",
        # Insights - Sections
        "detailed_analysis": "📋 Detailed analysis",
        "monthly_distribution": "**🗓️ Monthly distribution**",
        "favorite_days": "**📅 Favorite days**",
        "suggestions": "💡 Suggestions",
        "not_to_miss": "📸 **Not to miss:**",
        "enrich_memories": "📈 **To enrich your memories:**",
        # Insights - Detailed suggestions
        "think_weekday_photos": "• Remember to take photos during the week too",
        "capture_daily_moments": "• Try to capture everyday moments",
        "more_photos_evolution": "• A few more photos per month would give a nice overview of the evolution",
        "small_moments_matter": "• Small moments matter as much as big ones!",
        # Insights - Distribution
        "months_pattern": "• {start}-{end} months: {count} photos",
        "and_other_months": "... and {count} other months",
        "photos_count": "• {day}: {count} photos",
        # Additional messages
        "errors_encountered": "❌ Errors encountered:",
        "select_file_type": "❌ Please select at least one file type (Photos and/or Videos)",
        "files_reset": "✅ {count} files put back in the photos folder",
    },
}


class Translator:
    """Classe pour gérer les traductions."""

    def __init__(self, language="fr"):
        """
        Initialise le traducteur avec une langue.

        Args:
            language: Code de langue ('fr' ou 'en')
        """
        self.language = language
        self.translations = TRANSLATIONS

    def set_language(self, language: str):
        """Change la langue active."""
        if language in self.translations:
            self.language = language

    def t(self, key: str, **kwargs) -> str:
        """
        Traduit une clé avec des paramètres optionnels.

        Args:
            key: Clé de traduction
            **kwargs: Paramètres pour le formatage du texte

        Returns:
            Texte traduit
        """
        text = self.translations.get(self.language, {}).get(key, key)

        # Si des paramètres sont fournis, formater le texte
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                # Si une clé manque, retourner le texte sans formatage
                pass

        return text

    def get_current_language(self) -> str:
        """Retourne la langue actuelle."""
        return self.language
