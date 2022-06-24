from PyQt6 import uic,QtWidgets
import sqlite3

def função_principal():
    defeito = qt.lineEdit.text()
    modelo = qt.comboBox.currentText()
    
    try:
        banco = sqlite3.connect('banco_defeitos.db')
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Defeitos (Defeito text,Modelo tex)")
        cursor.execute("INSERT INTO Defeitos VALUES('"+defeito+"','"+modelo+"')")
        banco.commit()
        banco.close()
        qt.lineEdit.setText("")

    except sqlite3.Error as erro:
        print("Erro ao salvar os dados:",erro)
    

app = QtWidgets.QApplication([])
qt=uic.loadUi("qt.ui")
qt.comboBox.addItems(["Renegade","Toro","Compass","Commander"])
qt.pushButton.clicked.connect(função_principal)
qt.show()
app.exec()