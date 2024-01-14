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
                    # Hata durumunda kullanıcıya bilgi mesajı göster
            messagebox.showerror("Veri Tabanı Hatası", "Veri tabanına bağlanılamadı. Lütfen internet bağlantısını kontrol edin.")
                    # Bağlantıyı kapat
            self.close_connection()

    def execute(self, query):
        try:
                    # Veritabanı sorgusunu gerçekleştir
            self.cursor.execute(query)
                    # Değişiklikleri kaydet
            self.connection.commit()
                    # İşlem başarılı, True değeri döndür
            return True
        finally:
                    # Hata olsa da olmasa da bağlantıyı kapat
            self.close_connection()

        def fetch(self, query):
            try:
                        # Veritabanı sorgusunu gerçekleştir
                self.cursor.execute(query)
                        # Sorgu sonuçlarını al
                result = self.cursor.fetchall()
                        # Sonuçları döndür
                return result
            except mysql.connector.Error as e:
                        # Hata durumunda kullanıcıya bilgi mesajı göster
                messagebox.showinfo("Veri Tabanı Hatası!", f"Veri alınırken hata oluştu: \n{e}")
                        # Hata durumunda False değeri döndür
                return False
            finally:
                        # Hata olsa da olmasa da bağlantıyı kapat
                self.close_connection()

        def close_connection(self):
            try:
                        # Bağlantıyı kapat
                self.connection.close()
            except AttributeError:
                        # AttributeError hatası oluştuysa (bağlantı yoksa) geç
                pass
