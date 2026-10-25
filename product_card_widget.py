from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from ui_py_files.card_product import Ui_Form as SportCard
from bd import *

class ProductCardWidget(QWidget):
    def __init__(self, equipment_data, user_id=None, parent=None):
        super().__init__(parent)
        try:
            self.ui = SportCard()
            self.ui.setupUi(self)
            self.equipment_id = equipment_data[0]
            self.user_id = user_id

            if equipment_data[2] and equipment_data[2] != "images/":
                pixmap = QPixmap(equipment_data[2]).scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            else:
                pixmap = QPixmap("images/bike.png").scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

            self.ui.label.setPixmap(pixmap)
            self.ui.label_2.setText(equipment_data[1])
            self.ui.label_4.setText(f"{equipment_data[3]}₽ в сутки")
            self.ui.label_3.setText(equipment_data[4])

            if "Не в наличии" in equipment_data[4] or "Пункт" in equipment_data[4]:
                self.setStyleSheet("background-color: lightgray;")

            if user_id:
                self.ui.pushButton.clicked.connect(self.create_request)
            self.setFixedSize(220, 320)
        except Exception as e:
            print(e)

    def create_request(self):
        try:
            sql = "SELECT customer_id FROM customers WHERE user_id = %s"
            customer = select_query(sql, (self.user_id,))

            if customer:
                customer_id = customer[0][0]
                from PyQt6.QtWidgets import QInputDialog, QMessageBox
                days, ok = QInputDialog.getInt(self, "Аренда", "Введите количество дней аренды:", 1, 1, 30)
                if ok:
                    from datetime import datetime, timedelta
                    start_date = datetime.now().date()
                    end_date = start_date + timedelta(days=days)

                    sql = """
                    INSERT INTO rental_requests (customer_id, equipment_id, status_id, start_date, end_date, created_at)
                    VALUES (%s, %s, 1, %s, %s, NOW())
                    """
                    update_query(sql, (customer_id, self.equipment_id, start_date, end_date))
                    QMessageBox.information(self, "Успех", "Заявка создана и ожидает подтверждения")
        except Exception as e:
            print(e)
