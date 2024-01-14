from vt import vt
from datetime import timedelta
import calendar, numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class Fonk:
    # Sınıfın başlatıcı metodudur. Kullanıcı nesnesi oluşturulurken, 
    # kullaniciAdi, sifre, ve sicilNo değerleri ile başlatılır.
    def __init__(self, kullaniciAdi=None, sifre=None, sicilNo=None):
        self.kullaniciAdi = kullaniciAdi
        self.sifre = sifre
        self.sicilNo = sicilNo

# Fonksiyonu: Kullanıcının giriş yapma işlemini gerçekleştirir.
    def giris_yap(self):
        try:
            self.dogru_sifre = vt().fetch(f"""SELECT sifre FROM kullanicilar WHERE kullanici_adi = '{self.kullaniciAdi}'""")[0][0]
            if self.dogru_sifre:
                return self.dogru_sifre == self.sifre
        except IndexError: return False


#kullanici_al: Belirli bir kullanıcının bilgilerini çekme işlemi yapar.
    def kullanici_al(self, tablo="kullanicilar"):
        if self.kullaniciAdi:
            return vt().fetch(f"""SELECT * FROM {tablo} WHERE kullanici_adi = '{self.kullaniciAdi}'""")[0]
        elif self.sicilNo:
            return vt().fetch(f"""SELECT * FROM {tablo} WHERE sicil_no = '{self.sicilNo}'""")
        else:
            return vt().fetch(f"""SELECT * FROM {tablo}""")

    # Yeni bir kullanıcı ekler.
    def yeni_kullanici(self, kullaniciAdi, sifre, isim, soyisim, tc_no, dogum, cinsiyet, adres, telefon, mail, sicil_no, unvan, rol, tatil1, tatil2, ise_baslama):
        if vt().fetch(f"""SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = '{kullaniciAdi}'""")[0][0] == 0 and vt().fetch(f"""SELECT COUNT(*) FROM kullanicilar WHERE sicil_no = '{sicil_no}'""")[0][0] == 0:
            return vt().execute(f"""
                                INSERT INTO kullanicilar 
                                (kullanici_adi, sifre, isim, soyisim, tc_no, dogum_gunu, cinsiyet, adres, telefon, mail, sicil_no, unvan, rol, tatil1, tatil2, ise_baslama) VALUES
                                ("{kullaniciAdi}", "{sifre}", "{isim}", "{soyisim}", "{tc_no}", "{dogum}", "{cinsiyet}", "{adres}", "{telefon}", "{mail}", "{sicil_no}", "{unvan}", "{rol}", "{tatil1}", "{tatil2}", "{ise_baslama}")
                                """)
#kullanici_sil: Belirli bir kullanıcıyı ve bu kullanıcıya ait verileri siler.
    def kullanici_sil(self):
        for table in ("kullanicilar", "izinler", "vardiyalar", "mesailer"):
            vt().execute(f"""DELETE FROM {table} WHERE sicil_no = '{self.sicilNo}'""")
        return True


