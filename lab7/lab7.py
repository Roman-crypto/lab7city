import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTableWidget, QTableWidgetItem, QToolBar, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class CityDialog(QDialog):
    def __init__(self, parent=None, city_data=None):
        super(CityDialog, self).__init__(parent)
        self.setWindowTitle("Дані про нове місто" if city_data is None else "Редагувати місто")

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.country_edit = QLineEdit()
        self.region_edit = QLineEdit()
        self.population_edit = QLineEdit()
        self.income_edit = QLineEdit()
        self.area_edit = QLineEdit()
        self.port_check = QCheckBox("Місто має порт")
        self.airport_check = QCheckBox("Місто має аеропорт")

        self.form_layout.addRow("Назва міста", self.name_edit)
        self.form_layout.addRow("Країна", self.country_edit)
        self.form_layout.addRow("Регіон", self.region_edit)
        self.form_layout.addRow("Кількість мешканців", self.population_edit)
        self.form_layout.addRow("Річний дохід, грн", self.income_edit)
        self.form_layout.addRow("Площа, кв. км", self.area_edit)
        self.form_layout.addRow(self.port_check)
        self.form_layout.addRow(self.airport_check)

        if city_data:
            self.name_edit.setText(city_data['name'])
            self.country_edit.setText(city_data['country'])
            self.region_edit.setText(city_data['region'])
            self.population_edit.setText(city_data['population'])
            self.income_edit.setText(city_data['income'])
            self.area_edit.setText(city_data['area'])
            self.port_check.setChecked(city_data['port'])
            self.airport_check.setChecked(city_data['airport'])

        self.layout.addLayout(self.form_layout)

        self.button_layout = QVBoxLayout()
        self.ok_button = QPushButton("Ок")
        self.cancel_button = QPushButton("Скасувати")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Лабораторна робота №9")
        self.setGeometry(100, 100, 800, 400)

        self.create_menu()
        self.create_toolbar()
        self.create_table()

    def create_menu(self):
        self.menu = self.menuBar().addMenu("Файл")
        exit_action = QAction("Вихід", self)
        exit_action.triggered.connect(self.close)
        self.menu.addAction(exit_action)

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        add_action = QAction("Додати запис", self)
        add_action.triggered.connect(self.add_record)
        self.toolbar.addAction(add_action)

        edit_action = QAction("Змінити запис", self)
        edit_action.triggered.connect(self.edit_record)
        self.toolbar.addAction(edit_action)

        delete_action = QAction("Видалити запис", self)
        delete_action.triggered.connect(self.delete_record)
        self.toolbar.addAction(delete_action)

        clear_action = QAction("Очистити таблицю", self)
        clear_action.triggered.connect(self.clear_table)
        self.toolbar.addAction(clear_action)

    def create_table(self):
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["Назва", "Країна", "Регіон", "Мешканців", "Річн. дохід", "Площа", "Порт", "Аеропорт"])
        self.setCentralWidget(self.table)

    def add_record(self):
        dialog = CityDialog(self)
        if dialog.exec():
            name = dialog.name_edit.text()
            country = dialog.country_edit.text()
            region = dialog.region_edit.text()
            population = dialog.population_edit.text()
            income = dialog.income_edit.text()
            area = dialog.area_edit.text()
            port = dialog.port_check.isChecked()
            airport = dialog.airport_check.isChecked()

            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(name))
            self.table.setItem(row_position, 1, QTableWidgetItem(country))
            self.table.setItem(row_position, 2, QTableWidgetItem(region))
            self.table.setItem(row_position, 3, QTableWidgetItem(population))
            self.table.setItem(row_position, 4, QTableWidgetItem(income))
            self.table.setItem(row_position, 5, QTableWidgetItem(area))
            self.table.setItem(row_position, 6, QTableWidgetItem("Так" if port else "Ні"))
            self.table.setItem(row_position, 7, QTableWidgetItem("Так" if airport else "Ні"))

    def edit_record(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            city_data = {
                'name': self.table.item(selected_row, 0).text(),
                'country': self.table.item(selected_row, 1).text(),
                'region': self.table.item(selected_row, 2).text(),
                'population': self.table.item(selected_row, 3).text(),
                'income': self.table.item(selected_row, 4).text(),
                'area': self.table.item(selected_row, 5).text(),
                'port': self.table.item(selected_row, 6).text() == "Так",
                'airport': self.table.item(selected_row, 7).text() == "Так"
            }

            dialog = CityDialog(self, city_data)
            if dialog.exec():
                self.table.setItem(selected_row, 0, QTableWidgetItem(dialog.name_edit.text()))
                self.table.setItem(selected_row, 1, QTableWidgetItem(dialog.country_edit.text()))
                self.table.setItem(selected_row, 2, QTableWidgetItem(dialog.region_edit.text()))
                self.table.setItem(selected_row, 3, QTableWidgetItem(dialog.population_edit.text()))
                self.table.setItem(selected_row, 4, QTableWidgetItem(dialog.income_edit.text()))
                self.table.setItem(selected_row, 5, QTableWidgetItem(dialog.area_edit.text()))
                self.table.setItem(selected_row, 6, QTableWidgetItem("Так" if dialog.port_check.isChecked() else "Ні"))
                self.table.setItem(selected_row, 7, QTableWidgetItem("Так" if dialog.airport_check.isChecked() else "Ні"))
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, виберіть рядок для редагування.")

    def delete_record(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, виберіть рядок для видалення.")

    def clear_table(self):
        self.table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


