from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from ui_py_files.employee_ui import Ui_EmployeeWindow
from bd import *
from main import LoginWin

class EmployeeWin(QMainWindow, Ui_EmployeeWindow):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        user_data = select_query("SELECT full_name FROM users WHERE user_id = %s", (user_id,))
        if user_data:
            self.label.setText(f"Сотрудник: {user_data[0][0]}")

        self.comboBox.addItems(
            ["Все статусы", "Ожидание подтверждения", "Подтверждена", "Выдана", "Завершена", "Отменена"])

        self.load_requests()

        self.pushButton.clicked.connect(self.logout)
        self.lineEdit.textChanged.connect(self.search)
        self.comboBox.currentTextChanged.connect(self.filter_by_status)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID заявки", "Клиент", "Оборудование", "Дата начала", "Дата окончания", "Статус", "Действие"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setColumnWidth(6, 150)

    def load_requests(self):
        try:
            sql = """
            SELECT 
                rr.request_id,
                u.full_name,
                e.name,
                DATE_FORMAT(rr.start_date, '%d.%m.%Y'),
                DATE_FORMAT(rr.end_date, '%d.%m.%Y'),
                rs.status_name,
                rr.request_id
            FROM rental_requests rr
            JOIN customers c ON rr.customer_id = c.customer_id
            JOIN users u ON c.user_id = u.user_id
            JOIN equipment e ON rr.equipment_id = e.equipment_id
            JOIN rental_statuses rs ON rr.status_id = rs.status_id
            ORDER BY rr.created_at DESC
            """
            self.all_requests = select_query(sql)
            self.display_requests(self.all_requests)
        except Exception as e:
            print(e)

    def display_requests(self, requests):
        try:
            self.tableWidget.setRowCount(len(requests))
            for i, req in enumerate(requests):
                for j in range(6):
                    item = QtWidgets.QTableWidgetItem(str(req[j]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.tableWidget.setItem(i, j, item)

                change_btn = QtWidgets.QPushButton("Изменить статус")
                change_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(153, 148, 179);
                        color: white;
                        border-radius: 10px;
                        padding: 5px;
                    }
                """)
                change_btn.clicked.connect(lambda checked, req_id=req[6]: self.change_status(req_id))
                self.tableWidget.setCellWidget(i, 6, change_btn)
        except Exception as e:
            print(e)

    def search(self):
        try:
            search_text = self.lineEdit.text().lower()
            if not search_text:
                self.filter_by_status(self.comboBox.currentText())
                return

            filtered = [req for req in self.all_requests if
                        search_text in req[1].lower() or search_text in req[2].lower()]
            self.filter_current_list(filtered, self.comboBox.currentText())
        except Exception as e:
            print(e)

    def filter_by_status(self, status):
        try:
            self.filter_current_list(self.all_requests, status)
        except Exception as e:
            print(e)

    def filter_current_list(self, requests, status):
        try:
            if status != "Все статусы":
                filtered = [req for req in requests if req[5] == status]
            else:
                filtered = requests

            if self.lineEdit.text():
                search_text = self.lineEdit.text().lower()
                filtered = [req for req in filtered if search_text in req[1].lower() or search_text in req[2].lower()]

            self.display_requests(filtered)
        except Exception as e:
            print(e)

    def change_status(self, request_id):
        try:
            statuses = ["Ожидание подтверждения", "Подтверждена", "Выдана", "Завершена", "Отменена"]
            status, ok = QtWidgets.QInputDialog.getItem(self, "Изменение статуса", "Выберите новый статус:", statuses,
                                                        0, False)

            if ok and status:
                status_id = statuses.index(status) + 1

                employee_id = select_query("SELECT employee_id FROM employees WHERE user_id = %s", (self.user_id,))
                if employee_id:
                    update_query("UPDATE rental_requests SET status_id = %s, employee_id = %s WHERE request_id = %s",
                                 (status_id, employee_id[0][0], request_id))

                    if status == "Выдана":
                        update_query(
                            "UPDATE equipment SET is_available = 0 WHERE equipment_id = (SELECT equipment_id FROM rental_requests WHERE request_id = %s)",
                            (request_id,))
                    elif status == "Завершена":
                        update_query(
                            "UPDATE equipment SET is_available = 1 WHERE equipment_id = (SELECT equipment_id FROM rental_requests WHERE request_id = %s)",
                            (request_id,))

                    QMessageBox.information(self, "Успех", f"Статус заявки №{request_id} изменен на '{status}'")
                    self.load_requests()
        except Exception as e:
            print(e)

    def logout(self):
        self.login_win = LoginWin()
        self.login_win.show()
        self.close()