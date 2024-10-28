import tkinter as tk
import os
from tkinter import font
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import keyboard
import threading
import time
import math

#Uso de aplicacion con escalado de pantalla en 125%


# Variables globales
running = False
paused = False
elapsed_time = 0
start_time = 0
key_combination_start_stop = "ctrl+alt+t"  # Iniciar/Detener y ocultar/mostrar
key_combination_pause = "ctrl+alt+p"       # Pausar/Reanudar sin ocultar
update_task = None  # Para manejar la tarea de actualización y evitar duplicados
icon_path = os.path.join(os.path.dirname(__file__), 'th.ico')

# Función para iniciar/detener el cronómetro
def toggle_timer():
    global running, paused, elapsed_time, start_time, update_task
    if running:
        # Detener y ocultar el cronómetro
        running = False
        paused = False
        elapsed_time = 0  # Reiniciar el tiempo
        timer_text.set("00:00")  # Reiniciar la visualización del cronómetro
        overlay.withdraw()  # Oculta el cronómetro
        if update_task:
            overlay.after_cancel(update_task)  # Cancela cualquier tarea en ejecución
    else:
        # Reiniciar y mostrar el cronómetro
        running = True
        paused = False
        overlay.deiconify()  # Muestra el cronómetro en pantalla
        start_time = time.time()  # Reiniciar el tiempo de inicio
        update_task = overlay.after(1000, lambda: update_timer())

# Función para pausar/reanudar el cronómetro
def pause_timer():
    global paused, start_time, elapsed_time
    if not paused:
        # Pausar el cronómetro
        paused = True
        elapsed_time += int(time.time() - start_time)  # Actualizar el tiempo acumulado
    else:
        # Reanudar el cronómetro
        paused = False
        start_time = time.time()  # Reiniciar el tiempo de inicio

# Función para actualizar el cronómetro
def update_timer():
    global elapsed_time, update_task
    if running:
        if not paused:
            current_time = int(time.time() - start_time) + elapsed_time  # Tiempo total transcurrido
            minutes, seconds = divmod(current_time, 60)
            timer_text.set(f"{minutes:02}:{seconds:02}")
        # Vuelve a llamar después de 1 segundo
        update_task = overlay.after(1000, update_timer)


# Crear ventana de overlay sin bordes ni decoraciones
overlay = tk.Tk()
overlay.title("Cronómetro")


screen_width = overlay.winfo_screenwidth() * 1.25 #<-- quitar(100% de escalado de pantalla) o cambiar el 1.25 al escalado de pantalla que utilice

posición = round(screen_width * 0.3479166666666667)
print(screen_width)
print(posición)
                         
overlay.geometry(f"200x80+{posición}+0")  # Tamaño y posición ajustable para la visibilidad
overlay.attributes("-topmost", True)  # Superpone la ventana a otras aplicaciones
overlay.attributes("-transparentcolor", "pink")  # Fondo transparente (blanco)
overlay.overrideredirect(True)  # Quita completamente los bordes

# Etiqueta para mostrar el tiempo
timer_text = tk.StringVar(value="00:00")
label = tk.Label(overlay, textvariable=timer_text, font=("MS Sans Serif", 24), fg="white", bg="pink", borderwidth=0)
label.pack(expand=True)

# Fondo temporal visible para depuración
overlay.configure(bg="pink")  # Cambiará a transparente cuando esté funcionando bien

# Ocultar el cronómetro inicialmente
overlay.withdraw()

# Configuración del menú de la bandeja
def create_image():
    image = Image.open("th.ico")  # Archivo .ico para el icono de la bandeja
    return image

# Función para mostrar la ventana de configuración desde la bandeja
def show_settings(icon, item):
    settings_window.deiconify()

# Función para cerrar el programa desde la bandeja
def quit_program(icon, item):
    icon.stop()
    overlay.quit()
    overlay.destroy()
    settings_window.quit()

# Crear icono en la bandeja con menú de opciones
def minimize_to_tray():
    image = create_image()
    menu = Menu(
        MenuItem("Configuración", show_settings),
        MenuItem("Salir", quit_program)
    )
    icon = Icon("cronometro", image, "Cronómetro", menu)
    threading.Thread(target=icon.run, daemon=True).start()

# Ventana de configuración
settings_window = tk.Toplevel()
settings_window.iconbitmap(icon_path)
settings_window.title("Configuración del Cronómetro")
settings_window.geometry("300x200")
settings_window.protocol("WM_DELETE_WINDOW", lambda: settings_window.withdraw())  # Oculta en lugar de cerrar

