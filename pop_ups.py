"""
    Pop up window's module.

    Is responsible for creating and managing pop up windows.
"""
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout,
                             QGroupBox, QLabel, QLineEdit, QListWidget,
                             QVBoxLayout, QCheckBox, QComboBox, QErrorMessage)


class PopUpError(QErrorMessage):
    def __init__(self, msg):
        super().__init__()
        self.showMessage(msg)
        self.show()
        self.exec_()


class PopUpForm(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, name, origins=[(0, 'Unknown')], pdata=None):
        QDialog.__init__(self)
        self.origins = origins
        if self.origins != [(0, 'Unknown')]:
            self.origins = [(0, 'Unknown')] + self.origins
        self.create_form_group_box()
        ok = QDialogButtonBox.Ok
        btnBox = QDialogButtonBox(ok | QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.accept)
        btnBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(btnBox)
        if pdata is not None:
            self.update_data(pdata)
        self.setLayout(mainLayout)
        self.setWindowTitle(name)
        self.show()
        self.exec_()

    def create_form_group_box(self):
        self.formGroupBox = QGroupBox("Enter data")
        layout = QFormLayout()
        check_name = QCheckBox("Unknown")
        layout.addRow(check_name)
        self.nl = QLineEdit()
        layout.addRow(QLabel("Name:"), self.nl)
        check_surname = QCheckBox("Unknown")
        layout.addRow(check_surname)
        self.sl = QLineEdit()
        layout.addRow(QLabel("Surname:"), self.sl)
        check_birth = QCheckBox("Unknown")
        layout.addRow(check_birth)
        self.bl = QLineEdit()
        layout.addRow(QLabel("Birth:"), self.bl)
        check_dead = QCheckBox("Is alive? / Unknown")
        layout.addRow(check_dead)
        self.dl = QLineEdit()
        layout.addRow(QLabel("Death:"), self.dl)
        check_name.stateChanged.connect(lambda: self.toggle_state(self.nl))
        check_surname.stateChanged.connect(lambda: self.toggle_state(self.sl))
        check_birth.stateChanged.connect(lambda: self.toggle_state(self.bl))
        check_dead.stateChanged.connect(lambda: self.toggle_state(self.dl))
        self.origin = QListWidget()
        for i, el in list(enumerate(self.origins)):
            self.origin.insertItem(i, el[1])
        layout.addRow("Origin", self.origin)
        self.formGroupBox.setLayout(layout)

    def update_data(self, data):
        self.nl.setText(' '.join(data[0]))
        self.sl.setText(' '.join(data[1]))
        self.bl.setText(' '.join(data[2]))
        self.dl.setText(' '.join(data[3]))
        if data[4] is not None:
            index = list(map(lambda t: t[0], self.origins)).index(data[4])
        else:
            index = 0
        self.origin.setCurrentItem(self.origin.item(index))

    def get_results(self):
        ret = [self.nl.text().split(), self.sl.text().split()]
        ret += [self.bl.text().split(), self.dl.text().split()]
        if self.origin.currentItem() is None:
            ret += [0]
        else:
            id = self.origin.row(self.origin.currentItem())
            ret += [self.origins[id][0]]
        return ret

    def toggle_state(self, check):
        if check.isEnabled():
            check.setEnabled(False)
            check.clear()
        else:
            check.setEnabled(True)


class PopUpSelect(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, people):
        QDialog.__init__(self)
        self.ppl = people
        self.create_form_group_box()
        ok = QDialogButtonBox.Ok
        btnBox = QDialogButtonBox(ok | QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.accept)
        btnBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(btnBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Select person")
        self.show()
        self.exec_()

    def create_form_group_box(self):
        self.formGroupBox = QGroupBox("Chose person")
        layout = QFormLayout()
        self.cb = QComboBox()
        list_of_strings = list(map(lambda t: t[1], self.ppl))
        self.cb.addItems(list_of_strings)
        layout.addRow("Person", self.cb)
        self.formGroupBox.setLayout(layout)

    def get_result(self):
        return self.ppl[self.cb.currentIndex()][0]
