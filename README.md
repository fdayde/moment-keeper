# MomentKeeper

🦖🍼 **Automatic (Baby) Photo Organizer** - Organize precious moments chronologically with intelligent automation.

## 🎯 Overview

MomentKeeper automatically organizes baby photos into monthly folders based on birth date and photo timestamps extracted from filenames. 
Transform thousands of photos from chaos to chronological perfection in minutes.

## ✨ Features

- **Smart Organization**: Automatically sorts photos into monthly folders (0-1months, 1-2months, etc.)
- **Date Intelligence**: Extracts dates from filename patterns (`YYYYMMDD_description.jpg`)
- **Dual Interface**: Web interface (Streamlit) and command-line interface
- **Safe Operation**: Simulation mode before actual organization
- **Reset Capability**: Undo organization if needed
- **Error Handling**: Robust handling of invalid dates and file formats
- **Interactive Folder Selection**: Browse and select folders with native dialogs

## 🛠️ Technical Architecture

### Core Modules
- `OrganisateurPhotos`: Main organization logic with calendar-accurate age calculation
- `PhotoCopier`: File operations and safety with move/copy capabilities
- `PathManager`: Cross-platform path handling

### Workflow
1. **Configuration**: Set root folder, photos subfolder, and baby's birth date
2. **Simulation**: Preview organization without moving files
3. **Confirmation**: User validates the plan
4. **Organization**: Execute the actual file organization
5. **Reset**: Optional rollback capability

## 📁 Project Structure

### Input
```
project-folder/           (root directory)
└── photos/              (subfolder with photos to organize)
    ├── 20240315_first_smile.jpg
    ├── 20240420_crawling.jpg
    ├── 20240515_sitting_up.jpg
    └── ...
```

### Output
```
project-folder/           (root directory)
├── photos/              (original photos subfolder)
├── 0-1months/           (organized by age - created in root)
│   └── 20240315_first_smile.jpg
├── 1-2months/
│   └── 20240420_crawling.jpg
├── 2-3months/
│   └── 20240515_sitting_up.jpg
└── ...
```

## 🚀 Quick Start

### Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

### Install and run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit web interface
streamlit run app.py

# Or use the command line interface
python -m src.moment_keeper.cli /path/to/project-folder 2024-06-25
```

## 🖥️ Usage

### Streamlit Web Interface
1. **Configure paths**: Select root directory and photos subfolder using browse buttons
2. **Set birth date**: Choose baby's birth date with date picker
3. **Simulate**: Preview organization with "Analyser les photos"
4. **Organize**: Confirm and run actual organization
5. **Reset**: Undo organization if needed

### Command Line Interface
```bash
# Basic usage
python -m src.moment_keeper.cli /path/to/project 2024-06-25

# Simulation mode
python -m src.moment_keeper.cli /path/to/project 2024-06-25 --simulate

# Custom photos subfolder
python -m src.moment_keeper.cli /path/to/project 2024-06-25 --photos-dir images

# Reset organization
python -m src.moment_keeper.cli /path/to/project 2024-06-25 --reset
```

## 🔧 Configuration

- **Root Directory**: Main project folder containing photos subfolder
- **Photos Subfolder**: Subdirectory with photos to organize (default: "photos")
- **Birth Date**: Baby's birth date for precise age calculations
- **File Pattern**: Supports `YYYYMMDD_description.jpg` format

## 🎨 User Interface

**Streamlit Web App Features:**
- Native folder browsing with tkinter dialogs
- Dual path configuration (root + subfolder)
- Date picker with validation
- Real-time simulation preview
- Progress tracking and detailed error reporting
- Debug information for ignored files
- One-click reset functionality

## 🛡️ Safety Features

- **Simulation First**: Always preview before acting
- **File Validation**: Check file existence and format
- **Calendar-Accurate Age Calculation**: Proper month-based age calculation
- **Error Recovery**: Graceful handling of edge cases and file conflicts
- **Rollback Capability**: Complete reset to original state

## 📋 Development Status

- ✅ Core organization logic with accurate age calculation
- ✅ Cross-platform path handling
- ✅ Complete Streamlit interface
- ✅ Command-line interface
- ✅ Jupyter notebook integration
- ✅ Advanced error handling and debugging

## 💡 Use Cases

- **New Parents**: Organize growing photo collections
- **Family Archives**: Sort historical baby photos
- **Photo Enthusiasts**: Maintain chronological photo libraries
- **Memory Keeping**: Create timeline-based photo albums

## 🚀 Development

### Running Tests
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (recommended)
pre-commit install

# Run code formatting manually
black src tests
isort src tests

# Run linting manually
ruff check src tests

# Run all pre-commit hooks manually
pre-commit run --all-files

# Run tests (when implemented)
pytest
```

### Project Structure
```
moment-keeper/
├── src/moment_keeper/       # Main package
│   ├── organizer.py         # Core organization logic
│   ├── photo_copier.py      # File operations
│   ├── path_manager.py      # Path utilities
│   └── cli.py              # Command-line interface
├── app.py                   # Streamlit web interface
├── notebooks/               # Jupyter notebooks
├── tests/                   # Unit tests
└── requirements*.txt        # Dependencies
```

---

*Built with ❤️ for preserving precious family moments*