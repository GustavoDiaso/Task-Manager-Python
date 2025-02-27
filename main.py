from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtGui
from css import main_css as css
import sys
import json
import uuid


JSON_PATH = Path(__file__).parent / "my_tasks_json/tasks.json"


def get_tasks() -> list:
    """returns the current tasks present in the json database"""
    tasks = []
    with open(JSON_PATH, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
        try:
            for task in data:
                tasks.append(task)

        except json.JSONDecodeError:
            # If this happens, it means that your json file does not contain any data
            return []

    return tasks


class Main_Window(QtWidgets.QWidget):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setStyleSheet(css.main_window)
        screen = QtGui.QGuiApplication.primaryScreen()
        self.screen_geometry = screen.availableGeometry()
        self.setMinimumSize(self.screen_geometry.width(), self.screen_geometry.height())

        self.left_bar = LeftSideBar(parent=self, main_window_=self)
        self.left_bar.btn_my_tasks.click()

        self.tasks_window = MyTasksWindow(parent=self, main_window_=self)
        self.left_bar.raise_()


# ------------------------------------------------------------------------------------------
class LeftSideBar(QtWidgets.QLabel):
    def __init__(self, parent, main_window_: Main_Window):
        super(LeftSideBar, self).__init__(parent=parent)
        self.setStyleSheet(css.left_side_bar)
        height_ = main_window_.screen_geometry.height() - 100
        width_ = int(main_window_.screen_geometry.width() / 5)
        self.setMinimumSize(width_, height_)
        self.move(
            int(main_window_.screen_geometry.width() / 50),
            int(main_window_.screen_geometry.height() / 2 - height_ / 2),
        )

        # Creating the buttons from de leftsidebar

        self.btn_my_tasks = QtWidgets.QPushButton("My Tasks")
        self.btn_my_tasks.setStyleSheet(css.btn_tasks)
        self.btn_my_tasks.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_my_tasks.clicked.connect(
            lambda: self.highlight_button(self.btn_my_tasks)
        )
        self.btn_my_tasks.clicked.connect(
            lambda: self.toggleSecondaryWindow(main_window_, "my_tasks")
        )

        self.btn_dashboard = QtWidgets.QPushButton("Dashboard")
        self.btn_dashboard.setStyleSheet(css.btn_tasks)
        self.btn_dashboard.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_dashboard.clicked.connect(
            lambda: self.highlight_button(self.btn_dashboard)
        )
        self.btn_dashboard.clicked.connect(
            lambda: self.toggleSecondaryWindow(main_window_, "dashboard")
        )

        self.btn_notification = QtWidgets.QPushButton("Notifications")
        self.btn_notification.setStyleSheet(css.btn_tasks)
        self.btn_notification.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_notification.clicked.connect(
            lambda: self.highlight_button(self.btn_notification)
        )
        self.btn_notification.clicked.connect(
            lambda: self.toggleSecondaryWindow(main_window_, "notification")
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

    @QtCore.Slot()
    def toggleSecondaryWindow(self, main_window_, target_window: str):
        try:
            if target_window == "my_tasks":
                if not main_window_.tasks_window.isVisible():
                    main_window_.tasks_window.show()

            if target_window == "dashboard":
                main_window_.tasks_window.hide()

            if target_window == "notification":
                main_window_.tasks_window.hide()
        except AttributeError:
            ...


# ------------------------------------------------------------------------------------------
class TaskSquare(QtWidgets.QLabel):
    def __init__(self, task_id, task_desciption, task_date, task_urgecy, task_window):
        super(TaskSquare, self).__init__()
        self.setStyleSheet(css.task_square)
        self.id_ = task_id
        self.width_ = int(task_window.div_task_layout.width() * 1 / 4 - 10)
        self.height_ = 300
        self.setFixedSize(self.width_, self.height_)

        colored_task_header = QtWidgets.QLabel(parent=self)
        colored_task_header.setFixedSize(self.width(), 50)
        colored_task_header.setStyleSheet(css.task_colored_header)
        colored_task_header.move(0, 0)

        btn_delete_task = QtWidgets.QPushButton(parent=colored_task_header)
        btn_delete_task.setIcon(QtGui.QIcon(str(Path(__file__).parent / "icons/x.png")))
        btn_delete_task.setIconSize(QtCore.QSize(15, 15))
        btn_delete_task.setStyleSheet(css.btn_delete_task)
        btn_delete_task.setFixedSize(34, 34)
        btn_delete_task.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_delete_task.move(
            int(colored_task_header.width() - btn_delete_task.width() - 5),
            int(colored_task_header.height() / 2 - btn_delete_task.height() / 2),
        )
        btn_delete_task.clicked.connect(lambda: self.remove_task(task_id, task_window))

        btn_lookup_task = QtWidgets.QPushButton(parent=colored_task_header)
        btn_lookup_task.setIcon(
            QtGui.QIcon(str(Path(__file__).parent / "icons/olho.png"))
        )
        btn_lookup_task.setIconSize(QtCore.QSize(30, 30))
        btn_lookup_task.setStyleSheet(css.btn_delete_task)
        btn_lookup_task.setFixedSize(34, 34)
        btn_lookup_task.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        btn_lookup_task.move(
            8, int(colored_task_header.height() / 2 - btn_lookup_task.height() / 2)
        )

        lbl_description = QtWidgets.QLabel("Task preview", parent=self)
        lbl_description.setStyleSheet(css.square_bold_text)
        lbl_description.setFixedSize(lbl_description.width() + 20, 25)
        lbl_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl_description.move(
            int(self.width() / 2 - lbl_description.width() / 2),
            70,
        )
        square_description = QtWidgets.QLabel(task_desciption, parent=self)
        square_description.setStyleSheet(css.square_base_text)
        square_description.setFixedSize(300, 25)
        square_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        square_description.move(
            int(self.width() / 2 - (square_description.width() / 2)),
            100,
        )

        lbl_data = QtWidgets.QLabel("Date", parent=self)
        lbl_data.setStyleSheet(css.square_bold_text)
        lbl_data.setFixedSize(lbl_data.width() + 20, 25)
        lbl_data.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl_data.move(
            int(self.width() / 2 - lbl_data.width() / 2),
            140,
        )
        square_date = QtWidgets.QLabel(task_date, parent=self)
        square_date.setStyleSheet(css.square_base_text)
        square_date.setFixedSize(300, 25)
        square_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        square_date.move(int(self.width() / 2 - square_date.width() / 2), 170)

        lbl_urgency = QtWidgets.QLabel("Urgency", parent=self)
        lbl_urgency.setStyleSheet(css.square_bold_text)
        lbl_urgency.setFixedSize(lbl_urgency.width() + 20, 25)
        lbl_urgency.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl_urgency.move(
            int(self.width() / 2 - lbl_urgency.width() / 2),
            210,
        )
        square_urgency = QtWidgets.QLabel(task_urgecy, parent=self)
        match square_urgency.text():
            case "Low":
                square_urgency.setStyleSheet("""font-size: 18px;color: green;""")
            case "Medium":
                square_urgency.setStyleSheet("""font-size: 18px;color: yellow;""")
            case "High":
                square_urgency.setStyleSheet("""font-size: 18px;color: red;""")

        square_urgency.setFixedSize(300, 25)
        square_urgency.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        square_urgency.move(int(self.width() / 2 - square_urgency.width() / 2), 240)

    @QtCore.Slot()
    def remove_task(self, task_id, task_window):
        current_taks = get_tasks()
        new_tasks = []
        if len(current_taks) > 0:
            for task in current_taks:
                if task["id"] != task_id:
                    new_tasks.append(task)

        with open(JSON_PATH, "w", encoding="utf8") as json_file:
            json.dump(new_tasks, json_file, indent=4, ensure_ascii=True)  # type: ignore

        task_window.tasks_grid_layout.update_layout()


class MyTasksLayout(QtWidgets.QGridLayout):
    def __init__(self, task_window_):
        super(MyTasksLayout, self).__init__()
        self.parent_ = task_window_
        # setting the default configurations
        self.setSpacing(10),
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft
        )

        with open(JSON_PATH, "r", encoding="utf8") as json_file:
            try:
                data = json.load(json_file)

                row = 1
                column = 1
                for task in data:
                    formated_description = task["description"][:20]
                    if len(formated_description) >= 20:
                        formated_description += "..."

                    task_square_ = TaskSquare(
                        task["id"],
                        formated_description,
                        task["date"],
                        task["urgency"],
                        task_window_,
                    )

                    if column == 5:
                        row += 1
                        column = 1

                    self.addWidget(task_square_, row, column)
                    column += 1

            except json.JSONDecodeError:
                # this will happen if the json_file is empty
                print("Json_file is empty")

    @QtCore.Slot()
    def get_last_task_position(self) -> list[int] | None:
        # if there are no tasks, there is no last task position
        if self.count() == 0:
            return None

        last_task_position = self.getItemPosition(self.count() - 1)

        last_task_position = (
            str(last_task_position).replace(" ", "").replace("(", "").replace(")", "")
        )

        last_task_position_list = last_task_position.split(",")
        return [int(last_task_position_list[0]), int(last_task_position_list[1])]

    @QtCore.Slot()
    def clear_layout(self):

        last_task_position = self.get_last_task_position()

        if last_task_position is not None:
            for row in range(1, last_task_position[0] + 1):
                for column in range(1, 5):
                    # widget: TaskSquare
                    if self.itemAtPosition(row, column) is not None:
                        widget = self.itemAtPosition(row, column).widget()
                        widget.setParent(None)
                        widget.deleteLater()

    @QtCore.Slot()
    def order_layout_by_urgency(self):
        self.clear_layout()

    @QtCore.Slot()
    def order_layout_by_date(self):
        self.clear_layout()

    @QtCore.Slot()
    def update_layout(self):
        self.clear_layout()

        with open(JSON_PATH, "r", encoding="utf8") as json_file:
            try:
                data = json.load(json_file)

                row = 1
                column = 1
                for task in data:
                    formated_description = task["description"][:20]
                    if len(formated_description) >= 20:
                        formated_description += "..."

                    task_square_ = TaskSquare(
                        task["id"],
                        formated_description,
                        task["date"],
                        task["urgency"],
                        self.parent_,
                    )

                    if column == 5:
                        row += 1
                        column = 1

                    self.addWidget(task_square_, row, column)
                    column += 1

            except json.JSONDecodeError:
                # this will happen if the json_file is empty
                print("Json_file is empty")

        self.update()
        self.invalidate()

        last_task_position = self.get_last_task_position()
        if last_task_position is not None:
            self.parent_.div_task_layout.setFixedHeight(last_task_position[0] * 320)
        self.parent_.div_task_layout.updateGeometry()


class MyTasksWindow(QtWidgets.QWidget):
    def __init__(self, parent, main_window_: Main_Window):
        super(MyTasksWindow, self).__init__(parent=parent)
        self.header = QtWidgets.QLabel(parent=self)
        self.header.setStyleSheet(css.my_task_window_header)
        self.header.setMinimumSize(
            (
                main_window_.screen_geometry.width()
                - int(
                    main_window_.screen_geometry.width() / 50
                    + main_window_.left_bar.width()
                    + 40
                )
                - 40
            ),
            90,
        )
        self.header.move(
            int(
                main_window_.screen_geometry.width() / 50
                + main_window_.left_bar.width()
                + 40
            ),
            50,
        )

        # __________________________________________________________

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
        self.btn_addtask.clicked.connect(lambda: self.popup_addtask.toggle_popup())

        # ____________________________________________________________

        self.scroll_area = QtWidgets.QScrollArea(parent=self)
        self.scroll_area.setStyleSheet(css.scroll_area)
        self.scroll_area.setMinimumSize(
            self.header.width(), int(main_window_.left_bar.height() - 120)
        )

        self.scroll_area.move(
            int(
                main_window_.screen_geometry.width() / 50
                + main_window_.left_bar.width()
                + 40
            ),
            int(self.header.height() + self.header.y() + 30),
        )

        # This div only purpose is to hold the grid with all the task squares
        # Then, We insert this div inside the ScrollArea
        self.div_task_layout = QtWidgets.QWidget(parent=self.scroll_area)
        self.div_task_layout.setMinimumSize(
            self.scroll_area.width() - 20, self.scroll_area.height()
        )

        self.div_task_layout.setStyleSheet(css.div_task_layout)

        self.tasks_grid_layout = MyTasksLayout(task_window_=self)
        self.div_task_layout.setLayout(self.tasks_grid_layout)
        self.scroll_area.setWidget(self.div_task_layout)


# ______________________________________________________________________________________________________


class PopUpAddTask(QtWidgets.QLabel):
    def __init__(self, parent: MyTasksWindow, main_window_: Main_Window):
        super(PopUpAddTask, self).__init__(parent=parent)
        self.setStyleSheet(css.popup_addtask)
        self.setMinimumSize(500, 500)

        self.parent_widget = parent

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
        self.btn_close_popup.clicked.connect(self.close_popup)
        self.btn_close_popup.move(435, 15)

        self.input_task_description = QtWidgets.QLineEdit(parent=self)
        self.input_task_description.setStyleSheet(css.task_creation_input)
        self.input_task_description.setMinimumSize(400, 40)
        self.input_task_description.move(
            250 - self.input_task_description.width() // 2, 150
        )
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
        self.input_task_urgency.addItems(["Low", "Medium", "High"])
        self.input_task_urgency.setStyleSheet(css.task_creation_input)
        self.input_task_urgency.setMinimumSize(400, 40)
        self.input_task_urgency.move(250 - self.input_task_urgency.width() // 2, 335)

        self.lbl_task_urgency = QtWidgets.QLabel("Task urgency:", parent=self)
        self.lbl_task_urgency.setStyleSheet(css.lbl_task)
        self.lbl_task_urgency.move(250 - self.input_task_urgency.width() // 2, 305)

        self.btn_add_new_task = QtWidgets.QPushButton("ADD TASK", parent=self)
        self.btn_add_new_task.setMinimumSize(self.width() // 2, 60)
        self.btn_add_new_task.setStyleSheet(css.btn_add_task)
        self.btn_add_new_task.move(
            int(self.width() / 2 - self.btn_add_new_task.width() / 2),
            int(self.height() - self.btn_add_new_task.height() - 35),
        )
        self.btn_add_new_task.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_add_new_task.clicked.connect(
            lambda: self.add_new_task(
                task_description=self.input_task_description.text(),
                task_date=self.input_task_date.text(),
                task_urgency=self.input_task_urgency.currentText(),
                tasks_window=parent,
                main_window_=main_window_,
            )
        )

    @QtCore.Slot()
    def toggle_popup(self):
        if self.isVisible() == False:
            self.show()
            self.raise_()
            self.parent_widget.adjustSize()
            self.parent_widget.update()

    @QtCore.Slot()
    def close_popup(self):
        self.input_task_description.clear()
        self.input_task_date.setDate(QtCore.QDate.currentDate())
        self.hide()

    @QtCore.Slot()
    def add_new_task(
        self, task_description, task_date, task_urgency, tasks_window, main_window_
    ):

        new_task = {
            "description": task_description,
            "date": task_date,
            "urgency": task_urgency,
            "id": str(uuid.uuid4()),
        }

        tasks = get_tasks()
        tasks.append(new_task)

        with open(JSON_PATH, "w", encoding="utf8") as json_file:
            json.dump(tasks, json_file, indent=4, ensure_ascii=True)  # type: ignore

        # Add the task we just created to the grid
        tasks_window.tasks_grid_layout.update_layout()
        self.btn_close_popup.click()


class PopUpTaskInfo(QtWidgets.QLabel):
    def __init__(self, parent: MyTasksWindow, main_window_: Main_Window):
        super(PopUpTaskInfo, self).__init__(parent)
        self.parent_widget = parent
        self.setStyleSheet(css.popup_addtask)
        self.setMinimumSize(500, 500)
        x = int(main_window_.screen_geometry.width() / 2 - (500 / 2))
        y = int(main_window_.screen_geometry.height() / 2 - (500 / 2))
        self.move(x, y)

        self.task_info_header = QtWidgets.QLabel("Task Info", parent=self)
        self.task_info_header.setStyleSheet(css.task_info_header)
        self.task_info_header.move(500 // 2 - self.task_info_header.width() // 2, 50)

        self.btn_close_popup = QtWidgets.QPushButton("X", parent=self)
        self.btn_close_popup.setMinimumSize(50, 30)
        self.btn_close_popup.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_close_popup.setStyleSheet(css.btn_close_popup)
        self.btn_close_popup.clicked.connect(self.close_popup)
        self.btn_close_popup.move(435, 15)

    @QtCore.Slot()
    def toggle_popup(self):
        if self.isVisible() == False:
            self.show()
            self.raise_()
            self.parent_widget.adjustSize()
            self.parent_widget.update()

    @QtCore.Slot()
    def close_popup(self):
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    main_window = Main_Window()
    main_window.showMaximized()
    sys.exit(app.exec())
