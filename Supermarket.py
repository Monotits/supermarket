#Eğitim Amaçlı Hazırlanmıştır.

import sqlite3
import time

class Ürün():

    def __init__(self,isim, gfiyat, sfiyat, stok, üretici, tedarikçi, kategori,kalan):
        self.isim=isim    #ürün ismi
        self.gfiyat=gfiyat  #ürün geliş fiyatı
        self.sfiyat=sfiyat  #ürün satış fiyatı
        self.stok=stok    #ürünün stok adedi (int)
        self.üretici=üretici     #ürünün üreticisi
        self.tedarikçi=tedarikçi   #ürünün tedarikçisi
        self.kategori=kategori   #ürün kategorisi
        self.kalan=kalan   #ürünün raf alanı

        #Göz Göz Göztepe!

    def __str__(self):
         return "Ürün İsmi: {}\nAlım Fiyatı: {}\nSatış Fiyatı: {}\nStok Adedi: {}\nÜretici: {}\nTedarikçi: " \
                "{}\nKategori: {}\nÜrünün Raf Alanı: " \
                "{}\n".format(self.isim,self.gfiyat,self.sfiyat,self.stok,self.üretici,self.tedarikçi,self.kategori,self.kalan)

class Market():
    def __init__(self):
        self.baglanti_olustur()
        self.alan = 1000         #Markette ki toplam raf alanını 1000 birim olarak belirledim.

    def baglanti_olustur(self):
        self.baglanti=sqlite3.connect("supermarket.db")
        self.cursor=self.baglanti.cursor()

        sorgu= "CREATE Table if not exists market (isim TEXT, gelis_fiyat INT, satis_fiyat INT, stok INT, uretici TEXT, " \
               "tedarikçi TEXT, kategori INT,raf_alani INT)"

        self.cursor.execute(sorgu)
        self.baglanti.commit()

    def baglantiyi_kes(self):
        self.baglanti.close()

    def marketi_goster(self):       #Markette yer alan tüm ürünlerin detaylı gösterimi
        sorgu= "SELECT * from market"
        self.cursor.execute(sorgu)
        market_all = self.cursor.fetchall()

        for i in market_all:
            market_ürünleri=Ürün(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])    #Ürün sınıfı - srt fonksiyonu
            print(market_ürünleri)

    def ürün_sorgula(self,isim):
        while True:
            try:
                sorgu = "SELECT * from market where isim=?"
                self.cursor.execute(sorgu,(isim,))
                ürünler = self.cursor.fetchall()
                ürünler=Ürün(ürünler[0][0],ürünler[0][1],ürünler[0][2],ürünler[0][3],ürünler[0][4],ürünler[0][5],ürünler[0][6],ürünler[0][7])
                print(ürünler)
                break
            except:
                print("Bu isimde bir ürün markette bulunmuyor. Lütfen tekrar giriş yapın.\n")
                break
    def ürün_ekle(self,ürün):
        sorgu = "insert into market values (?,?,?,?,?,?,?,?)"
        a= float(ürün.kalan)    #ürünün rafta kapladığı alan ondalıklı olabilmesi ihtimali nedeniyle float dönüşüm yapıldı.
        self.cursor.execute(sorgu,(ürün.isim,ürün.gfiyat,ürün.sfiyat,ürün.stok,ürün.üretici,ürün.tedarikçi,ürün.kategori,a))
        self.baglanti.commit()

        self.rafalanı()


    def ürün_sil(self,isim):
        while True:
            try:
                sorgu = "SELECT * from market where isim=?"
                self.cursor.execute(sorgu,(isim,))
                ürünler = self.cursor.fetchall()
                ürünler=Ürün(ürünler[0][0],ürünler[0][1],ürünler[0][2],ürünler[0][3],ürünler[0][4],ürünler[0][5],ürünler[0][6],ürünler[0][7])
                time.sleep(1)
                print("Silinen ürünün bilgileri:\n", ürünler)

                sorgu="DELETE FROM market WHERE isim=?"
                self.cursor.execute(sorgu,(isim,))
                self.baglanti.commit()
                break
            except:
                print("Bu isimde bir ürün markette bulunmuyor. Lütfen tekrar giriş yapın.\n")
                break

    def ürün_satış(self,isim):
        sorgu1="SELECT * from market where isim=?"
        self.cursor.execute(sorgu1,(isim,))
        ürüns=self.cursor.fetchall()

        stok=ürüns[0][3]
        çık=stok-1   #stok eksiltme

        sorgu2="UPDATE market set stok = ? Where isim = ?"
        self.cursor.execute(sorgu2,(çık, isim))
        self.baglanti.commit()
        print("Satış tamamlandı. Kalan stok: ",çık)

    def ürün_iade(self,iade):
        sorgu="SELECT * from market where isim=?"
        self.cursor.execute(sorgu,(iade,))
        ürüns = self.cursor.fetchall()

        iade_stok=int(ürüns[0][3])
        iade_stok += 1   #stok arttırma

        sorgu1= "UPDATE market set stok = ? Where isim = ?"
        self.cursor.execute(sorgu1,(iade_stok,iade))
        self.baglanti.commit()
        print("İade işlemi tamamlandı. Mevcut ürün stoğu:",iade_stok)

    def sfiyat_yükselt(self,isim):
        sorgu = "SELECT * from market Where isim=?"
        self.cursor.execute(sorgu,(isim,))
        ürüns = self.cursor.fetchall()

        sfiyat = ürüns[0][2]
        print("Ürünün mevcut satış fiyatı:",sfiyat)
        miktar=int(input("Artış Miktarını Girin: "))
        a= int(sfiyat+miktar)     #mevcut fiyat üzerine artış

        sorgu2 = "UPDATE market set satis_fiyat = ? Where isim = ?"

        self.cursor.execute(sorgu2, (a, isim))
        self.baglanti.commit()
        print("Satış fiyatı güncellendi.")
        self.ürün_sorgula(isim)

    def toplam_stok_değeri(self):    #stokların alış ve satış fiyatlarına göre değeri
        sorgu = "SELECT gelis_fiyat, stok from market"
        self.cursor.execute(sorgu)
        toplam = self.cursor.fetchall()
        gtopla = 0
        for i in toplam:
            gtopla += (int(i[0]) * int(i[1]))
        print("Alış Fiyatına Göre Stok Değeri:", gtopla)

        sorgu = "SELECT satis_fiyat, stok from market"
        self.cursor.execute(sorgu)
        toplam = self.cursor.fetchall()
        stopla = 0
        for i in toplam:
            stopla += (int(i[0]) * int(i[1]))
        print("Satış Fiyatına Göre Stok Değeri:", stopla)

        print("Beklenen kar:",(stopla-gtopla))

    def stok_sorgu(self):
        sorgu = "Select isim, stok From market"
        self.cursor.execute(sorgu)
        stok=self.cursor.fetchall()
        print("Market Stok Bilgileri: \n")
        for i in stok:
            print("Ürün İsmi:",i[0],"Stok Miktarı:",i[1])

    def rafalanı(self):   #markete ürün eklerken market içinde yeterli raf alanı olup olmadığını kontrol eden fonksiyon
        sorgu= "Select raf_alani, stok From market"
        self.cursor.execute(sorgu)
        toplam=self.cursor.fetchall()
        toplam_alan=0
        for i in toplam:
            toplam_alan += (float(i[0]) * int(i[1]))
        if toplam_alan > self.alan:
            print("Toplam market raf alanı aşıldı. Lütfen Stokları gözden geçirin!")

    def rafalanı_sorgu(self):    #ürünlerin markette ne kadarlık raf alanı kapladığını sorgulayan fonksiyon
        sorgu="Select raf_alani, stok From market"
        self.cursor.execute(sorgu)
        toplam=self.cursor.fetchall()
        toplam_alan= 0
        for i in toplam:
            toplam_alan += (float(i[0]) * int(i[1]))
        print("Market toplam raf alanı 1000 birim olup mevcut kullanılan raf alanı", toplam_alan, "birimdir.\n")


