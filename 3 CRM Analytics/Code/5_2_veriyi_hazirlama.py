############################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)
############################################

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması

##################################################
# 1. Veri Hazırlama
##################################################

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_ = pd.read_excel(r"C:\Users\zbura\OneDrive\Masaüstü\CRM Analytics\3 CRM Analytics\Files\crmAnalytics\datasets\online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()

df.isnull().sum()

# C ile baslayan ifadeler bize iade olan urunleri belirtmektedir. Bunlari verisetimizden cikartalim.
df = df[~df["Invoice"].str.contains("C", na=False)]
#  Basinda C olmayan ifadeleri cagirdik.
df.isnull().sum()

df.describe().T
# Veri setinin betimsel istatistigini getirdigimizde quantity degerinde - (eksi) degerlerin oldugunu gorduk.
# Boyle bir sey olamayacagi icin 0'dan buyuk degerleri almamiz gerekir
df = df[(df['Quantity'] > 0)]

df.dropna(inplace=True)
# Eksik degerleri ucurduk.

df["TotalPrice"] = df["Quantity"] * df["Price"]
# TotalPrice adinda yeni bir degisken olusturarak her alisverislerde urun basi elde ettigimiz kazanci getirdik.
df.head()

cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

# Customer ID'ye gore grupladiktan sonra, Invoice degiskeninin essiz degerlerini saydir,
# Quantity degiskeninin toplamini al ve TotalPrice degiskeninin toplamini al.

cltv_c

cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
# sutun isimlerini degistirdik.

cltv_c


















