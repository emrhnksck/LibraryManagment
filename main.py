from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector
from dbinfo import host, user, password
from PyQt5.QtWidgets import QTableWidgetItem
import datetime
from xlrd import *
from xlsxwriter import *



ui, _ = loadUiType("untitled.ui")
loginui,_ = loadUiType("login.ui")

class Login(QWidget, loginui):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.db_connect()
        self.qdark_theme()
        self.pushButton.clicked.connect(self.handle_login)

    def db_connect(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password)
        self.mycursor = self.mydb.cursor()

    def qdark_theme(self):
        style = open("theme/style.css","r")
        style = style.read()
        self.setStyleSheet(style)

    def handle_login(self):

        try:
            username = self.lineEdit.text()
            pswrd = self.lineEdit_2.text()

            self.mycursor.execute(f"SELECT * FROM library.users WHERE username = '{username}'")
            info = self.mycursor.fetchone()
            if username == info[1] and pswrd == info[3]:
                self.window2 = MainApp()
                self.close()
                self.window2.show()
        except:
            self.label.setText("Sorry, your password was incorrect. Please double-check your password.")

class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_changes()
        self.Handle_butons()
        self.qdark_theme()

        self.db_connect()

        self.show_category()
        self.show_author()
        self.show_publisher()

        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()

        self.show_all_clients()
        self.show_all_books()
        self.show_all_operations()

    def Handle_UI_changes(self):
        #self.hideThemes()
        self.tabWidget.tabBar().setVisible(False)

    def Handle_butons(self):
        self.pushButton_2.clicked.connect(self.open_client_tab)
        #self.pushButton_8.clicked.connect(self.hideThemes)
        self.pushButton.clicked.connect(self.open_days_to_day_tab)
        self.pushButton_5.clicked.connect(self.open_books_tab)
        self.pushButton_4.clicked.connect(self.open_users_tab)
        self.pushButton_3.clicked.connect(self.open_settings_tab)

        self.pushButton_17.clicked.connect(self.add_category)

        self.pushButton_19.clicked.connect(self.add_author)

        self.pushButton_20.clicked.connect(self.add_publisher)
        # Delete/Edit Books buttons
        self.pushButton_7.clicked.connect(self.add_new_book)
        self.pushButton_12.clicked.connect(self.search_books)
        self.pushButton_9.clicked.connect(self.edit_books)
        self.pushButton_13.clicked.connect(self.deleteBook)

        # User buttons
        self.pushButton_14.clicked.connect(self.add_new_user)
        self.pushButton_15.clicked.connect(self.login)
        self.pushButton_16.clicked.connect(self.edit_user)

        #Client Buttons
        self.pushButton_10.clicked.connect(self.add_client)     #add client
        self.pushButton_18.clicked.connect(self.search_client)  # client search
        self.pushButton_11.clicked.connect(self.edit_client)    #edit client
        self.pushButton_25.clicked.connect(self.delete_client)  #delete client

        #day operatinn buttons
        self.pushButton_6.clicked.connect(self.day_operations)

        #excel operation buttons
        self.pushButton_8.clicked.connect(self.export_day_operations)
        self.pushButton_21.clicked.connect(self.export_books)
        self.pushButton_22.clicked.connect(self.clienst_export)

    def db_connect(self):
        self.mydb = mysql.connector.connect(host=host, user=user, password=password)
        self.mycursor = self.mydb.cursor()

    '''def showThemes(self):
        self.groupBox_3.show()

    def hideThemes(self):
        self.groupBox_3.hide()
    '''
    def open_days_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(4)

