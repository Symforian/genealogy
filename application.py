import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from program import program
from pop_up_forms import pop_up_form as puf, pop_up_select as pus


class app_window(QMainWindow):
    def add_m_el(self, name, shortcut, tip, funct):
        elementAction = QtWidgets.QAction(name, self)
        elementAction.setShortcut(shortcut)
        elementAction.setStatusTip(tip)
        elementAction.triggered.connect(funct)
        return elementAction

    def __init__(self, p):
        QMainWindow.__init__(self)
        self.prog = p
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Genealogy")
        self.create_menubar()

    def create_menubar(self):
        mainMenu = QtWidgets.QMenuBar(self)
        mainMenu.setObjectName("menubar")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        fileMenu = mainMenu.addMenu('&File')
        fileMenu = self.create_filemenu(fileMenu)
        editMenu = mainMenu.addMenu('&Edit')
        editMenu = self.create_editmenu(editMenu)
        focusMenu = mainMenu.addMenu('&Focus')
        focusMenu = self.create_focusmenu(focusMenu)
        self.setMenuBar(mainMenu)

    def create_filemenu(self, fileMenu):
        tip = 'New file'
        newAct = self.add_m_el('&New', "Ctrl+N", tip, self.file_new)
        tip = 'Import GEDCOM file'
        importAct = self.add_m_el('&Import', "Ctrl+O", tip, self.file_open)
        tip = 'Export GEDCOM file'
        exportAct = self.add_m_el('&Export', "Ctrl+E", tip, self.file_export)
        fileMenu.addAction(newAct)
        fileMenu.addAction(importAct)
        fileMenu.addAction(exportAct)

    def create_editmenu(self, editMenu):
        tip = 'Add person'
        addAct = self.add_m_el('&Add', "Ctrl+A", tip, self.add_person)
        tip = 'Modify person'
        modAct = self.add_m_el('&Modify', "Ctrl+M", tip, self.mod_person)
        tip = 'Remove person'
        remAct = self.add_m_el('&Remove', "Ctrl+R", tip, self.rem_person)
        editMenu.addAction(addAct)
        editMenu.addAction(modAct)
        editMenu.addAction(remAct)

    def create_focusmenu(self, focusMenu):
        tip = 'Select person'
        selAct = self.add_m_el('&Select', "Ctrl+F", tip, self.sel_person)
        tip = 'Deselect'
        desAct = self.add_m_el('&Deselect', "Ctrl+D", tip, self.deselect)
        focusMenu.addAction(selAct)
        focusMenu.addAction(desAct)

    def file_new(self):
        # TODO somekind of warning
        self.prog = program()

    def file_open(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        name = name[0][name[0].rfind('/')+1:-4]
        print(name)
        self.prog.import_gedcom(name)
        self.prog.show()

    def file_export(self):
        # TODO popup to chose name of file
        self.prog.export_gedcom("ExportedGedcomData")

    def add_person(self):
        origins = self.prog.get_ids_desc('family')
        pop = puf("Add person", origins)
        if pop.result() == pop.DialogCode.Accepted:
            (n, s, b, d, o) = pop.getResults()
            self.prog.add_entry(n, s, b, d, o)
            self.prog.show()

    def mod_person(self):
        people = self.prog.get_ids_desc('person')
        if people != []:
            pop = pus(people)
            if pop.result() == pop.DialogCode.Accepted:
                pid = pop.getResult()
                data = self.prog.get_person_data(pid)
                ori = self.prog.get_ids_desc('family')
                pop = puf("Modify person", origins=ori, pdata=data)
                (n, s, b, d, o) = pop.getResults()
                self.prog.mod_entry(pid, n, s, b, d, o)
                self.prog.show()
        else:
            print("Error no ppl to select from")

    def rem_person(self):
        people = self.prog.get_ids_desc('person')
        if people != []:
            pop = pus(people)
            if pop.result() == pop.DialogCode.Accepted:
                pid = pop.getResult()
                self.prog.rem_entry(pid)
                self.prog.show()
        else:
            print("Error no ppl to select from")

    def sel_person(self):
        pass

    def deselect(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = app_window(program())
    window.show()
    sys.exit(app.exec_())