# Selector de fuente  "MS Sans Serif", 24
def set_font(font_name="MS Sans Serif", font_size=24):
    label.config(font=(font_name, font_size))

font_selector = tk.StringVar(settings_window)
font_selector.set("MS Sans Serif")  # Fuente por defecto

size_selector = tk.IntVar(settings_window)
size_selector.set(24)  # Tamaño por defecto

font_menu = tk.OptionMenu(settings_window, font_selector, "Arial", "Courier", "Helvetica", "Fixedsys", "Terminal", "Modern", "Roman", "Script", "Courier", "MS Serif", "MS Sans Serif", "Small Fonts", "Marlett", "Arial", "Arabic Transparent", "Arial Baltic", "Arial CE", "Arial CYR", "Arial Greek", "Arial TUR", "Arial Black", "Bahnschrift Light", "Bahnschrift SemiLight", "Bahnschrift", "Bahnschrift SemiBold", "Bahnschrift Light SemiCondensed", "Bahnschrift SemiLight SemiConde", "Bahnschrift SemiCondensed", "Bahnschrift SemiBold SemiConden", "Bahnschrift Light Condensed", "Bahnschrift SemiLight Condensed", "Bahnschrift Condensed", "Bahnschrift SemiBold Condensed", "Calibri", "Calibri Light", "Cambria", "Cambria Math", "Candara", "Candara Light", "Comic Sans MS", "Consolas", "Constantia", "Corbel", "Corbel Light", "Courier New", "Courier New Baltic", "Courier New CE", "Courier New CYR", "Courier New Greek", "Courier New TUR", "Ebrima", "Franklin Gothic Medium", "Gabriola", "Gadugi", "Georgia", "Impact", "Ink Free", "Javanese Text", "Leelawadee UI", "Leelawadee UI Semilight", "Lucida Console", "Lucida Sans Unicode", "Malgun Gothic", "@Malgun Gothic", "Malgun Gothic Semilight", "@Malgun Gothic Semilight", "Microsoft Himalaya", "Microsoft JhengHei", "@Microsoft JhengHei", "Microsoft JhengHei UI", "@Microsoft JhengHei UI", "Microsoft JhengHei Light", "@Microsoft JhengHei Light", "Microsoft JhengHei UI Light", "@Microsoft JhengHei UI Light", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif", "Microsoft Tai Le", "Microsoft YaHei", "@Microsoft YaHei", "Microsoft YaHei UI", "@Microsoft YaHei UI", "Microsoft YaHei Light", "@Microsoft YaHei Light", "Microsoft YaHei UI Light", "@Microsoft YaHei UI Light", "Microsoft Yi Baiti", "MingLiU-ExtB", "@MingLiU-ExtB", "PMingLiU-ExtB", "@PMingLiU-ExtB", "MingLiU_HKSCS-ExtB", "@MingLiU_HKSCS-ExtB", "Mongolian Baiti", "MS Gothic", "@MS Gothic", "MS UI Gothic", "@MS UI Gothic", "MS PGothic", "@MS PGothic", "MV Boli", "Myanmar Text", "Nirmala UI", "Nirmala UI Semilight", "Palatino Linotype", "Sans Serif Collection", "Segoe Fluent Icons", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script", "Segoe UI", "Segoe UI Black", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Semilight", "Segoe UI Symbol", "Segoe UI Variable Small Light", "Segoe UI Variable Small Semilig", "Segoe UI Variable Small", "Segoe UI Variable Small Semibol", "Segoe UI Variable Text Light", "Segoe UI Variable Text Semiligh", "Segoe UI Variable Text", "Segoe UI Variable Text Semibold", "Segoe UI Variable Display Light", "Segoe UI Variable Display Semil", "Segoe UI Variable Display", "Segoe UI Variable Display Semib", "SimSun", "@SimSun", "NSimSun", "@NSimSun", "SimSun-ExtB", "@SimSun-ExtB", "Sitka Small", "Sitka Small Semibold", "Sitka Text", "Sitka Text Semibold", "Sitka Subheading", "Sitka Subheading Semibold", "Sitka Heading", "Sitka Heading Semibold", "Sitka Display", "Sitka Display Semibold", "Sitka Banner", "Sitka Banner Semibold", "Sylfaen", "Symbol", "Tahoma", "Times New Roman", "Times New Roman Baltic", "Times New Roman CE", "Times New Roman CYR", "Times New Roman Greek", "Times New Roman TUR", "Trebuchet MS", "Verdana", "Webdings", "Wingdings", "Yu Gothic", "@Yu Gothic", "Yu Gothic UI", "@Yu Gothic UI", "Yu Gothic UI Semibold", "@Yu Gothic UI Semibold", "Yu Gothic Light", "@Yu Gothic Light", "Yu Gothic UI Light", "@Yu Gothic UI Light", "Yu Gothic Medium", "@Yu Gothic Medium", "Yu Gothic UI Semilight", "@Yu Gothic UI Semilight", "HoloLens MDL2 Assets", "Agency FB", "Algerian", "Book Antiqua", "Arial Narrow", "Arial Rounded MT Bold", "Baskerville Old Face", "Bauhaus 93", "Bell MT", "Bernard MT Condensed", "Bodoni MT", "Bodoni MT Black", "Bodoni MT Condensed", "Bodoni MT Poster Compressed", "Bookman Old Style", "Bradley Hand ITC", "Britannic Bold", "Berlin Sans FB", "Berlin Sans FB Demi", "Broadway", "Brush Script MT", "Bookshelf Symbol 7", "Californian FB", "Calisto MT", "Castellar", "Century Schoolbook", "Centaur", "Century", "Chiller", "Colonna MT", "Cooper Black", "Copperplate Gothic Bold", "Copperplate Gothic Light", "Curlz MT", "Dubai", "Dubai Light", "Dubai Medium", "Elephant", "Engravers MT", "Eras Bold ITC", "Eras Demi ITC", "Eras Light ITC", "Eras Medium ITC", "Felix Titling", "Forte", "Franklin Gothic Book", "Franklin Gothic Demi", "Franklin Gothic Demi Cond", "Franklin Gothic Heavy", "Franklin Gothic Medium Cond", "Freestyle Script", "French Script MT", "Footlight MT Light", "Garamond", "Gigi", "Gill Sans MT", "Gill Sans MT Condensed", "Gill Sans Ultra Bold Condensed", "Gill Sans Ultra Bold", "Gloucester MT Extra Condensed", "Gill Sans MT Ext Condensed Bold", "Century Gothic", "Goudy Old Style", "Goudy Stout", "Harlow Solid Italic", "Harrington", "Haettenschweiler", "High Tower Text", "Imprint MT Shadow", "Informal Roman", "Blackadder ITC", "Edwardian Script ITC", "Kristen ITC", "Jokerman", "Juice ITC", "Kunstler Script", "Wide Latin", "Lucida Bright", "Lucida Calligraphy", "Leelawadee", "Lucida Fax", "Lucida Handwriting", "Lucida Sans", "Lucida Sans Typewriter", "Magneto", "Maiandra GD", "Matura MT Script Capitals", "Mistral", "Modern No. 20", "Microsoft Uighur", "Monotype Corsiva", "MT Extra", "Niagara Engraved", "Niagara Solid", "OCR A Extended", "Old English Text MT", "Onyx", "MS Outlook", "Palace Script MT", "Papyrus", "Parchment", "Perpetua", "Perpetua Titling MT", "Playbill", "Poor Richard", "Pristina", "Rage Italic", "Ravie", "MS Reference Sans Serif", "MS Reference Specialty", "Rockwell Condensed", "Rockwell", "Rockwell Extra Bold", "Script MT Bold", "Showcard Gothic", "Snap ITC", "Stencil", "Tw Cen MT", command=lambda f: set_font(f, size_selector.get()))
font_menu.pack()

size_menu = tk.OptionMenu(settings_window, size_selector, 12, 24, 36, 48, 60, command=lambda s: set_font(font_selector.get(), s))
size_menu.pack()

# Botón de pausa
pause_button = tk.Button(settings_window, text="Pausar/Reanudar", command=pause_timer)
pause_button.pack()

# Minimizar la configuración a la bandeja y comenzar el cronómetro
minimize_to_tray()

# Atajos de teclado para iniciar/detener y pausar/reanudar
keyboard.add_hotkey(key_combination_start_stop, toggle_timer)
keyboard.add_hotkey(key_combination_pause, pause_timer)

# Ejecuta la interfaz
settings_window.withdraw()  # Oculta la ventana de configuración inicialmente
overlay.mainloop()
