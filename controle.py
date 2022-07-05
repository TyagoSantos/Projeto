from PyQt6 import uic,QtWidgets
from datetime import datetime
import sqlite3

def menu_consulta():
    qt_2.show()
    banco = sqlite3.connect('banco_defeitos.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * From Defeitos")
    lista_defeitos = cursor.fetchall()
    qt_2.tableWidget.setRowCount(len(lista_defeitos))
    qt_2.tableWidget.setColumnCount(4)
        
    for i in range(0, len(lista_defeitos)):
        for j in range(0,4):
            qt_2.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(lista_defeitos[i][j])))

    banco.close()

def menu():
    defeito = qt.lineEdit.text()
    modelo = qt.comboBox.currentText()
    data = datetime.today().strftime('%d-%m-%Y')
    hora = datetime.today().strftime('%H:%M')


    try:
        banco = sqlite3.connect('banco_defeitos.db')
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Defeitos (Defeito text,Modelo text,Data text, Hora text)")
        cursor.execute("INSERT INTO Defeitos VALUES('"+defeito+"','"+modelo+"','"+data+"','"+hora+"')")
        banco.commit()
        banco.close()
        qt.lineEdit.setText("")

    except sqlite3.Error as erro:
        print("Erro ao salvar os dados:",erro)

app = QtWidgets.QApplication([])
qt_2 = uic.loadUi("qt_2.ui")
qt = uic.loadUi("qt.ui")
qt.comboBox.addItems(["Renegade","Toro","Compass","Commander"])
qt.pushButton.clicked.connect(menu)
qt.pushButton_2.clicked.connect(menu_consulta)
qt.show()
app.exec()
