from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QCheckBox, QPushButton

class SettingsWindow(QWidget):
    """A window for application settings."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # Vault Location
        self.vault_location_edit = QLineEdit()
        form_layout.addRow("Vault Location:", self.vault_location_edit)

        # Theme Selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        form_layout.addRow("Theme:", self.theme_combo)

        # AI Toggle
        self.ai_toggle_check = QCheckBox("Enable AI Features")
        form_layout.addRow("AI:", self.ai_toggle_check)

        self.layout.addLayout(form_layout)

        # Save Button
        self.save_button = QPushButton("Save")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_settings)

    def save_settings(self):
        """Saves the current settings."""
        # This is a placeholder for now.
        print("Settings saved (placeholder).")
        self.close()
