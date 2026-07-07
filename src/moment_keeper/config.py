"""Configuration centralisée pour MomentKeeper."""

from typing import Optional

# Extensions de fichiers supportées
EXTENSIONS_PHOTOS: set[str] = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
EXTENSIONS_VIDEOS: set[str] = {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".3gp", ".wmv"}
ALL_EXTENSIONS: set[str] = EXTENSIONS_PHOTOS | EXTENSIONS_VIDEOS

# Types de fichiers pour l'interface
FILE_TYPES = {
    "photos_only": "📸 Photos uniquement",
    "videos_only": "🎬 Vidéos uniquement",
    "both": "📸🎬 Photos et Vidéos",
}


def includes_photos(type_fichiers: Optional[str]) -> bool:
    """True si le mode sélectionné inclut les photos."""
    return type_fichiers in (FILE_TYPES["photos_only"], FILE_TYPES["both"])


def includes_videos(type_fichiers: Optional[str]) -> bool:
    """True si le mode sélectionné inclut les vidéos."""
    return type_fichiers in (FILE_TYPES["videos_only"], FILE_TYPES["both"])


def is_both(type_fichiers: Optional[str]) -> bool:
    """True si le mode sélectionné inclut photos ET vidéos."""
    return type_fichiers == FILE_TYPES["both"]


# Configuration par défaut
DEFAULT_PHOTOS_DIR = "photos"
DEFAULT_DATE_FORMAT = "%Y%m%d"
MONTH_FOLDER_PATTERN = "{start}-{end}months"

# Sentinelles internes pour la galerie (jamais affichées telles quelles à l'utilisateur)
ALL_MONTHS_SENTINEL = "__all_months__"
UNSORTED_SENTINEL = "__unsorted__"

# Clés internes des modes d'affichage de la galerie (stables, indépendantes de la langue)
GALLERY_MODES = ["random", "chronological", "highlights", "timeline", "timelapse"]

# Configuration de l'interface
PAGE_CONFIG = {
    "page_title": "🦖 MomentKeeper",
    "page_icon": "🦖",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Limites d'affichage
MAX_FILES_PREVIEW = 10
MAX_FILES_EXPANDER = 5
MAX_IGNORED_FILES_DISPLAY = 5

# Seuils pour les insights
INSIGHTS_THRESHOLDS = {
    "min_gap_days": 5,
    "burst_mode_threshold": 10,
    "productive_day_threshold": 5,
    "large_collection": 100,
    "medium_collection": 50,
    "regular_rhythm": 20,
    "long_gap": 7,
    "very_long_gap": 10,
    "recent_days": 30,
    "recent_active_threshold": 20,
    "special_event_multiplier": 2,
    "special_event_min": 8,
    "major_event_threshold": 25,
    "nice_event_threshold": 15,
    "intensive_period_gap": 3,
    "weekend_intensity_high": 3,
    "weekend_intensity_low": 0.4,
    "trend_increase_threshold": 8,
    "trend_decrease_threshold": -8,
    "evolution_significant": 50,
    "evolution_decrease": -40,
    "contrast_ratio_min": 2,
}

# Configuration des graphiques
CHART_CONFIG = {
    "height_heatmap": 200,
    "max_preview_items": 3,
    "tick_angle": 45,
    "line_width": 4,
    "marker_size": 8,
    "marker_line_width": 2,
}

# Configuration GitHub
GITHUB_REPO = "https://github.com/fdayde/moment-keeper"
