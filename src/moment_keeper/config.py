"""Configuration centralisée pour MomentKeeper."""

from typing import Set

# Extensions de fichiers supportées
EXTENSIONS_PHOTOS: Set[str] = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
EXTENSIONS_VIDEOS: Set[str] = {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".3gp", ".wmv"}
ALL_EXTENSIONS: Set[str] = EXTENSIONS_PHOTOS | EXTENSIONS_VIDEOS

# Types de fichiers pour l'interface
FILE_TYPES = {
    "photos_only": "📸 Photos uniquement",
    "videos_only": "🎬 Vidéos uniquement",
    "both": "📸🎬 Photos et Vidéos",
}

# Configuration par défaut
DEFAULT_PHOTOS_DIR = "photos"
DEFAULT_DATE_FORMAT = "%Y%m%d"
MONTH_FOLDER_PATTERN = "{start}-{end}months"

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
