# RPG Tracker

UNDER DEVELOPMENT

**RPG Tracker** to aplikacja do zarządzania kampaniami RPG, stworzona w Pythonie z wykorzystaniem KivyMD.

## Planowane funkcjonalności
- Zarządzanie listą kampanii.
- Harmonogram sesji i notatki.
- Automatyczne przypomnienia o terminach i uzupełnianiu doświadczenia BG.

## Wymagania
- Python 3.12.7

## Instalacja
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/your-username/rpg_tracker.git
   cd rpg_tracker
   ```
2. Utwórz i aktywuj środowisko wirtualne:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```
3. Zainstaluj zależności przy użyciu poetry:
    ```bash
    poetry install
    ```
4. Uruchom aplikację
    ```bash
    python rpg_tracker/main.py
    ```

## Testy
    ```bash
        pytest
    ```

