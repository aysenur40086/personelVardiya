import TKinterModernThemes as TKMT
from tkinter.ttk import Label, Entry, Frame, LabelFrame, Button, Treeview, Combobox, Separator, Checkbutton, Spinbox
from tkinter import Toplevel, messagebox, StringVar, IntVar, filedialog
from tkcalendar import DateEntry
from datetime import datetime
from fonksiyonlar import Fonk, Algoritma
from os import system

def geometry(root, frame):
    frame.update_idletasks()
    frame_width = frame.winfo_reqwidth()
    frame_height = frame.winfo_reqheight()

    root.geometry(f"{frame_width}x{frame_height}")

def tabloSırala(tree, col, reverse=False):
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    data.sort(reverse=reverse)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: tabloSırala(tree, col, not reverse))

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Giriş Yap", "park", "dark", usecommandlineargs=True, useconfigfile=True)
        self.root.resizable(False, False)
        self.root.iconbitmap("icon.ico")

        self.girisFrame = Frame(self.root)
        self.girisFrame.grid()

        self.kullaniciAdiLabel = Label(self.girisFrame, text="Kullanıcı Adı:")
        self.kullaniciAdiEntry = Entry(self.girisFrame)
        self.sifreLabel = Label(self.girisFrame, text="Şifre:")
        self.sifreEntry = Entry(self.girisFrame, show="•")
        self.girisButton = Button(self.girisFrame, text="Giriş Yap", command=self.giris_yap)

        self.kullaniciAdiLabel.grid(row=0, column=0, padx=10, pady=20)
        self.sifreLabel.grid(row=1, column=0, padx=10, pady=20)
        self.kullaniciAdiEntry.grid(row=0, column=1, padx=10, pady=20)
        self.sifreEntry.grid(row=1, column=1, padx=10, pady=20)
        self.girisButton.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

        self.run(cleanresize=False)

    def giris_yap(self):
        if self.kullaniciAdiEntry.get() != "" and self.sifreEntry.get() != "":
            if Fonk(self.kullaniciAdiEntry.get(), self.sifreEntry.get()).giris_yap():
                self.kullanici = Fonk(kullaniciAdi=self.kullaniciAdiEntry.get()).kullanici_al()
                self.girisFrame.destroy()
                if self.kullanici[14] == "Yönetici":
                    Admin(self.root, self.kullanici)
                else:
                    Personel(self.root, self.kullanici)
            else:
                messagebox.showerror("Hatalı Bilgi!", "Hatalı kullanıcı adı veya şifre.")

