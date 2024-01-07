import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QListWidgetItem


class CofeeBase:
    def __init__(self):
        connection = sqlite3.connect('coffee.sqlite')
        self.cur = connection.cursor()

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


class CoffeeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.database = CofeeBase()
        uic.loadUi('main.ui', self)
        self.update()

    def update(self):
        list_of_names = self.database.get_all_names()
        for name in list_of_names:
            item = QListWidgetItem(name[0])
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.item_clicked)

    def item_clicked(self, item):
        name = item.text()
        result = self.database.get_infromation(name)
        self.ID_lab.setText(str(result[0]))
        self.name_lab.setText(result[1])
        self.degree.setText(result[2])
        self.status.setText(result[3])
        self.taste.setText(result[4])
        self.price.setText(str(result[5]))
        self.volum.setText(str(result[6]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeGUI()
    ex.show()
    sys.exit(app.exec_())
