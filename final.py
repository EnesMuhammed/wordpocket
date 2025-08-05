import sys
import json
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                              QLineEdit, QPushButton, QToolButton, QLabel, QTableWidget, 
                              QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
                              QDialog, QListWidget, QListWidgetItem, QDialogButtonBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QRegion, QPainterPath
try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
    TRANSLATOR_TYPE = "deep_translator"
    print("Using deep-translator for translations")
except ImportError:
    try:
        # Fallback to older googletrans version
        from googletrans import Translator
        translator = Translator()
        TRANSLATOR_AVAILABLE = True
        TRANSLATOR_TYPE = "googletrans"
        print("Using googletrans for translations")
    except ImportError:
        TRANSLATOR_AVAILABLE = False
        print("Warning: Neither 'deep-translator' nor 'googletrans' installed. Translation will be disabled.")
        print("Install with: pip install deep-translator")
    else:
        TRANSLATOR_TYPE = "deep_translator"




# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

    # Import for Arabic text shaping
    from arabic_reshaper import ArabicReshaper
    from bidi.algorithm import get_display

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: 'reportlab', 'arabic-reshaper', or 'python-bidi' not installed. PDF export will be disabled.")
LANGUAGES = {
    'EN': {'name': 'English', 'code': 'en', 'font': 'NotoSans-Regular.ttf'},
    'TR': {'name': 'Türkçe', 'code': 'tr', 'font': 'NotoSans-Regular.ttf'},
    'AR': {'name': 'العربية', 'code': 'ar', 'font': 'NotoSansArabic-Regular.ttf'},
    'FR': {'name': 'Français', 'code': 'fr', 'font': 'NotoSans-Regular.ttf'},
    'DE': {'name': 'Deutsch', 'code': 'de', 'font': 'NotoSans-Regular.ttf'},
    'ES': {'name': 'Español', 'code': 'es', 'font': 'NotoSans-Regular.ttf'},
    'IT': {'name': 'Italiano', 'code': 'it', 'font': 'NotoSans-Regular.ttf'},
    'RU': {'name': 'Русский', 'code': 'ru', 'font': 'NotoSans-Regular.ttf'},
    'JA': {'name': '日本語', 'code': 'ja', 'font': 'NotoSansJP-Regular.ttf'},
    'KO': {'name': '한국어', 'code': 'ko', 'font': 'NotoSansKR-Regular.ttf'},
    'ZH': {'name': '中文', 'code': 'zh', 'font': 'NotoSansSC-Regular.ttf'},
    'PT': {'name': 'Português', 'code': 'pt', 'font': 'NotoSans-Regular.ttf'},
    'NL': {'name': 'Nederlands', 'code': 'nl', 'font': 'NotoSans-Regular.ttf'},
    'SV': {'name': 'Svenska', 'code': 'sv', 'font': 'NotoSans-Regular.ttf'},
    'DA': {'name': 'Dansk', 'code': 'da', 'font': 'NotoSans-Regular.ttf'},
    'NO': {'name': 'Norsk', 'code': 'no', 'font': 'NotoSans-Regular.ttf'},
    'FI': {'name': 'Suomi', 'code': 'fi', 'font': 'NotoSans-Regular.ttf'},
    'PL': {'name': 'Polski', 'code': 'pl', 'font': 'NotoSans-Regular.ttf'},
    'CS': {'name': 'Čeština', 'code': 'cs', 'font': 'NotoSans-Regular.ttf'},
    'HU': {'name': 'Magyar', 'code': 'hu', 'font': 'NotoSans-Regular.ttf'}
}

# Add font mapping to the LANGUAGES dictionary
default_latin_font = 'NotoSans-Regular.ttf'
for lang_key in LANGUAGES:
    if lang_key not in ['AR', 'JA', 'KO', 'ZH']:
        LANGUAGES[lang_key]['font'] = default_latin_font

