"""
    Application window module.
    Is responsible for:

    Creating GUI using PyQt5.

    Running program with GUI.
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                             QWidget, QScrollArea)
from PyQt5.QtGui import QPixmap
from program import Program
from pop_ups import PopUpForm, PopUpSelect, PopUpError, PopUpYesNo


class AppWindow(QMainWindow):
    def add_menu_el(self, name, shortcut, tip, funct):
        """Add element to the menubar."""
        elementAction = QtWidgets.QAction(name, self)
        elementAction.setShortcut(shortcut)
        elementAction.setStatusTip(tip)
        elementAction.triggered.connect(funct)
        return elementAction

    def __init__(self, p):
        """Initialize new window with given program `p` state."""
        QMainWindow.__init__(self)
        self.prog = p
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Genealogy")
        self.create_menubar()
        self.create_imgbox_area()

    def create_imgbox_area(self):
        """Create place to display tree img."""
        self.imgbox = QLabel(self)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.lay = QVBoxLayout(self.central_widget)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.imgbox)
        self.lay.addWidget(self.scroll)

    def update_imgbox(self, name):
        """Load new img in the tree place."""
        self.pixmap = QPixmap(name)
        self.imgbox.setPixmap(self.pixmap)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.show()

    def create_menubar(self):
        mainMenu = QtWidgets.QMenuBar(self)
        mainMenu.setObjectName("menubar")
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        fileMenu = mainMenu.addMenu('&File')
        self.create_filemenu(fileMenu)
        editMenu = mainMenu.addMenu('&Edit')
        self.create_editmenu(editMenu)
        focusMenu = mainMenu.addMenu('&Focus')
        self.create_focusmenu(focusMenu)
        self.setMenuBar(mainMenu)

    def create_filemenu(self, fileMenu):
        """Create filemenu in menubar."""
        tip = 'New file'
        newAct = self.add_menu_el('&New', "Ctrl+N", tip, self.file_new)
        tip = 'Import GEDCOM file'
        importAct = self.add_menu_el('&Import', "Ctrl+O", tip, self.file_open)
        tip = 'Export GEDCOM file'
        exportAct = self.add_menu_el('&Export', "Ctrl+E", tip,
                                     self.file_export)
        tip = 'Closes program without saving'
        closeAct = self.add_menu_el('&Quit', "Esc", tip, self.close)
        fileMenu.addAction(newAct)
        fileMenu.addAction(importAct)
        fileMenu.addAction(exportAct)
        fileMenu.addAction(closeAct)

    def create_editmenu(self, editMenu):
        """Create editmenu in menubar."""
        tip = 'Add person'
        addAct = self.add_menu_el('&Add', "Ctrl+A", tip, self.add_person)
        tip = 'Modify person'
        modAct = self.add_menu_el('&Modify', "Ctrl+M", tip, self.mod_person)
        tip = 'Connect two people, either marriage or common children'
        conAct = self.add_menu_el('&Connect', "Ctrl+C", tip, self.connect)
        tip = 'Remove person'
        remAct = self.add_menu_el('&Remove', "Ctrl+R", tip, self.rem_person)
        editMenu.addAction(addAct)
        editMenu.addAction(modAct)
        editMenu.addAction(conAct)
        editMenu.addAction(remAct)

    def create_focusmenu(self, focusMenu):
        """Create focusmenu in menubar."""
        tip = 'Select person'
        selAct = self.add_menu_el('&Select', "Ctrl+F", tip, self.sel_person)
        tip = 'Deselect'
        desAct = self.add_menu_el('&Deselect', "Ctrl+D", tip, self.deselect)
        focusMenu.addAction(selAct)
        focusMenu.addAction(desAct)

    def file_new(self):
        """Clear program state."""
        msg = "Do you really want to close currently opened tree?\n"
        pop = PopUpYesNo(msg)
        if (pop.result() == pop.DialogCode.Accepted):
            self.prog = Program()
            self.update_imgbox(self.prog.show())

    def file_open(self):
        """Open new file and import to the program state."""
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if (len(name[0])):
            self.prog.import_gedcom(name[0])
            self.update_imgbox(self.prog.show())

    def file_export(self):
        """Export current program data to [temp] fixed filename."""
        file_types = "GEDcom files (*.GED)"
        qfile = QtWidgets.QFileDialog
        filename = qfile.getSaveFileName(self, 'Save File', None, file_types)
        if (len(filename[0])):
            self.prog.export_gedcom(filename[0])

    def add_person(self):
        """Add person functionality `CTRL+A`."""
        origins = self.prog.get_ids_desc('family')
        pop = PopUpForm("Add person", origins)
        if pop.result() == pop.DialogCode.Accepted:
            (name, surname, birth, death, origin) = pop.get_results()
            self.prog.add_entry(name, surname, birth, death, origin)
            self.update_imgbox(self.prog.show())

    def choose_person(self):
        """Open window to chose person."""
        people = self.prog.get_ids_desc('person')
        if people:
            pop = PopUpSelect(people)
            if pop.result() == pop.DialogCode.Accepted:
                return True, pop.get_result()
        else:
            PopUpError("No people to select from.")
        return False, None

    def mod_person(self):
        """Modify person functionality `CTRL+M`."""
        (was_found, results) = self.choose_person()
        if was_found:
            data = self.prog.get_person_data(results)
            ori = self.prog.get_ids_desc('family')
            pop = PopUpForm("Modify person", origins=ori, pdata=data)
            if pop.result() == pop.DialogCode.Accepted:
                (name, surname, birth, death, origin) = pop.get_results()
                self.prog.mod_entry(results,
                                    name, surname, birth, death, origin)
                self.update_imgbox(self.prog.show())

    def rem_person(self):
        """Remove person functionality `CTRL+D`."""
        (was_found, results) = self.choose_person()
        if was_found:
            self.prog.rem_entry(results)
            self.update_imgbox(self.prog.show())

    def sel_person(self):
        """Focus person functionality `CTRL+F`."""
        (was_found, results) = self.choose_person()
        if was_found:
            self.prog.select(results)
            self.update_imgbox(self.prog.show())

    def deselect(self):
        """Clears all the colors from the nodes."""
        self.prog.select(None)
        self.update_imgbox(self.prog.show())
        print(self.prog.env.entries())

    def connect(self):
        """Connect people functionality `CTRL+C`."""
        (found_head, result_head) = self.choose_person()
        if found_head:
            (found_partner, result_partner) = self.choose_person()
            if found_partner:
                if result_head != result_partner:
                    self.prog.connect(result_head, result_partner)
                    self.update_imgbox(self.prog.show())
                else:
                    PopUpError("Cannot connect to a person to themselves.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow(Program())
    window.show()
    sys.exit(app.exec_())
