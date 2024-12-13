import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
from fpdf import FPDF

# Mapa kolorów do RGB
color_map = {
    "pink": (255, 105, 180),
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}


def generate_qr():
    # Pobierz dane z pola tekstowego
    data = entry.get()
    if not data:
        messagebox.showwarning("Brak danych", "Wprowadź dane do wygenerowania kodu QR!")
        return

    # Pobierz wybrany kolor kodu QR
    color_name = color_var.get()
    if color_name not in color_map:
        messagebox.showwarning("Błędny kolor", "Wybierz poprawny kolor!")
        return

    # Pobierz wybrany kolor tła
    bg_color_name = bg_color_var.get()
    if bg_color_name not in color_map:
        messagebox.showwarning("Błędny kolor tła", "Wybierz poprawny kolor tła!")
        return

    # Wygeneruj kod QR z wybranym kolorem i tłem
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Ustal kolory (czarny i biały, jeśli nie wybrano koloru)
    fill_color = color_map[color_name]
    back_color = color_map[bg_color_name]

    # Generowanie kodu QR z wybranym kolorem
    qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Zapytaj użytkownika, w jakim formacie chce zapisać kod QR
    format_choice = format_var.get()

    if format_choice == 'PNG':
        save_as_png(qr_image)
    elif format_choice == 'PDF':
        save_as_pdf(qr_image)
    else:
        messagebox.showwarning("Błąd", "Wybierz format zapisu!")


def save_as_png(qr_image):
    # Zapisz QR jako PNG
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Zapisz kod QR jako"
    )
    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("Sukces", f"Kod QR został zapisany jako {file_path}")
        show_qr(file_path)


def save_as_pdf(qr_image):
    # Zapisz QR jako PDF
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Zapisz kod QR jako PDF"
    )
    if file_path:
        # Zapisz tymczasowy plik PNG
        qr_img_path = "qr_temp.png"
        qr_image.save(qr_img_path)

        # Tworzenie PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.image(qr_img_path, x=10, y=10, w=100)
        pdf.output(file_path)
        messagebox.showinfo("Sukces", f"Kod QR został zapisany jako {file_path}")


def show_qr(file_path):
    # Wyświetl obraz w aplikacji
    img = Image.open(file_path)
    img = img.resize((200, 200))  # Skalowanie do okna
    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img


def update_color_selection(event):
    # Sprawdź, czy cokolwiek zostało zaznaczone
    selection = color_listbox.curselection()
    if not selection:
        return  # Jeśli brak zaznaczenia, zakończ funkcję
    selected_color = color_listbox.get(selection)
    color_var.set(selected_color)

    # Ustaw kolor tła dla wybranych elementów
    for i in range(color_listbox.size()):
        color_listbox.itemconfig(i, bg="black")  # Resetuj tło
    if selected_color == "white" or selected_color == "black":
        color_listbox.itemconfig(selection[0], bg="gray")
    else:
        color_listbox.itemconfig(selection[0], bg=selected_color)# Podświetl wybrany element

def update_bg_color_selection(event):
    # Sprawdź, czy cokolwiek zostało zaznaczone
    selection = bg_color_listbox.curselection()
    if not selection:
        return  # Jeśli brak zaznaczenia, zakończ funkcję
    selected_color = bg_color_listbox.get(selection)
    bg_color_var.set(selected_color)

    # Ustaw kolor tła dla wybranych elementów
    for i in range(bg_color_listbox.size()):
        bg_color_listbox.itemconfig(i, bg="black")  # Resetuj tło
    if selected_color == "white" or selected_color == "black":
        bg_color_listbox.itemconfig(selection[0], bg="gray")
    else:
        bg_color_listbox.itemconfig(selection[0], bg=selected_color)# Podświetl wybrany element



# Ustawienia głównego okna
root = tk.Tk()
root.title("Generator kodów QR")
root.geometry("400x700")

# Pole do wpisania tekstu
tk.Label(root, text="Wprowadź dane do kodu QR:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# Opcje wyboru formatu
format_var = tk.StringVar(value='PNG')  # Domyślnie PNG
tk.Radiobutton(root, text="PNG", variable=format_var, value="PNG").pack(pady=5)
tk.Radiobutton(root, text="PDF", variable=format_var, value="PDF").pack(pady=5)

# Pole do wyboru koloru kodu QR
tk.Label(root, text="Wybierz kolor dla kodu QR:").pack(pady=10)

# Zmienna do trzymania wybranego koloru
color_var = tk.StringVar(value="pink")  # Domyślnie kolor różowy

# Lista sugerowanych kolorów
color_listbox = tk.Listbox(root, height=4, width=20, selectmode=tk.SINGLE)
for color in color_map.keys():
    color_listbox.insert(tk.END, color)
color_listbox.pack(pady=10)

# Zaznacz domyślny kolor w pierwszej liście
color_listbox.select_set(color_listbox.get(0, tk.END).index(color_var.get()))

# Podłączenie zdarzenia, które ustawia wybrany kolor
color_listbox.bind('<<ListboxSelect>>', update_color_selection)

# Pole do wyboru koloru tła
tk.Label(root, text="Wybierz kolor tła:").pack(pady=10)

# Zmienna do trzymania wybranego koloru tła
bg_color_var = tk.StringVar(value="white")  # Domyślnie kolor tła biały

# Lista sugerowanych kolorów tła
bg_color_listbox = tk.Listbox(root, height=4, width=20, selectmode=tk.SINGLE)
for color in color_map.keys():
    bg_color_listbox.insert(tk.END, color)
bg_color_listbox.pack(pady=10)

# Zaznacz domyślny kolor tła w drugiej liście
bg_color_listbox.select_set(bg_color_listbox.get(0, tk.END).index(bg_color_var.get()))

# Podłączenie zdarzenia, które ustawia wybrany kolor tła
bg_color_listbox.bind('<<ListboxSelect>>', update_bg_color_selection)

# Przycisk do generowania QR
tk.Button(root, text="Generuj kod QR", command=generate_qr).pack(pady=10)

# Obszar do wyświetlania kodu QR
qr_label = tk.Label(root)
qr_label.pack(pady=20)

# Uruchomienie aplikacji
root.mainloop()