class LanguageSettingsDialog(QDialog):
    # This class remains unchanged
    def __init__(self, parent, current_settings):
        super().__init__(parent)
        self.setWindowTitle("Language Settings")
        self.setGeometry(300, 300, 400, 500)
        self.setModal(True)

        layout = QVBoxLayout(self)

        source_label = QLabel("Source Languages:")
        source_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(source_label)

        self.source_list = QListWidget()
        for lang_key, lang_info in LANGUAGES.items():
            item = QListWidgetItem(f"{lang_key} - {lang_info['name']}")
            item.setData(Qt.UserRole, lang_key)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if lang_key in current_settings.get('source_languages', ['EN', 'TR']):
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.source_list.addItem(item)
        layout.addWidget(self.source_list)

        target_label = QLabel("Target Languages:")
        target_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(target_label)

        self.target_list = QListWidget()
        for lang_key, lang_info in LANGUAGES.items():
            item = QListWidgetItem(f"{lang_key} - {lang_info['name']}")
            item.setData(Qt.UserRole, lang_key)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if lang_key in current_settings.get('target_languages', ['AR', 'FR']):
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.target_list.addItem(item)
        layout.addWidget(self.target_list)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_languages(self):
        source_languages = []
        target_languages = []

        for i in range(self.source_list.count()):
            item = self.source_list.item(i)
            if item.checkState() == Qt.Checked:
                source_languages.append(item.data(Qt.UserRole))

        for i in range(self.target_list.count()):
            item = self.target_list.item(i)
            if item.checkState() == Qt.Checked:
                target_languages.append(item.data(Qt.UserRole))

        return source_languages, target_languages