#Day operation

    def day_operations(self):

        book_title = self.lineEdit.text()
        client_name = self.lineEdit_16.text()
        type = self.comboBox.currentText()
        days = self.comboBox_2.currentIndex() + 1
        date = datetime.date.today()
        to_date = date + datetime.timedelta(days=days)
        sql = "INSERT INTO library.daytoday(book_name,type,date,client,to_date) VALUES (%s,%s,%s,%s,%s)"
        values = [book_title,type,date,client_name,to_date]
        self.mycursor.execute(sql,values)
        self.mydb.commit()
        self.statusBar().showMessage("New operation added")


    def show_all_operations(self):

        self.mycursor.execute("SELECT * FROM library.daytoday")
        data = self.mycursor.fetchall()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for row in range(len(data)):
            for i in range(len(data[row])):
                self.tableWidget.setItem(row,i,QTableWidgetItem(str(data[row][i])))



# Books

    def add_new_book(self):
        try:
            book_title = self.lineEdit_2.text()
            book_description = self.textEdit.toPlainText()
            book_code = int(self.lineEdit_4.text())
            book_category = self.comboBox_5.currentIndex() + 1
            book_author = self.comboBox_6.currentIndex() + 1
            book_publisher = self.comboBox_4.currentIndex() + 1
            book_price = self.lineEdit_5.text()

            SQL = "INSERT INTO library.books (book_title,book_code,book_description, book_category ,book_price, " \
                  "book_author,book_publisher) VALUES (%s,%s,%s,%s,%s,%s,%s) "
            values = [book_title, book_code, book_description, book_category, book_price, book_author, book_publisher]

            self.mycursor.execute(SQL, values)
            self.mydb.commit()
            self.statusBar().showMessage("New book added")

            self.lineEdit_2.setText('')
            self.lineEdit_4.setText('')
            self.textEdit.setPlainText('')
            self.comboBox_5.setCurrentIndex(0)
            self.comboBox_6.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)
            self.lineEdit_5.setText('')
            self.show_all_books()

        except Exception as ex:
            print(ex)


    def show_all_books(self):
        self.mycursor.execute("SELECT * FROM library.books")
        data = self.mycursor.fetchall()
        self.tableWidget_3.setRowCount(len(data))
        self.tableWidget_3.setColumnCount(8)

        for row_index in range(len(data)):
            for i in range(8):
                self.tableWidget_3.setItem(row_index,i,QTableWidgetItem(str(data[row_index][i])))




    def search_books(self):

        book_title = self.lineEdit_17.text()

        self.mycursor.execute(f"SELECT * FROM library.books WHERE book_title = '{book_title}'")
        data = self.mycursor.fetchone()
        print(data)

        self.lineEdit_9.setText(data[1])
        self.lineEdit_10.setText(str(data[2]))
        self.comboBox_10.setCurrentIndex(data[4] - 1)
        self.comboBox_11.setCurrentIndex(data[6] - 1)
        self.comboBox_12.setCurrentIndex(data[7] - 1)
        self.lineEdit_8.setText(str(data[5]))
        self.textEdit_2.setPlainText(data[3])

    def edit_books(self):
        try:
            book_title = self.lineEdit_9.text()
            book_description = self.textEdit_2.toPlainText()
            book_code = int(self.lineEdit_10.text())
            book_category = self.comboBox_10.currentIndex() + 1
            book_author = self.comboBox_11.currentIndex() + 1
            book_publiser = self.comboBox_12.currentIndex() + 1
            book_price = self.lineEdit_8.text()

            search_book_title = self.lineEdit_17.text()
            sql = f"UPDATE library.books SET book_title ='{book_title}',book_description='{book_description}',book_code={book_code},book_category={book_category}," \
                  f"book_author={book_author},book_publisher={book_publiser},book_price={book_price} WHERE book_title='{search_book_title}' "

            self.mycursor.execute(sql)
            self.mydb.commit()
            self.statusBar().showMessage("Book Edited")
            self.show_all_books()
        except Exception as ex:
            print(ex)

    def deleteBook(self):
        book_title_delete = self.lineEdit_17.text()

        sql = f"DELETE FROM library.books WHERE book_title='{book_title_delete}'"
        warning = QMessageBox.warning(self, "Delete Book", "Delete Book?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.mycursor.execute(sql)
            self.mydb.commit()
            self.statusBar().showMessage("Book Deleted")
            self.show_all_books()

    def show_category_combobox(self):
        self.mycursor.execute("SELECT * FROM library.category")
        data = self.mycursor.fetchall()
        self.comboBox_5.clear()
        for cate in data:
            self.comboBox_5.addItem(str(cate[0]) + "-" + cate[1])
            self.comboBox_10.addItem(str(cate[0]) + "-" + cate[1])

    def show_author_combobox(self):
        self.mycursor.execute("SELECT * FROM library.author")
        data = self.mycursor.fetchall()
        self.comboBox_6.clear()
        for author in data:
            self.comboBox_6.addItem(str(author[0]) + "-" + author[1])
            self.comboBox_11.addItem(str(author[0]) + "-" + author[1])

    def show_publisher_combobox(self):
        self.mycursor.execute("SELECT * FROM library.publisher")
        data = self.mycursor.fetchall()
        self.comboBox_4.clear()
        for publisher in data:
            self.comboBox_4.addItem(str(publisher[0]) + "-" + publisher[1])
            self.comboBox_12.addItem(str(publisher[0]) + "-" + publisher[1])

# User

    def add_new_user(self):
        try:
            username = self.lineEdit_18.text()
            email = self.lineEdit_19.text()
            password = self.lineEdit_20.text()
            password2 = self.lineEdit_21.text()

            sql = "INSERT INTO library.users (username,email,user_password) VALUES (%s,%s,%s)"
            values = [username, email, password]

            if password == password2:
                self.mycursor.execute(sql, values)
                self.mydb.commit()
                self.statusBar().showMessage("Added New User")
            else:
                QMessageBox.warning(self, "Warning", "Passwords do not match!", QMessageBox.Ok)
        except Exception as ex:
            print(ex)

    def login(self):

        username = self.lineEdit_26.text()
        pswrd = self.lineEdit_27.text()

        try:
            self.mycursor.execute(f"SELECT * FROM library.users WHERE username = '{username}'")
            info = self.mycursor.fetchone()
            if username == info[1] and pswrd == info[3]:
                self.statusBar().showMessage("Logged in")
                self.groupBox_4.setEnabled(True)

                self.lineEdit_25.setText(info[1])
                self.lineEdit_23.setText(info[2])
                self.lineEdit_24.setText(info[3])

        except Exception as ex:
            QMessageBox.warning(self, "Error", "Username or password incorrect")


    def edit_user(self):
        changed_user_name = self.lineEdit_26.text()
        new_username = self.lineEdit_25.text()
        new_mail = self.lineEdit_23.text()
        new_password = self.lineEdit_24.text()
        new_password2 = self.lineEdit_22.text()

        try:
            if new_password == new_password2:
                self.mycursor.execute(f"UPDATE library.users SET username = '{new_username}',email ='{new_mail}',user_password = '{new_password}' "
                                      f"WHERE username = '{changed_user_name}' ")
                self.mydb.commit()
                self.statusBar().showMessage("User Updated")
            else:
                self.statusBar().showMessage("Passwords doesn't match")
        except Exception as ex:
            print(ex)

# Settings

    def add_category(self):
        try:
            category_name = self.lineEdit_28.text()
            self.mycursor.execute(f"INSERT INTO library.category (category_name) VALUES ('{category_name}')")
            self.mydb.commit()
            self.statusBar().showMessage("Added New Category")
            self.lineEdit_28.setText("")
            self.show_category()
            self.show_category_combobox()
        except Exception as ex:
            print(ex)

    def show_category(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(0)
        self.mycursor.execute("SELECT * FROM library.category")
        data = self.mycursor.fetchall()
        self.tableWidget_2.setRowCount(len(data))
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setHorizontalHeaderLabels(("Categorry Name", "Id"))
        row_index = 0
        for categories in data:
            self.tableWidget_2.setItem(row_index, 1, QTableWidgetItem(str(data[row_index][0])))
            self.tableWidget_2.setItem(row_index, 0, QTableWidgetItem(data[row_index][1]))
            row_index += 1

    def add_author(self):
        author_name = self.lineEdit_30.text()
        self.mycursor.execute(f"INSERT INTO library.author (author_name) VALUES ('{author_name}')")
        self.mydb.commit()
        self.lineEdit_30.setText("")
        self.statusBar().showMessage("Added New Author")
        self.show_author()
        self.show_author_combobox()

    def show_author(self):
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.setColumnCount(0)
        self.mycursor.execute("SELECT * FROM library.author")
        data = self.mycursor.fetchall()
        self.tableWidget_4.setRowCount(len(data))
        self.tableWidget_4.setColumnCount(2)
        self.tableWidget_4.setHorizontalHeaderLabels(("Author Name", "Id"))
        row_index = 0
        for categories in data:
            self.tableWidget_4.setItem(row_index, 1, QTableWidgetItem(str(data[row_index][0])))
            self.tableWidget_4.setItem(row_index, 0, QTableWidgetItem(data[row_index][1]))
            row_index += 1

    def add_publisher(self):
        publisher_name = self.lineEdit_31.text()
        self.mycursor.execute(f"INSERT INTO library.publisher (publisher_name) VALUES ('{publisher_name}')")
        self.mydb.commit()
        self.lineEdit_31.setText("")
        self.statusBar().showMessage("Added New Publisher")
        self.show_publisher()
        self.show_publisher_combobox()

    def show_publisher(self):
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.setColumnCount(0)
        self.mycursor.execute("SELECT * FROM library.publisher")
        data = self.mycursor.fetchall()
        self.tableWidget_5.setRowCount(len(data))
        self.tableWidget_5.setColumnCount(2)
        self.tableWidget_5.setHorizontalHeaderLabels(("Publisher Name", "Id"))
        row_index = 0
        for categories in data:
            self.tableWidget_5.setItem(row_index, 1, QTableWidgetItem(str(data[row_index][0])))
            self.tableWidget_5.setItem(row_index, 0, QTableWidgetItem(data[row_index][1]))
            row_index += 1

    def delete_book(self):
        pass



#Client

    def add_client(self):
        try:
            client_name= self.lineEdit_3.text()
            client_surname = self.lineEdit_6.text()
            client_mail = self.lineEdit_7.text()
            client_number = self.lineEdit_14.text()

            sql = "INSERT INTO library.clients (client_name,client_surname,client_mail,client_number) VALUES (%s,%s,%s,%s)"
            client_info = [client_name,client_surname,client_mail,client_number]

            self.mycursor.execute(sql,client_info)
            self.mydb.commit()
            self.statusBar().showMessage("New Client Added")

            self.lineEdit_3.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.lineEdit_14.setText("")
            self.show_all_clients()
        except Exception as ex:
            print(ex)

    def show_all_clients(self):
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.setColumnCount(0)
        self.mycursor.execute("SELECT * FROM library.clients")
        data = self.mycursor.fetchall()
        self.tableWidget_6.setRowCount(len(data))
        self.tableWidget_6.setColumnCount(5)
        self.tableWidget_6.setHorizontalHeaderLabels(("Client ID","Client Name","Client Surname","Client Mail","Client Number"))
        row_index = 0
        for clients in data:
            self.tableWidget_6.setItem(row_index,0,QTableWidgetItem(str(data[row_index][0])))
            self.tableWidget_6.setItem(row_index,1,QTableWidgetItem(data[row_index][1]))
            self.tableWidget_6.setItem(row_index,2,QTableWidgetItem(data[row_index][2]))
            self.tableWidget_6.setItem(row_index,3,QTableWidgetItem(data[row_index][3]))
            self.tableWidget_6.setItem(row_index,4,QTableWidgetItem(str(data[row_index][4])))
            row_index += 1


    def search_client(self):
        client_id = self.lineEdit_29.text()

        try:
            self.mycursor.execute(f"SELECT * FROM library.clients WHERE id={client_id} ")
            data = self.mycursor.fetchone()
            print(data)

            self.lineEdit_11.setText(data[1])
            self.lineEdit_12.setText(data[2])
            self.lineEdit_13.setText(data[3])
            self.lineEdit_15.setText(data[4])
        except:
            warning = QMessageBox.warning(self,"Error","There are no users with this ID.",QMessageBox.Ok)


    def edit_client(self):

        new_name = self.lineEdit_11.text()
        new_surname = self.lineEdit_12.text()
        new_mail = self.lineEdit_13.text()
        new_number = self.lineEdit_15.text()

        new_data = [new_name,new_surname,new_mail,new_number]

        sql = "UPDATE library.clients SET client_name = %s,client_surname = %s,client_mail = %s, client_number = %s"
        self.mycursor.execute(sql,new_data)
        self.mydb.commit()
        self.statusBar().showMessage("Client Updated")

    def delete_client(self):

        id = self.lineEdit_29.text()

        warning = QMessageBox.warning(self,"DELETE CLIENT","ARE YOU SURE DELETE THIS CLIENT?",QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.mycursor.execute(f"DELETE FROM library.clients WHERE id = {id}" )
            self.mydb.commit()
            self.statusBar().showMessage("Client Deleted")

            self.lineEdit_29.setText("")
            self.lineEdit_11.setText("")
            self.lineEdit_12.setText("")
            self.lineEdit_13.setText("")
            self.lineEdit_15.setText("")

#Excel

    def export_day_operations(self):

        self.mycursor.execute("SELECT * FROM library.daytoday")
        data = self.mycursor.fetchall()
        wb = Workbook("day_operations.xlsx")
        sheet = wb.add_worksheet()
        sheet.write(0,0,"ID")
        sheet.write(0,1,"Book Name")
        sheet.write(0,2,"Type")
        sheet.write(0,3,"From date")
        sheet.write(0,4,"Client")
        sheet.write(0,5,"To Date")
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet.write(row_number,column_number,str(item))
                column_number += 1
            row_number += 1
        wb.close()
        self.statusBar().showMessage("Day Operation Excel File Created Succesfully")

    def export_books(self):

        self.mycursor.execute("SELECT * FROM library.books")
        data = self.mycursor.fetchall()
        wb = Workbook("books.xlsx")
        sheet = wb.add_worksheet()
        sheet.write(0,0,"Book ID")
        sheet.write(0,1,"Book Title")
        sheet.write(0,2,"Book Code")
        sheet.write(0,3,"Book Description")
        sheet.write(0,4,"Book Category")
        sheet.write(0,5,"Book Price")
        sheet.write(0,6,"Book Author")
        sheet.write(0,7,"Book Publisher")
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet.write(row_number,column_number,str(item))
                column_number+=1
            row_number += 1
        wb.close()
        self.statusBar().showMessage("Books Excel File Created Succesfully ")

    def clienst_export(self):
        self.mycursor.execute("SELECT * FROM library.clients")
        data = self.mycursor.fetchall()
        wb = Workbook("clients.xlsx")
        sheet = wb.add_worksheet()
        sheet.write(0,0,"Client ID")
        sheet.write(0,1,"Client Name")
        sheet.write(0,2,"Client Surname")
        sheet.write(0,3,"Client Mail")
        sheet.write(0,4,"Client Number")
        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet.write(row_number,column_number,str(item))
                column_number+=1
            row_number+=1
        wb.close()
        self.statusBar().showMessage("Clients Excel File Created Succesfully")


#UI Theme
    def qdark_theme(self):
        style = open("theme/style.css","r")
        style = style.read()
        self.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    win = Login()
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
