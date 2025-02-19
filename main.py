import shutil

from PySide6 import QtWidgets, QtCore, QtGui
from css import main_css as css
from functools import partial
import sys

from css.main_css import grid_tarefas


class Main_Window(QtWidgets.QWidget):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setStyleSheet(css.main_window)
        screen = QtGui.QGuiApplication.primaryScreen()
        self.screen_geometry = screen.availableGeometry()
        self.setMinimumSize(self.screen_geometry.width(), self.screen_geometry.height())

        self.left_bar = LeftSideBarMenuWidget(self)
        self.left_bar.height_ = self.screen_geometry.height() - 100
        self.left_bar.width_ = int(self.screen_geometry.width() / 5)
        self.left_bar.setMinimumSize(self.left_bar.width_, self.left_bar.height_)
        self.left_bar.move(
            int(self.screen_geometry.width() / 50),
            int(self.screen_geometry.height() / 2 - self.left_bar.height_ / 2),
        )

        self.tasks_window = MyTasksWindow(parent=self, main_window_=self)

        self.left_bar.raise_()


# ------------------------------------------------------------------------------------------
class LeftSideBarMenuWidget(QtWidgets.QLabel):
    def __init__(self, parent: Main_Window):
        super(LeftSideBarMenuWidget, self).__init__(parent=parent)
        self.setStyleSheet(css.left_side_bar)
        self.setFixedSize(200, 300)

        # Creating the buttons from de leftsidebar

        self.btn_my_tasks = QtWidgets.QPushButton("My Tasks")
        self.btn_my_tasks.setStyleSheet(css.btn_tasks)
        self.btn_my_tasks.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_my_tasks.clicked.connect(
            lambda: self.highlight_button(self.btn_my_tasks)
        )

        self.btn_dashboard = QtWidgets.QPushButton("Dashboard")
        self.btn_dashboard.setStyleSheet(css.btn_tasks)
        self.btn_dashboard.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_dashboard.clicked.connect(
            lambda: self.highlight_button(self.btn_dashboard)
        )

        self.btn_notification = QtWidgets.QPushButton("Notifications")
        self.btn_notification.setStyleSheet(css.btn_tasks)
        self.btn_notification.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_notification.clicked.connect(
            lambda: self.highlight_button(self.btn_notification)
        )

        self.left_sidebar_buttons = [
            self.btn_dashboard,
            self.btn_my_tasks,
            self.btn_notification,
        ]

        # Creating the div that holds the leftSideBar buttons
        self.div_btn_menu = QtWidgets.QWidget(parent=self)
        self.div_btn_menu.setStyleSheet(css.div_btn_menu)

        self.div_btn_menu.layout = QtWidgets.QGridLayout(parent=self.div_btn_menu)
        self.div_btn_menu.layout.setSpacing(0)
        self.div_btn_menu.layout.setContentsMargins(0, 0, 0, 0)
        self.div_btn_menu.layout.setRowStretch(1, 1)
        self.div_btn_menu.layout.setRowStretch(2, 1)
        self.div_btn_menu.layout.setRowStretch(3, 1)

        self.div_btn_menu.setMinimumWidth(int(parent.screen_geometry.width() / 5))
        self.div_btn_menu.layout.addWidget(self.btn_my_tasks)
        self.div_btn_menu.layout.addWidget(self.btn_dashboard)
        self.div_btn_menu.layout.addWidget(self.btn_notification)
        self.div_btn_menu.setLayout(self.div_btn_menu.layout)
        self.div_btn_menu.move(0, 100)

    @QtCore.Slot()
    def highlight_button(self, button: QtWidgets.QPushButton):
        for btn in self.left_sidebar_buttons:
            if hasattr(btn, "highlighted") == False:
                btn.highlighted = False

        for btn in self.left_sidebar_buttons:
            if btn != button and btn.highlighted == True:
                btn.highlighted = False
                btn.setStyleSheet(css.btn_tasks)

            elif btn == button and btn.highlighted == False:
                btn.highlighted = True
                btn.setStyleSheet(css.btn_tasks_highlighted)


# ------------------------------------------------------------------------------------------


class MyTasksLayout(QtWidgets.QGridLayout):
    def __init__(self, parent):
        super(MyTasksLayout, self).__init__(parent=parent)
        # setting the default configurations
        self.setSpacing(0),
        self.setContentsMargins(0, 0, 0, 0)

        self.task_collection: list[QtWidgets.QLabel] = []