#Bu fonksiyon, bir kullanıcının bilgilerini güncellemek için kullanılır. 
    def kullanici_guncelle(self, eskiKullaniciAdi, eskiSicilNo, kullaniciAdi, sifre, isim, soyisim, tc_no, dogum, cinsiyet, adres, telefon, mail, sicil_no, unvan, rol, tatil1, tatil2, ise_baslama):
        kullaniciId = vt().fetch(f"""SELECT id FROM kullanicilar WHERE kullanici_adi = '{eskiKullaniciAdi}'""")[0][0]
        vt().execute(f"""
                            UPDATE kullanicilar SET
                            kullanici_adi = "{kullaniciAdi}",
                            sifre = "{sifre}",
                            isim = "{isim}",
                            soyisim = "{soyisim}",
                            tc_no = "{tc_no}",
                            dogum_gunu = "{dogum}",
                            cinsiyet = "{cinsiyet}",
                            adres = "{adres}",
                            telefon = "{telefon}",
                            mail = "{mail}",
                            sicil_no = "{sicil_no}",
                            unvan = "{unvan}",
                            rol = "{rol}",
                            tatil1 = "{tatil1}",
                            tatil2 = "{tatil2}",
                            ise_baslama = "{ise_baslama}"
                            WHERE id = "{kullaniciId}"
                            """)
        
        for table in ("izinler", "vardiyalar", "mesailer"):
            vt().execute(f"""
                            UPDATE {table} SET
                            isim = "{isim}",
                            soyisim = "{soyisim}",
                            sicil_no = "{sicil_no}"
                            WHERE sicil_no = "{eskiSicilNo}"
                            """)
        return True




    def izin_ekle(self, isim, soyisim, sicilNo, baslama, bitis): # Yeni bir izin kaydı ekler.
        return vt().execute(f"""
                    INSERT INTO izinler 
                    (isim, soyisim, sicil_no, baslama, bitis) VALUES
                    ("{isim}", "{soyisim}", "{sicilNo}", "{baslama}", "{bitis}")
                    """)

    def izin_sil(self, id): #Belirli bir izin kaydını veritabanından siler.
        return vt().execute(f"""DELETE FROM izinler WHERE id = '{id}' LIMIT 1""")

    def vardiya_ekle(self, isim, soyisim, sicilNo, tarih, yer, saat): # Yeni bir vardiya kaydı ekler.
        return vt().execute(f"""
                    INSERT INTO vardiyalar 
                    (isim, soyisim, sicil_no, vardiya_tarihi, vardiya_yeri, vardiya_saati) VALUES
                    ("{isim}", "{soyisim}", "{sicilNo}", "{tarih}", "{yer}", "{saat}")
                    """)

    def vardiya_sil(self, id):
        return vt().execute(f"""DELETE FROM vardiyalar WHERE id = '{id}'""") # Belirli bir vardiya kaydını veritabanından siler.



    def toplu_sil(self, tip=("hepsi", "herkes", "tum_tarih", "kisi"), isim=None, soyisim=None, sicil=None, tarih=None, tarih2=None, yer=None, saat=None):
           # Eğer tip "hepsi" ise, tüm vardiyaları sil
        if tip == "hepsi":
            return vt().execute(f"""DELETE FROM vardiyalar""")
                # Eğer tip "herkes" ise, belirli bir tarih aralığındaki tüm vardiyaları sil
        elif tip == "herkes":
            simdi = tarih
            while simdi <= tarih2:
                vt().execute(f"""DELETE FROM vardiyalar WHERE vardiya_tarihi = '{simdi}'""")
                simdi += timedelta(days=1)
                        # İşlem başarıyla tamamlandı, True değeri döndür
            return True
                # Eğer tip "tum_tarih" ise, belirli bir kişinin tüm vardiyalarını sil
        elif tip == "tum_tarih":
            return vt().execute(f"""DELETE FROM vardiyalar WHERE sicil_no = '{sicil}'""")
        else:
                    # Belirli bir kişinin belirli bir tarih aralığındaki vardiyalarını sil
            simdi = tarih
            while simdi <= tarih2:
                vt().execute(f"""DELETE FROM vardiyalar WHERE sicil_no = '{sicil}' and vardiya_tarihi = '{simdi}'""")
                simdi += timedelta(days=1)
                        # İşlem başarıyla tamamlandı, True değeri döndür
            return True


    def mesai_sil(self, tip=("izin", "prim"), id=None, sicilNo=None, prim=None):
            # Eğer tip "prim" ise
        if tip == "prim":
                    # Kullanıcının mevcut primini ve verilen primi topla
            self.prim = int(vt().fetch(f"""SELECT prim FROM kullanicilar WHERE sicil_no = '{sicilNo}'""")[0][0]) + int(prim)
                    # Toplam primi kullanıcının prim alanına kaydet
            vt().execute(f"""UPDATE kullanicilar SET
                                prim = '{str(self.prim)}'
                                WHERE sicil_no = '{sicilNo}'""")
    # Belirtilen ID'ye sahip mesai kaydını sil
        vt().execute(f"""DELETE FROM mesailer WHERE id = '{id}'""")
            # Fonksiyon başarıyla tamamlandı, True değeri döndür
        return True

    def ozel_gun_ekle(self, isim, tarih):
            # Veritabanına özel gün eklemek için SQL sorgusu
        return vt().execute(f"""
                    INSERT INTO ozelGunler 
                    (isim, tarih) VALUES
                    ("{isim}", "{tarih}")
                    """)

    def ozel_gun_sil(self, id):
            # Veritabanından belirli bir özel günü silmek için SQL sorgusu
        return vt().execute(f"""DELETE FROM ozelGunler WHERE id = '{id}'""")




    def pdf_olustur(self, tip=("hepsi", "herkes", "tum_tarih", "kisi"),tip2=("izin", "vardiya", None),  sicil=None, tarih=None, tarih2=None, baslik=None, bugun=None, path=None, data = [['Vardiya Tarihi', 'Vardiya Yeri', 'Vardiya Saati']]):
        
        data2 = [] # boş liste oluştur
        if tip == "hepsi":
            data2 = vt().fetch("""SELECT * FROM vardiyalar""")
        elif tip == "herkes":
            # tip hepsi ise tüm vardiya getir
            simdi = tarih
            while simdi <= tarih2:
                data2.append(vt().fetch(f"""SELECT * FROM vardiyalar WHERE vardiya_tarihi = '{simdi}'"""))
                simdi += timedelta(days=1)
        elif tip == "tum_tarih":
            if not tip2:
                        # tip "tum_tarih" ve tip2 belirtilmemişse, belirli bir kişinin tüm vardiyalarını getir
                data2 = vt().fetch(f"""SELECT * FROM vardiyalar WHERE sicil_no = '{sicil}'""")
            else:
                        # tip "tum_tarih" ve tip2 belirtilmişse, izin veya vardiya tablosundan ilgili verileri getir
                if tip2 == "izin":
                    data2 = vt().fetch(f"""SELECT * FROM izinler WHERE sicil_no = '{sicil}'""")
                else:
                    data2 = vt().fetch(f"""SELECT * FROM vardiyalar WHERE sicil_no = '{sicil}'""")
        else:
    # tip "hepsi", "herkes" veya "tum_tarih" değilse, belirli bir kişinin belirli bir tarih aralığındaki vardiyalarını getir
            simdi = tarih
            while simdi <= tarih2:
                        # Belirli bir tarihte vardiya varsa, o tarih için ilgili vardiyaları getir
                if vt().fetch(f"""SELECT COUNT(*) FROM vardiyalar WHERE sicil_no = '{sicil}' and vardiya_tarihi = '{simdi}'""")[0]:
                    for i in range(vt().fetch(f"""SELECT COUNT(*) FROM vardiyalar WHERE sicil_no = '{sicil}' and vardiya_tarihi = '{simdi}'""")[0][0]):
                        data2.append(vt().fetch(f"""SELECT * FROM vardiyalar WHERE sicil_no = '{sicil}' and vardiya_tarihi = '{simdi}'"""))
                    simdi += timedelta(days=1)

        if not data2:
            return "Veri Yok"