class Admin(App):
    def __init__(self, root, kullanici):
        self.root = root
        self.kullanici = kullanici
        self.root.title(f"Personel Takip Sitemi | {self.kullanici[1]} - Yönetici")

        self.adminFrame = Frame(self.root)
        self.adminFrame.grid()

        self.yeniButton = Button(self.adminFrame, text="Yeni Personel", command=lambda: self.yeni_personel("yeni"))
        self.yeniButton.grid(row=0, column=0, padx=10, pady=10)

        self.izinButton = Button(self.adminFrame, text="İzin", command=self.izin_ayarlar)
        self.izinButton.grid(row=1, column=0, padx=10, pady=10)

        self.vardiyaButton = Button(self.adminFrame, text="Vardiya", command=self.vardiya_ayarlar)
        self.vardiyaButton.grid(row=2, column=0, padx=10, pady=10)

        self.mesaiButton = Button(self.adminFrame, text="Mesai", command=self.mesai_ayarlar)
        self.mesaiButton.grid(row=3, column=0, padx=10, pady=10)

        self.ozelGunlerButton = Button(self.adminFrame, text="Özel Günler", command=self.ozel_gunler_ayarlar)
        self.ozelGunlerButton.grid(row=4, column=0, padx=10, pady=10)

        self.tablo = Treeview(self.adminFrame, columns=("Sicil Numarası", "İsim", "Telefon", "Rol"), show="headings", selectmode="browse")
        self.tablo.heading("#1", text="Sicil Numarası", command=lambda: tabloSırala(self.tablo, "Sicil Numarası", False))
        self.tablo.heading("#2", text="İsim", command=lambda: tabloSırala(self.tablo, "Sicil Numarası", False))
        self.tablo.heading("#3", text="Telefon", command=lambda: tabloSırala(self.tablo, "Telefon", False))
        self.tablo.heading("#4", text="Rol", command=lambda: tabloSırala(self.tablo, "Rol", False))
        self.tablo.column("#1", width=120, stretch=False)
        self.tablo.column("#2", width=220, stretch=False)
        self.tablo.column("#3", width=120, stretch=False)
        self.tablo.column("#4", width=80, stretch=False)
        self.tablo.grid(row=0, column=1, columnspan=3, rowspan=5, padx=20, pady=20)

        self.tablo_güncelle()

        def kullanici_duzenle(event):
            if self.tablo.item(self.tablo.selection())["values"]:
                self.yeni_personel("düzenle", Fonk(sicilNo=self.tablo.item(self.tablo.selection())["values"][0]).kullanici_al()[0])

        self.tablo.bind("<Double-1>", kullanici_duzenle)

    def tablo_güncelle(self):
        self.tablo.delete(*self.tablo.get_children())
        for self.i in Fonk().kullanici_al():
            self.tablo.insert("", "end", values=(self.i[11], (self.i[3], self.i[4]), self.i[9], self.i[14]))

    def yeni_personel(self, tip=("yeni", "düzenle"), personel=None):
        self.yeniTop = Toplevel(self.root)
        self.yeniTop.withdraw()
        self.yeniTop.resizable(False, False)
        self.yeniTop.iconbitmap("icon.ico")
        self.yeniTop.grab_set()

        self.yeniFrame = Frame(self.yeniTop)
        self.kullaniciFrame = LabelFrame(self.yeniFrame, text="Hesap Bilgileri")
        self.personelFrame = LabelFrame(self.yeniFrame, text="Kişisel Bilgiler")
        self.isFrame = LabelFrame(self.yeniFrame, text="İş Bilgileri")

        self.yeniFrame.grid()
        self.kullaniciFrame.grid(row=0, column=0, padx=10, pady=(30, 5))
        self.personelFrame.grid(row=0, column=1, rowspan=2, padx=10)
        self.isFrame.grid(row=1, column=0, padx=10, pady=(5, 30))

        self.kullaniciAdiLabel = Label(self.kullaniciFrame, text="Kullanıcı Adı:").grid(row=0, column=0, padx=10, pady=10)
        self.sifreLabel = Label(self.kullaniciFrame, text="Şifre:").grid(row=1, column=0, padx=10, pady=10)
        self.kullaniciAdiEntry = Entry(self.kullaniciFrame)
        self.sifreEntry = Entry(self.kullaniciFrame, show="•")
        self.kullaniciAdiEntry.grid(row=0, column=1, padx=10, pady=10)
        self.sifreEntry.grid(row=1, column=1, padx=10, pady=10)
        
        self.isimLabel = Label(self.personelFrame, text="İsim:").grid(row=0, column=0, padx=10, pady=10)
        self.soyisimLabel = Label(self.personelFrame, text="Soyisim:").grid(row=1, column=0, padx=10, pady=10)
        self.tcLabel = Label(self.personelFrame, text="TC No:").grid(row=2, column=0, padx=10, pady=10)
        self.dogumLabel = Label(self.personelFrame, text="Doğum Tarihi:").grid(row=3, column=0, padx=10, pady=10)
        self.cinsiyetLabel = Label(self.personelFrame, text="Cinsiyeti:").grid(row=4, column=0, padx=10, pady=10)
        self.sicilLabel = Label(self.personelFrame, text="Sicil No:").grid(row=5, column=0, padx=10, pady=10)
        self.adresLabel = Label(self.personelFrame, text="Adres:").grid(row=6, column=0, padx=10, pady=10)
        self.mailLabel = Label(self.personelFrame, text="Mail:").grid(row=7, column=0, padx=10, pady=10)
        self.telefonLabel = Label(self.personelFrame, text="Telefon:").grid(row=8, column=0, padx=10, pady=10)
        self.isimEntry = Entry(self.personelFrame)
        self.soyisimEntry = Entry(self.personelFrame)
        self.tcEntry = Entry(self.personelFrame)
        self.dogumVar = StringVar()
        self.dogumEntry = DateEntry(self.personelFrame, textvariable=self.dogumVar, locale="tr_TR")
        self.cinsiyetCombo = Combobox(self.personelFrame, values=("Erkek", "Kadın"), state="readonly")
        self.sicilEntry = Entry(self.personelFrame)
        self.adresEntry = Entry(self.personelFrame)
        self.mailEntry = Entry(self.personelFrame)
        self.telefonEntry = Entry(self.personelFrame)
        self.isimEntry.grid(row=0, column=1, padx=10, pady=10)
        self.soyisimEntry.grid(row=1, column=1, padx=10, pady=10)
        self.tcEntry.grid(row=2, column=1, padx=10, pady=10)
        self.dogumEntry.grid(row=3, column=1, padx=10, pady=10)
        self.cinsiyetCombo.grid(row=4, column=1, padx=10, pady=10)
        self.sicilEntry.grid(row=5, column=1, padx=10, pady=10)
        self.adresEntry.grid(row=6, column=1, padx=10, pady=10)
        self.mailEntry.grid(row=7, column=1, padx=10, pady=10)
        self.telefonEntry.grid(row=8, column=1, padx=10, pady=10)

        def tatil2_ayarla(event):
            if self.rolCombo.get() == "Taşeron":
                self.tatil2Combo["state"] = "disabled"
                self.tatil2Combo.current(0)
            else:
                self.tatil2Combo["state"] = "readonly"

        self.unvanLabel = Label(self.isFrame, text="Ünvan:").grid(row=0, column=0, padx=10, pady=10)
        self.rolLabel = Label(self.isFrame, text="Rol:").grid(row=1, column=0, padx=10, pady=10)
        self.tatil1Label = Label(self.isFrame, text="1. Tatil:").grid(row=4, column=0, padx=10, pady=10)
        self.tatil2Label = Label(self.isFrame, text="2. Tatil:").grid(row=5, column=0, padx=10, pady=10)
        self.unvanEntry = Entry(self.isFrame)
        self.rolCombo = Combobox(self.isFrame, state="readonly", values=("Memur", "Taşeron", "Yönetici"))
        self.tatil1Combo = Combobox(self.isFrame, state="readonly", values=("-", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"))
        self.tatil2Combo = Combobox(self.isFrame, state="readonly", values=("-", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"))
        self.unvanEntry.grid(row=0, column=1, padx=10, pady=10)
        self.rolCombo.grid(row=1, column=1, padx=10, pady=10)
        self.tatil1Combo.grid(row=4, column=1, padx=10, pady=10)
        self.tatil2Combo.grid(row=5, column=1, padx=10, pady=10)
        self.rolCombo.bind("<<ComboboxSelected>>", tatil2_ayarla)

        def kaydet(tip=("yeni", "düzenle")):
            if all([self.kullaniciAdiEntry.get(), self.sifreEntry.get(), self.isimEntry.get(), self.soyisimEntry.get(), self.tcEntry.get(), self.sicilEntry.get(), self.adresEntry.get(), self.mailEntry.get(), self.telefonEntry.get(), self.unvanEntry.get(), self.rolCombo.get()]):
                if tip == "yeni":
                    if Fonk().yeni_kullanici(self.kullaniciAdiEntry.get(), self.sifreEntry.get(), self.isimEntry.get(), self.soyisimEntry.get(), self.tcEntry.get(), self.dogumEntry.get_date(), self.cinsiyetCombo.get(), self.adresEntry.get(), self.telefonEntry.get(), self.mailEntry.get(), self.sicilEntry.get(), self.unvanEntry.get(), self.rolCombo.get(), self.tatil1Combo.get(), self.tatil2Combo.get(), datetime.now().strftime("%Y-%m-%d")):
                        messagebox.showinfo("Kayıt Başarılı!", "Yeni kullanici başarıyla kaydedildi.", parent=self.yeniTop)
                        self.tablo_güncelle()
                        self.yeniTop.destroy()
                    else:
                        messagebox.showerror("Kayıt başarısız!", "Yeni kullanıcı kaydedilemedi:\n- Kullanıcı adı ve sicil numarası eşsiz olmalıdır.", parent=self.yeniTop)
                else:
                    if Fonk().kullanici_guncelle(self.personel[1], self.personel[11], self.kullaniciAdiEntry.get(), self.sifreEntry.get(), self.isimEntry.get(), self.soyisimEntry.get(), self.tcEntry.get(), self.dogumEntry.get_date(), self.cinsiyetCombo.get(), self.adresEntry.get(), self.telefonEntry.get(), self.mailEntry.get(), self.sicilEntry.get(), self.unvanEntry.get(), self.rolCombo.get(), self.tatil1Combo.get(), self.tatil2Combo.get(), datetime.now().strftime("%Y-%m-%d")):
                        messagebox.showinfo("Güncelleme Başarılı!", "Yeni kullanici başarıyla güncellendi.", parent=self.yeniTop)
                        self.tablo_güncelle()
                        self.yeniTop.destroy()
                    else:
                        messagebox.showerror("Güncelleme başarısız!", "Kullanıcı güncellenemedi.", parent=self.yeniTop)
            else:
                messagebox.showerror(message="Gerekli alanları doldurun!", parent=self.yeniTop)

        def sil():
            if messagebox.askquestion(message=f"{self.personel[1]} kullanıcısını silmek istediğine emin misin?", parent=self.yeniTop):
                if Fonk(sicilNo=self.personel[11]).kullanici_sil():
                    messagebox.showinfo(message=f"{self.personel[1]} kullanıcısı başarıyla silindi.", parent=self.yeniTop)
                    self.yeniTop.destroy()
                    self.tablo_güncelle()
                else:
                    messagebox.showerror(message=f"{self.personel[1]} kullanıcısı silinemedi.", parent=self.yeniTop)

        self.kaydetButton = Button(self.yeniFrame, text="Kaydet")
        self.iptalButton = Button(self.yeniFrame)
        self.kaydetButton.grid(row=2, column=0, padx=10, pady=10)
        self.iptalButton.grid(row=2, column=1, padx=10, pady=10)

        if tip == "yeni":
            self.yeniTop.title("Yeni Personel Ekle")

            self.cinsiyetCombo.current(0)
            self.rolCombo.current(0)
            self.tatil1Combo.current(0)
            self.tatil2Combo.current(0)

            self.kaydetButton["command"] = lambda: kaydet("yeni")
            self.iptalButton["command"] = lambda: self.yeniTop.destroy()
            self.iptalButton["text"] = "İptal"
        else:
            self.yeniTop.title("Personel Düzenle")
            self.personel = personel
            self.kullaniciAdiEntry.insert(0, self.personel[1])
            self.sifreEntry.insert(0, self.personel[2])
            self.isimEntry.insert(0, self.personel[3])
            self.soyisimEntry.insert(0, self.personel[4])
            self.tcEntry.insert(0, self.personel[5])
            self.dogumVar.set(f"{self.personel[6][8:]}.{self.personel[6][5:7]}.{self.personel[6][:4]}")
            self.cinsiyetCombo.set(self.personel[7])
            self.sicilEntry.insert(0, self.personel[11])
            self.adresEntry.insert(0, self.personel[8])
            self.mailEntry.insert(0, self.personel[10])
            self.telefonEntry.insert(0, self.personel[9])
            self.unvanEntry.insert(0, self.personel[12])
            self.rolCombo.set(self.personel[14])
            self.tatil1Combo.set(self.personel[15])
            self.tatil2Combo.set(self.personel[16])

            self.kaydetButton["command"] = lambda: kaydet("düzenle")
            self.iptalButton["command"] = sil
            self.iptalButton["text"] = "Sil"

        self.yeniTop.deiconify()

    def izin_ayarlar(self):
        self.izinTop = Toplevel(self.root)
        self.izinTop.withdraw()
        self.izinTop.resizable(False, False)
        self.izinTop.iconbitmap("icon.ico")
        self.izinTop.title("İzinler")
        self.izinTop.grab_set()

        self.izinFrame = Frame(self.izinTop)
        self.yeniIzinFrame = Frame(self.izinFrame)
        self.izinlerFrame = Frame(self.izinFrame)
        self.izinFrame.grid()
        self.yeniIzinFrame.grid(row=0, column=0)
        self.izinlerFrame.grid(row=1, column=0)

        self.personelLabel = Label(self.yeniIzinFrame, text="Personel:").grid(row=0, column=0, padx=10, pady=10)
        self.izinBaslamaLabel = Label(self.yeniIzinFrame, text="İzin Başlangıç:").grid(row=1, column=0, padx=10, pady=10)
        self.izinBitmeLabel = Label(self.yeniIzinFrame, text="İzin Bitme:").grid(row=2, column=0, padx=10, pady=10)

        self.personeller = []
        for self.i in Fonk().kullanici_al():
            self.personeller.append(f"{self.i[3]} {self.i[4]} - {self.i[11]}")
        self.personelCombo = Combobox(self.yeniIzinFrame, state="readonly" ,values=self.personeller)
        self.izinBaslamaEntry = DateEntry(self.yeniIzinFrame, locale="tr_TR")
        self.izinBitmeEntry = DateEntry(self.yeniIzinFrame, locale="tr_TR")
        self.personelCombo.grid(row=0, column=1, padx=10, pady=10)
        self.izinBaslamaEntry.grid(row=1, column=1, padx=10, pady=10)
        self.izinBitmeEntry.grid(row=2, column=1, padx=10, pady=10)

        def izinEkle():
            if all ([self.personelCombo.get(), self.izinBaslamaEntry.get_date(), self.izinBitmeEntry.get_date()]):
                if self.izinBaslamaEntry.get_date() < self.izinBitmeEntry.get_date():
                    self.isim = ' '.join(self.personelCombo.get().split(" - ")[0].split(" ")[:-1])
                    self.soyisim = self.personelCombo.get().split(" - ")[0].split(" ")[-1]
                    self.sicil = self.personelCombo.get().split(" - ")[-1]
                    if Fonk().izin_ekle(isim=self.isim, soyisim=self.soyisim, sicilNo=self.sicil, baslama=self.izinBaslamaEntry.get_date(), bitis=self.izinBitmeEntry.get_date()):
                        messagebox.showinfo("İzin Eklendi!", "İzin başarıyla eklendi.", parent=self.izinTop)
                        izinTabloGüncelle()
                    else:
                        messagebox.showerror("İzin Eklenemedi!", "İzin eklenemedi.", parent=self.izinTop)
                else:
                    messagebox.showerror("Hatalı Tarih!", "Son tarih, ilk tarihten küçük olamaz.", parent=self.izinTop)

        self.ekleButton = Button(self.yeniIzinFrame, text="Ekle", command=izinEkle)
        self.ekleButton.grid(row=1, column=3, padx=10, pady=10)

        def izinTabloGüncelle():
            self.izinlerTablo.delete(*self.izinlerTablo.get_children())
            for self.i in Fonk().kullanici_al(tablo="izinler"):
                self.izinlerTablo.insert("", "end", values=(self.i[0], (self.i[1], self.i[2]), self.i[3], self.i[4], self.i[5]))

        def double_click(event):
            if self.izinlerTablo.item(self.izinlerTablo.selection())["values"]:
                if messagebox.askyesno("İzin Sil!", "İzni silmek istediğinize emin misin?", parent=self.izinTop):
                    if Fonk().izin_sil(self.izinlerTablo.item(self.izinlerTablo.selection())["values"][0]):
                        messagebox.showinfo("İzin Silindi!", "İzin başarıyla silindi.", parent=self.izinTop)
                        izinTabloGüncelle()
                    else:
                        messagebox.showerror("İzin Silinemedi!", "İzin silinemedi.", parent=self.izinTop)

        self.izinlerTablo = Treeview(self.izinlerFrame, columns=("id", "İsim", "Sicil Numarası", "Başlangıç", "Bitiş"), show="headings", selectmode="browse")
        self.izinlerTablo.heading("#1", text="")
        self.izinlerTablo.heading("#2", text="İsim")
        self.izinlerTablo.heading("#3", text="Sicil Numarası")
        self.izinlerTablo.heading("#4", text="Başlangıç")
        self.izinlerTablo.heading("#5", text="Bitiş")
        self.izinlerTablo.column("#1", width=0)
        self.izinlerTablo.column("#2", width=150)
        self.izinlerTablo.column("#3", width=150)
        self.izinlerTablo.column("#4", width=150)
        self.izinlerTablo.column("#4", width=150)
        self.izinlerTablo["displaycolumns"]=("İsim", "Sicil Numarası", "Başlangıç", "Bitiş")
        self.izinlerTablo.grid(row=0, column=0, padx=10, pady=10)
        self.izinlerTablo.bind("<Double-1>", double_click)
        izinTabloGüncelle()

        self.izinTop.deiconify()

    def vardiya_ayarlar(self):
        self.vardiyaTop = Toplevel(self.root)
        self.vardiyaTop.withdraw()
        self.vardiyaTop.resizable(False, False)
        self.vardiyaTop.iconbitmap("icon.ico")
        self.vardiyaTop.grab_set()
        self.vardiyaTop.title("Vardiyalar")

        self.vardiyaFrame = Frame(self.vardiyaTop)
        self.yeniVardiyaFrame = Frame(self.vardiyaFrame)
        self.vardiyalarFrame = Frame(self.vardiyaFrame)
        self.vardiyaFrame.grid()
        self.yeniVardiyaFrame.grid(row=0, column=0)
        self.vardiyalarFrame.grid(row=1, column=0)

        self.personelLabel = Label(self.yeniVardiyaFrame, text="Personel:").grid(row=0, column=0, padx=10, pady=10)
        self.tarihLabel = Label(self.yeniVardiyaFrame, text="Tarih:").grid(row=1, column=0, padx=10, pady=10)
        self.tarih2Label = Label(self.yeniVardiyaFrame, text="Son Tarih:").grid(row=2, column=0, padx=10, pady=10)
        self.yerLabel = Label(self.yeniVardiyaFrame, text="Yer:").grid(row=3, column=0, padx=10, pady=10)
        self.saatLabel = Label(self.yeniVardiyaFrame, text="Saat:").grid(row=4, column=0, padx=10, pady=10)

        def saat_combo_ayarla(event):
            if self.yerCombo.get() == "Kampus Ici":
                self.saatCombo["values"] = ("08:00-16:00", "09:00-17:00")
                self.saatCombo.current(0)
            else:
                self.saatCombo["values"] = ("00:00-08:00", "08:00-16:00", "16:00-24:00")
                self.saatCombo.current(0)

        self.personeller = []
        for self.i in Fonk().kullanici_al():
            self.personeller.append(f"{self.i[3]} {self.i[4]} - {self.i[11]}")
        self.personelCombo = Combobox(self.yeniVardiyaFrame, state="readonly" ,values=self.personeller)
        self.tarihEntry = DateEntry(self.yeniVardiyaFrame, locale="tr_TR")
        self.tarih2Entry = DateEntry(self.yeniVardiyaFrame, locale="tr_TR")
        self.yerCombo = Combobox(self.yeniVardiyaFrame, values=("Kampus Ici", "Kampus Girisi"), state="readonly")
        self.saatCombo = Combobox(self.yeniVardiyaFrame, state="readonly")
        self.personelCombo.grid(row=0, column=1, padx=10, pady=10)
        self.tarihEntry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.tarih2Entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")
        self.yerCombo.grid(row=3, column=1, padx=10, pady=10)
        self.saatCombo.grid(row=4, column=1, padx=10, pady=10)
        self.yerCombo.bind("<<ComboboxSelected>>", saat_combo_ayarla)

        def vardiyaEkle():
            if all ([self.personelCombo.get(), self.tarihEntry.get_date(), self.yerCombo.get(), self.saatCombo.get()]):
                if self.tarihEntry.get_date() < self.tarih2Entry.get_date():
                    self.isim = ' '.join(self.personelCombo.get().split(" - ")[0].split(" ")[:-1])
                    self.soyisim = self.personelCombo.get().split(" - ")[0].split(" ")[-1]
                    self.sicil = self.personelCombo.get().split(" - ")[-1]
                    if Fonk().vardiya_ekle(isim=self.isim, soyisim=self.soyisim, sicilNo=self.sicil, tarih=self.tarihEntry.get_date(), yer=self.yerCombo.get(), saat=self.saatCombo.get()):
                        messagebox.showinfo("Vardiya Eklendi!", "Vardiya başarıyla eklendi.", parent=self.vardiyaTop)
                        vardiyaTabloGüncelle()
                    else:
                        messagebox.showerror("Vardiya Eklenemedi!", "Vardiya eklenemedi.", parent=self.vardiyaTop)
                else:
                    messagebox.showerror("Hatalı Tarih!", "Son tarih, ilk tarihten küçük olamaz.", parent=self.vardiyaTop)

        self.ekleButton = Button(self.yeniVardiyaFrame, text="Ekle", command=vardiyaEkle)
        self.ekleButton.grid(row=2, column=3, padx=10, pady=10)

        self.sep = Separator(self.yeniVardiyaFrame, orient='vertical')
        self.sep.grid(row=0, column=4, rowspan=5, sticky="ns")

        def checkCommand():
            if self.herkesVar.get():
                self.personelCombo["state"] = "disabled"
            else:
                self.personelCombo["state"] = "readonly"

            if self.tumTarihVar.get():
                self.tarihEntry["state"] = "disabled"
                self.tarih2Entry["state"] = "disabled"
            else:
                self.tarihEntry["state"] = "normal"
                self.tarih2Entry["state"] = "normal"

            if self.herkesVar.get() or self.tumTarihVar.get():
                self.yerCombo["state"] = "disabled"
                self.saatCombo["state"] = "disabled"
            else:
                self.yerCombo["state"] = "readonly"
                self.saatCombo["state"] = "readonly"

        self.herkesVar = IntVar()
        self.herkesCButton = Checkbutton(self.yeniVardiyaFrame, text="Herkes", variable=self.herkesVar, command=checkCommand)
        self.herkesCButton.grid(row=0, column=5, padx=10, pady=10, sticky="we")

        self.tumTarihVar = IntVar()
        self.tumTarihCButton = Checkbutton(self.yeniVardiyaFrame, text="Tüm Tarih", variable=self.tumTarihVar, command=checkCommand)
        self.tumTarihCButton.grid(row=1, column=5, padx=10, pady=10, sticky="we")

        def topluEkle():
            if self.tarihEntry.get_date() < self.tarih2Entry.get_date():
                if Algoritma(self.tarihEntry.get_date(), self.tarih2Entry.get_date()):
                    messagebox.showerror("İşlem Tamamlandı!", "Toplu vardiya ekleme tamamlandı.", parent=self.vardiyaTop)
                    vardiyaTabloGüncelle()
                else:
                    messagebox.showerror("İşlem Yapılamadı!", "Toplu vardiya ekleme tamamlanamadı.", parent=self.vardiyaTop)
            else:
                messagebox.showerror("Hatalı Tarih!", "Son tarih, ilk tarihten küçük olamaz.", parent=self.vardiyaTop)

        self.topluEkleButton = Button(self.yeniVardiyaFrame, text="Toplu Ekle", command=topluEkle)
        self.topluEkleButton.grid(row=2, column=5, padx=10, pady=10)

        def topluSil():
            if self.herkesVar.get() or self.tumTarihVar.get():
                if self.herkesVar.get():
                    self.tip = "herkes"
                if self.tumTarihVar.get():
                    self.tip = "tum_tarih"
                if self.herkesVar.get() and self.tumTarihVar.get():
                    self.tip = "hepsi"
            else:
                self.tip = "kisi"
                if self.personelCombo.get() == "":
                    return messagebox.showerror("Boş Bilgi!", "Personel bilgisini boş bırakmayın.", parent=self.vardiyaTop)

            self.isim = ' '.join(self.personelCombo.get().split(" - ")[0].split(" ")[:-1])
            self.soyisim = self.personelCombo.get().split(" - ")[0].split(" ")[-1]
            self.sicil = self.personelCombo.get().split(" - ")[-1]

            if self.tarihEntry.get_date() < self.tarih2Entry.get_date():
                if Fonk().toplu_sil(self.tip, self.isim, self.soyisim, self.sicil, self.tarihEntry.get_date(), self.tarih2Entry.get_date(), self.yerCombo.get(), self.saatCombo.get()):
                    vardiyaTabloGüncelle()
                    messagebox.showinfo("Toplu Silindi!", "Toplu silme işlemi başarıyla tamamlandı.", parent=self.vardiyaTop)
                else:
                    messagebox.showerror("Toplu Silinemedi!", "Toplu silme işlemi tamamlanamadı.", parent=self.vardiyaTop)
            else:
                messagebox.showerror("Hatalı Tarih!", "Son tarih, ilk tarihten küçük olamaz.", parent=self.vardiyaTop)

        self.topluSilButton = Button(self.yeniVardiyaFrame, text="Toplu Sil", command=topluSil)
        self.topluSilButton.grid(row=3, column=5, padx=10, pady=10)

        def listeAl():
            if self.herkesVar.get() or self.tumTarihVar.get():
                if self.herkesVar.get():
                    self.tip = "herkes"
                if self.tumTarihVar.get():
                    self.tip = "tum_tarih"
                if self.herkesVar.get() and self.tumTarihVar.get():
                    self.tip = "hepsi"
            else:
                self.tip = "kisi"
                if self.personelCombo.get() == "":
                    return messagebox.showerror("Boş Bilgi!", "Personel bilgisini boş bırakmayın.", parent=self.vardiyaTop)

            if self.tarihEntry.get_date() < self.tarih2Entry.get_date():
                self.path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF dosyası", "*.pdf")], initialfile=f'{datetime.now().strftime("%Y-%m-%d")}_Vardiyalar.pdf')
                if self.path:
                    self.islem = Fonk().pdf_olustur(self.tip, self.personelCombo.get().split(" - ")[-1], self.tarihEntry.get_date(), self.tarih2Entry.get_date(), "Vardiya Listesi", datetime.now().strftime("%Y-%m-%d"), path=self.path)
                    if self.islem:
                        if self.islem == "Veri Yok":
                            messagebox.showinfo("Liste Oluşturulamadı!", "PDF dosyası oluşturmak için yeterli veri yok.", parent=self.vardiyaTop)
                        else:
                            if messagebox.askquestion("Liste Oluşturuldu!", "PDF dosyası başarıyla oluşturuldu. Dosya açılsın mı?", parent=self.vardiyaTop):
                                system(f"start {self.path}")
            else:
                messagebox.showerror("Hatalı Tarih!", "Son tarih, ilk tarihten küçük olamaz.", parent=self.vardiyaTop)

        self.listeAlButton = Button(self.yeniVardiyaFrame, text="Liste Çıkart", command=listeAl)
        self.listeAlButton.grid(row=4, column=5, padx=10, pady=10)

        def vardiyaTabloGüncelle():
            self.vardiyalarTablo.delete(*self.vardiyalarTablo.get_children())
            for self.i in Fonk().kullanici_al(tablo="vardiyalar"):
                self.vardiyalarTablo.insert("", "end", values=(self.i[0], (self.i[1], self.i[2]), self.i[3], self.i[4], self.i[5], self.i[6]))

        def double_click(event):
            if self.vardiyalarTablo.item(self.vardiyalarTablo.selection())["values"]:
                if messagebox.askyesno("Vardiya Sil!", "Vardiyayı silmek istediğinize emin misin?", parent=self.vardiyaTop):
                    if Fonk().vardiya_sil(id=self.vardiyalarTablo.item(self.vardiyalarTablo.selection())["values"][0]):
                        messagebox.showinfo("Vardiya Silindi!", "Vardiya başarıyla silindi.", parent=self.vardiyaTop)
                        vardiyaTabloGüncelle()
                    else:
                        messagebox.showerror("Vardiya Silinemedi!", "Vardiya silinemedi.", parent=self.vardiyaTop)

        self.vardiyalarTablo = Treeview(self.vardiyalarFrame, columns=("id", "İsim", "Sicil Numarası", "Vardiya Tarihi", "Vardiya Yeri", "Vardiya Saati"), show="headings", selectmode="browse")
        self.vardiyalarTablo.heading("#1", text="")
        self.vardiyalarTablo.heading("#2", text="İsim")
        self.vardiyalarTablo.heading("#3", text="Sicil Numarası")
        self.vardiyalarTablo.heading("#4", text="Vardiya Tarihi")
        self.vardiyalarTablo.heading("#5", text="Vardiya Yeri")
        self.vardiyalarTablo.heading("#6", text="Vardiya Saati")
        self.vardiyalarTablo.column("#0", width=0)
        self.vardiyalarTablo.column("#1", width=150)
        self.vardiyalarTablo.column("#2", width=150)
        self.vardiyalarTablo.column("#3", width=150)
        self.vardiyalarTablo.column("#4", width=150)
        self.vardiyalarTablo.column("#5", width=150)
        self.vardiyalarTablo.column("#6", width=150)
        self.vardiyalarTablo["displaycolumns"]=("İsim", "Sicil Numarası", "Vardiya Tarihi", "Vardiya Yeri", "Vardiya Saati")
        self.vardiyalarTablo.grid(row=0, column=0, padx=10, pady=10)
        self.vardiyalarTablo.bind("<Double-1>", double_click)
        vardiyaTabloGüncelle()

        self.vardiyaTop.deiconify()

    def mesai_ayarlar(self):
        self.mesaiTop = Toplevel(self.root)
        self.mesaiTop.withdraw()
        self.mesaiTop.resizable(False, False)
        self.mesaiTop.iconbitmap("icon.ico")
        self.mesaiTop.grab_set()
        self.mesaiTop.title("Mesailer")

        self.mesaiFrame = Frame(self.mesaiTop)
        self.mesaiFrame.grid()

        def double_click(event):
            if self.mesaiTablo.item(self.mesaiTablo.selection())["values"]:
                self.mesaiAyarlaTop = Toplevel(self.mesaiTop)
                self.mesaiAyarlaTop.resizable(False, False)
                self.mesaiAyarlaTop.iconbitmap("icon.ico")
                self.mesaiAyarlaTop.grab_set()
                self.mesaiAyarlaTop.title("Mesai Ayarla")

                self.frame = Frame(self.mesaiAyarlaTop)
                self.izinFrame = LabelFrame(self.frame, text="İzin Ver")
                self.primFrame = LabelFrame(self.frame, text="Prim Ver")
                self.frame.grid()
                self.izinFrame.grid(row=0, column=0, padx=10, pady=10)
                self.primFrame.grid(row=0, column=1, padx=10, pady=10)

                self.izinBaslamaLabel = Label(self.izinFrame, text="İzin Başlangıç:").grid(row=0, column=0, padx=10, pady=10)
                self.izinBitmeLabel = Label(self.izinFrame, text="İzin Bitme:").grid(row=1, column=0, padx=10, pady=10)
                self.izinBaslamaEntry = DateEntry(self.izinFrame, locale="tr_TR")
                self.izinBitmeEntry = DateEntry(self.izinFrame, locale="tr_TR")
                self.izinBaslamaEntry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
                self.izinBitmeEntry.grid(row=1, column=1, padx=10, pady=10, sticky="we")

                def izin_ver():
                    if self.izinBaslamaEntry.get_date() < self.izinBitmeEntry.get_date():
                        self.isimSutun = self.mesaiTablo.item(self.mesaiTablo.selection())["values"][1]
                        self.isim = " ".join(self.isimSutun.split()[:-1])
                        self.soyisim = self.isimSutun.split()[-1]
                        self.sicil = self.mesaiTablo.item(self.mesaiTablo.selection())["values"][2]
                        if Fonk().izin_ekle(isim=self.isim, soyisim=self.soyisim, sicilNo=self.sicil, baslama=self.izinBaslamaEntry.get_date(), bitis=self.izinBitmeEntry.get_date()):
                            if Fonk().mesai_sil(tip="izin", id=self.mesaiTablo.item(self.mesaiTablo.selection())["values"][0], sicilNo=self.sicil):
                                self.mesaiAyarlaTop.destroy()
                                messagebox.showinfo("İzin Eklendi!", "İzin başarıyla eklendi.", parent=self.mesaiAyarlaTop)
                                mesai_tablo_güncelle()
                            else:
                                messagebox.showerror("Mesai Silinemedi!", "İzin eklendi ama mesai kaydı silinemedi.", parent=self.mesaiAyarlaTop)
                        else:
                            messagebox.showerror("İzin Eklenemedi!", "İzin eklenemedi.", parent=self.mesaiAyarlaTop)
                    else:
                        messagebox.showerror("Hatalı Tarih!", "Son tarih, ilk tarihten küçük olamaz.", parent=self.mesaiAyarlaTop)

                self.izinVerButton = Button(self.izinFrame, text="İzin Ver", command=izin_ver)
                self.izinVerButton.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

                self.validate_cmd = self.primFrame.register(lambda P: P.isdigit())
                self.primLabel = Label(self.primFrame, text="Prim:").grid(row=0, column=0, padx=10, pady=10)
                self.primSpin = Spinbox(self.primFrame, from_=1, to=1000000, increment=100, validate="key", validatecommand=(self.validate_cmd, "%P"))
                self.primSpin.grid(row=0, column=1, padx=10, pady=10, sticky="we")

                def prim_ver():
                    self.sicil = self.mesaiTablo.item(self.mesaiTablo.selection())["values"][2]
                    if Fonk().mesai_sil(tip="prim", id=self.mesaiTablo.item(self.mesaiTablo.selection())["values"][0], sicilNo=self.sicil, prim=str(self.primSpin.get())):
                        self.mesaiAyarlaTop.destroy()
                        messagebox.showinfo("Prim Eklendi!", "Prim başarıyla eklendi.", parent=self.mesaiAyarlaTop)
                        mesai_tablo_güncelle()
                    else:
                        messagebox.showerror("Mesai Silinemedi!", "Mesai kaydı silinemedi.", parent=self.mesaiAyarlaTop)

                self.primVerButton = Button(self.primFrame, text="Prim Ver", command=prim_ver)
                self.primVerButton.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        self.mesaiTablo = Treeview(self.mesaiFrame, columns=("id", "İsim", "Sicil Numarası", "Mesai Saati"), show="headings", selectmode="browse")
        self.mesaiTablo.heading("#1", text="")
        self.mesaiTablo.heading("#2", text="İsim", command=lambda: tabloSırala(self.mesaiTablo, "İsim", False))
        self.mesaiTablo.heading("#3", text="Sicil Numarası", command=lambda: tabloSırala(self.mesaiTablo, "Sicil Numarası", False))
        self.mesaiTablo.heading("#4", text="Mesai Saati", command=lambda: tabloSırala(self.mesaiTablo, "Mesai Saati", False))
        self.mesaiTablo.column("#1", width=0)
        self.mesaiTablo.column("#2", width=220, stretch=False)
        self.mesaiTablo.column("#3", width=120, stretch=False)
        self.mesaiTablo.column("#4", width=120, stretch=False)
        self.mesaiTablo["displaycolumns"]=("İsim", "Sicil Numarası", "Mesai Saati")
        self.mesaiTablo.bind("<Double-1>", double_click)
        self.mesaiTablo.grid(padx=20, pady=20)

        def mesai_tablo_güncelle():
            self.mesaiTablo.delete(*self.mesaiTablo.get_children())
            for self.i in Fonk().kullanici_al(tablo="mesailer"):
                self.mesaiTablo.insert("", "end", values=(self.i[0], (self.i[2], self.i[3]), self.i[1], self.i[4]))

        mesai_tablo_güncelle()

        self.mesaiTop.deiconify()

    def ozel_gunler_ayarlar(self):
        self.gunlerTop = Toplevel(self.root)
        self.gunlerTop.withdraw()
        self.gunlerTop.resizable(False, False)
        self.gunlerTop.iconbitmap("icon.ico")
        self.gunlerTop.grab_set()
        self.gunlerTop.title("Özel Günler")

        self.gunFrame = Frame(self.gunlerTop)
        self.yeniGunFrame = Frame(self.gunFrame)
        self.gunlerFrame = Frame(self.gunFrame)
        self.gunFrame.grid()
        self.yeniGunFrame.grid(row=0, column=0)
        self.gunlerFrame.grid(row=1, column=0)

        self.isimLabel = Label(self.yeniGunFrame, text="İsim:").grid(row=0, column=0, padx=10, pady=10)
        self.tarihLabel = Label(self.yeniGunFrame, text="Tarih:").grid(row=1, column=0, padx=10, pady=10)

        self.isimEntry = Entry(self.yeniGunFrame)
        self.tarihEntry = DateEntry(self.yeniGunFrame, locale="tr_TR")
        self.isimEntry.grid(row=0, column=1, padx=10, pady=10)
        self.tarihEntry.grid(row=1, column=1, padx=10, pady=10)

        def gunEkle():
            if all ([self.isimEntry.get(), self.tarihEntry.get_date()]):
                if Fonk().ozel_gun_ekle(self.isimEntry.get(), self.tarihEntry.get_date()):
                    messagebox.showinfo("Özel Gün Eklendi!", "Özel gün başarıyla eklendi.", parent=self.gunlerTop)
                    gunlerTabloGüncelle()
                else:
                    messagebox.showerror("Özel Gün Eklenemedi!", "Özel gün eklenemedi.", parent=self.gunlerTop)

        self.ekleButton = Button(self.yeniGunFrame, text="Ekle", command=gunEkle)
        self.ekleButton.grid(row=1, column=3, padx=10, pady=10)

        def gunlerTabloGüncelle():
            self.gunlerTablo.delete(*self.gunlerTablo.get_children())
            for self.i in Fonk().kullanici_al(tablo="ozelGunler"):
                self.gunlerTablo.insert("", "end", values=(self.i[0], self.i[1], self.i[2]))

        def double_click(event):
            if self.gunlerTablo.item(self.gunlerTablo.selection())["values"]:
                if messagebox.askyesno("Özel Gün Sil!", "Özel günü silmek istediğine emin misin?", parent=self.gunlerTop):
                    if Fonk().ozel_gun_sil(id=self.gunlerTablo.item(self.gunlerTablo.selection())["values"][0]):
                        messagebox.showinfo("Özel Gün Silindi!", "Özel gün başarıyla silindi.", parent=self.gunlerTop)
                        gunlerTabloGüncelle()
                    else:
                        messagebox.showerror("Özel Gün Silinemedi!", "Özel gün silinemedi.", parent=self.gunlerTop)

        self.gunlerTablo = Treeview(self.gunlerFrame, columns=("id", "İsim", "Tarih"), show="headings", selectmode="browse")
        self.gunlerTablo.heading("#1", text="")
        self.gunlerTablo.heading("#2", text="İsim")
        self.gunlerTablo.heading("#3", text="Tarih")
        self.gunlerTablo.column("#1", width=0)
        self.gunlerTablo.column("#2", width=150)
        self.gunlerTablo.column("#3", width=150)
        self.gunlerTablo["displaycolumns"]=("İsim", "Tarih")
        self.gunlerTablo.grid(row=0, column=0, padx=10, pady=10)
        self.gunlerTablo.bind("<Double-1>", double_click)
        gunlerTabloGüncelle()

        self.gunlerTop.deiconify()

class Personel(TKMT.ThemedTKinterFrame):
    def __init__(self, root, kullanici):
        self.root = root
        self.kullanici = kullanici
        self.root.title(f"Personel Takip Sitemi | {self.kullanici[1]} - {self.kullanici[14]}")

        self.tabloFrame = Frame(self.root)
        self.altFrame = Frame(self.root)
        self.vardiyaFrame = LabelFrame(self.tabloFrame, text="Vardiyalar")
        self.izinFrame = LabelFrame(self.tabloFrame, text="İzinler")

        self.tabloFrame.grid(row=0, column=0)
        self.altFrame.grid(row=1, column=0)
        self.vardiyaFrame.grid(row=0, column=0, padx=10, pady=10)
        self.izinFrame.grid(row=0, column=1, padx=10, pady=10)

        def vardiyaTabloGüncelle():
            self.vardiyalarTablo.delete(*self.vardiyalarTablo.get_children())
            for self.i in Fonk(sicilNo=self.kullanici[11]).kullanici_al(tablo="vardiyalar"):
                self.vardiyalarTablo.insert("", "end", values=(self.i[4], self.i[5], self.i[6]))

        self.vardiyalarTablo = Treeview(self.vardiyaFrame, columns=("Vardiya Tarihi", "Vardiya Yeri", "Vardiya Saati"), show="headings", selectmode="browse")
        self.vardiyalarTablo.heading("#1", text="Vardiya Tarihi")
        self.vardiyalarTablo.heading("#2", text="Vardiya Yeri")
        self.vardiyalarTablo.heading("#3", text="Vardiya Saati")
        self.vardiyalarTablo.column("#1", width=150)
        self.vardiyalarTablo.column("#2", width=150)
        self.vardiyalarTablo.column("#3", width=150)
        self.vardiyalarTablo.grid(row=0, column=0, padx=10, pady=10)
        vardiyaTabloGüncelle()

        def izinTabloGüncelle():
            self.izinlerTablo.delete(*self.izinlerTablo.get_children())
            for self.i in Fonk(sicilNo=self.kullanici[11]).kullanici_al(tablo="izinler"):
                self.izinlerTablo.insert("", "end", values=(self.i[4], self.i[5]))

        self.izinlerTablo = Treeview(self.izinFrame, columns=("Vardiya Tarihi", "Bitiş Tarihi"), show="headings", selectmode="browse")
        self.izinlerTablo.heading("#1", text="Başlangıç Tarihi")
        self.izinlerTablo.heading("#2", text="Bitiş Tarihi")
        self.izinlerTablo.column("#1", width=150)
        self.izinlerTablo.column("#2", width=150)
        self.izinlerTablo.grid(row=0, column=0, padx=10, pady=10)
        izinTabloGüncelle()

        def liste_al(tip2=("vardiya", "izin")):
            self.path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF dosyası", "*.pdf")], initialfile=f'{datetime.now().strftime("%Y-%m-%d")}_{tip2}.pdf')
            if self.path:
                self.data = [['Vardiya Tarihi', 'Vardiya Yeri', 'Vardiya Saati']]
                self.baslik = f"{self.kullanici[3]} {self.kullanici[4]} Vardiya Listesi"
                if tip2 == "izin":
                    self.data = [['Başlangıç Tarihi', 'Bitiş Tarihi']]
                    self.baslik = f"{self.kullanici[3]} {self.kullanici[4]} İzin Listesi"
                self.islem = Fonk().pdf_olustur(tip="tum_tarih", tip2=tip2, sicil=self.kullanici[11], baslik=self.baslik, bugun=datetime.now().strftime("%Y-%m-%d"), path=self.path, data=self.data)
                if self.islem:
                    if self.islem == "Veri Yok":
                        messagebox.showinfo("Liste Oluşturulamadı!", "PDF dosyası oluşturmak için yeterli veri yok.", parent=self.root)
                    else:
                        if messagebox.askquestion("Liste Oluşturuldu!", "PDF dosyası başarıyla oluşturuldu. Dosya açılsın mı?", parent=self.root):
                            system(f"start {self.path}")

        self.isimLabel = Label(self.altFrame, text=(self.kullanici[3], self.kullanici[4]))
        self.sicilLabel = Label(self.altFrame, text=self.kullanici[11])
        self.primLabel = Label(self.altFrame, text=f"Prim: {self.kullanici[13]}")
        self.vardiyaListeButton = Button(self.altFrame, text="Vardiya Listesi Al", command=lambda: liste_al("vardiya"))
        self.izinListeButton = Button(self.altFrame, text="İzin Listesi Al", command=lambda: liste_al("izin"))
        self.vardiyaListeButton.grid(row=0, column=0, padx=10, pady=10)
        self.isimLabel.grid(row=0, column=1, padx=10, pady=10)
        self.sicilLabel.grid(row=0, column=2, padx=10, pady=10)
        self.primLabel.grid(row=0, column=3, padx=10, pady=10)
        self.izinListeButton.grid(row=0, column=4, padx=10, pady=10)