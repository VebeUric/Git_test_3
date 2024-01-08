import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem


class CofeeBase:
    def __init__(self):
        self.connection = sqlite3.connect('coffee.sqlite')
        self.cur = self.connection.cursor()

    def change_item(self, data, id):
        need_list = ['name', 'degree_of_doneness', 'ground_or_grains', 'taste', 'price', 'volume']
        for tmp in range(0, 6):
            query = f'''
            UPDATE cofee_information
            SET {', '.join(f'{key} = ?' for key in need_list)} WHERE ID = ?
            '''
            self.cur.execute(query, (*data, id))
            self.connection.commit()

    def add_item(self, data):
        query = '''
        INSERT INTO cofee_information
        (name, degree_of_doneness, ground_or_grains, taste, price, volume)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cur.execute(query, data)
        self.connection.commit()

    def get_all_names(self):
        query = """
        SELECT name FROM cofee_information
        """
        return self.cur.execute(query).fetchall()

    def get_infromation(self, name):
        query = """
        SELECT * FROM cofee_information
        WHERE name = ?
        """
        return self.cur.execute(query, (name,)).fetchone()


class addEditCoffeeForm(QWidget):
    def __init__(self, database, update):
        super().__init__()
        self.update = update
        self.data = None
        self.inf_before = None
        self.database = database
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.edit_item)
        self.label.hide()

    def edit_item(self):
        try:
            if not (
                    self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text()
                    and self.lineEdit_4.text() and self.lineEdit_6.text() and self.lineEdit.text()):
                self.label.show()
            else:
                self.label.hide()
                data = self.get_data()
                if self.inf_before:
                    self.database.change_item(data, self.inf_before[0])
                else:
                    self.database.add_item(data)
                self.update()
        except Exception as e:
            print(e)

    def get_data(self):
        name = self.lineEdit.text()
        degree = self.lineEdit_2.text()
        status = self.lineEdit_3.text()
        taste = self.lineEdit_4.text()
        price = self.lineEdit_6.text()
        volum = self.lineEdit_7.text()
        return name, degree, status, taste, price, volum


class CoffeeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.result = None
        uic.loadUi('main.ui', self)
        self.isChoused = None
        self.add_butt.clicked.connect(self.add_coffee)
        self.change_but.clicked.connect(self.edit_coffee)
        self.database = CofeeBase()
        self.error_label.hide()
        self.editfrom = addEditCoffeeForm(self.database, self.update)
        self.update()

    def show_editWidget(self):
        try:
            self.editfrom.lineEdit.setText(self.result[1])
            self.editfrom.lineEdit_2.setText(self.result[2])
            self.editfrom.lineEdit_3.setText(self.result[3])
            self.editfrom.lineEdit_4.setText(self.result[4])
            self.editfrom.lineEdit_6.setText(str(self.result[5]))
            self.editfrom.lineEdit_7.setText(str(self.result[6]))
            self.editfrom.inf_before = self.result
            self.editfrom.show()
        except Exception as e:
            print(e)

    def add_coffee(self):
        self.editfrom.lineEdit.setText('')
        self.editfrom.lineEdit_2.setText('')
        self.editfrom.lineEdit_3.setText('')
        self.editfrom.lineEdit_4.setText('')
        self.editfrom.lineEdit_6.setText('')
        self.editfrom.lineEdit_7.setText('')
        self.editfrom.inf_before = None
        self.editfrom.show()

    def edit_coffee(self):
        if self.isChoused:
            self.error_label.hide()
            self.show_editWidget()
        else:
            self.error_label.show()

    def update(self):
        self.listWidget.clear()
        list_of_names = self.database.get_all_names()
        for name in list_of_names:
            item = QListWidgetItem(name[0])
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.item_clicked)

    def item_clicked(self, item):
        name = item.text()
        if name:
            self.isChoused = True
        self.result = self.database.get_infromation(name)
        self.ID_lab.setText(str(self.result[0]))
        self.name_lab.setText(self.result[1])
        self.degree.setText(self.result[2])
        self.status.setText(self.result[3])
        self.taste.setText(self.result[4])
        self.price.setText(str(self.result[5]))
        self.volum.setText(str(self.result[6]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeGUI()
    ex.show()
    sys.exit(app.exec_())
