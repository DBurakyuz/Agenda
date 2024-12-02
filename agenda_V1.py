from datetime import datetime, date #tarihi doğru almak için import ettik


class Node:
    def __init__(self, date, event):# ağaç yapısı
        self.date = date
        self.event = event
        self.left = None
        self.right = None


class Agenda:
    def __init__(self):#ajanda yapısı
        self.root = None

    def add_event(self, date, event):
        if self.root is None:#kökün boş olup olmadığını kontrol ettik. Boşsa yeni düğüm oluşturur.
            self.root = Node(date, event)
        else:#boş değilse ekleme fonksiyonunu çalıştırır
            self._add(self.root, date, event)#şu anki tarihi kök olarak ekler

    def _add(self, current, date, event):
        if date < current.date:#şu anki tarih aradığımız tarihten küçükse düğümün solundan devam eder
            if current.left is None:#düğümün solu boşsa oraya yeni düğüm oluşturur
                current.left = Node(date, event)
            else:#değilse ekleme fonksiyonu tekrar çalışır
                self._add(current.left, date, event)
        elif date > current.date:#büyükse sağından devam eder
            if current.right is None:#sağdaki düğüm boşsa yeni düğüm oluşturur
                current.right = Node(date, event)
            else:# boş değilse fonksiyon tekrar çalışır.
                self._add(current.right, date, event)
        else:
            print("{} için zaten bir etkinlik mevcut!".format(date))#tarih doluysa etkinlik ekleyemez(geliştirilecek)

    def display(self):#ajandayı terminale yazdırır
        self._inorder(self.root)#kökten itibaren göstermeye başlar

    def _inorder(self, current):
        if current is not None:#ilk başta ağacın en soluna gider ve onu yazdırır sonra kökü yazdırır sonra kökün sağını yazdırır.
            #Sonra en baştaki köke gidene kadar bunu yapmaya devam eder.Ağacın kökünü yazdırır.
            #Sonra ağacın sağ tarafı için aynısını yapmaya devam eder.(inorder gibi)
            self._inorder(current.left)
            self._inorder(current.right)
            print("Tarih: {}, Etkinlik: {}".format(current.date,current.event))


def menu():
    agenda = Agenda()
    while True:
        print("\n--- Ajanda Uygulaması ---")
        print("1. Etkinlik Ekle")
        print("2. Tüm Etkinlikleri Görüntüle")
        print("3. Çıkış")
        choice = input("Seçiminizi yapın (1-3): ")

        if choice == "1":
            date_str = input("Tarih girin (YYYY-MM-DD): ")
            try:# kullanıcın yanlış değer girmesine rağmen kodun hata verip durmaması için try ve except kullanılır.
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()#kullanıcının string ile girdiği tarihi datetime a çevirir.
                event = input("Etkinlik açıklamasını girin: ")
                agenda.add_event(date_obj, event)
                print("Etkinlik başarıyla eklendi!")
            except ValueError: #eğer kullanıcı tarih girmezse hata verir.
                print("Geçersiz tarih formatı! Lütfen YYYY-MM-DD formatında tarih girin.")


        elif choice == "2":
            print("\nTüm Etkinlikler:")
            agenda.display()
        elif choice == "3":
            print("Uygulama kapatılıyor. Hoşça kalın!")
            break
        else:
            print("Geçersiz bir seçim yaptınız. Lütfen tekrar deneyin.")



menu()# Uygulamayı çalıştır menu çalışır
