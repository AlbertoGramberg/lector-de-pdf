import tkinter as tk
from tkinter import filedialog
import PyPDF2
import openai
import openai_secret_manager



# replace YOUR_API_KEY with your actual API key for the ChatGPT service
openai.api_key = "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"
# Authenticate with OpenAI's API
# Obtenemos las credenciales de OpenAI
# Authenticate with OpenAI's API
#openai.api_key = "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"
#secrets = openai_secret_manager.get_secret("openai")

# Now you can access your API key as follows:
#api_key = secrets["VbYhW2bmLpH06PnuLg2RT3BlbkFJIFmEKSQFs8gGtciJlJHM"]
# Global variables to store text to be sent to OpenAI
file_text = ""
# Función para abrir un archivo PDF y mostrar su contenido en la ventana
def open_file():
    global file_text
    # Pedimos al usuario que seleccione un archivo PDF
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        # Si se seleccionó un archivo, lo leemos con PyPDF2
        pdf_reader = PyPDF2.PdfReader(file_path)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            label = tk.Label(canvas, text=page_text, wraplength=800)
            canvas.create_window((0, page_num * 400), window=label, anchor="nw")
            file_text += page_text
        canvas.configure(scrollregion=canvas.bbox("all"))

# Función para copiar el texto mostrado en la ventana al portapapeles
def copy_text():
    text = ""
    # Recorremos todos los widgets en la ventana y copiamos el texto de las etiquetas (labels)
    for child in canvas.winfo_children():
        if isinstance(child, tk.Label):
            text += child.cget("text") + "\n"
    # Limpiamos el portapapeles y copiamos el texto
    root.clipboard_clear()
    root.clipboard_append(text)

# Función para generar una respuesta de OpenAI en función del texto mostrado en la ventana
# Función para generar una respuesta de OpenAI en función del texto mostrado en la ventana
def chat():
    global file_text
    prompt = input("Ingresa tu consulta: ")
    text_to_promp = prompt + "\n" + file_text 

    # Enviamos una consulta a OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text_to_promp,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=10,
    )
    # Obtenemos la respuesta de OpenAI y la mostramos en la ventana
    message = response.choices[0].text.strip()
    # Creamos una ventana emergente para mostrar la respuesta
    popup = tk.Toplevel(root)
    popup.title("OpenAI Response")
    label = tk.Label(popup, text=message, wraplength=800)
    label.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    ok_button = tk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack(side="bottom", pady=10)

# Creamos la ventana principal y la configuramos

root = tk.Tk()
root.title("Lector PDF")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

open_file_button = tk.Button(root, text="Abrir archivo", command=open_file)
open_file_button.pack(side="left")

copy_text_button = tk.Button(root, text="Copiar texto", command=copy_text)
copy_text_button.pack(side="left")

chat_button = tk.Button(root, text="Chat", command=chat)
chat_button.pack(side="left")

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

root.mainloop()
