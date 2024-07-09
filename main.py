import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
import hashlib
import json
import os

oluşumlar = {}

#kayıtlı kodları yükleme
if os.path.exists("oluşumlar.json"):
    with open("oluşumlar.json", "r") as file:
        oluşumlar = json.load(file)



#kod oluşturma
def kod_oluşturma(metin, şifre):
    anahtar = Fernet.generate_key()
    f = Fernet(anahtar)
    şifreli_metin = f.encrypt(metin.encode())
    şifre_hash = hashlib.sha256(şifre.encode()).hexdigest()
    kod = anahtar.decode() + ":" + şifre_hash
    oluşumlar[kod] = şifreli_metin.decode()  # Kod ve şifreli metni oluşumlara ekleme

    # Kodları dosyaya kaydetme
    with open("oluşumlar.json", "w") as file:
        json.dump(oluşumlar, file)
    return kod


#hata mesajı
def hata_mesaji(mesaj):
    messagebox.showerror("Hata", mesaj)


#kaydetme işlemi
def kaydetme_işlemi():
    not_ismi = isim_entry.get().strip()
    metin = not_text.get("1.0", tk.END).strip()
    şifre = şifre_entry.get()

    if not not_ismi:
        hata_mesaji("Lütfen not ismini girin.")
        return
    if not metin:
        hata_mesaji("Lütfen notunuzu girin.")
        return
    if not şifre:
        hata_mesaji("Lütfen şifrenizi girin.")
        return

    kod = kod_oluşturma(metin, şifre)

    file_path = f"{not_ismi}.txt"
    with open(file_path, 'w') as file:
        file.write(kod)

    messagebox.showinfo("Başarılı", f"Not başarıyla kaydedildi.")


#kodu çözme
def kodu_çöz(kod, şifre):
    try:
        anahtar, şifre_hash = kod.split(':')
    except ValueError:
        return "Kod formatı hatalı"

    if hashlib.sha256(şifre.encode()).hexdigest() == şifre_hash:
        f = Fernet(anahtar.encode())
        if kod in oluşumlar:
            try:
                çözülmüş_metin = f.decrypt(oluşumlar[kod].encode()).decode()
                return çözülmüş_metin
            except Exception as e:
                return f"Şifre çözme hatası: {str(e)}"
        else:
            return "Kod bulunamadı"
    else:
        return "Kod veya şifre hatalı"


#notu açma
def açma_işlemi():
    kod = not_text.get("1.0", tk.END).strip()
    if not kod:
        hata_mesaji("Lütfen kodu girin.")
        return

    şifre_girildi = False
    while not şifre_girildi:
        şifre = şifre_entry.get()
        if not şifre:
            hata_mesaji("Lütfen şifre girin.")
            return

        çözülmüş_metin = kodu_çöz(kod, şifre)
        if çözülmüş_metin.startswith("Kod") or çözülmüş_metin.startswith("Şifre"):
            hata_mesaji(çözülmüş_metin)
            return
        else:
            not_text.delete("1.0", tk.END)
            not_text.insert(tk.END, çözülmüş_metin)
            şifre_girildi = True

#ekran
ekran = tk.Tk()
ekran.title("Gizli Not Uygulaması")
ekran.minsize(360, 600)

#resim
img = ImageTk.PhotoImage(Image.open("OIP.jpeg"))
resim_label = tk.Label(ekran, image=img)
resim_label.pack(pady=15)

#not ismi
isim_label = tk.Label(ekran, text="Not ismini giriniz", fg="black", font="20")
isim_label.pack()
isim_entry = tk.Entry(ekran, bg="orange")
isim_entry.pack(pady=2)

#not
not_label = tk.Label(ekran, text="Notunuzu giriniz", fg="black", font="20")
not_label.pack()
not_text = tk.Text(ekran, height=13, width=30, bg="orange")
not_text.pack()

#şifre
şifre_label = tk.Label(ekran, text="Şifre giriniz", fg="black", font="20")
şifre_label.pack()
şifre_entry = tk.Entry(ekran, bg="orange", show="*")
şifre_entry.pack(pady=7)

#kaydetme butonu
kaydetme = tk.Button(ekran, text="Kaydet", width=11, fg="black", bg="orange", font="bold", command=kaydetme_işlemi)
kaydetme.pack(pady=8)

#yükleme butonu
yazdırma = tk.Button(ekran, text="Aç", width=9, fg="black", bg="orange", font="bold", command=açma_işlemi)
yazdırma.pack()


ekran.mainloop()
