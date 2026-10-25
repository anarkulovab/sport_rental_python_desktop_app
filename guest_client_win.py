from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from main import LoginWin
from ui_py_files.guest_client_ui import Ui_MainWindow as GuestClientUI
from product_card_widget import ProductCardWidget
from bd import *


class ClientWin(QMainWindow, GuestClientUI):
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.all_equipment = []

        self.comboBox.addItems(["Без сортировки", "По возрастанию", "По убыванию"])

        if user_id:
            self.pushButton.setText("Выйти")
            self.tabWidget.setTabVisible(1, True)
            user_data = select_query("SELECT full_name FROM users WHERE user_id = %s", (user_id,))
            if user_data:
                self.label.setText(f"Добро пожаловать, {user_data[0][0]}!")
            self.load_my_requests()
            self.tabWidget.currentChanged.connect(self.on_tab_changed)
        else:
            self.pushButton.setText("Войти")
            self.tabWidget.setTabVisible(1, False)
            self.label.setText("Добро пожаловать, Гость!")

        self.set_catalog()
        self.pushButton.clicked.connect(self.open_login)
        self.lineEdit.textChanged.connect(self.search)
        self.comboBox.currentTextChanged.connect(self.sort)

    def set_catalog(self):
        try:
            sql = """
            SELECT 
                e.equipment_id,
                e.name,
                e.image_url,
                e.rental_price_per_day,
                CASE 
                    WHEN e.is_available = 1 THEN 'В наличии'
                    ELSE CONCAT('Пункт: ', p.name)
                END as status_or_location
            FROM equipment e
            LEFT JOIN pickup_points p ON e.point_id = p.point_id
            """
            self.all_equipment = select_query(sql)
            self.display_equipment(self.all_equipment)
        except Exception as e:
            print(e)

    def display_equipment(self, equipment_list):
        try:
            for i in reversed(range(self.gridLayout.count())):
                item = self.gridLayout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()

            row = 0
            col = 0
            for equipment in equipment_list:
                card = ProductCardWidget(equipment, self.user_id, self)
                self.gridLayout.addWidget(card, row, col)
                col += 1
                if col > 2:
                    col = 0
                    row += 1
        except Exception as e:
            print(e)

    def search(self):
        try:
            search_text = self.lineEdit.text().lower()
            if not search_text:
                self.sort(self.comboBox.currentText())
                return

            filtered = [eq for eq in self.all_equipment if search_text in eq[1].lower()]
            self.sort_current_list(filtered, self.comboBox.currentText())
        except Exception as e:
            print(e)

    def sort(self, sort_type):
        try:
            self.sort_current_list(self.all_equipment, sort_type)
        except Exception as e:
            print(e)

    def sort_current_list(self, equipment_list, sort_type):
        try:
            if sort_type == "По возрастанию":
                sorted_list = sorted(equipment_list, key=lambda x: float(x[3]))
            elif sort_type == "По убыванию":
                sorted_list = sorted(equipment_list, key=lambda x: float(x[3]), reverse=True)
            else:
                sorted_list = equipment_list

            if self.lineEdit.text():
                search_text = self.lineEdit.text().lower()
                sorted_list = [eq for eq in sorted_list if search_text in eq[1].lower()]

            self.display_equipment(sorted_list)
        except Exception as e:
            print(e)

    def load_my_requests(self):
        try:
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(
                ["ID", "Оборудование", "Дата начала", "Дата окончания", "Статус"])

            sql = """
            SELECT 
                rr.request_id,
                e.name,
                rr.start_date,
                rr.end_date,
                rs.status_name
            FROM rental_requests rr
            JOIN equipment e ON rr.equipment_id = e.equipment_id
            JOIN rental_statuses rs ON rr.status_id = rs.status_id
            JOIN customers c ON rr.customer_id = c.customer_id
            WHERE c.user_id = %s
            """
            requests = select_query(sql, (self.user_id,))

            self.tableWidget.setRowCount(len(requests))
            for i, req in enumerate(requests):
                for j in range(5):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(req[j])))
        except Exception as e:
            print(e)

    def on_tab_changed(self, index):
        try:
            if index == 1 and self.user_id:
                self.load_my_requests()
        except Exception as e:
            print(e)

    def open_login(self):
        try:
            if self.user_id:
                reply = QMessageBox.question(self, "Выход", "Вы действительно хотите выйти?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.login_win = LoginWin()
                    self.login_win.show()
                    self.close()
            else:
                self.login_win = LoginWin()
                self.login_win.show()
                self.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ClientWin(2)
    window.show()
    sys.exit(app.exec())
