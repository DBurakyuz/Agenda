import os
from datetime import datetime
import heapq
#gerekli kütüphaneler eklendi

class Node:
    def __init__(self, date, events):
        self.date = date
        self.events = events
        self.left = None
        self.right = None

class EventTree:
    def __init__(self):
        self.root = None

    def add_event(self, date, event, is_priority=False):
        #Ağaca bir etkinlik ekler.
        if self.root is None:
            self.root = Node(date, [(event, is_priority)])
        else:
            self._add(self.root, date, event, is_priority)

    def _add(self, current, date, event, is_priority):
        if date < current.date:
            if current.left is None:
                current.left = Node(date, [(event, is_priority)])
            else:
                self._add(current.left, date, event, is_priority)
        elif date > current.date:
            if current.right is None:
                current.right = Node(date, [(event, is_priority)])
            else:
                self._add(current.right, date, event, is_priority)
        else:  # Aynı tarihe ait yeni etkinlik eklenir
            current.events.append((event, is_priority))

    def find_events(self, date, time=None):
        if time:
            date = date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
        return self._find(self.root, date)

    def _find(self, current, date):
        if current is None:
            return None
        if date == current.date:
            return current.events
        elif date < current.date:
            return self._find(current.left, date)
        else:
            return self._find(current.right, date)

    def update_event(self, date, old_event, new_event):
        """Belirli bir tarihteki etkinliği günceller."""
        events = self.find_events(date)  #verilen tarihe ait etkinlikleri bul
        if events:
            for i, (event, is_priority) in enumerate(events):
                if event == old_event:  # eski etkinlik bulunduysa
                    events[i] = (new_event, is_priority)  # etkinliği güncelle
                    return True
        return False  # eğer etkinlik bulunamadıysa, False döndür

    def inorder_traversal(self):
        """Tüm ağacı sıralı bir şekilde döner."""
        events = []
        self._inorder(self.root, events)
        return events

    def _inorder(self, current, events):
        if current is not None:
            self._inorder(current.left, events)
            events.append((current.date, current.events))
            self._inorder(current.right, events)

    def remove_event(self, date, event):
        """Belirli bir tarihteki etkinliği siler."""
        self.root = self._remove(self.root, date, event)

    def _remove(self, current, date, event):
        if current is None:
            return None
        if date < current.date:
            current.left = self._remove(current.left, date, event)
        elif date > current.date:
            current.right = self._remove(current.right, date, event)
        else:  # Tarih eşleşti
            updated_events = []  #güncellenmiş etkinlikler için boş bir liste oluşturuyoruz
            for e, p in current.events:  #current.events içinde döngü başlatıyoruz
                if e != event:  #eğer etkinlik, silmek istediğimiz etkinlik ile eşleşmiyorsa
                    updated_events.append((e, p))  #bu etkinliği listeye ekliyoruz
            current.events = updated_events  #güncellenmiş listeyi current.events'e atıyoruz

            if not current.events:  #eğer o tarihe ait başka etkinlik yoksa düğümü kaldır
                if current.left is None:
                    return current.right
                elif current.right is None:
                    return current.left
                min_larger_node = self._find_min(current.right)
                current.date, current.events = min_larger_node.date, min_larger_node.events
                current.right = self._remove_min(current.right)

        return current

    def _find_min(self, current):
        while current.left is not None:
            current = current.left
        return current

    def _remove_min(self, current):
        if current.left is None:
            return current.right
        current.left = self._remove_min(current.left)
        return current