# PDF oluşturmak için kullanılan değişkenler
        fig_background_color = 'skyblue'
        fig_border = 'steelblue'
        pdf_pages = []
        # Verileri 12'şerli gruplara böler ve her bir grup için bir PDF sayfası oluşturur
        for i in range(0, len(data2), 12):
            new_data = []
            yeni_liste = data2[i:i+12]
                # Verileri uygun formata dönüştürme
            for j in yeni_liste:
                if tip == "herkes" or tip == "kisi":
                    if len(j) > 1:
                        for k in range(len(j)):
                            new_data.append([f'{j[k][1]} {j[k][2]}', j[k][4], j[k][5], j[k][6]])
                    else:
                        new_data.append([f'{j[0][1]} {j[0][2]}', j[0][4], j[0][5], j[0][6]])
                else:
                    if not tip2 == "izin":
                        new_data.append([f'{j[1]} {j[2]}', j[4], j[5], j[6]])
                    else:
                        new_data.append([f'{j[1]} {j[2]}', j[4], j[5]])
    # Tablo için gerekli bilgileri ayarla

            column_headers = data[0]
            row_headers = [x[0] for x in new_data]
            cell_text = [[str(x) for x in row[1:]] for row in new_data]
    # Renkler

            rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
            ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    # Matplotlib figürünü oluştur

            plt.figure(linewidth=2,
                        edgecolor=fig_border,
                        facecolor=fig_background_color,
                        tight_layout={'pad': 1},
                        )
    # Tabloyu çiz

            the_table = plt.table(cellText=cell_text,
                                rowLabels=row_headers,
                                rowColours=rcolors,
                                rowLoc='right',
                                colColours=ccolors,
                                colLabels=column_headers,
                                loc='center')

            the_table.scale(1, 1.5)

            ax = plt.gca()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)

            plt.box(on=None)

            plt.suptitle(baslik)

            plt.figtext(0.95, 0.05, bugun, horizontalalignment='right', size=6, weight='light')
    # PDF sayfasına ekle
            pdf_pages.append(plt.gcf())
            plt.close()

