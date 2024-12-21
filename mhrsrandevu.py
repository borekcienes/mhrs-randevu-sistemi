#   Mehmet Enes Börekçi - Melisa Nur Çağlar 
#   Aciklama: LinkedList ve Sözlük yapısı kullanılarak Hastane için bir randevu sistemi tasarlandı. 

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# Node sınıf tanımlanır
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# LL sınıfı tanimlanması
class LinkedList:
    def __init__(self):
        self.head = None

    # Yeni bir randevu eklemek için kullanılan fonksiyon
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next: 
            last_node = last_node.next
        last_node.next = new_node
    #  Bölümleri ekleme sırasına göre sıralayarak döndüren fonksiyon
    def get_bolumler(self):
        bolumler_list = []
        current_node = self.head

        # Node olduğu sürece her node verisi listeye eklenir, sonraki node'a geçilir
        while current_node:
            bolumler_list.append(current_node.data)
            current_node = current_node.next

        # Zamana göre sıralanmış hali liste gönderilir
        sorted_bolumler = sorted(
            bolumler_list,
            key=lambda x: datetime.strptime(
                f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"
            ),
        )
        return sorted_bolumler

# Uzmanlık sınıfının tanımlanması
class Bolum:
    def __init__(self, name, expertise):
        self.name = name
        self.expertise = expertise
        self.bolumler = LinkedList()

