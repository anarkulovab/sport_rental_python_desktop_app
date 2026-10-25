from PyQt6.QtWidgets import QApplication, QWidget
from ui_py_files.login import Ui_Form as LoginForm
from bd import *


class LoginWin(QWidget, LoginForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.log_in)
        self.pushButton_2.clicked.connect(self.open_catalog)

    def log_in(self):
        try:
            login = self.lineEdit.text()
            passw = self.lineEdit_2.text()
            sql = "SELECT u.user_id, r.role_name FROM users u JOIN roles r ON u.role_id = r.role_id WHERE u.login = %s AND u.password = %s"
            result = select_query(sql, (login, passw))

            if result:
                user_id, role = result[0]
                if role == "Администратор":
                    from admin_win import AdminWin
                    self.role_win = AdminWin(user_id)
                elif role == "Сотрудник":
                    from employee_win import EmployeeWin
                    self.role_win = EmployeeWin(user_id)
                elif role == "Клиент":
                    from guest_client_win import ClientWin
                    self.role_win = ClientWin(user_id)
                else:
                    from guest_client_win import ClientWin
                    self.role_win = ClientWin()
                self.role_win.show()
                self.close()
            else:
                self.open_catalog()
        except Exception as e:
            print(e)

    def open_catalog(self):
        try:
            from guest_client_win import ClientWin
            self.guest_win = ClientWin()
            self.guest_win.show()
            self.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginWin()
    window.show()
    sys.exit(app.exec())