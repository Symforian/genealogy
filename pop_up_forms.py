from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout,
                             QGroupBox, QLabel, QLineEdit, QListWidget,
                             QVBoxLayout, QCheckBox)


class pop_up_form(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self, name, origins=[(0, 'Unknown')]):
        QDialog.__init__(self)
        self.origins = origins
        self.createFormGroupBox()
        ok = QDialogButtonBox.Ok
        btnBox = QDialogButtonBox(ok | QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.accept)
        btnBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(btnBox)
        self.setLayout(mainLayout)
        self.setWindowTitle(name)
        self.show()
        self.exec_()

    def createFormGroupBox(self):
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
        check_dead = QCheckBox("Is dead?")
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

    def getResults(self):
        ret = [self.nl.text(), self.sl.text(), self.bl.text()]
        ret += [self.dl.text()]
        if self.origin.currentItem() is None:
            ret += ['Unknown']
        else:
            ret += [self.origins[self.origin.currentItem().type()][1]]
        return ret

    def toggle_state(self, check):
        if check.isEnabled():
            check.setEnabled(False)
            check.clear()
        else:
            check.setEnabled(True)
