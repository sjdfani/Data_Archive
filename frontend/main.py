from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from login_register import Ui_login_register
from DataArchive import Ui_MainWindow
import datetime
import requests
import _thread
import time
import webbrowser

# ============= Login class ======================
login_url = "http://localhost:8000/user_info/login/"
create_url = "http://localhost:8000/user_info/create/"
check_admin_url = "http://localhost:8000/user_info/check-admin/"
# ============== main class =====================

get_profile_data_url = "http://localhost:8000/user_info/get-user-info/"
update_profile_data_url = "http://localhost:8000/user_info/update-user/"
send_data_url = "http://localhost:8000/payment/create/"
get_all_data_url = "http://localhost:8000/payment/get-all-payment/"
get_user_data = "http://localhost:8000/payment/get-by-username/"
delete_data_url = "http://localhost:8000/payment/delete-data/"
users_url = "http://localhost:8000/user_info/all-del-user/"
create_feedback_url = "http://localhost:8000/feedback/create/"
get_feedback_url = "http://localhost:8000/feedback/get-all/"
del_feedback_url = "http://localhost:8000/feedback/delete/"
admin_url = "http://localhost:8000/admin/"

# ===============================================
delivery_username = None
delivery_payment_data = None
log_out_obj = None


class DataArchive(QMainWindow):
    h_url_frame = False
    h_profile_edit = False
    h_api_edit = False
    h_get_data = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Data Archive")
        self.setWindowIcon(QIcon(r"photo/download.jfif"))

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.app_connection()
        self.app_tools()

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def app_connection(self):
        self.home_connection()
        self.profile_connection()
        self.setting_connection()
        self.send_data_connection()
        self.get_data_connection()
        self.users_connection()
        self.feedback_connection()

    def app_tools(self):
        self.home_tools()
        self.setting_tools()
        self.profile_tools()
        self.send_data_tools()
        self.get_data_tools()
        self.feedback_tools()
        self.users_tools()

    def errors_msg(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.show()

    def info_msg(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.show()

    # =============================
    def home_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

    def home_tools(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        timer = QTimer(self)
        timer.timeout.connect(self.set_time)
        timer.start(1000)
        self.set_date()
        self.ui.users_btn.setEnabled(False)
        self.ui.setting_btn.setEnabled(False)

    def home_connection(self):
        _thread.start_new_thread(self.connection, (False,))
        _thread.start_new_thread(self.func_tools, (2,))
        self.ui.home_btn.clicked.connect(self.home_func)
        self.ui.profile_btn.clicked.connect(self.profile_func)
        self.ui.setting_btn.clicked.connect(self.setting_func)
        self.ui.send_data_btn.clicked.connect(self.send_data_func)
        self.ui.get_data_btn.clicked.connect(self.get_data_func)
        self.ui.users_btn.clicked.connect(self.users_func)
        self.ui.feedback_btn.clicked.connect(self.feedback_func)
        self.ui.info_btn.clicked.connect(self.info_func)
        self.ui.log_out_btn.clicked.connect(self.logout_func)
        self.ui.api_btn.clicked.connect(self.api_frame)
        self.ui.connection_btn.clicked.connect(self.check_connect)

    def set_detail_connection(self, state):
        if state:
            icon = QIcon()
            icon.addPixmap(QPixmap("photo/icons8-wi-fi-green.png"), QIcon.Normal, QIcon.Off)
            self.ui.connection_btn.setIcon(icon)
            self.ui.connection_btn.setText(" Connect")
            self.ui.connection_btn.setStyleSheet("QPushButton{\n"
                                                 "color: rgb(255, 255, 255);\n"
                                                 "background-color: rgb(0, 115, 0);\n"
                                                 "\n"
                                                 "border-radius:10px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "    color: rgb(255, 255, 255);\n"
                                                 "border-radius:5px;\n"
                                                 "}\n"
                                                 "")
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap("photo/icons8-wi-fi-red.png"), QIcon.Normal, QIcon.Off)
            self.ui.connection_btn.setIcon(icon)
            self.ui.connection_btn.setText("Disconnect")
            self.ui.connection_btn.setStyleSheet("QPushButton{\n"
                                                 "color: rgb(255, 255, 255);\n"
                                                 "background-color: rgb(104, 0, 0);\n"
                                                 "\n"
                                                 "border-radius:10px;\n"
                                                 "}\n"
                                                 "QPushButton:hover{\n"
                                                 "    color: rgb(255, 255, 255);\n"
                                                 "border-radius:5px;\n"
                                                 "}\n"
                                                 "")

    def connection(self, state):
        url = "https://www.google.com"
        if state:
            try:
                requests.get(url=url)
                self.set_detail_connection(True)
            except requests.ConnectionError:
                self.set_detail_connection(False)
        else:
            while True:
                try:
                    requests.get(url=url)
                    self.set_detail_connection(True)
                except requests.ConnectionError:
                    self.set_detail_connection(False)
                time.sleep(3)

    def check_connect(self):
        _thread.start_new_thread(self.connection, (True,))

    def set_time(self):
        curr_time = QTime.currentTime()
        curr_time = curr_time.toString()
        self.ui.up_time_label.setText(curr_time)

    def set_date(self):
        curr_date = datetime.datetime.utcnow().date()
        curr_date = curr_date.strftime("%Y/%m/%d")
        self.ui.up_date_label.setText(curr_date)

    def func_tools(self, num):
        data = {"username": delivery_username}
        url = check_admin_url
        try:
            response = requests.post(url=url, json=data)
            res_data = response.json()
            if res_data['state'] == "is_admin":
                self.ui.users_btn.setEnabled(True)
                self.ui.setting_btn.setEnabled(True)
            else:
                self.ui.users_btn.setEnabled(False)
                self.ui.setting_btn.setEnabled(False)
        except requests.ConnectionError:
            _thread.start_new_thread(self.func_tools, (2,))

    # =============================
    def profile_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.profile)

    def profile_tools(self):
        self.ui.profile_username.setReadOnly(True)
        self.ui.profile_type.setReadOnly(True)
        self.ui.profile_email.setReadOnly(True)
        self.ui.profile_password.setReadOnly(True)
        self.ui.profile_fullname.setReadOnly(True)
        self.ui.profile_submit.setEnabled(False)

    def profile_connection(self):
        self.ui.profile_edit.clicked.connect(self.profile_edit_func)
        self.ui.profile_refresh.clicked.connect(self.refresh_detail_profile)
        self.ui.profile_submit.clicked.connect(self.submit_profile)

    def profile_edit_func(self):
        if not self.h_profile_edit:
            self.ui.profile_email.setReadOnly(False)
            self.ui.profile_password.setReadOnly(False)
            self.ui.profile_fullname.setReadOnly(False)
            self.ui.profile_submit.setEnabled(True)
            self.ui.profile_edit.setStyleSheet("QPushButton{\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "    background-color: rgb(0, 136, 0);\n"
                                               "border-radius:10px;\n"
                                               "}\n"
                                               "QPushButton:hover{\n"
                                               "    color: rgb(255, 255, 255);\n"
                                               "border-radius:5px;\n"
                                               "background-color: rgb(89, 89, 89);\n"
                                               "    \n"
                                               "}\n"
                                               "")
            self.h_profile_edit = True
        else:
            self.ui.profile_email.setReadOnly(True)
            self.ui.profile_password.setReadOnly(True)
            self.ui.profile_fullname.setReadOnly(True)
            self.ui.profile_submit.setEnabled(False)
            self.ui.profile_edit.setStyleSheet("QPushButton{\n"
                                               "color: rgb(0, 0, 0);\n"
                                               "    background-color: rgb(113, 113, 113);\n"
                                               "border-radius:10px;\n"
                                               "}\n"
                                               "QPushButton:hover{\n"
                                               "    color: rgb(255, 255, 255);\n"
                                               "border-radius:5px;\n"
                                               "background-color: rgb(89, 89, 89);\n"
                                               "}\n"
                                               "")
            self.h_profile_edit = False

    def refresh_detail_profile(self):
        _thread.start_new_thread(self.fill_detail_profile, (2,))

    def fill_detail_profile(self, num):
        self.ui.profile_refresh.setEnabled(False)
        self.ui.profile_state.setText("Please wait...")
        data = {"username": delivery_username}
        url = get_profile_data_url
        try:
            response = requests.post(url=url, json=data)
            res_data = response.json()
            self.ui.profile_username.setText(res_data["username"])
            self.ui.profile_fullname.setText(res_data["fullname"])
            self.ui.profile_email.setText(res_data["email"])
            self.ui.profile_password.setText(res_data["password"])
            self.ui.profile_type.setText(res_data["type"])
            self.ui.profile_state.setText("")
            self.ui.profile_refresh.setEnabled(True)
        except requests.ConnectionError:
            self.ui.profile_state.setText("Please check your Internet.")
        except:
            self.ui.profile_state.setText("Something went wrong.")

    def submit_profile(self):
        if len(self.ui.profile_fullname.text()) != 0:
            if len(self.ui.profile_email.text()) != 0:
                if len(self.ui.profile_password.text()) != 0:
                    _thread.start_new_thread(self.submit_process, (2,))
                else:
                    self.ui.profile_state.setText("Please write your password.")
            else:
                self.ui.profile_state.setText("Please write your email.")
        else:
            self.ui.profile_state.setText("Please write your fullname.")

    def submit_process(self, num):
        data = dict()
        self.ui.profile_submit.setEnabled(False)
        self.ui.profile_state.setText("Please wait...")
        url = update_profile_data_url
        data["username"] = self.ui.profile_username.text()
        data["fullname"] = self.ui.profile_fullname.text()
        data["email"] = self.ui.profile_email.text()
        data["password"] = self.ui.profile_password.text()
        try:
            request = requests.patch(url=url, json=data)
            req_data = request.json()
            print(req_data["state"])
            if req_data["state"] == "done":
                self.ui.profile_state.setText(req_data["message"])
            else:
                self.ui.profile_state.setText("Please try again.")
        except requests.ConnectionError:
            self.ui.profile_state.setText("Please check your Internet.")
        except:
            self.ui.profile_state.setText("Something went wrong.")
        self.ui.profile_submit.setEnabled(True)

    # =============================

    def setting_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.setting)
        self.ui.feedback_chart_btn.clicked.connect(self.feedbacks_chart_func)
        self.ui.setting_back_btn.clicked.connect(self.setting_func)
        self.fill_api_list()

    def setting_connection(self):
        self.ui.admin_btn.clicked.connect(self.admin_panel)
        self.ui.feedbacks_refresh_btn.clicked.connect(self.refresh_feedback_func)
        self.ui.feedbacks_delete_btn.clicked.connect(self.del_feedback_func)

    def setting_tools(self):
        self.ui.setting_login_url.setReadOnly(True)
        self.ui.setting_register_url.setReadOnly(True)
        self.ui.setting_checkbox_url.setReadOnly(True)
        self.ui.setting_profile_url.setReadOnly(True)
        self.ui.setting_send_data_url.setReadOnly(True)
        self.ui.setting_get_data_url.setReadOnly(True)
        self.ui.setting_del_data_url.setReadOnly(True)
        self.ui.setting_get_profile_url.setReadOnly(True)
        self.ui.setting_insert_feedback_url.setReadOnly(True)
        self.ui.setting_get_feedback_url.setReadOnly(True)
        self.ui.setting_del_feedback_url.setReadOnly(True)
        self.ui.setting_admin_url.setReadOnly(True)
        self.ui.setting_users_url.setReadOnly(True)
        self.ui.urls_frame.hide()
        self.ui.tableWidget_feedback.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def api_frame(self):
        if not self.h_url_frame:
            self.ui.urls_frame.show()
            self.h_url_frame = True
        else:
            self.ui.urls_frame.hide()
            self.h_url_frame = False

    def fill_api_list(self):
        self.ui.setting_login_url.setText(login_url)
        self.ui.setting_register_url.setText(create_url)
        self.ui.setting_checkbox_url.setText(check_admin_url)
        self.ui.setting_profile_url.setText(update_profile_data_url)
        self.ui.setting_get_profile_url.setText(get_profile_data_url)
        self.ui.setting_send_data_url.setText(send_data_url)
        self.ui.setting_get_data_url.setText(get_all_data_url)
        self.ui.setting_del_data_url.setText(delete_data_url)
        self.ui.setting_users_url.setText(users_url)
        self.ui.setting_insert_feedback_url.setText(create_feedback_url)
        self.ui.setting_get_feedback_url.setText(get_feedback_url)
        self.ui.setting_del_feedback_url.setText(del_feedback_url)
        self.ui.setting_admin_url.setText(admin_url)

    @staticmethod
    def admin_panel():
        url = admin_url
        webbrowser.open_new_tab(url)

    def feedbacks_chart_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.feedback_chart)

    def refresh_feedback_func(self):
        self.ui.feedbacks_state_label.setText("Please wait...")
        _thread.start_new_thread(self.insert_data_feedback_chart, (2,))

    def insert_data_feedback_chart(self, num):
        self.ui.feedbacks_refresh_btn.setEnabled(False)
        url = get_feedback_url
        try:
            response = requests.get(url=url)
            data = response.json()
            response.close()
            self.insert_data_process(data)
            self.ui.feedbacks_state_label.setText("")
        except requests.ConnectionError:
            self.ui.feedbacks_state_label.setText("Please check internet.")
        except:
            self.ui.feedbacks_state_label.setText("Something went wrong.")
        self.ui.feedbacks_refresh_btn.setEnabled(True)

    def insert_data_process(self, feedbacks):
        size = len(feedbacks)
        self.ui.tableWidget_feedback.setRowCount(size)
        row = 0
        for feedback in feedbacks:
            self.ui.tableWidget_feedback.setItem(row, 0, QTableWidgetItem(str(feedback['id'])))
            self.ui.tableWidget_feedback.setItem(row, 1, QTableWidgetItem(feedback['username']))
            self.ui.tableWidget_feedback.setItem(row, 2, QTableWidgetItem(feedback['title']))
            self.ui.tableWidget_feedback.setItem(row, 3, QTableWidgetItem(feedback['subject']))
            self.ui.tableWidget_feedback.setItem(row, 4, QTableWidgetItem(feedback['message']))
            row += 1

    def del_feedback_func(self):
        if len(self.ui.feedbacks_id_lineedit.text()) != 0:
            if self.ui.feedbacks_id_lineedit.text().isnumeric():
                _thread.start_new_thread(self.del_feedback_process, (2,))
            else:
                self.ui.feedbacks_state_label.setText("ID should be number.")
        else:
            self.ui.feedbacks_state_label.setText("Please fill ID.")

    def del_feedback_process(self, num):
        self.ui.feedbacks_state_label.setText("Please wait...")
        self.ui.feedbacks_delete_btn.setEnabled(False)
        data = dict()
        data["id"] = self.ui.feedbacks_id_lineedit.text()
        url = del_feedback_url
        try:
            response = requests.delete(url=url, json=data)
            res_data = response.json()
            response.close()
            if res_data["state"] == "not_found":
                self.ui.feedbacks_state_label.setText(res_data["message"])
            elif res_data["state"] == "done":
                self.ui.feedbacks_state_label.setText(res_data["message"])
                time.sleep(3)
                self.ui.feedbacks_state_label.setText("Please refresh.")
        except requests.ConnectionError:
            self.ui.feedbacks_state_label.setText("Please check your Internet.")
        except:
            self.ui.feedbacks_state_label.setText("Something went wrong.")
        self.ui.feedbacks_delete_btn.setEnabled(True)

    # =============================
    def send_data_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.send_data)

    def send_data_connection(self):
        self.ui.send_data_submit_btn.clicked.connect(self.send_data_submit_func)
        self.ui.send_data_price.textChanged.connect(self.textchange_price)
        self.ui.send_data_combobox_pay.currentTextChanged.connect(self.textchange_pay)
        self.ui.send_data_clear_btn.clicked.connect(self.send_data_clear)

    def send_data_tools(self):
        self.ui.send_data_frame_tracking.hide()

    def send_data_submit_func(self):
        if len(self.ui.send_data_title.text()) != 0:
            if len(self.ui.send_data_fullname.text()) != 0:
                if len(self.ui.send_data_phone.text()) != 0:
                    if len(self.ui.send_data_price.text()) != 0:
                        if self.ui.send_data_combobox_price.currentText() != "None":
                            if len(self.ui.send_data_date.text()) != 0:
                                if len(self.ui.send_data_time.text()) != 0:
                                    if self.ui.send_data_combobox_state.currentText() != "None":
                                        if self.ui.send_data_combobox_pay.currentText() != "None":
                                            if self.ui.send_data_combobox_pay.currentText() == "Yes":
                                                if len(self.ui.send_data_tracking_code.text()) != 0:
                                                    self.ui.send_data_state_label.setText("Please wait...")
                                                    _thread.start_new_thread(self.send_data_submit_process, (2,))
                                                else:
                                                    self.ui.send_data_state_label.setText(
                                                        "You should fill tracking code.")
                                            else:
                                                self.ui.send_data_state_label.setText("Please wait...")
                                                _thread.start_new_thread(self.send_data_submit_process, (2,))
                                        else:
                                            self.ui.send_data_state_label.setText("You should choose pay state.")
                                    else:
                                        self.ui.send_data_state_label.setText("You should choose state of payment.")
                                else:
                                    self.ui.send_data_state_label.setText("You should fill time.")
                            else:
                                self.ui.send_data_state_label.setText("You should fill date.")
                        else:
                            self.ui.send_data_state_label.setText("You should choose type of price.")
                    else:
                        self.ui.send_data_state_label.setText("You should fill price.")
                else:
                    self.ui.send_data_state_label.setText("You should fill phone.")
            else:
                self.ui.send_data_state_label.setText("You should fill fullname.")
        else:
            self.ui.send_data_state_label.setText("You should fill title.")

    def send_data_submit_process(self, num):
        self.ui.send_data_submit_btn.setEnabled(False)
        data = dict()
        url = send_data_url
        data["username"] = delivery_username
        data["title"] = self.ui.send_data_title.text()
        data["fullname"] = self.ui.send_data_fullname.text()
        data["phone"] = self.ui.send_data_phone.text()
        if len(self.ui.send_data_company.text()) == 0:
            data["company"] = "None"
        else:
            data["company"] = self.ui.send_data_company.text()
        data["price"] = f"{self.ui.send_data_price.text()} {self.ui.send_data_combobox_price.currentText()}"
        data["date"] = self.ui.send_data_date.text()
        data["time"] = self.ui.send_data_time.text()
        data["state"] = self.ui.send_data_combobox_state.currentText()
        data["is_pay"] = self.ui.send_data_combobox_pay.currentText()
        if len(self.ui.send_data_tracking_code.text()) == 0:
            data["tracking_code"] = "None"
        else:
            data["tracking_code"] = self.ui.send_data_tracking_code.text()
        try:
            response = requests.post(url=url, json=data)
            res_data = response.json()
            if res_data.get("state") == "done":
                self.ui.send_data_state_label.setText(res_data["message"])
            else:
                self.ui.send_data_state_label.setText("Please try again.")
        except requests.ConnectionError:
            self.ui.send_data_state_label.setText("Please check your Internet.")
        except:
            self.ui.send_data_state_label.setText("Something went wrong.")
        self.ui.send_data_submit_btn.setEnabled(True)

    def textchange_price(self):
        if not self.ui.send_data_price.text().isnumeric():
            self.ui.send_data_price.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                  "border-radius:5px;\n"
                                                  "border:2px solid red;"
                                                  "")
            self.ui.send_data_submit_btn.setEnabled(False)
        else:
            self.ui.send_data_price.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                  "border-radius:5px;\n"
                                                  "")
            self.ui.send_data_submit_btn.setEnabled(True)

    def textchange_pay(self):
        state = self.ui.send_data_combobox_pay.currentText()
        if state == "Yes":
            self.ui.send_data_frame_tracking.show()
        else:
            self.ui.send_data_frame_tracking.hide()

    def send_data_clear(self):
        self.ui.send_data_title.setText("")
        self.ui.send_data_fullname.setText("")
        self.ui.send_data_date.setText("")
        self.ui.send_data_time.setText("")
        self.ui.send_data_tracking_code.setText("")
        self.ui.send_data_price.setText("")
        self.ui.send_data_phone.setText("")
        self.ui.send_data_company.setText("")
        self.ui.send_data_state_label.setText("")
        self.ui.send_data_combobox_pay.setCurrentIndex(0)
        self.ui.send_data_combobox_price.setCurrentIndex(0)
        self.ui.send_data_combobox_state.setCurrentIndex(0)

    # =============================
    def get_data_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.get_data)
        self.ui.get_data_id_lineedit.setEnabled(False)

    def get_data_connection(self):
        self.ui.get_data_all_data_btn.clicked.connect(self.all_data_func)
        self.ui.get_data_your_user_btn.clicked.connect(self.user_data_func)
        self.ui.get_data_id_lineedit.textChanged.connect(self.get_data_textchange_id)
        self.ui.get_data_refresh_btn.clicked.connect(self.get_data_refresh)
        self.ui.get_data_delete_btn.clicked.connect(self.get_data_del_func)

    def get_data_tools(self):
        self.ui.tableWidget_get_data.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.get_data_refresh_btn.setEnabled(False)

    def get_data_textchange_id(self):
        if self.h_get_data:
            if not self.ui.get_data_id_lineedit.text().isnumeric():
                self.ui.get_data_id_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                           "border-radius:5px;\n"
                                                           "border:2px solid red;"
                                                           "")
                self.change_state(False)
            else:
                self.ui.get_data_id_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                           "border-radius:5px;\n"
                                                           "")
                self.change_state(True)

    def change_state(self, state: bool):
        self.ui.get_data_delete_btn.setEnabled(state)

    def all_data_func(self):
        self.ui.get_data_id_lineedit.setEnabled(True)
        self.ui.get_data_refresh_btn.setEnabled(True)
        self.h_get_data = False
        self.change_state(False)
        _thread.start_new_thread(self.all_data_process, (2,))

    def all_data_process(self, num):
        self.ui.get_data_state_label.setText("Please wait...")
        self.ui.get_data_all_data_btn.setEnabled(False)
        url = get_all_data_url
        try:
            response = requests.get(url=url)
            res_data = response.json()
            self.insert_data_chart(res_data)
            self.ui.get_data_state_label.setText("")
        except requests.ConnectionError:
            self.ui.get_data_state_label.setText("Please check your Internet.")
        except:
            self.ui.get_data_state_label.setText("Something went wrong.")
        self.ui.get_data_all_data_btn.setEnabled(True)

    def user_data_func(self):
        self.ui.get_data_id_lineedit.setEnabled(True)
        self.ui.get_data_refresh_btn.setEnabled(True)
        self.h_get_data = True
        self.change_state(True)
        _thread.start_new_thread(self.user_data_process, (2,))

    def user_data_process(self, num):
        self.ui.get_data_state_label.setText("Please wait...")
        self.ui.get_data_your_user_btn.setEnabled(False)
        url = get_user_data
        data = {"username": delivery_username}
        try:
            response = requests.get(url=url, json=data)
            res_data = response.json()
            self.insert_data_chart(res_data)
            self.ui.get_data_state_label.setText("")
        except requests.ConnectionError:
            self.ui.get_data_state_label.setText("Please check your Internet.")
        except:
            self.ui.get_data_state_label.setText("Something went wrong.")
        self.ui.get_data_your_user_btn.setEnabled(True)

    def insert_data_chart(self, all_data):
        size = len(all_data)
        self.ui.tableWidget_get_data.setRowCount(size)
        row = 0
        for data in all_data:
            self.ui.tableWidget_get_data.setItem(row, 0, QTableWidgetItem(str(data['id'])))
            self.ui.tableWidget_get_data.setItem(row, 1, QTableWidgetItem(str(data['username'])))
            self.ui.tableWidget_get_data.setItem(row, 2, QTableWidgetItem(str(data['title'])))
            self.ui.tableWidget_get_data.setItem(row, 3, QTableWidgetItem(str(data['fullname'])))
            self.ui.tableWidget_get_data.setItem(row, 4, QTableWidgetItem(str(data['phone'])))
            self.ui.tableWidget_get_data.setItem(row, 5, QTableWidgetItem(str(data['company'])))
            self.ui.tableWidget_get_data.setItem(row, 6, QTableWidgetItem(str(data['price'])))
            self.ui.tableWidget_get_data.setItem(row, 7, QTableWidgetItem(str(data['date'])))
            self.ui.tableWidget_get_data.setItem(row, 8, QTableWidgetItem(str(data['time'])))
            self.ui.tableWidget_get_data.setItem(row, 9, QTableWidgetItem(str(data['state'])))
            self.ui.tableWidget_get_data.setItem(row, 10, QTableWidgetItem(str(data['is_pay'])))
            self.ui.tableWidget_get_data.setItem(row, 11, QTableWidgetItem(str(data['tracking_code'])))
            row += 1

    def get_data_refresh(self):
        self.ui.get_data_refresh_btn.setEnabled(False)
        if self.h_get_data:
            _thread.start_new_thread(self.user_data_process, (2,))
        else:
            _thread.start_new_thread(self.all_data_process, (2,))
        self.ui.get_data_refresh_btn.setEnabled(True)

    def get_data_del_func(self):
        if len(self.ui.get_data_id_lineedit.text()) != 0:
            if self.ui.get_data_id_lineedit.text().isnumeric():
                self.ui.get_data_state_label.setText("Please wait...")
                _thread.start_new_thread(self.get_data_del_process, (2,))
            else:
                self.ui.get_data_state_label.setText("ID should be number.")
        else:
            self.ui.get_data_state_label.setText("Please enter ID.")

    def get_data_del_process(self, num):
        self.ui.get_data_delete_btn.setEnabled(False)
        data = {"id": self.ui.get_data_id_lineedit.text()}
        url = delete_data_url
        try:
            response = requests.delete(url=url, json=data)
            res_data = response.json()
            response.close()
            self.ui.get_data_state_label.setText(res_data["message"])
        except requests.ConnectionError:
            self.ui.get_data_state_label.setText("Please check your Internet.")
        except:
            self.ui.get_data_state_label.setText("Something went wrong.")

        self.ui.get_data_delete_btn.setEnabled(True)

    # =============================
    def users_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.users)

    def users_connection(self):
        self.ui.users_refresh_btn.clicked.connect(self.users_refresh_func)
        self.ui.users_delete_btn.clicked.connect(self.users_delete_func)
        self.ui.users_id_lineedit.textChanged.connect(self.users_textchange_id)

    def users_tools(self):
        self.ui.tableWidget_users.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def users_refresh_func(self):
        self.ui.users_state_label.setText("Please wait...")
        _thread.start_new_thread(self.users_refresh_process, (2,))

    def users_refresh_process(self, num):
        self.ui.users_refresh_btn.setEnabled(False)
        url = users_url
        try:
            response = requests.get(url=url)
            res_data = response.json()
            self.users_insert_data(res_data)
            self.ui.users_state_label.setText("")
        except requests.ConnectionError:
            self.ui.users_state_label.setText("Please check your Internet.")
        except:
            self.ui.users_state_label.setText("Something went wrong.")
        self.ui.users_refresh_btn.setEnabled(True)

    def users_insert_data(self, all_data):
        size = len(all_data)
        self.ui.tableWidget_users.setRowCount(size)
        row = 0
        for data in all_data:
            self.ui.tableWidget_users.setItem(row, 0, QTableWidgetItem(str(data['id'])))
            self.ui.tableWidget_users.setItem(row, 1, QTableWidgetItem(str(data['username'])))
            self.ui.tableWidget_users.setItem(row, 2, QTableWidgetItem(str(data['fullname'])))
            self.ui.tableWidget_users.setItem(row, 3, QTableWidgetItem(str(data['email'])))
            self.ui.tableWidget_users.setItem(row, 4, QTableWidgetItem(str(data['password'])))
            self.ui.tableWidget_users.setItem(row, 5, QTableWidgetItem(str(data['type'])))
            row += 1

    def users_delete_func(self):
        if len(self.ui.users_id_lineedit.text()) != 0:
            if self.ui.users_id_lineedit.text().isnumeric():
                self.ui.users_state_label.setText("Please wait...")
                _thread.start_new_thread(self.users_delete_process, (2,))
            else:
                self.ui.users_state_label.setText("ID should be number.")
        else:
            self.ui.users_state_label.setText("Please write ID.")

    def users_delete_process(self, num):
        self.ui.users_delete_btn.setEnabled(False)
        data = {"id": self.ui.users_id_lineedit.text()}
        url = users_url
        try:
            response = requests.delete(url=url, json=data)
            res_data = response.json()
            self.ui.users_state_label.setText(res_data["message"])
        except requests.ConnectionError:
            self.ui.users_state_label.setText("Please check your Internet.")
        except:
            self.ui.users_state_label.setText("Something went wrong.")
        self.ui.users_delete_btn.setEnabled(True)

    def users_textchange_id(self):
        if not self.ui.users_id_lineedit.text().isnumeric():
            self.ui.users_id_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                    "border-radius:5px;\n"
                                                    "border:2px solid red;"
                                                    "")
            self.ui.users_delete_btn.setEnabled(False)
        else:
            self.ui.users_id_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                    "border-radius:5px;\n"
                                                    "")
            self.ui.users_delete_btn.setEnabled(True)

    # =============================
    def feedback_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.feedback)
        self.ui.feedback_username.setText(delivery_username)

    def feedback_connection(self):
        self.ui.feedback_send_btn.clicked.connect(self.submit_func)
        self.ui.feedback_clear_btn.clicked.connect(self.clear_feedback)

    def feedback_tools(self):
        self.ui.feedback_username.setReadOnly(True)

    def submit_func(self):
        if len(self.ui.feedback_title.text()) != 0:
            if len(self.ui.feedback_subject.text()) != 0:
                if len(self.ui.feedback_TextEdit.toPlainText()) != 0:
                    self.ui.feedback_state_label.setText("Please wait...")
                    _thread.start_new_thread(self.feedback_process, (2,))
                else:
                    self.ui.feedback_state_label.setText("Please write your message.")
            else:
                self.ui.feedback_state_label.setText("Please write your subject.")
        else:
            self.ui.feedback_state_label.setText("Please write your title.")

    def feedback_process(self, num):
        data = dict()
        self.ui.feedback_send_btn.setEnabled(False)
        data['username'] = self.ui.feedback_username.text()
        data['title'] = self.ui.feedback_title.text()
        data['subject'] = self.ui.feedback_subject.text()
        data['message'] = self.ui.feedback_TextEdit.toPlainText()
        url = create_feedback_url
        try:
            response = requests.post(url=url, json=data)
            state = response.json().get("state")
            if state == "done":
                self.ui.feedback_state_label.setText("Your message has been sent.")
            else:
                self.ui.feedback_state_label.setText("Please try again.")
        except requests.ConnectionError:
            self.ui.feedback_state_label.setText("Please check your Internet.")
        except:
            self.ui.feedback_state_label.setText("Something went wrong.")
        self.ui.feedback_send_btn.setEnabled(True)

    def clear_feedback(self):
        self.ui.feedback_title.setText("")
        self.ui.feedback_subject.setText("")
        self.ui.feedback_TextEdit.setText("")

    # =============================
    def info_func(self):
        pass

    # =============================
    def logout_func(self):
        pass


