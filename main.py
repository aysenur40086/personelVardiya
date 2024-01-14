# arayuz modülünden App sınıfını içe aktar
from arayuz import App

# Ana fonksiyon
def main():
    # App sınıfından bir nesne oluştur
    app = App()
    
    # Uygulama döngüsünü başlat
    app.root.mainloop()

# Eğer bu dosya doğrudan çalıştırılıyorsa main fonksiyonunu çağır
if __name__ == "__main__":
    main()
