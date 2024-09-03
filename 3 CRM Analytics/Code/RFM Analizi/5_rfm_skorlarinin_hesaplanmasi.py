###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_ = pd.read_excel(r"C:\Users\zbura\OneDrive\Masaüstü\CRM Analytics\3 CRM Analytics\Files\crmAnalytics\datasets\online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.shape
df.isnull().sum()

# essiz urun sayisi nedir?
df["Description"].nunique()

df["Description"].value_counts().head()

df.groupby("Description").agg({"Quantity": "sum"}).head()

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()

df["Invoice"].nunique()

df["TotalPrice"] = df["Quantity"] * df["Price"]

df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()

###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################

df.shape
df.isnull().sum()
df.describe().T
df = df[(df['Quantity'] > 0)]
df.dropna(inplace=True)
df = df[~df["Invoice"].str.contains("C", na=False)]

###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

# Recency, Frequency, Monetary

# Recency : Musterinin yeniligi, sicakligi. ((Analizin yapildigi tarih)-(Musterinin alisveris yaptigi tarih))
# Frequency : Musterinin yaptigi toplam satin alma
# Monetary : Musterinin yaptigi toplam satin almalar neticesinde biraktigi parasal deger.
df.head()

# verisetimiz 2009-2011 yillari arasinda gecmektedir. Biz o donemde yasamadigimiz icin analizin yapildigi gunu herhangi
# bir gun olarak bir degiskene atamamiz gerekmektedir.

df["InvoiceDate"].max()
# burada son fatura tarihini bulduk ve asagide ise bu tarihten 2 gun sonrasini baz alacagimizi soyleyecegiz.

today_date = dt.datetime(2010, 12, 11)
type(today_date)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()
rfm.columns = ['recency', 'frequency', 'monetary']
rfm.describe().T
# Bu ifade icerisinde monetary degeri 0 olan satirlar da oldugu icin bunlari almamaya karar verdik.

rfm = rfm[rfm["monetary"] > 0] # monetary degeri 0 dan buyuk olan tum satirlari sec dedik.
rfm.describe().T
rfm.shape # Yeni verisetimizdeki musteri sayimiz.

###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# qcut fonksiyonu degiskenimiz icindeki degerleri belirttigimiz araliklara boler.
# Biz bu fonksiyonda ilk parametre olarak sutunu verdik.
# Ikinci parametre olarak kac parcaya bolecegini verdik.
# Ucuncu parametre olarak ise boldugumuz parcalara tek tek isim ya da numara verdik.
# Ornek olarak : 0-100 araligini 0-20, 20-40, 40-60, 60-80, 80-100 olarak boler.
rfm.head()

rfm["monetar_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[5, 4, 3, 2, 1])
# Burada ornegin bir sayisi cok fazla tekrar ederek 5 alandan 3 tanesini doldurmus.
# Bu yuzden hata aldik. rank metoduyla ilk gordugunu ilk sinifa ata diyerek bu problemin onune geciyoruz.

rfm.head()

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
# sayisal olan recency_score ve frequency_score degerlerini string'e cevirdik ve birlestirerek RFM_SCORE kolonuna yazdirdik.
rfm.head()

rfm[rfm["RFM_SCORE"] == "55"]
rfm[rfm["RFM_SCORE"] == "24"]





