# Belirtilen 'path' (dosya yolu) ile PdfPages nesnesi oluşturuluyor
        with PdfPages(path) as pdf:
            for page in pdf_pages:
                pdf.savefig(page,
                            edgecolor=page.get_edgecolor(),
                            facecolor=page.get_facecolor(),
                            dpi=150
                            )
        return True


class Algoritma:
    def __init__(self, baslangic, bitis):

        #başlangıç ve birişi al ve 2 gün arasındaki farkı hesapla
        self.baslangic = baslangic
        self.bitis = bitis
        self.fark = (self.bitis - self.baslangic).days + 1
        self.otoEkle()

    def otoEkle(self):
        #gün farkı kadar döndür
        if self.fark > 0:
            # çalışma saatleri
            self.saat1 = ["00:00-08:00", "08:00-16:00", "16:00-24:00"]
            self.saat2 = ["08:00-16:00", "09:00-17:00"]

            # tüm sicilleri buraya al
            siciller = []
            for sicil in vt().fetch(f"""SELECT sicil_no FROM kullanicilar"""):
                siciller.append(sicil[0])
            
            
            # Bu kod, bir döngü içinde self.gun değişkenini self.fark değerine kadar artırarak dolaşan bir yapıdır.
            # Bu döngü, muhtemelen bir tarih aralığında günleri temsil etmek için kullanılıyor.
            for self.gun in range(self.fark):
                self.simdi = self.baslangic + timedelta(days=self.gun)

                #adil dağitmak amaclı hangi vardiye kaç kişi atandığını not alıyoruz
                self.vardiya1 = 0
                self.vardiya2 = 0
                self.vardiya3 = 0

                self.vardiya4 = 0
                self.vardiya5 = 0


                self.kampusGiris = 0
                self.kampusIci = 0
                # mevcut gün özel günse
                if self.ozelGunKontrol(self.simdi):
                    if siciller:
                        for sicil in siciller:

                            # vardiyada hiç kişi yoksa ekle varsa eklemeyeceğiz.
                            if self.vardiyaKontrol(sicil, self.simdi):
                                if self.vardiya1 == 0:
                                    self.vardiya1 += 1
                                    self.mesaiEkle(sicil, "8")
                                    self.vardiyaEkle(sicil, self.simdi, "Kampus Girisi", "00:00-08:00")
                                elif self.vardiya2 == 0:
                                    self.vardiya2 += 1
                                    self.mesaiEkle(sicil, "8")
                                    self.vardiyaEkle(sicil, self.simdi, "Kampus Girisi", "08:00-16:00")
                                elif self.vardiya3 == 0:
                                    self.vardiya3 += 1
                                    self.mesaiEkle(sicil, "8")
                                    self.vardiyaEkle(sicil, self.simdi, "Kampus Girisi", "16:00-24:00")

                else:
                    if siciller:
                        for sicil in siciller:
                            if self.vardiyaKontrol(sicil, self.simdi):

                                # burada kampüsGirisi mi az kişi var yoksa 
                                    # kontrolu var ve tamamlayarak ilerliyoruz.
                                if self.kampusGiris < self.kampusIci:

                                    # en az vardiya ataması olanı buluyoruz
                                    self.enKucukVardiya = min(self.vardiya1, self.vardiya2, self.vardiya3) 

                                    # burada vardiyaları atıyoruz. saati buluyoruz en min olanı
                                    if self.enKucukVardiya == self.vardiya1:
                                        self.saat = self.saat1[0]
                                        self.vardiya1 += 1
                                    elif self.enKucukVardiya == self.vardiya2:
                                        self.saat = self.saat1[1]
                                        self.vardiya2 += 1
                                    elif self.enKucukVardiya == self.vardiya3:
                                        self.saat = self.saat1[2]
                                        self.vardiya3 += 1
                                        self.kampusGiris += 1
                                    
                                    self.vardiyaEkle(sicil, self.simdi, "Kampus Girisi", self.saat)
                                else:
                                    # en min saati bulup ekleme yapıyoruz.
                                    if self.vardiya4 < self.vardiya5:
                                        self.saat = self.saat2[0]
                                        self.vardiya4 += 1
                                    else:
                                        self.saat = self.saat2[1]
                                        self.vardiya5 += 1
                                        self.kampusIci += 1
                                    self.vardiyaEkle(sicil, self.simdi, "Kampus Ici", self.saat)

        return False

    def mesaiEkle(self, sicil, saat): # kullanıcıya mesai ekle.
        self.kullanici = vt().fetch(f"""SELECT * FROM kullanicilar WHERE sicil_no = '{sicil}'""")[0]

        vt().execute(f"""
                    INSERT INTO mesailer 
                    (sicil_no, isim, soyisim, mesai) VALUES
                    ("{sicil}", "{self.kullanici[3]}", "{self.kullanici[4]}", "{saat}")
                    """)

    def vardiyaEkle(self, sicil, tarih, yer, saat): # kullanıcıya vardiya ekle
        self.kullanici = vt().fetch(f"""SELECT * FROM kullanicilar WHERE sicil_no = '{sicil}'""")[0]
        vt().execute(f"""
                    INSERT INTO vardiyalar 
                    (isim, soyisim, sicil_no, vardiya_tarihi, vardiya_yeri, vardiya_saati) VALUES
                    ("{self.kullanici[3]}", "{self.kullanici[4]}", "{sicil}", "{tarih}", "{yer}", "{saat}")
                    """)

    def izinKontrol(self, sicil_no, tarih): # İzinli mi kontrolü
        self.count = vt().fetch(f"""SELECT COUNT(*) FROM izinler WHERE sicil_no = '{sicil_no}' AND baslama = '{tarih}'""")[0][0]
        return int(self.count) > 0

    def isKontrol(self, sicil_no, tarih): # o gün çalışıyor mu
        self.count = vt().fetch(f"""SELECT COUNT(*) FROM vardiyalar WHERE sicil_no = '{sicil_no}' AND vardiya_tarihi = '{tarih}'""")[0][0]
        return int(self.count) > 0

    def tatilKontrol(self, sicil_no, tarih): # Haftalık izin günü kontrolü
        english_days = list(calendar.day_name)
        turkish_days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        bugunun_gunu = english_days[tarih.weekday()]
        turkce_gun = turkish_days[english_days.index(bugunun_gunu)]

        self.kontrol1 = vt().fetch(f"""SELECT tatil1 FROM kullanicilar WHERE sicil_no = '{sicil_no}'""")[0]
        self.kontrol2 = vt().fetch(f"""SELECT tatil2 FROM kullanicilar WHERE sicil_no = '{sicil_no}'""")[0]

        return self.kontrol1[0][0] == turkce_gun or self.kontrol2[0][0] == turkce_gun

    def ozelGunKontrol(self, tarih): # Özel gün kontrolü
        self.count = vt().fetch(f"""SELECT COUNT(*) FROM ozelGunler WHERE tarih = '{tarih}'""")[0][0]
        return int(self.count )> 0

    def vardiyaKontrol(self, sicil_no, tarih):        # Çalışma ve tatil kontrolü yap
        if not self.izinKontrol(sicil_no, tarih):
            if not self.isKontrol(sicil_no, tarih) and not self.tatilKontrol(sicil_no, tarih):
                return True
        return False