class doktorbolumlerystem:
    def __init__(self):
        # Doktorlar ve uzmanlıklarının oluşturulması
        self.bolumler = [
            Bolum("Lütfen Bölüm Seçiniz", []),
            Bolum("Dahiliye", ["Dr. Ayşe Yılmaz", "Dr. Emre Kara", "Dr. Fatma Günay"]),
            Bolum("Kardiyoloji", ["Dr. Serkan Arslan", "Dr. Zeynep Çelik", "Prof. Dr. Mehmet Demir"]),
            Bolum("Üroloji", ["Dr. Tayfun Ekentok", "Doç. Dr. Cihan Güloğlu", "Prof. Dr. Enis Öksüz"]),
            Bolum("Kulak Burun Boğaz", ["Dr. Ceren Aksoy", "Dr. Onur Aydın", "Doç. Dr. Ebru Sarı"]),
            Bolum("Ortopedi ve Travmatoloji", ["Dr. Hasan Ünal", "Dr. Büşra Kaplan", "Prof. Dr. Hakan Yıldırım"]),
            Bolum("Göz Hastalıkları", ["Dr. Pelin Yıldız", "Dr. Murat Caner", "Prof. Dr. Selim Erdoğan"]),
            Bolum("Diş Hekimliği", ["Dr. Sevgi Öztürk", "Dr. Halil Demirtaş", "Doç. Dr. Bahar Deniz"]),
            Bolum("Kadın Hastalıkları ve Doğum", ["Dr. Elif Akın", "Doç. Dr. Fahreddin Enes Sözer", "Prof. Dr. Yasemin Koç"]),
            Bolum("Çocuk Sağlığı ve Hastalıkları", ["Dr. Özgür Şahin", "Dr. Merve Güzel", "Dr. Nihat Soylu"]),
            Bolum("Dermatoloji", ["Dr. Canan Er", "Dr. Eren Demir", "Doç. Dr. Nurhan Kılıç"]),
            Bolum("Psikiyatri", ["Dr. Cem Öz", "Dr. Aylin Arıkan", "Doç. Dr. Tarık Çelik"]),
            Bolum("Nöroloji", ["Dr. Cansu Yılmaz", "Dr. Orhan Bayraktar", "Prof. Dr. Selda Kaya"]),
            Bolum("Genel Cerrahi", ["Dr. Burak Yücel", "Dr. Nazlı Güneş", "Doç. Dr. Mahir Özkan"])
        ]

    # Bölüm nesnesini getiren fonksiyon
    def get_bolum_name(self, bolum_name):
        for bolum in self.bolumler:
            if bolum.name == bolum_name:
                return bolum
        return None

    # Hastanede bulunan bolumleri getiren fonksiyon
    def get_bolum_expertise(self, bolum_name):
        bolum = self.get_bolum_name(bolum_name)
        return bolum.expertise if bolum else []

    # Uygun saat araligini kontrol eder
    def is_valid_doctor_time(self, time):
        start_morning_time = datetime.strptime("09:00", "%H:%M")
        end_morning_time = datetime.strptime("11:20", "%H:%M")
        start_afternoon_time = datetime.strptime("13:00", "%H:%M")
        end_afternoon_time = datetime.strptime("16:50", "%H:%M")

        # Input olarak alinan zaman  datetime nesnesine donusturulur.
        doctor_time = datetime.strptime(time, "%H:%M")

        # 09:00 - 11:20  ve  13:00 - 16:50 arasindaki saat araliklarina randevu alinabilir oldugunu kontrol eder.  | Son randevular 11:30'a ve 17:00'a kadar surmesi icin 11:20 ve 16:50 secilmistir.
        if (
            (start_morning_time <= doctor_time <= end_morning_time)
            or (start_afternoon_time <= doctor_time <= end_afternoon_time)
        ):
            return True
        else:
            return False

    # Randevu alma islemi icin kullanilan fonksiyon
    def schedule_doctor(self, patient_name, date, time, bolum_name, doctor_type):
        # Bolum bilgisi alinir
        bolum = self.get_bolum_name(bolum_name)
        # Bolum bilgisi yoksa veya randevu saati uygun degilse False doner 
        if not bolum or not self.is_valid_doctor_time(time):
            return False

        # Yeni randevu icin datetime nesnesi olusturulur
        new_doctor_time = datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %H:%M"
        )
        # Ayni doktor'un mevcut randevularina bakilir.
        for existing_doctor in bolum.bolumler.get_bolumler():
            existing_doctor_time = datetime.strptime(
                f"{existing_doctor['date']} {existing_doctor['time']}",
                "%Y-%m-%d %H:%M",
            )
            # Eger mevcut randevu yeni randevuyla cakisiyorsa +- 10 dakika (Ornek 10:00 alinmis mevcut randevu varsa 09:51 - 10:09 arasina randevu alinmasi engellenir. 09:50 ve 10:10'a alinabilir)
            if (
                new_doctor_time > existing_doctor_time - timedelta(minutes=10)
                and new_doctor_time < existing_doctor_time + timedelta(minutes=10)
            ):
                return False
        
        # Mevcut randevular arasinda 10 dakika icinde baska bir randevu var mi yok mu o arastirilir (cakisma kontrolu)
        other_doctor_time = datetime.now() + timedelta(minutes=10)
        for existing_doctor in bolum.bolumler.get_bolumler():
            existing_doctor_time = datetime.strptime(
                f"{existing_doctor['date']} {existing_doctor['time']}",
                "%Y-%m-%d %H:%M",
            )

            if (
                existing_doctor_time > datetime.now()
                and existing_doctor_time <= other_doctor_time
            ):
                return False

        # Randevu bilgileri iceren bir sozluk yapisi olusturulur
        new_data = {
            "patient_name": patient_name,
            "date": date,
            "time": time,
            "type": doctor_type,
        }

        # Bu sozluk yapisi Bolum ustundeki Linked list icine aktarilir
        bolum.bolumler.append(new_data)
        return True
    
    # Randevu iptali
    def cancel_doctor(self, date, time, bolum_name):
        # Bolum nesnesine ulasilir
        bolum = self.get_bolum_name(bolum_name)
        if not bolum:
            return False

        # Bolum randevulari arasinda gezinilir
        current_node = bolum.bolumler.head
        prev_node = None

        # Eger randevu bulunursa iptal edilir
        while current_node:
            # Iptal edilmek istenen tarih ve saat eslesiyorsa
            if (
                current_node.data["date"] == date
                and current_node.data["time"] == time
            ):
                # Eger randevu iptal edilecekse
                if prev_node:
                    # Bir önceki node ile bir sonraki node birbirine baglanir 
                    prev_node.next = current_node.next
                else:
                    # İlk node iptal edilmek istenen randevunun ardindaki node ile degisir
                    bolum.bolumler.head = current_node.next
                return True
            # Mevcut node bir onceki node olur
            prev_node = current_node
            # Bir sonraki node su anki node olur
            current_node = current_node.next

        return False
    # Bölüm ismine gore randevulari getirir
    def get_bolumler(self, bolum_name):
        bolum = self.get_bolum_name(bolum_name)
        # Bölüme ait randevular olmamasi durumunda bos bir liste dondurur
        return bolum.bolumler.get_bolumler() if bolum else []

class doktorbolumlerystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MHRS Randevu Sistemi")
        self.bolum_system = doktorbolumlerystem()

        # Pencere boyutu
        root.geometry("750x450")

        # Pencere arkaplan resmi
        image_path = "background.png"
        self.background_image = Image.open(image_path)                      # Arka plan resmini ayarla
        
        # Arkaplan fotografinin yeniden boyutlandirir
        resized_image = self.background_image.resize((750,450))
        self.background_photo = ImageTk.PhotoImage(resized_image)           # GUI'a resim eklenmesi icin kullanilir
        self.background_label = tk.Label(root, image=self.background_photo) # Arka plani yerlestirmek icin etiketlenir arka plan fotografi 
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)      # GUI'in 0 , 0 noktasindan baslayarak arka plan yerslestirilir 1-1 oranla frame buyutuldukce arka planin sabit kalmasi saglanir

        # Pencerenin opakligini ayarlama
        root.attributes("-alpha", 1.0)  # Opaklik Seviyesi 1.0 - 0.0
        
        self.name_label = tk.Label(root, text="Hasta Adı:", bg="#f1f1f1")           # Hasta adi GUI
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Tarih: \nYYYY-MM-DD", bg="#f1f1f1")  # Tarih GUI
        self.date_entry = tk.Entry(root)

        self.time_label = tk.Label(root, text="Saat: \nHH:MM", bg="#f1f1f1")        # Saat GUI
        self.time_entry = tk.Entry(root)

        self.bolum_label = tk.Label(root, text="Lütfen Bölüm Seçiniz:", bg="#f1f1f1") # Bolum GUI
        self.bolum_var = tk.StringVar()                                            # Secilen degeri tutar GUI
        self.bolum_var.set("Lütfen Bölüm Seçiniz")                                # İlk GUI'da bu ifade secili olsun
        bolum_names = [bolum.name for bolum in self.bolum_system.bolumler]
        self.bolum_menu = tk.OptionMenu(root, self.bolum_var, *bolum_names)      # *bolum_names kullanilmasinin sebebi listedeki bolum isimlerini bolum seceneklerine seceneklerine teker teker ayirmak

        self.type_label = tk.Label(root, text="Doktor Seçiniz:", bg="#f1f1f1")
        self.type_var = tk.StringVar()
        self.type_var.set("Doktor Seçiniz")                               # Randevu turunu default olarak "Doktor Seçiniz" yapiyoruz
        self.type_options = []                                                  # Bos bir liste ile baslatiyoruz
        self.type_menu = tk.OptionMenu(root, self.type_var, self.type_options)  # Secimler Bolume göre degisiklik göstericek  

        self.schedule_button = tk.Button(                                       # Randevu alma butonu
            root, text="Randevu Al", command=self.schedule_doctor
        )
        self.cancel_button = tk.Button(                                         # Randevu iptal etme butonu
            root, text="Randevu İptali", command=self.cancel_doctor
        )
        self.display_button = tk.Button(                                        # Randevulari gosterme butonu
            root,
            text="Randevu Listesini Görüntüle",
            command=self.display_bolumler,
        )

        # Pencereye yerlestirme (Widgetlar) Satir / Sutun /x kaydirma / y kaydirma 
        self.name_label.grid(row=0, column=0, padx=(30,10), pady=(40,10))       # Gui'a yazdirilan orn: Hasta Adi:
        self.name_entry.grid(row=0, column=1, padx=(30,10), pady=(40,10))       # Input yeri "Hasta Adi:" karsisindaki doldurma yer 
        self.date_label.grid(row=1, column=0, padx=(30,10), pady=10)
        self.date_entry.grid(row=1, column=1, padx=(30,10), pady=10)
        self.time_label.grid(row=2, column=0, padx=(30,10), pady=10)
        self.time_entry.grid(row=2, column=1, padx=(30,10), pady=10)
        self.bolum_label.grid(row=3, column=0, padx=(30,10), pady=10)
        self.bolum_menu.grid(row=3, column=1, padx=(30,10), pady=10)
        self.type_label.grid(row=4, column=0, padx=(30,10), pady=10)
        self.type_menu.grid(row=4, column=1, padx=(30,10), pady=10)
        # Pencereye yerlestirme (Widgetlar) Satir / Sutun /kac sutunluk yere sahip olmali /x kaydirma /y kaydirma /x yonunde sol sag kenarlarin icerik ile arasinda kaplicagi alan / y ekseninde asagi yukari kenarlarin icerik ile arasinda kaplayacagi alan
        self.schedule_button.grid(row=5, column=0, columnspan=2, padx=(30,10), pady=10, ipadx=115, ipady=0)
        self.cancel_button.grid(row=6, column=0, columnspan=2, padx=(30,10), pady=10, ipadx=110, ipady=0)
        self.display_button.grid(row=7, column=0, columnspan=2, padx=(30,10), pady=10, ipadx=75, ipady=0)

        # Bolum secildiginde doktorları guncelleyecek event baglantisi
        self.bolum_menu.bind("<Configure>", self.update_doctor_types)

        # Son secili doktoru saklamak icin degisken
        self.last_selected_bolum = "Lütfen Doktor Seçiniz"
    
    # Doktorları guncelleme
    def update_doctor_types(self, event):
        # Secili olan Bolumu sakla
        selected_bolum = self.bolum_var.get()
        
        # Eger bolum degistiyse doktoru default deger yap
        if selected_bolum != self.last_selected_bolum:
            self.type_var.set("Doktor Seçiniz")
            self.last_selected_bolum = selected_bolum

        # Bolumun doktorlarını cagir
        bolum_expertise = self.bolum_system.get_bolum_expertise(selected_bolum)
        # Lutfen secim yapiniz tipi + bolumun doktorlarını seceneklere ekle
        self.type_options = ["Doktor Seçiniz"] + bolum_expertise

        # Type menuyu guncelle
        self.type_menu['menu'].delete(0, 'end')  # Önceki secenekleri temizle

        # Secenekler option'a eklenir ve secilen bolume gore bir self_type.var yani gui'a atanir
        for option in self.type_options:
            self.type_menu['menu'].add_command(
                label=option,
                command=lambda value=option: self.type_var.set(value)
            )

    def schedule_doctor(self):
        # Gerekli bilgilerin atanmasi
        patient_name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        doctor_type = self.type_var.get()
        bolum_name = self.bolum_var.get()

        # Hasta adi bos birakilirsa hata ver
        if not patient_name:
            messagebox.showerror(
                "Hata",
                "Hasta adı boş bırakılamaz! \nLütfen geçerli bir hasta adı girin.",
            )
            return
        # Hasta adi sadece harf, bosluk ve - icermelidir haricinde hata ver
        elif not all(char.isalpha() or char.isspace() or char == '-' for char in patient_name):
            messagebox.showerror(
                "Hata",
                "Hasta adı sadece harf ve boşluk karakteri içeriyor olmalıdır! \nLütfen geçerli bir hasta adı girin.",
            )
            return
        
        # İlk kelimenin basinda veya sonuncu kelimenin sonunda bosluk kontrolu yapılır varsa hata ver
        if patient_name.startswith(" ") or patient_name.endswith(" "):
            messagebox.showerror(
                "Hata",
                "Hasta adının başında veya sonunda boşluk olamaz! \nLütfen geçerli bir hasta adı girin.",
            )
            return
        
        # Bosluklari kaldirir
        words = patient_name.split() 
        # Kelimelerin arasina bosluk koyar
        patient_name = ' '.join(words)
        
        # Eger kelimelerden biri 2 karakterden daha kısa olursa hata ver
        if any(len(word) < 2 for word in words):
            messagebox.showerror(
                "Hata",
                "Hasta adı 2 karakterden kısa olamaz! \nLütfen geçerli bir hasta adı girin.",
            )
            return
        
        # Hasta adi 100 karakterden fazla olursa hata ver
        if len(patient_name) > 100:
            messagebox.showerror(
                "Hata",
                "Hasta adı 100 karakterden uzun olamaz! \nLütfen geçerli bir hasta adı girin.",
            )
            return

        # Doktor secimi yapilmadiysa hata ver
        if bolum_name == "Lütfen Seçim Yapınız":
            messagebox.showerror("Hata", "Lütfen bir bölüm seçin!")
            return


        # Tarih eksik girilirse / hatali girilirse hata ver
        try:
            doctor_datetime = datetime.strptime(
                f"{date} {time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            messagebox.showerror(
                "Hata",
                "Lütfen geçerli bir tarih ve saat girin! \n(Örnegin, '2023-11-26 14:30').",
            )
            return
        
        # Randevu alinabilir saatlerin disinda bir zaman girilirse hata ver
        if not self.bolum_system.is_valid_doctor_time(time):
            messagebox.showerror(
                "Hata", "Belirtilen saat aralığında randevu alınamaz!"
            )
            return
        
        # Bugunun tarihinde bir randevu alinacasak saatleri karsilastirilir
        today = datetime.now()
        if (
            doctor_datetime.date() == today.date()
                                and 
            doctor_datetime.time() < today.time()
            ):
            messagebox.showerror(
                "Hata",
                "Geçmiş bir saat için randevu alınamaz! \nLütfen ileri bir tarih ve saat girin.",
                )
            return
        
        # Saat eksik girilirse / hatali girilirse hata ver
        try:    # 10    :   30
            time_format = "%H:%M"
            if ":" not in time or len(time.split(":")) != 2:
                raise ValueError("Geçersiz saat formatı! \nSaati HH:MM biçiminde girin.")
            # 10  30    seklinde int olarak bol ve zamana esitle
            hour, minute = map(int, time.split(":"))
            
            # sonu 00 | 10 | 20 | 30 | 40 | 50 | 60 olan dakikalara randevu alinabilecek 
            if minute % 10 != 0:
                raise ValueError("Dakika kısmı 10'a tam bölünebilmeli.")
            
            time = f"{hour:02d}:{minute:02d}"
            
        except ValueError as e:
            # raise'lanan hata gosterilir
            messagebox.showerror("Hata", str(e))
            return
        
        # Gecmis bir tarihe randevu alinamaz
        today = datetime.now()
        if doctor_datetime < today:
            messagebox.showerror(
                "Hata",
                "Girilen tarih geçmis bir tarih olamaz!"
            )
            return

        # Doktor secilmediyse hata ver
        if doctor_type == "Lütfen Seçim Yapınız":
            messagebox.showerror(
                "Hata", "Lütfen bir doktor seçin!"
            )
            return
        # Randevu alinabilir
        elif self.bolum_system.schedule_doctor(
            patient_name, date, time, bolum_name, doctor_type
        ):
            messagebox.showinfo("Başarılı", "Randevu başarıyla alındı!")
        else:
        # Randevu alinamadi            
            messagebox.showerror(
                "Hata", "Randevu alınamadı! \nLütfen uygun bir saat seçin."
            )

    # Randevu Iptali
    def cancel_doctor(self):
        date = self.date_entry.get()
        time = self.time_entry.get()
        bolum_name = self.bolum_var.get()
        if self.bolum_system.cancel_doctor(date, time, bolum_name):
            messagebox.showinfo("Basarılı", "Randevu başarıyla iptal edildi!")
        else:
            messagebox.showerror(
                "Hata",
                "Randevu iptal edilemedi! \nBelirtilen tarihte ve saatte randevu bulunamadı.",
            )

    # Randevu Gosterme
    def display_bolumler(self):
        bolum_name = self.bolum_var.get()
        bolumler = self.bolum_system.get_bolumler(bolum_name)
        # Randevu yoksa bilgi mesaj kutusu yolla
        if not bolumler:
            messagebox.showinfo("Bilgi", "Henüz randevu bulunmamaktadır!")
        else:
            # Sirayla ekle Hasta: ... | Muayne Tarihi: ... | Saat: ... | Bölüm: ... | Doktor: ... |
            doctor_str = "\n".join(
                [
                    f"Hasta: {doctor['patient_name']} | Muayene Tarihi: {doctor['date']} | Saat: {doctor['time']} | Bölüm: {bolum_name} | Doktor: {doctor['type']}"
                    for doctor in bolumler
                ]
            )
            # Listeyi Goster
            messagebox.showinfo("Randevu Listesi", doctor_str)

if __name__ == "__main__":
    root = tk.Tk()                          # Tkinter penceresi olusturur
    app = doktorbolumlerystemUI(root)  # GUI'nin olusturulmasi ve Tkinter'a erisimi saglar
    root.mainloop()                         # Pencere kapatilana kadar calismasini saglar