#******************************************

print("""
Down Cafe Market Yönetim Sistemine Hoş Geldiniz!

İşlem Seçenekleri:
    1- Full Market Sorgusu
    2- Ürün Sorgu
    3- Ürün Ekle
    4- Ürün Sil
    5- Ürün Satış
    6- Ürün İade
    7- Ürün Satış Fiyatı Güncelle
    8- Toplam Stok Değeri
    9- Stok Sorgusu 
    10- Raf Alanı Sorgusu
    
    11- Program Çıkışı
""")

süpermarket = Market()

while True:
    seçim = (input("Yapmak İstediğiniz İşlemi Seçin: "))

    try:

        if int(seçim) == 1:
            süpermarket.marketi_goster()

        elif int(seçim) == 2:
            seç = input("Sorgulamak istediğiniz ürün ismini girin: ")
            süpermarket.ürün_sorgula(seç)

        elif int(seçim) == 3:
            seç1 = input("Eklemek istediğiniz ürünün ismi: ")
            seç2 = float(input("Ürün - Alım Fiyatı: "))
            seç3 = float(input("Ürün - Satış Fiyatı: "))
            seç4 = int(input("Stok - Alım Miktarı: "))
            seç5 = input("Üretici Firma: ")
            seç6 = input("Tedarikçi Firma: ")
            seç7 = input("Ürün Kategorisi: ")
            seç8 = input("Ürünün Raf Alanı: ")

            yeni_ürün = Ürün(seç1, seç2, seç3, seç4, seç5, seç6, seç7, seç8)

            süpermarket.ürün_ekle(yeni_ürün)
            time.sleep(1)

            print("\nMarkete yeni ürün eklendi..\n")

        elif int(seçim) == 4:
            a = input("Marketten ürün silmek/kaldırmak istediğinize eminmisiniz? E/H")

            if a == "e" or a == "E":
                b = input("Silmek istediğiniz ürünin ismini girin: ")
                süpermarket.ürün_sil(b)
            else:
                print("Yanlış giriş yaptınız. Tekrar deneyin!")

        elif int(seçim) == 5:
            seç = input("Satışı yapılacak ürün ismi girin: ")
            süpermarket.ürün_satış(seç)

        elif int(seçim) == 6:
            seç = input("İadesi yapılacak ürün ismi girin: ")
            süpermarket.ürün_iade(seç)

        elif int(seçim) == 7:
            seç = input("Fiyatı güncellenecek ürün ismi girin: ")
            süpermarket.sfiyat_yükselt(seç)

        elif int(seçim) == 8:
            süpermarket.toplam_stok_değeri()

        elif int(seçim) == 9:
            süpermarket.stok_sorgu()

        elif int(seçim) == 10:
            süpermarket.rafalanı_sorgu()

        elif int(seçim) == 11:
            print("Down Cafe Market Yönetim Sisteminden Çıkılıyor..")
            time.sleep(2)
            print("Yine gel ok BYE!")
            break
        else:
            print("Lütfen yaptığınız seçimi gözden geçirerek tekrar giriş yapın!")

    except:
        print("Lütfen geçerli bir giriş yapın!\n")

süpermarket.baglantiyi_kes()