class TableEditorWindow(QWidget):
    def __init__(self, parent, source_lang, target_lang):
        super().__init__()
        self.parent = parent
        self.source_lang = source_lang
        self.target_lang = target_lang

        # Use relative path for JSON file
        self.json_file = os.path.join(DATA_DIR, f"dict_{source_lang}_{target_lang}.json")

        self.setWindowTitle(f"Dictionary Editor - {source_lang} to {target_lang}")
        self.setGeometry(200, 200, 600, 400)

        # Use relative path for icon
        icon_path = os.path.join(SCRIPT_DIR, "app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Warning: Icon file not found: {icon_path}")

        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)

        headers = [LANGUAGES[source_lang]['name'], LANGUAGES[target_lang]['name']]
        self.table.setHorizontalHeaderLabels(headers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Row", self)
        add_button.clicked.connect(self.add_row)

        delete_button = QPushButton("Delete Row", self)
        delete_button.clicked.connect(self.delete_row)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_data)

        export_button = QPushButton("Export PDF", self)
        if not REPORTLAB_AVAILABLE:
            export_button.setEnabled(False)
            export_button.setToolTip("PDF export requires 'reportlab', 'arabic-reshaper', 'python-bidi' to be installed.")
        export_button.clicked.connect(self.export_pdf)

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(export_button)

        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.table.setRowCount(len(data))

                for row, item in enumerate(data):
                    word_item = QTableWidgetItem(item.get('word', ''))
                    meaning_item = QTableWidgetItem(item.get('meaning', ''))

                    self.table.setItem(row, 0, word_item)
                    self.table.setItem(row, 1, meaning_item)
            else:
                self.table.setRowCount(0)
                # Ensure directory exists before creating file
                os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", f"JSON file is corrupted: {self.json_file}. Please check or delete it.")
            self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error loading file: {str(e)}")

    def add_row(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        self.table.setItem(row_count, 0, QTableWidgetItem(""))
        self.table.setItem(row_count, 1, QTableWidgetItem(""))

    def delete_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def save_data(self):
        try:
            data = []

            for row in range(self.table.rowCount()):
                word_item = self.table.item(row, 0)
                meaning_item = self.table.item(row, 1)

                if word_item and meaning_item:
                    word = word_item.text().strip()
                    meaning = meaning_item.text().strip()

                    if word or meaning:
                        data.append({
                            'word': word,
                            'meaning': meaning
                        })

            # Ensure directory exists
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save error: {str(e)}")

    def refresh_table(self):
        """Refresh table data - can be called from parent"""
        self.load_data()

    def export_pdf(self):
        if not REPORTLAB_AVAILABLE:
            QMessageBox.critical(self, "Error", "PDF export requires 'reportlab', 'arabic-reshaper', 'python-bidi' libraries.\n\nInstall with: pip install reportlab arabic-reshaper python-bidi")
            return

        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save as PDF",
                f"dictionary_{self.source_lang}_{self.target_lang}.pdf",
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return

            doc = SimpleDocTemplate(file_path, pagesize=A4)
            elements = []
            styles = getSampleStyleSheet()

            # --- Font Selection and Registration ---
            # Font for source language
            source_font_path = os.path.join(SCRIPT_DIR, "fonts", LANGUAGES[self.source_lang]['font'])
            source_font_name = f'Font-{self.source_lang}'
            if os.path.exists(source_font_path) and source_font_name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(source_font_name, source_font_path))
            
            # Font for target language
            target_font_path = os.path.join(SCRIPT_DIR, "fonts", LANGUAGES[self.target_lang]['font'])
            target_font_name = f'Font-{self.target_lang}'
            if os.path.exists(target_font_path) and target_font_name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(target_font_name, target_font_path))

            # Fallback font
            fallback_font_name = 'Helvetica'

            # --- Paragraph Styles ---
            source_style = styles['Normal'].clone('SourceStyle')
            source_style.fontName = source_font_name if source_font_name in pdfmetrics.getRegisteredFontNames() else fallback_font_name
            source_style.alignment = TA_CENTER
            source_style.fontSize = 12
            source_style.leading = 15

            target_style = styles['Normal'].clone('TargetStyle')
            target_style.fontName = target_font_name if target_font_name in pdfmetrics.getRegisteredFontNames() else fallback_font_name
            target_style.alignment = TA_CENTER
            target_style.fontSize = 12
            target_style.leading = 15

            # --- Header Styles ---
            header_source_style = styles['Heading2'].clone('HeaderSourceStyle')
            header_source_style.fontName = source_style.fontName
            header_source_style.alignment = TA_CENTER

            header_target_style = styles['Heading2'].clone('HeaderTargetStyle')
            header_target_style.fontName = target_style.fontName
            header_target_style.alignment = TA_CENTER

            table_data = []

            # Add headers with their specific fonts
            processed_headers = [
                Paragraph(self.process_text(LANGUAGES[self.source_lang]['name'], self.source_lang), header_source_style),
                Paragraph(self.process_text(LANGUAGES[self.target_lang]['name'], self.target_lang), header_target_style)
            ]

            table_data.append(processed_headers)

            # Process table data
            for row in range(self.table.rowCount()):
                word_item = self.table.item(row, 0)
                meaning_item = self.table.item(row, 1)

                if word_item and meaning_item:
                    word = word_item.text().strip()
                    meaning = meaning_item.text().strip()

                    if word or meaning:
                        processed_word = self.process_text(word, self.source_lang)
                        processed_meaning = self.process_text(meaning, self.target_lang)

                        table_data.append([
                            Paragraph(processed_word, source_style),
                            Paragraph(processed_meaning, target_style)
                        ])

            if len(table_data) <= 1:
                QMessageBox.information(self, "Info", "No data in table to export to PDF!")
                return

            # Create and style the table
            table = Table(table_data, colWidths=[3*inch, 3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))

            elements.append(table)
            doc.build(elements)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"PDF save error: {str(e)}")
            print(e)

    def process_text(self, text, lang_code):
        """Process text for PDF display, handling RTL and special characters."""
        if not text:
            return ""
        
        if lang_code == 'AR' or self.is_arabic_text(text):
            return self.prepare_arabic_text(text)
        
        return text

    def is_arabic_text(self, text):
        for char in text:
            if '\u0600' <= char <= '\u06FF' or \
               '\u0750' <= char <= '\u077F' or \
               '\u08A0' <= char <= '\u08FF' or \
               '\uFB50' <= char <= '\uFDFF' or \
               '\uFE70' <= char <= '\uFEFF':
                return True
        return False

    def prepare_arabic_text(self, text):
        reshaper = ArabicReshaper(
            configuration={
                'delete_harakat': False,
                'delete_tatweel': False,
                'support_ligatures': True,
                'arabic_reshaper_join_by_shadda': True,
                'delete_unnecessary_dots': False,
                'shift_harakat_position': False,
                'support_vocalized_arabic': True,
            }
        )
        reshaped_text = reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text

    def closeEvent(self, event):
        self.save_data()
        # Notify parent that table window is closing
        if hasattr(self.parent, 'table_window'):
            self.parent.table_window = None
        event.accept()

class DictionaryApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dictionary")
        self.setGeometry(1210, 100, 220, 20)
        self.title_bar_visible = True
        self.always_on_top = False
        self.table_window = None

        self.target_lang_index = 0
        self.source_lang_index = 0

        # Load settings
        self.settings_file = os.path.join(SCRIPT_DIR, "settings.json")
        self.load_settings()

        # Use relative path for icon
        icon_path = os.path.join(SCRIPT_DIR, "app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # --- 1. Layer: Transparent window ---
        outer_layout = QVBoxLayout(self)
        outer_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # --- 2. Layer: Content with radius ---
        self.content_widget = QWidget(self)
        self.content_widget.setStyleSheet("""
            background-color: #2E2E2E;
            border-radius: 7px;
        """)
        outer_layout.addWidget(self.content_widget)

        # --- Layouts ---
        main_layout = QVBoxLayout(self.content_widget)

        input_layout1 = QHBoxLayout()
        input_layout2 = QHBoxLayout()

        # --- Input box (word) ---
        self.word_entry = QLineEdit(self.content_widget)
        self.word_entry.setPlaceholderText("Word")
        self.word_entry.setStyleSheet("""
            font-size: 12pt;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #FD7B01;
            width: 120px;
        """)
        self.word_entry.textChanged.connect(self.reset_timer)

        # --- Translation box ---
        self.translation_entry = QLineEdit(self.content_widget)
        self.translation_entry.setReadOnly(True)
        self.translation_entry.setPlaceholderText("Translation")
        self.translation_entry.setStyleSheet("""
            font-size: 12pt;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #FF4031;
            width: 120px;
        """)

        # --- Save Button ---
        self.save_button = QPushButton("Save", self.content_widget)
        self.save_button.setStyleSheet("""
            font-size: 12pt;
            padding: 5px;
            border-radius: 5px;
            background-color: #E73927;
            color: white;
            width: 80px;
            height: 24px;
        """)
        self.save_button.clicked.connect(self.save_to_json)

        # --- Source Language Button ---
        self.source_lang_button = QToolButton(self.content_widget)
        self.source_lang_button.setText(self.source_languages[self.source_lang_index])
        self.source_lang_button.setStyleSheet("""
            background-color: #FD7B01;
            border-radius: 5px;
            font-size: 12pt;
            padding: 5px;
            width: 30px;
            height: 22px;
        """)
        self.source_lang_button.clicked.connect(self.toggle_source_language)

        # --- Target Language Button ---
        self.target_lang_button = QToolButton(self.content_widget)
        self.target_lang_button.setText(self.target_languages[self.target_lang_index])
        self.target_lang_button.setStyleSheet("""
            background-color: #FF4031;
            border-radius: 5px;
            font-size: 12pt;
            padding: 5px;
            width: 30px;
            height: 22px;
        """)
        self.target_lang_button.clicked.connect(self.toggle_target_language)

        # --- Settings Button ---
        self.settings_button = QToolButton(self.content_widget)
        self.settings_button.setText("⚙")
        self.settings_button.setStyleSheet("""
            background-color: #FFBC4C;
            border-radius: 5px;
            font-size: 12pt;
            padding: 5px;
            width: 23px;
            height: 22px;
        """)
        self.settings_button.clicked.connect(self.open_settings)

        # --- Pin Button ---
        self.pin_button = QToolButton(self.content_widget)
        self.pin_button.setText("⚲")
        self.pin_button.setStyleSheet("""
            background-color: #BE5103;
            border-radius: 5px;
            font-size: 12pt;
            padding: 5px;
            width: 23px;
            height: 22px;
        """)
        self.pin_button.clicked.connect(self.toggle_title_bar)

        # --- Table Editor Button ---
        self.table_button = QToolButton(self.content_widget)
        self.table_button.setText("📄")
        self.table_button.setStyleSheet("""
            background-color: #8C4C1F;
            border-radius: 5px;
            font-size: 12pt;
            padding: 5px;
            width: 23px;
            height: 22px;
        """)
        self.table_button.clicked.connect(self.open_table_editor)

        # --- Add to layouts ---
        input_layout1.addWidget(self.word_entry)
        input_layout1.addWidget(self.source_lang_button)
        input_layout2.addWidget(self.translation_entry)
        input_layout2.addWidget(self.target_lang_button)
        
        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.save_button)
        button_layout1.addWidget(self.table_button)
        button_layout1.addWidget(self.settings_button)
        button_layout1.addWidget(self.pin_button)

        main_layout.addLayout(input_layout1)
        main_layout.addLayout(input_layout2)
        main_layout.addLayout(button_layout1)

        # Timer for debouncing
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # Only run once after the timeout
        self.timer.timeout.connect(self.translate_word)

    def load_settings(self):
        """Load language settings from file"""
        default_settings = {
            'source_languages': ['FR', 'EN'],
            'target_languages': ['AR', 'TR']
        }

        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.source_languages = settings.get('source_languages', default_settings['source_languages'])
                    self.target_languages = settings.get('target_languages', default_settings['target_languages'])
            else:
                self.source_languages = default_settings['source_languages']
                self.target_languages = default_settings['target_languages']
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.source_languages = default_settings['source_languages']
            self.target_languages = default_settings['target_languages']

        # Fix: Initialize settings variable before using it
        settings = {}
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            except:
                pass

        self.source_lang_index = settings.get('source_language_index', 0)
        self.target_lang_index = settings.get('target_language_index', 0)
        print(f"Loaded settings: {self.source_languages[self.source_lang_index]}, {self.target_languages[self.target_lang_index]}")

    def save_settings(self):
        """Save language settings to file"""
        try:
            settings = {
                'source_languages': self.source_languages,
                'target_languages': self.target_languages,
                'source_language_index': self.source_lang_index,
                'target_language_index': self.target_lang_index
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
        print(f"Saved settings: {self.source_languages[self.source_lang_index]}, {self.target_languages[self.target_lang_index]}")

    def reset_timer(self):
        """Reset the timer every time the user types a new character"""
        self.timer.start(500)  # Start the timer again with a 500ms delay

    def translate_word(self):
        """Function to translate the word"""
        if not TRANSLATOR_AVAILABLE:
            self.translation_entry.setText("Translator not available")
            return
            
        if self.word_entry.text().strip() == "":
            self.translation_entry.clear()
            return

        word = self.word_entry.text().strip()
        source_code = LANGUAGES[self.source_languages[self.source_lang_index]]['code']
        target_code = LANGUAGES[self.target_languages[self.target_lang_index]]['code']

        try:
            if TRANSLATOR_TYPE == "deep_translator":
                # Using deep-translator (recommended)
                translator = GoogleTranslator(source=source_code, target=target_code)
                translation = translator.translate(word)
            else:
                # Using old googletrans (fallback)
                temp_translator = Translator()
                result = temp_translator.translate(word, src=source_code, dest=target_code)
                if hasattr(result, 'text'):
                    translation = result.text
                else:
                    translation = str(result)
            
            if translation and translation.strip():
                self.translation_entry.setText(translation.strip())
            else:
                raise Exception("Empty translation result")
                
        except Exception as e:
            print(f"Translation error: {e}")
            self.translation_entry.setText("Translation error")

    def toggle_source_language(self):
        """Toggle source language"""
        self.source_lang_index = (self.source_lang_index + 1) % len(self.source_languages)
        self.source_lang_button.setText(self.source_languages[self.source_lang_index])
        self.translate_word()

    def toggle_target_language(self):
        """Toggle target language"""
        self.target_lang_index = (self.target_lang_index + 1) % len(self.target_languages)
        self.target_lang_button.setText(self.target_languages[self.target_lang_index])
        self.translate_word()

    def open_settings(self):
        """Open language settings dialog"""
        current_settings = {
            'source_languages': self.source_languages,
            'target_languages': self.target_languages
        }
        
        dialog = LanguageSettingsDialog(self, current_settings)
        if dialog.exec() == QDialog.Accepted:
            source_langs, target_langs = dialog.get_selected_languages()
            
            if not source_langs or not target_langs:
                QMessageBox.warning(self, "Warning", "Please select at least one language for each button.")
                return
            
            self.source_languages = source_langs
            self.target_languages = target_langs
            
            # Reset indices if current selection is out of bounds
            if self.source_lang_index >= len(self.source_languages):
                self.source_lang_index = 0
            if self.target_lang_index >= len(self.target_languages):
                self.target_lang_index = 0
            
            # Update button texts
            self.source_lang_button.setText(self.source_languages[self.source_lang_index])
            self.target_lang_button.setText(self.target_languages[self.target_lang_index])
            
            self.save_settings()
            self.translate_word()

    def toggle_title_bar(self):
        if self.always_on_top:
            self.setWindowFlags(Qt.Window)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.setMask(QRegion())
            self.always_on_top = False
            self.content_widget.setStyleSheet("""
            background-color: #2E2E2E;
            border-radius: 7px;
        """)
        else:
            self.move(self.x(), self.y() + 30)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.always_on_top = True
            self.apply_rounded_mask()

        self.setGeometry(self.x(), self.y(), self.width(), self.height())
        self.show()

    def apply_rounded_mask(self):
        radius = 8
        rect = self.rect()

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def save_to_json(self):
        """Save the translated word to JSON file"""
        if self.word_entry.text() == "":
            return
        
        word = self.word_entry.text().strip()
        translation = self.translation_entry.text().strip()
        
        source_lang = self.source_languages[self.source_lang_index]
        target_lang = self.target_languages[self.target_lang_index]
        
        # Use relative path for JSON file
        json_file = os.path.join(DATA_DIR, f"dict_{source_lang}_{target_lang}.json")
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            
            # Load existing data
            data = []
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, Exception) as e:
                    print(f"Error reading JSON file: {e}")
                    # If file is corrupted, start with empty data
                    data = []
            
            # Add new data
            new_entry = {
                'word': word,
                'meaning': translation
            }
            
            # Check if word already exists
            word_exists = False
            for i, entry in enumerate(data):
                if entry.get('word', '').lower() == word.lower():
                    data[i] = new_entry  # Update
                    word_exists = True
                    break
            
            if not word_exists:
                data.append(new_entry)  # Add new
            
            # Save to file with proper error handling
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Word saved successfully: {word} -> {translation}")
            
            # Refresh table if it's open
            if self.table_window and self.table_window.isVisible():
                self.table_window.refresh_table()
            
        except Exception as e:
            print(f"JSON save error: {e}")
            QMessageBox.critical(self, "Save Error", f"Could not save word: {str(e)}")
            return

        # Clear inputs only if save was successful
        self.word_entry.clear()
        self.word_entry.setFocus()
        self.translation_entry.clear()

    def open_table_editor(self):
        """Open table editor window"""
        source_lang = self.source_languages[self.source_lang_index]
        target_lang = self.target_languages[self.target_lang_index]
        
        if self.table_window is None or not self.table_window.isVisible():
            self.table_window = TableEditorWindow(self, source_lang, target_lang)
            self.table_window.show()
        else:
            self.table_window.raise_()
            self.table_window.activateWindow()

    def closeEvent(self, event):
        """Override the close event to hide the window instead of quitting the application"""
        self.save_settings()
        if self.table_window:
            self.table_window.close()
        # Hide the window instead of closing it
        event.accept()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DictionaryApp()
    window.show()
    sys.exit(app.exec())