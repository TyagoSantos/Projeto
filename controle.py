from asyncio import streams
from PyQt6 import uic,QtWidgets
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
import sqlite3
from reportlab.pdfgen import canvas 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

def email():
    host = "smtp.gmail.com"
    porta = "587"
    login = "tfs16@discente.ifpe.edu.br"
    senha = "Sport@0408"
    
    server = smtplib.SMTP(host, porta)
    server.ehlo()
    server.starttls()
    server.login(login,senha)

    attachment = open(r"C:\Users\tyago\OneDrive\Documentos\Pojeto\Relatório_PDF")
    att = MIMEBase('application', 'pdf')
    att.set_payload((attachment).read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', "attachment; filename= Relatório_PDF")
    attachment.close()
   


    email = qt_2.lineEdit.text()
    qt_2.lineEdit.setText("")
    if email == "":
        QMessageBox.about(qt_2, "alerta", "Informe o email")
    else:
        QMessageBox.about(qt_2, "alerta","Enviado")

    corpo = "Segue Relatório"
    msg = MIMEMultipart()
    msg['From'] = 'tfs16@discente.ifpe.edu.br'
    msg['To'] = email
    msg['Subject'] = "Relatório de Defeitos"
    msg.attach(MIMEText(corpo,'plain'))
    msg.attach(att)

    server.sendmail(login,email,msg.as_string())
    server.quit
   

def relatorio_pdf():
    banco = sqlite3.connect('banco_defeitos.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * From Defeitos")
    lista_defeitos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("Relatório_PDF")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(150,800,"Histórico de Defeitos")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(20,750,"Defeito")
    pdf.drawString(250,750,"Modelo")
    pdf.drawString(380,750,"Data")
    pdf.drawString(510,750,"Hora")

    for i in range(0, len(lista_defeitos)):
        y = y + 50
        pdf.drawString(10,750 - y,str(lista_defeitos[i][0]))
        pdf.drawString(250,750 - y,str(lista_defeitos[i][1]))
        pdf.drawString(380,750 - y,str(lista_defeitos[i][2]))
        pdf.drawString(510,750 - y,str(lista_defeitos[i][3]))

    pdf.save()


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
    if defeito == "":
        QMessageBox.about(qt, "alerta", "Informe o defeito")
    else:
        QMessageBox.about(qt, "alerta","Enviado")

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
qt_2.pushButton_2.clicked.connect(relatorio_pdf)
qt_2.pushButton.clicked.connect(email)

qt.show()
app.exec()