class LoginRegister(QMainWindow):
    check_state = False
    username_tmp = None
    password_tmp = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.home = Ui_login_register()
        self.home.setupUi(self)
        self.Panel = DataArchive()
        self.setWindowTitle("Data Archive")
        self.setWindowIcon(QIcon(r"photo/download.jfif"))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.app_tools()

    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def app_tools(self):
        _thread.start_new_thread(self.checkbox_state, (2,))
        self.home.stackedWidget.setCurrentWidget(self.home.page)
        self.home.state_register_label.hide()
        self.home.state_login_label.hide()
        self.home.reg_log_btn.clicked.connect(self.register_func)
        self.home.check_btn.clicked.connect(self.check_func)
        self.home.register_submit_btn.clicked.connect(self.sign_up_func)
        self.home.login_username.textChanged.connect(self.textchange_username)
        self.home.login_password.textChanged.connect(self.textchange_password)

    # =================================
    def checkbox_state(self, num):
        url = check_admin_url
        try:
            request = requests.get(url=url)
            state = request.json()['state']
            if state == "is_exist":
                self.home.checkBox.hide()
        except requests.ConnectionError:
            self.home.state_register_label.setText("Please check your Internet.")

    @staticmethod
    def check_connection():
        url = 'https://google.com'
        timeout = 5
        try:
            requests.get(url=url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    # =================================
    def login_func(self):
        self.home.reg_log_btn.setText("Register")
        self.home.state_login_label.hide()
        self.home.stackedWidget.setCurrentWidget(self.home.page)
        self.home.reg_log_btn.clicked.connect(self.register_func)

    def check_func(self):
        self.home.state_login_label.show()
        if len(self.home.login_username.text()) != 0:
            if len(self.home.login_password.text()) != 0:
                self.home.state_login_label.setText("Please wait...")
                _thread.start_new_thread(self.check_process, (2,))
            else:
                self.home.state_login_label.setText('Please fill password.')
        else:
            self.home.state_login_label.setText('Please fill username.')

    def check_process(self, num):
        global delivery_username
        if self.check_connection():
            data = dict()
            data['username'] = self.home.login_username.text()
            data['password'] = self.home.login_password.text()
            url = login_url
            try:
                request = requests.post(url=url, json=data)
                json_data = request.json()
                if json_data['state'] == "None":
                    self.home.state_login_label.setText(json_data["message"])
                elif json_data['state'] == "incorrect":
                    self.home.state_login_label.setText(json_data["message"])
                elif json_data['state'] == "correct":
                    self.home.state_login_label.setText(json_data["message"])
                    time.sleep(2)
                    delivery_username = data['username']
                    self.username_tmp = data['username']
                    self.password_tmp = data['password']
                    self.check_state = True
                    self.change_state("sign_in")
                request.close()
            except requests.ConnectionError:
                self.home.state_login_label.setText("Please check your Internet.")
            except:
                self.home.state_login_label.setText("Something went wrong.")
        else:
            self.home.state_login_label.setText("Please check your Internet.")
            self.home.state_login_label.show()

    def change_state(self, state):
        if state == "sign_in":
            self.home.check_btn.setText("Sign in")
            self.home.check_btn.clicked.connect(self.sign_in_func)
        elif state == "check":
            self.home.check_btn.setText("Check")
            self.home.check_btn.clicked.connect(self.check_func)
            self.home.state_login_label.setText("")

    def sign_in_func(self):
        if self.check_state:
            self.Panel.show()
            self.hide()

    def textchange_username(self):
        if self.home.login_username.text() != self.username_tmp:
            self.change_state("check")

    def textchange_password(self):
        if self.home.login_password.text() != self.password_tmp:
            self.change_state("check")

    # =================================

    def register_func(self):
        _thread.start_new_thread(self.checkbox_state, (2,))
        self.home.reg_log_btn.setText("Log-in")
        self.home.state_register_label.hide()
        self.home.stackedWidget.setCurrentWidget(self.home.page_2)
        self.home.reg_log_btn.clicked.connect(self.login_func)

    def clear_func(self):
        self.home.register_fullname.setText("")
        self.home.register_username.setText("")
        self.home.register_email.setText("")
        self.home.register_password.setText("")
        self.home.register_re_password.setText("")
        self.home.checkBox.setChecked(False)

    def sign_up_func(self):
        self.home.state_register_label.show()
        if len(self.home.register_fullname.text()) != 0:
            if len(self.home.register_username.text()) != 0:
                if len(self.home.register_email.text()) != 0:
                    if len(self.home.register_password.text()) != 0:
                        if len(self.home.register_re_password.text()) != 0:
                            if self.home.register_password.text() == self.home.register_re_password.text():
                                self.home.state_register_label.setText("Please wait...")
                                _thread.start_new_thread(self.sign_up_process, (2,))
                            else:
                                self.home.state_register_label.setText("The passwords is not match.")
                        else:
                            self.home.state_register_label.setText("Please fill second password.")
                    else:
                        self.home.state_register_label.setText("Please fill password.")
                else:
                    self.home.state_register_label.setText("Please fill email.")
            else:
                self.home.state_register_label.setText("Please fill username.")
        else:
            self.home.state_register_label.setText("Please fill fullname.")

    def sign_up_process(self, num):
        if self.check_connection():
            data = dict()
            data["fullname"] = self.home.register_fullname.text()
            data["username"] = self.home.register_username.text()
            data["email"] = self.home.register_email.text()
            data["password"] = self.home.register_password.text()
            if self.home.checkBox.isChecked():
                data["type"] = "admin"
            else:
                data["type"] = "employee"
            url = create_url
            try:
                request = requests.post(url=url, json=data)
                json_data = request.json()
                if json_data.get("username") is not None:
                    msg = json_data.get("username")[0]
                    self.home.state_register_label.setText(msg)
                elif json_data.get("state") is not None:
                    msg = json_data.get("state")
                    if msg == "done":
                        self.home.state_register_label.setText("Register is successful.")
                        self.clear_func()
                        _thread.start_new_thread(self.checkbox_state, (2,))
                        time.sleep(2)
                        self.login_func()
            except requests.ConnectionError:
                self.home.state_register_label.setText("Please check your Internet.")
                self.home.state_register_label.show()
            except:
                self.home.state_register_label.setText("Something went wrong.")
        else:
            self.home.state_register_label.setText("Please check your Internet.")
            self.home.state_register_label.show()


def setup():
    app = QApplication([])
    ui = LoginRegister()
    # ui = DataArchive()
    ui.show()
    app.exec_()


setup()