class Agenda:
    def __init__(self, file_name="agenda.txt"):
        self.tree = EventTree()
        self.file_name = file_name
        self.load_from_file()

    def add_event(self, date, event, is_priority=False):
        self.tree.add_event(date, event, is_priority)
        self.save_to_file()

    def find_events(self, date, time=None):
        if time:
            date = date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
        return self.tree.find_events(date, time)

    def update_event(self, date, old_event, new_event):
        if self.tree.update_event(date, old_event, new_event):
            self.save_to_file()
            return True
        return False

    def remove_event(self, date, event):
        self.tree.remove_event(date, event)
        self.save_to_file()

    def display(self):
        #tüm etkinlikleri ağacı gezerek alıyoruz
        events = self.tree.inorder_traversal()
        priority_events = []  #öncelikli etkinlikleri buraya koyacağız
        normal_events = []  #normal etkinlikleri buraya koyacağız

        for date, event_list in events:#etkinlikleri tek tek kontrol ediyoruz
            for event, is_priority in event_list:
                if is_priority:#eğer etkinlik öncelikli ise, öncelikli listeye ekle
                    heapq.heappush(priority_events, (date, event))
                else:#yoksa normal listeye ekle
                    normal_events.append((date, event))

        print("\n**** Öncelikli Etkinlikler ****")
        while priority_events:
            date, event = heapq.heappop(priority_events)#öncelikli etkinliklerden birini alıyoruz
            if date.hour or date.minute:#eğer tarih saat içeriyorsa saati düzenledik
                event_time = date.strftime('%H:%M')
            else:
                event_time = " "  #saat yoksa boş bırak
            print(f"Tarih: {date.strftime('%d-%m-%Y')} Saat: {event_time} Etkinlik: {event}")

        print("\n--- Normal Etkinlikler ---")
        for date, event in normal_events:
            if date.hour or date.minute:#eğer tarih saat içeriyorsa saati düzenle
                event_time = date.strftime('%H:%M')
            else:
                event_time = " "  #saat yoksa boş bırak
            print(f"Tarih: {date.strftime('%d-%m-%Y')} Saat: {event_time} Etkinlik: {event}")

    def save_to_file(self):
        with open(self.file_name, "w") as file:#dosyayı yazmak için açıyoruz
            events = self.tree.inorder_traversal()#etkinlikleri sıralı bir şekilde alıyoruz
            for date, event_list in events:# her etkinliği tek tek kontrol ediyoruz
                for event, is_priority in event_list:
                    if date.hour != 0 or date.minute != 0:
                        event_time = date.strftime('%H:%M')
                    else:# eğer saat belirtilmemişse, " " olarak kaydediyoruz
                        event_time = " "  # saat yoksa boş bırak

                    if is_priority:# eğer saat belirtilmemişse, " " olarak kaydediyoruz
                        priority_label = "Oncelikli"
                    else:
                        priority_label = " "  # normal etkinliklerde boş bırak
                    file.write(f"{date.strftime('%d-%m-%Y')},{event_time},{event},{priority_label}\n")# Etkinliği dosyaya yazıyoruz

    def load_from_file(self):
        if os.path.exists(self.file_name):#dosya varmı diye kontrol ediyoruz
            with open(self.file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Boş satırı atla
                        continue
                    try:
                        parts = line.split(",", 3)
                        date_str, time_str, event, priority_label = parts
                        is_priority = priority_label.strip().lower() == 'oncelikli'
                        if time_str.strip():  # Eğer zaman belirtilmişse
                            date_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
                        else:  # Saat verilmemişse
                            date_time = datetime.strptime(date_str, "%d-%m-%Y")
                        self.add_event(date_time, event, is_priority)
                    except ValueError:
                        print(f"Geçersiz satır: {line} (Format hatası)")

    def find_events_on_day(self, date):
        #Belirli bir günde yapılacak etkinlikleri bulur.
        target_date = date.date()#zaman bilgisi hariç sadece tarihi alıyoruz
        events_on_day = []  #o günde yapılacak etkinlikleri tutacak liste
        events = self.tree.inorder_traversal()#ağacı sıralı şekilde tarıyoruz
        for event_date, event_list in events:
            # Eğer etkinliğin tarihi hedef tarihle aynıysa
            if event_date.date() == target_date:
                # Aynı gün olan etkinlikler için döngü başlatıyoruz
                for event, is_priority in event_list:
                    #Saat belirtilmemişse sadece tarih gösterilir
                    if event_date.hour != 0 or event_date.minute != 0:
                        event_time = event_date.strftime('%H:%M')  # Saat ve dakika yazılır
                    else:
                        event_time = " "  # Saat belirtilmemişse boş bırakılır
                    #Etkinlik öncelikli ise "Oncelikli" etiketi eklenir
                    if is_priority:
                        priority_label = "Oncelikli"
                    else:
                        priority_label = " "  # Normal etkinliklerde boş bırakılır
                    #Etkinliği listeye ekliyoruz
                    events_on_day.append((event_time, event, priority_label))
        return events_on_day


def menu():
    agenda = Agenda()
    while True:
        print("\n--- Ajanda Uygulaması ---")
        print("1. Etkinlik Ekle")
        print("2. Etkinlikleri Görüntüle")
        print("3. Etkinlik Sil")
        print("4. Etkinlik Güncelle")
        print("5. Belirli Bir Gündeki Etkinlikleri Görüntüle")
        print("6. Etkinlik Ara (Tarih ve Saat)")
        print("7. Çıkış")
        choice = input("Seçiminizi yapın (1-7): ")

        if choice == "1":
            date_str = input("Tarih girin (DD-MM-YYYY): ")
            time_str = input("Saat girin (HH:MM) [Opsiyonel]: ")
            try:
                if time_str:  # Saat girilmişse
                    date_obj = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
                else:  # Saat verilmemişse
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                event = input("Etkinlik açıklamasını girin: ")
                is_priority_str = input("Oncelikli mi? (Evet/Hayır): ").strip().lower()
                is_priority = is_priority_str == 'evet'
                agenda.add_event(date_obj, event, is_priority)
                print("Etkinlik başarıyla eklendi!")
            except ValueError:
                print("Geçersiz giriş! Lütfen tarih ve saati doğru formatta girin.")

        elif choice == "2":
            agenda.display()

        elif choice == "3":
            date_str = input("Tarihi girin (DD-MM-YYYY): ")
            time_str = input("Saat girin (HH:MM) [Opsiyonel]: ")
            try:
                if time_str:  # Saat girilmişse
                    date_obj = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
                else:  # Saat verilmemişse
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                event = input("Silmek istediğiniz etkinliği girin: ")
                agenda.remove_event(date_obj, event)
                print("Etkinlik başarıyla silindi!")
            except ValueError:
                print("Geçersiz tarih formatı! Lütfen DD-MM-YYYY HH:MM formatında tarih girin.")

        elif choice == "4":
            date_str = input("Tarihi girin (DD-MM-YYYY): ")
            time_str = input("Saat girin (HH:MM) [Opsiyonel]: ")
            try:
                if time_str:  # Saat girilmişse
                    date_obj = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
                else:  # Saat verilmemişse
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                old_event = input("Güncellemek istediğiniz etkinliği girin: ")
                new_event = input("Yeni etkinlik açıklamasını girin: ")
                if agenda.update_event(date_obj, old_event, new_event):
                    print("Etkinlik başarıyla güncellendi!")
                else:
                    print("Etkinlik bulunamadı.")
            except ValueError:
                print("Geçersiz tarih formatı! Lütfen DD-MM-YYYY HH:MM formatında tarih girin.")

        elif choice == "5":
            date_str = input("Günlük etkinlikleri görüntülemek için tarihi girin (DD-MM-YYYY): ")
            try:
                date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                events_on_day = agenda.find_events_on_day(date_obj)
                print(f"\n{date_str} tarihinde yapılacak etkinlikler:")
                for event_time, event, priority_label in events_on_day:
                    print(f"Saat: {event_time} Etkinlik: {event} {priority_label}")
            except ValueError:
                print("Geçersiz tarih formatı! Lütfen DD-MM-YYYY formatında tarih girin.")

        elif choice == "6":
            date_str = input("Tarih girin (DD-MM-YYYY): ")
            time_str = input("Saat girin (HH:MM) [Opsiyonel]: ")
            try:
                if time_str:  # Saat girilmişse
                    date_obj = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
                else:  # Saat verilmemişse
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                events = agenda.find_events(date_obj)  # Sadece date_obj gönderiliyor
                if events:
                    print("Bulunan etkinlikler:")
                    for event, is_priority in events:
                        priority_label = "Oncelikli" if is_priority else ""
                        print(f"Etkinlik: {event} {priority_label}")
                else:
                    print("Etkinlik bulunamadı.")
            except ValueError:
                print("Geçersiz tarih formatı! Lütfen DD-MM-YYYY HH:MM formatında tarih girin.")



        elif choice == "7":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçenek! Lütfen 1-7 arasında bir seçim yapın.")
menu()
