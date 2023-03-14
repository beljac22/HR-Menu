
"""GUI Module for Employee Information
We provide a default form with common Employee information, then inherit and subclass
to create custom forms for each type.
Ira Woodring
Winter 2023
"""

import csv

from PyQt6 import QtWidgets
from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QLabel, QLineEdit, QMenu, QHeaderView, QTableView, QMainWindow, QAbstractItemView, \
    QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QComboBox, QApplication, QMessageBox
import sys
from abc import ABC

from employee import *
from typing import *


class HRTableModel(QAbstractTableModel):
    """
    The HRTableModel allows us to display our information in a QTableView."""
    def __init__(self, data) -> None:
        super(HRTableModel, self).__init__()
        self._columns = ["ID#", "Type", "Name", "Pay", "Email"]
        self._data = data

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> str:
        """Gives the header info in a format PyQt wants."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            # return f"Column {section + 1}"
            return self._columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return f"{section + 1}"

    def data(self, index, role) -> str:
        """Returns the data at some table index."""
        if role == Qt.ItemDataRole.DisplayRole:
            e = self._data[index.row()]
            field = e.id_number
            if index.column() == 1:
                field = type(e).__name__
            if index.column() == 2:
                field = e.name
            if index.column() == 3:
                if isinstance(e, Salaried):
                    field = '${:,.2f}'.format(e.yearly)
                else:
                    field = '${:,.2f}'.format(e.hourly)
            if index.column() == 4:
                field = e.email
            return field

    def rowCount(self, index) -> int:
        """Provides the way for PyQt to get our row count."""
        return len(self._data)

    def columnCount(self, index) -> int:
        """Provides the column count, as PyQt expects."""
        return len(self._columns)


class MainWindow(QMainWindow):
    """MainWindow will have menus and a central list widget."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Employee Management v1.0.0")
        self.resize(800, 600)
        self._data = []
        self.load_file()
        self._model = HRTableModel(self._data)
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._table.setAlternatingRowColors(True)
        self._header = self._table.horizontalHeader()
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self._table)
        self._create_menu_bar()
        self._employee_form = None
        self._about_form = AboutForm()

    def _create_menu_bar(self) -> None:
        # Create the menus.
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = QMenu("&File", self)
        edit_menu = QMenu("&Edit", self)
        help_menu = QMenu("&Help", self)
        self._exit_action = QAction("&Exit")
        self._exit_action.triggered.connect(exit)
        self._load_action = QAction("&Load HR Data")
        self._save_action = QAction("&Save HR Data")
        self._save_action.setShortcut('Ctrl+S')
        file_menu.addAction(self._load_action)
        self._load_action.setShortcut('Ctrl+O')
        self._load_action.triggered.connect(self.load_file)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._exit_action)
        self._edit_action = QAction("&Edit current employee")
        edit_menu.addAction(self._edit_action)
        self._edit_action.triggered.connect(self.edit_employee)
        self._edit_action.setShortcut('Ctrl+E')
        self._save_action.triggered.connect(self.save_file)
        self._about_action = QAction("About this software")
        self._about_action.triggered.connect(self.show_help)
        help_menu.addAction(self._about_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)
        menu_bar.addMenu(help_menu)
        self.setMenuBar(menu_bar)

    def show_help(self) -> None:
        """Our 'help' form merely shows who wrote this, the version, and a description."""
        self._about_form.show()

    def data_to_rows(self) -> List[str]:
        """It is sometimes useful for us to have our model data as a list.  This method
        provides that feature."""
        data = [] 
        for e in self._data:
            row = [e.id_number, type(e).__name__, e.name]
            if isinstance(e, Salaried):
                row.append(str(e.yearly))
            else:
                row.append(str(e.hourly))
            row.append(e.email)
            data.append(row)
        return data

    def refresh_width(self) -> None:
        """Resize our table to fit our data width."""
        self._header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    def edit_employee(self) -> None:
        """Update an employee object by populating the correct type of form with the selected type of
        employee data."""
        index = self._table.selectionModel().selectedIndexes()
        if not index:
            return
        index = index[0].row()
        curr_employee = self._data[index]
        if isinstance(self._data[index], Executive):
            # passes the parent window and current employee into the instance of the class
            self._employee_form = ExecutiveForm(self, curr_employee)
        if isinstance(self._data[index], Manager):
            # passes the parent window and current employee into the instance of the class
            self._employee_form = ManagerForm(self, curr_employee)
        if isinstance(self._data[index], Permanent):
            # passes the parent window and current employee into the instance of the class
            self._employee_form = PermanentForm(self, curr_employee)
        if isinstance(self._data[index], Temporary):
            # passes the parent window and current employee into the instance of the class
            self._employee_form = TempForm(self, curr_employee)
        self._employee_form.fill_in(index)
        self._employee_form.show()

    def load_file(self) -> None:
        """Jack Bellgowan
        Read a representation of all of our Employees from a file and store in our
        _data variable.  The table will automatically be populated by this variable."""
        with open('employee.data.csv') as datafile:
            reader = csv.reader(datafile, quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                # will crash if any empty lines are im employee data, appends
                # a version of the class specified in the save file by converting it from text to a python command
                exec(f"self._data.append({row[0]}(\"{row[1]}\",\"{row[2]}\","
                     f"{row[4]},"+row[5].replace("!",",")+"))")
                # sets the object that was created to have an image from the save file
                self._data[-1].image = row[3]


    def save_file(self) -> None:
        """Jack Bellgowan
        Save a representation of all the Employees to a file."""
        # opens the employee save file
        with open("employee.data.csv", "w") as file:
            # iterates over each employee
            for employee in self._data:
                # adds each employee to the save file
                file.write(f"{employee.__repr__()}\n")

class EmployeeForm(QtWidgets.QWidget):
    """There will never be a generic employee form, but we don't want to repeat code,
    so we put it all here.  Each subtype of form will add to it."""
    def __init__(self, parent: QApplication, employee: Employee, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        outer_layout = QVBoxLayout()
        # object of type Employee corresponding to what type of form the window is
        self._employee: Employee = employee
        # Sets size of window to make image fit
        self.setFixedSize(400,550)
        # parent application of the form
        self._parent: QApplication = parent
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(outer_layout)
        self._id_label = QLabel()
        self.layout.addRow(QLabel("ID#"), self._id_label)
        self._name_edit = QLineEdit()
        self.layout.addRow(QLabel("Name: "), self._name_edit)
        self._pay_edit = QLineEdit()
        self._email_edit = QLineEdit()
        self.layout.addRow(QLabel("Email address:"), self._email_edit)
        self._image_path_edit = QLineEdit()
        self.layout.addRow(QLabel("Image path:"), self._image_path_edit)
        self._image = QLabel()
        self._image.setPixmap(QPixmap(self._employee.image))
        self.layout.addWidget(self._image)
        update = QPushButton("Update")
        update.clicked.connect(self.update_employee)
        outer_layout.addLayout(self.layout)
        outer_layout.addWidget(update)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        # message box object
        self._msg: QMessageBox = QMessageBox()
        # sets Icon of the window
        self._msg.setIcon(QMessageBox.Icon.Warning)

    def update_employee(self) -> None:
        """Change the selected employee's data to the updated values."""
        # tries to change the image, name and email of employee, shows the error window if
        # the input is invalid
        try:
            # changes employee name
            self._employee.name = self._name_edit.text()
            # changes employee name
            self._employee.email = self._email_edit.text()
            # changes employee name
            if self._image_path_edit.text():
                self._employee.image = self._image_path_edit.text()
            else:
                self._employee.image = self._employee.IMAGE_PLACEHOLDER
        except ValueError as error:
            # opens error window
            self.error_handler(error)
        self._parent.refresh_width()
        self.setVisible(False)

    def fill_in(self, index) -> None:
        """Upon opening the form, we wish to add the selected employee's data
        to the fields."""
        self._employee = self._parent._data[index]
        self.setWindowTitle("Edit " + type(self._employee).__name__ + " Employee Information")
        self._id_label.setText(str(self._employee.id_number))
        self._name_edit.setText(self._employee.name)
        self._email_edit.setText(self._employee.email)
        if self._employee.image == Employee.IMAGE_PLACEHOLDER:
            self._image_path_edit.setText('')
        else:
            self._image_path_edit.setText(self._employee.image)
        # makes the image the same size regardless of resolution, places image
        self._image.setPixmap(QPixmap(self._employee.image).scaled(300, 300))
        self.show()

    def error_handler(self, error_message: str) -> None:
        """ Tim Lightner
        Accepts error message as a str, returns None.
        Triggers an error pop up message with a specified message
        """
        # sets text to the text of the error message
        self._msg.setText(str(error_message))
        # sets the title of the window
        self._msg.setWindowTitle("Error")
        # places OK button
        self._msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        # creates window
        self._msg.exec()


# Complete the following forms so that they update and fill-in
# their custom information.

class SalariedForm(EmployeeForm):
    """Jack Bellgowan
    Object of type salaried, never referenced directly
    """
    def __init__(self, parent: MainWindow, employee: Employee):
        """Jack Bellgowan
        takes parent as a type Parent, and employee as type Employee
        Constructor for object of type SalariedForm
        returns None
        """
        # super class's constructor
        super().__init__(parent, employee)
        # adds a row corresponding to pay amount
        self.layout.addRow(QLabel("Salary:"), self._pay_edit)

    def fill_in(self, index: int) -> None:
        """Jack Bellgowan
        fills in the employee info to the window
        Accepts index as an int argument
        Returns None
        """
        # super class's fill_in() method
        super().fill_in(index)
        # sets the text to the employee's yearly salary
        self._pay_edit.setText(str(self._employee.yearly))

    def update_employee(self) -> None:
        """Jack Bellgowan
        Updates the employee info stored in self._employee
        returns None
        """
        # super class's fill_in() method
        super().update_employee()
        # checks if salary is blank
        if self._pay_edit.text():
            # sets salary to float value of text box
            self._employee.yearly = float(self._pay_edit.text())
        else:
            # raises error message to be handled elsewhere
            raise ValueError('Salary cannot be blank')

class ExecutiveForm(SalariedForm):
    def __init__(self, parent, employee):
        """Jack Bellgowan

        """
        super().__init__(parent, employee)
        self._role_cb = QComboBox()
        self._role_cb.addItems(role.name.upper() for role in Role)
        self.layout.addRow(self._role_cb)

    def fill_in(self, index) -> None:
        """Jack Bellgowan

        """
        super().fill_in(index)
        self.layout.addRow(self._role_cb)
        self._role_cb.setCurrentIndex([role for role in Role].index(self._employee.role))

    def update_employee(self) -> None:
        """Jack Bellgowan

        """
        try:
            super().update_employee()
            self._employee.role = Role[self._role_cb.currentText().upper()]
        except ValueError as error:
            self.error_handler(error)


class ManagerForm(SalariedForm):
    """Jack Bellgowan

    """
    def __init__(self, parent, employee):
        """Jack Bellgowan

        """
        super().__init__(parent, employee)
        self.dept_cb = QComboBox()
        self.dept_cb_items = [dept.name.title().replace("_"," ") for dept in Department]
        self.dept_cb.addItems(dept.name.title().replace("_"," ") for dept in Department)
        self.layout.addRow(self.dept_cb)

    def fill_in(self, index) -> None:
        """Jack Bellgowan

        """
        super().fill_in(index)
        self.layout.addRow(self.dept_cb)
        self.dept_cb.setCurrentIndex([dept for dept in Department].index(self._employee.department))

    def update_employee(self) -> None:
        """Jack Bellgowan

        """
        try:
            super().update_employee()
            self._employee.department = Department[self.dept_cb.currentText().upper().replace(" ","_")]
        except ValueError as error:
            self.error_handler(error)

class HourlyForm(EmployeeForm):
    """Jack Bellgowan

    """
    def __init__(self,parent, employee):
        """Jack Bellgowan

        """
        super().__init__(parent, employee)
        self.layout.addRow(QLabel("Hourly:"), self._pay_edit)
    def fill_in(self, index) -> None:
        """Jack Bellgowan

        """
        super().fill_in(index)
        self._pay_edit.setText(str(self._employee.hourly))

    def update_employee(self) -> None:
        """Jack Bellgowan

        """
        try:
            super().update_employee()
            self._employee.hourly = float(self._pay_edit.text())
        except ValueError as error:
            self.error_handler(error)


class TempForm(HourlyForm):
    """Jack Bellgowan

    """
    def __init__(self, parent, employee):
        """Jack Bellgowan

        """
        super().__init__(parent, employee)


    def fill_in(self, index) -> None:
        """Jack Bellgowan

        """
        super().fill_in(index)
        self.layout.addRow(QLabel("Last day: "), QLabel(str(self._employee.last_day)))


class PermanentForm(HourlyForm):
    """Jack Bellgowan

    """
    def __init__(self, parent, employee):
        """Jack Bellgowan

        """
        super().__init__(parent, employee)

    def fill_in(self, index) -> None:
        """Jack Bellgowan

        """
        super().fill_in(index)
        self.layout.addRow(QLabel("Hired date: "), QLabel(str(self._employee.hired_date)))


class AboutForm(QtWidgets.QWidget):
    """An About Form just gives information about our app to users who want to see it.  Automatically
    sets itself visible on creation."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("HR Management System"))
        self.layout.addWidget(QLabel("version 1.0.0"))
        self.layout.addWidget(QLabel("A simple system for storing important pieces of information about employees."))
        self.close = QPushButton("Close")
        self.close.clicked.connect(self.close_form)
        self.layout.addWidget(self.close)
        self.setLayout(self.layout)

    def close_form(self) -> None:
        """
        Hide the form."""
        self.setVisible(False)





def main():
    app = QApplication(sys.argv)
    mf = MainWindow()
    mf.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    main()