class MyTasksWindow(QtWidgets.QWidget):
    def __init__(self, parent, main_window_: Main_Window):
        super(MyTasksWindow, self).__init__(parent=parent)

        self.header = QtWidgets.QLabel(parent=self)
        self.header.setStyleSheet(css.my_task_window_header)
        self.header.setMinimumSize(
            (
                main_window_.screen_geometry.width() -
                int(main_window_.screen_geometry.width() / 50 + main_window_.left_bar.width() + 40) -
                40
             ),
            90
        )
        self.header.move(
            int(main_window_.screen_geometry.width() / 50 + main_window_.left_bar.width() + 40),
            50
        )

        self.btn_addtask = QtWidgets.QPushButton("+  New Task", parent=self.header)
        self.btn_addtask.setMinimumSize(140, 50)
        self.btn_addtask.setStyleSheet(css.btn_add_task)
        self.btn_addtask.move(
            int(self.header.width() - self.btn_addtask.width() - 30),
            int(self.header.height() / 2 - self.btn_addtask.height() / 2),
        )
        self.btn_addtask.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.popup_addtask = PopUpAddTask(self, main_window_)
        self.popup_addtask.hide()
        self.btn_addtask.clicked.connect(
            lambda: self.popup_addtask.toggle_popup(main_window_)
        )


class PopUpAddTask(QtWidgets.QLabel):
    def __init__(self, parent: MyTasksWindow, main_window_: Main_Window):
        super(PopUpAddTask, self).__init__(parent=parent)
        self.setStyleSheet(css.popup_addtask)
        self.setMinimumSize(500, 500)

        self.parent_widget: MyTasksWindow = parent

        x = int(main_window_.screen_geometry.width() / 2 - (500 / 2))
        y = int(main_window_.screen_geometry.height() / 2 - (500 / 2))
        self.move(x, y)

        self.new_task_header = QtWidgets.QLabel("New Task", parent=self)
        self.new_task_header.setStyleSheet(css.new_task_header)
        self.new_task_header.move(500 // 2 - self.new_task_header.width() // 2, 50)

        self.btn_close_popup = QtWidgets.QPushButton("X", parent=self)
        self.btn_close_popup.setMinimumSize(50, 30)
        self.btn_close_popup.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_close_popup.setStyleSheet(css.btn_close_popup)
        self.btn_close_popup.clicked.connect(self.hide)
        self.btn_close_popup.move(435, 15)

        self.input_task_description = QtWidgets.QLineEdit(parent=self)
        self.input_task_description.setStyleSheet(css.task_creation_input)
        self.input_task_description.setMinimumSize(400, 40)
        self.input_task_description.move(250 - self.input_task_description.width() // 2, 150)
        self.input_task_description.setMaxLength(60)

        self.lbl_task_name = QtWidgets.QLabel("Task description:", parent=self)
        self.lbl_task_name.setStyleSheet(css.lbl_task)
        self.lbl_task_name.move(250 - self.input_task_description.width() // 2, 120)

        self.input_task_date = QtWidgets.QDateEdit(parent=self)
        self.input_task_date.setStyleSheet(css.task_creation_input)
        self.input_task_date.setMinimumSize(400, 40)
        self.input_task_date.move(250 - self.input_task_date.width() // 2, 240)
        self.input_task_date.setDate(QtCore.QDate.currentDate())

        self.lbl_task_date = QtWidgets.QLabel("Task date:", parent=self)
        self.lbl_task_date.setStyleSheet(css.lbl_task)
        self.lbl_task_date.move(250 - self.input_task_date.width() // 2, 210)

        self.input_task_urgency = QtWidgets.QComboBox(parent=self)
        self.input_task_urgency.addItems(['Low', 'Medium', 'High'])
        self.input_task_urgency.setStyleSheet(css.task_creation_input)
        self.input_task_urgency.setMinimumSize(400, 40)
        self.input_task_urgency.move(250 - self.input_task_urgency.width() // 2, 335)

        self.lbl_task_urgency = QtWidgets.QLabel("Task urgency:", parent=self)
        self.lbl_task_urgency.setStyleSheet(css.lbl_task)
        self.lbl_task_urgency.move(250 - self.input_task_urgency.width() // 2, 305)

    @QtCore.Slot()
    def toggle_popup(self, main_window_: Main_Window):
        if self.isVisible() == False:
            self.show()
            self.parent_widget.adjustSize()
            self.parent_widget.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = Main_Window()
    main_window.showMaximized()
    sys.exit(app.exec())
