import string

from elevenlabs import generate, set_api_key, voices, save, Voice, VoiceSettings, clone
import os
from tkinter import *
from tkinter import messagebox as MessageBox, filedialog
import speech_recognition as sr
import time
from translate import Translator


# Key de la Api
apiKey = os.environ["API_KEY"]
set_api_key(apiKey)

""""""""" Obtener voces de la Api """""""""

def getDataVoices(voices):
    listaVoces = []
    for e in voices:
        dicc = {}
        dicc['voice_id'] = e.voice_id
        dicc['name'] = e.name
        dicc['gender'] = e.labels['gender']
        listaVoces.append(dicc)
    return listaVoces

voices = voices()
listaVoces = getDataVoices(voices)



""""""""" Descarga """""""""

contadorDescargas = 0

# Texto a Voz
def convertirTextoAVoz():
    global contadorDescargas
    voz = variable.get().split(' ')[0]
    voz_id = "ApGf6eGyktwLXILoQaYJ"
    for e in listaVoces:
        if voz in e['name']:
            voz_id = e['voice_id']
            print("Match voice: " + e['voice_id'])
    audio = generate(
        text=texto.get(),
        voice=Voice(
            voice_id=voz_id,
            settings=VoiceSettings(speaking_rate=0.9,stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2",
    )
    save(audio, f"output_{contadorDescargas}.wav")
    contadorDescargas += 1
    MessageBox.showinfo('Descarga',
                        'Se a descargado con exito.')

# Voz a Voz

pathAudio = ""
def convertirVozAVoz():
    print(pathAudio)
    r = sr.Recognizer()
    with sr.AudioFile(pathAudio) as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='es-ES')
            time.sleep(1.5)
            guardarVozNueva(text)
            print(text)
        except:
            print("No entiendo")

def guardarVozNueva(text):
    global contadorDescargas
    voz = variable.get().split(' ')[0]
    voz_id = "ApGf6eGyktwLXILoQaYJ"
    for e in listaVoces:
        if voz in e['name']:
            voz_id = e['voice_id']
            print("Match voice: " + e['voice_id'])
    audio = generate(
        text=text,
        voice=Voice(
            voice_id=voz_id,
            settings=VoiceSettings(speaking_rate=0.9,stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        ),
        model="eleven_multilingual_v2",
    )
    save(audio, f"output_{contadorDescargas}.wav")
    contadorDescargas += 1
    MessageBox.showinfo('Descarga',
                        'Se a descargado con exito.')

def abrirSelectorArchivo():
    global pathAudio
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Archivo seleccionado:", file_path)
        pathAudio = file_path

def desplegarInformacion():
    MessageBox.showinfo('Sobre mí', 'Enlace a mi perfil de LinkedIn: https://www.linkedin.com/in/ignacio-villarreal-518804267/')

def traducirAIngles():
    text = texto.get()
    print("Texto original:", repr(text))
    text_sin_puntuacion = text.translate(str.maketrans('', '', string.punctuation))
    translator = Translator(from_lang='spanish', to_lang='english', encoding='utf-8')
    nuevoTexto = translator.translate(text_sin_puntuacion)
    print("Texto traducido:", repr(nuevoTexto))
    guardarVozNueva(nuevoTexto)


""""""""" Interfaz """""""""

# Cuadro principal
root = Tk()
root.title('Texto a audio.')

# Obtener tamaño de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular posición central
x_centro = (ancho_pantalla - 700) // 2
y_centro = (alto_pantalla - 500) // 2

# Establecer posición y tamaño de la ventana
root.geometry(f"700x500+{x_centro}+{y_centro}")

# Descripcion
custom_font = ("Helvetica", 14)
instrucciones = Label(root, text='Convierte texto a voz.\n\n- Puede ingresar un texto, seleccionar una voz y darle a convertir texto a voz.\n- Puede seleccionar un archivo, seleccionar una voz y darle a convertir voz a voz.\n- Puede ingresar un texto, seleccionar una voz y darle a convertir español a inglés.\n', font=custom_font)
instrucciones.grid(row=0, column=0, pady=20, columnspan=2)

# Input URL
texto = Entry(root, width=30, font=("Helvetica", 12))
texto.grid(row=1, column=0, pady=(0, 20), columnspan=2)

# Opciones de voz
# Variable para almacenar la selección
variable = StringVar(root)
variable.set(listaVoces[0]['name'])

# Crear el menú de opciones
opciones = [f"{dicc['name']} ({dicc['gender']})" for dicc in listaVoces]
menu_opciones = OptionMenu(root, variable, *opciones)
menu_opciones.grid(row=2, column=0, pady=10, columnspan=2)

boton = Button(root, text='Convertir Texto a Voz', command=convertirTextoAVoz)
boton.grid(row=3, column=0, pady=10, columnspan=2)

# Crear un botón que abrirá el selector de archivos
boton_selector = Button(root, text="Seleccionar Archivo", command=abrirSelectorArchivo)
boton_selector.grid(row=4, column=0, pady=10, columnspan=2)  # Cambiar el nombre de la variable aquí

# Convertir Voz a Voz
boton2 = Button(root, text='Convertir Voz a Voz', command=convertirVozAVoz)
boton2.grid(row=5, column=0, pady=10, columnspan=2)

# Convertir Español a Ingles
boton3 = Button(root, text='Convertir español a ingles', command=traducirAIngles)
boton3.grid(row=6, column=0, pady=10, columnspan=2)


# Centrar elementos verticalmente en la fila
for i in range(7):
    root.grid_rowconfigure(i, weight=1)

# Centrar elementos horizontalmente en la columna
for i in range(2):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()




'''
voice = clone(
   name = "My Cloned Voice",
   files = ["audioPrueba1.wav", "audioPrueba2.wav", "audioPrueba3.wav"]
)
audio = generate("Hello world!", voice=voice)
save(audio, "pruebaVozClonada.wav")
'''