# ventana.py
import tkinter as tk
from PIL import Image, ImageTk
from ds_bot import toggle_discord_presence
import asyncio

def cargar_logo(frame):
    try:
        # Cargar y mostrar el logo
        image_path = "assets/icon.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((100, 100))
        logo_image = ImageTk.PhotoImage(resized_image)
        logo_label = tk.Label(frame, image=logo_image, bg="#222222")
        logo_label.image = logo_image
        logo_label.pack()
    except Exception as e:
        print(f"No se pudo cargar el logo: {e}")
        tk.Label(frame, text="LOGO", font=("Arial", 24), bg="#222222", fg="white").pack()

def create_row(frame, row, label1, label2):
    tk.Label(frame, text=label1, bg="#222222", fg="white").grid(row=row, column=0, sticky="w", padx=10, pady=5)
    entry1 = tk.Entry(frame, width=30, bg="#333333", fg="white", insertbackground="white", selectbackground="#E03657")
    entry1.grid(row=row, column=1, padx=10, pady=5)

    tk.Label(frame, text=label2, bg="#222222", fg="white").grid(row=row, column=2, sticky="w", padx=10, pady=5)
    entry2 = tk.Entry(frame, width=30, bg="#333333", fg="white", insertbackground="white", selectbackground="#E03657")
    entry2.grid(row=row, column=3, padx=10, pady=5)

    return entry1, entry2

def iniciar_aplicacion():
    root = tk.Tk()
    root.title("Discord Rich Presence Configurator")
    root.geometry("650x400")
    root.configure(bg="#222222")
    root.resizable(False, False)

    try:
        root.iconbitmap("assets/icon2.ico")
    except Exception as e:
        print(f"No se pudo cargar el ícono: {e}")

    # Frame para el logo
    logo_frame = tk.Frame(root, bg="#222222")
    logo_frame.pack(pady=10)
    cargar_logo(logo_frame)

    # Frame para los inputs
    inputs_frame = tk.Frame(root, bg="#222222")
    inputs_frame.pack(expand=True, padx=20, pady=10)

    # Crear filas de inputs
    client_id_entry, large_image_entry = create_row(inputs_frame, 0, "Client ID:", "Large Image:")
    large_text_entry, details_entry = create_row(inputs_frame, 1, "Large Text:", "Details:")
    button_label_1_entry, button_url_1_entry = create_row(inputs_frame, 2, "Botón Label:", "Botón URL:")

    tk.Label(inputs_frame, text="State:", bg="#222222", fg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    state_entry = tk.Entry(inputs_frame, width=30, bg="#333333", fg="white", insertbackground="white", selectbackground="#E03657")
    state_entry.grid(row=3, column=1, padx=10, pady=5)

    # Frame para el botón
    button_frame = tk.Frame(root, bg="#222222")
    button_frame.pack(pady=20)

    update_button = tk.Button(
        button_frame,
        text="Actualizar Estado",
        command=lambda: validar_campos_y_actualizar(
            client_id_entry.get().strip(),
            large_image_entry.get().strip(),
            large_text_entry.get().strip(),
            details_entry.get().strip(),
            state_entry.get().strip(),
            button_label_1_entry.get().strip(),
            button_url_1_entry.get().strip(),
            update_button,
            error_label
        ),
        bg="#E03657",
        fg="white",
        activebackground="#9F3657",
        width=20,
        height=2
    )
    update_button.pack()

    # Label para mostrar mensajes de error
    error_label = tk.Label(button_frame, text="", fg="#9F3657", bg="#222222", font=("Arial", 10))
    error_label.pack(pady=5)

    # Función para validar los campos y actualizar el estado
    def validar_campos_y_actualizar(client_id, large_image, large_text, details, state, button_label_1, button_url_1, button, error_label):
        # Limpiar el mensaje de error
        error_label.config(text="")

        # Validar que los campos obligatorios estén completos
        if not client_id or not large_image or not details or not state:
            error_label.config(text="Todos los campos obligatorios deben estar completos.")
            return

        # Llamar a la función para actualizar Discord
        toggle_discord_presence(client_id, large_image, large_text, details, state, button_label_1, button_url_1, button)

    # Función para cerrar la ventana
    def on_closing():
        if toggle_discord_presence(None, None, None, None, None, None, None, update_button, close_app=True):
            # Detener el bucle de eventos de asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.stop()
            root.destroy()  # Solo cerrar la ventana si la conexión RPC se cerró correctamente

    # Asociar la función de cierre a la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()