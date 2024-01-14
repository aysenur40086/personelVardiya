import mysql.connector
from tkinter import messagebox 

class vt:
    def __init__(self):
        try:
            # Veritabanına bağlantı yap
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="vardiyaotomasyonu"
            )
                                # Bağlantı üzerinde bir imleç oluştur
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Veri Tabanı Hatası", "Veri tabanına bağlanılamadı. Lütfen internet bağlantısını kontrol edin.")
            self.close_connection()

    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        finally:
            self.close_connection()

    def fetch(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            messagebox.showinfo("Veri Tabanı Hatası!", f"Veri alınırken hata oluştu: \n{e}")
            return False
        finally:
            self.close_connection()

    def close_connection(self):
        try:
            self.connection.close()
        except AttributeError:
            pass
