from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from main import LoginWin
from ui_py_files.admin_ui import Ui_AdminWindow
from bd import *

class AdminWin(QMainWindow, Ui_AdminWindow):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        user_data = select_query("SELECT full_name FROM users WHERE user_id = %s", (user_id,))
        if user_data:
            self.label.setText(f"Администратор: {user_data[0][0]}")

        types = select_query("SELECT type_name FROM equipment_types")
        self.comboBox.addItem("Все типы")
        for type_name in types:
            self.comboBox.addItem(type_name[0])

        self.load_equipment()

        self.pushButton.clicked.connect(self.logout)
        self.pushButton_2.clicked.connect(self.add_equipment)
        self.lineEdit.textChanged.connect(self.search)
        self.comboBox.currentTextChanged.connect(self.filter_by_type)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название", "Тип", "Цена/сутки", "Пункт выдачи", "Доступно", "Действия"])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)

    def load_equipment(self):
        try:
            sql = """
            SELECT 
                e.equipment_id,
                e.name,
                et.type_name,
                e.rental_price_per_day,
                p.name,
                CASE WHEN e.is_available = 1 THEN 'Да' ELSE 'Нет' END,
                e.equipment_id
            FROM equipment e
            LEFT JOIN equipment_types et ON e.type_id = et.type_id
            LEFT JOIN pickup_points p ON e.point_id = p.point_id
            ORDER BY e.equipment_id
            """
            self.all_equipment = select_query(sql)
            self.display_equipment(self.all_equipment)
        except Exception as e:
            print(e)

    def display_equipment(self, equipment):
        try:
            self.tableWidget.setRowCount(len(equipment))
            for i, eq in enumerate(equipment):
                for j in range(6):
                    item = QtWidgets.QTableWidgetItem(str(eq[j]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

                edit_btn = QtWidgets.QPushButton("Редактировать")
                delete_btn = QtWidgets.QPushButton("Удалить")

                edit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(153, 148, 179);
                        color: white;
                        border-radius: 10px;
                        padding: 5px;
                        font-size: 14px;
                        min-width: 110px;
                    }
                """)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(200, 100, 100);
                        color: white;
                        border-radius: 10px;
                        padding: 5px;
                        font-size: 14px;
                        min-width: 70px;
                    }
                """)

                edit_btn.clicked.connect(lambda checked, eq_id=eq[6]: self.edit_equipment(eq_id))
                delete_btn.clicked.connect(lambda checked, eq_id=eq[6]: self.delete_equipment(eq_id))

                widget = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout(widget)
                layout.addWidget(edit_btn)
                layout.addWidget(delete_btn)
                layout.setContentsMargins(5, 5, 5, 5)
                widget.setLayout(layout)
                self.tableWidget.setCellWidget(i, 6, widget)
        except Exception as e:
            print(e)

    def search(self):
        try:
            search_text = self.lineEdit.text().lower()
            if not search_text:
                self.filter_by_type(self.comboBox.currentText())
                return

            filtered = [eq for eq in self.all_equipment if search_text in eq[1].lower()]
            self.filter_current_list(filtered, self.comboBox.currentText())
        except Exception as e:
            print(e)

    def filter_by_type(self, eq_type):
        try:
            self.filter_current_list(self.all_equipment, eq_type)
        except Exception as e:
            print(e)

    def filter_current_list(self, equipment, eq_type):
        try:
            if eq_type != "Все типы":
                filtered = [eq for eq in equipment if eq[2] == eq_type]
            else:
                filtered = equipment

            if self.lineEdit.text():
                search_text = self.lineEdit.text().lower()
                filtered = [eq for eq in filtered if search_text in eq[1].lower()]

            self.display_equipment(filtered)
        except Exception as e:
            print(e)

    def add_equipment(self):
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, \
                QDialogButtonBox, QCheckBox

            dialog = QDialog(self)
            dialog.setWindowTitle("Добавление оборудования")
            dialog.setModal(True)
            dialog.resize(400, 350)

            layout = QVBoxLayout(dialog)

            name_layout = QHBoxLayout()
            name_layout.addWidget(QLabel("Название:"))
            name_edit = QLineEdit()
            name_layout.addWidget(name_edit)
            layout.addLayout(name_layout)

            type_layout = QHBoxLayout()
            type_layout.addWidget(QLabel("Тип:"))
            type_combo = QComboBox()
            types = select_query("SELECT type_name FROM equipment_types")
            for t in types:
                type_combo.addItem(t[0])
            type_layout.addWidget(type_combo)
            layout.addLayout(type_layout)

            price_layout = QHBoxLayout()
            price_layout.addWidget(QLabel("Цена за сутки:"))
            price_spin = QSpinBox()
            price_spin.setRange(100, 10000)
            price_spin.setSuffix(" ₽")
            price_layout.addWidget(price_spin)
            layout.addLayout(price_layout)

            point_layout = QHBoxLayout()
            point_layout.addWidget(QLabel("Пункт выдачи:"))
            point_combo = QComboBox()
            points = select_query("SELECT name FROM pickup_points")
            for p in points:
                point_combo.addItem(p[0])
            point_layout.addWidget(point_combo)
            layout.addLayout(point_layout)

            image_layout = QHBoxLayout()
            image_layout.addWidget(QLabel("Путь к изображению:"))
            image_edit = QLineEdit()
            image_edit.setPlaceholderText("images/название.jpg")
            image_layout.addWidget(image_edit)
            layout.addLayout(image_layout)

            available_check = QCheckBox("Доступно для аренды")
            available_check.setChecked(True)
            layout.addWidget(available_check)

            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                name = name_edit.text()
                type_name = type_combo.currentText()
                price = price_spin.value()
                point_name = point_combo.currentText()
                image_url = image_edit.text()
                is_available = 1 if available_check.isChecked() else 0

                if name and type_name and point_name:
                    type_id = select_query("SELECT type_id FROM equipment_types WHERE type_name = %s", (type_name,))[0][
                        0]
                    point_id = select_query("SELECT point_id FROM pickup_points WHERE name = %s", (point_name,))[0][0]

                    sql = """
                    INSERT INTO equipment (name, type_id, rental_price_per_day, point_id, image_url, is_available)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    update_query(sql, (name, type_id, price, point_id, image_url, is_available))

                    QMessageBox.information(self, "Успех", "Оборудование добавлено")
                    self.load_equipment()
                else:
                    QMessageBox.warning(self, "Ошибка", "Заполните все поля")
        except Exception as e:
            print(e)

    def edit_equipment(self, equipment_id):
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, \
                QDialogButtonBox, QCheckBox

            current = select_query("""
                SELECT e.name, et.type_name, e.rental_price_per_day, p.name, e.image_url, e.is_available 
                FROM equipment e
                LEFT JOIN equipment_types et ON e.type_id = et.type_id
                LEFT JOIN pickup_points p ON e.point_id = p.point_id
                WHERE e.equipment_id = %s
            """, (equipment_id,))[0]

            dialog = QDialog(self)
            dialog.setWindowTitle("Редактирование оборудования")
            dialog.setModal(True)
            dialog.resize(400, 350)

            layout = QVBoxLayout(dialog)

            name_layout = QHBoxLayout()
            name_layout.addWidget(QLabel("Название:"))
            name_edit = QLineEdit(current[0])
            name_layout.addWidget(name_edit)
            layout.addLayout(name_layout)

            type_layout = QHBoxLayout()
            type_layout.addWidget(QLabel("Тип:"))
            type_combo = QComboBox()
            types = select_query("SELECT type_name FROM equipment_types")
            type_index = 0
            for i, t in enumerate(types):
                type_combo.addItem(t[0])
                if t[0] == current[1]:
                    type_index = i
            type_combo.setCurrentIndex(type_index)
            type_layout.addWidget(type_combo)
            layout.addLayout(type_layout)

            price_layout = QHBoxLayout()
            price_layout.addWidget(QLabel("Цена за сутки:"))
            price_spin = QSpinBox()
            price_spin.setRange(100, 10000)
            price_spin.setValue(int(current[2]))
            price_spin.setSuffix(" ₽")
            price_layout.addWidget(price_spin)
            layout.addLayout(price_layout)

            point_layout = QHBoxLayout()
            point_layout.addWidget(QLabel("Пункт выдачи:"))
            point_combo = QComboBox()
            points = select_query("SELECT name FROM pickup_points")
            point_index = 0
            for i, p in enumerate(points):
                point_combo.addItem(p[0])
                if p[0] == current[3]:
                    point_index = i
            point_combo.setCurrentIndex(point_index)
            point_layout.addWidget(point_combo)
            layout.addLayout(point_layout)

            image_layout = QHBoxLayout()
            image_layout.addWidget(QLabel("Путь к изображению:"))
            image_edit = QLineEdit(current[4] if current[4] else "")
            image_layout.addWidget(image_edit)
            layout.addLayout(image_layout)

            available_check = QCheckBox("Доступно для аренды")
            available_check.setChecked(bool(current[5]))
            layout.addWidget(available_check)

            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                name = name_edit.text()
                type_name = type_combo.currentText()
                price = price_spin.value()
                point_name = point_combo.currentText()
                image_url = image_edit.text()
                is_available = 1 if available_check.isChecked() else 0

                if name and type_name and point_name:
                    type_id = select_query("SELECT type_id FROM equipment_types WHERE type_name = %s", (type_name,))[0][
                        0]
                    point_id = select_query("SELECT point_id FROM pickup_points WHERE name = %s", (point_name,))[0][0]

                    sql = """
                    UPDATE equipment 
                    SET name = %s, type_id = %s, rental_price_per_day = %s, point_id = %s, image_url = %s, is_available = %s
                    WHERE equipment_id = %s
                    """
                    update_query(sql, (name, type_id, price, point_id, image_url, is_available, equipment_id))

                    QMessageBox.information(self, "Успех", "Оборудование обновлено")
                    self.load_equipment()
                else:
                    QMessageBox.warning(self, "Ошибка", "Заполните все поля")
        except Exception as e:
            print(e)

    def delete_equipment(self, equipment_id):
        try:
            reply = QMessageBox.question(self, "Удаление", "Вы уверены, что хотите удалить это оборудование?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                check = \
                select_query("SELECT COUNT(*) FROM rental_requests WHERE equipment_id = %s", (equipment_id,))[0][0]
                if check > 0:
                    QMessageBox.warning(self, "Ошибка", "Нельзя удалить оборудование, на которое есть заявки")
                    return

                update_query("DELETE FROM equipment WHERE equipment_id = %s", (equipment_id,))
                QMessageBox.information(self, "Успех", "Оборудование удалено")
                self.load_equipment()
        except Exception as e:
            print(e)

    def logout(self):
        self.login_win = LoginWin()
        self.login_win.show()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AdminWin(3)
    window.show()
    sys.exit(app.exec())