from pypresence import Presence
import asyncio
import time

rpc = None
running = False

def toggle_discord_presence(client_id, large_image, large_text, details, state, button_label_1, button_url_1, button, close_app=False):
    global rpc, running

    if close_app:
        try:
            if rpc:
                rpc.close()
                print("Conexión RPC cerrada.")
            # Detener el bucle de eventos de asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.stop()
            return True  # Indicar que el cierre fue exitoso
        except Exception as e:
            print(f"Error al cerrar la conexión RPC: {e}")
            return False  # Indicar que hubo un error

    if not running:  # Si no está activo, iniciar el estado
        if not client_id or not large_image or not details or not state:
            print("Error: Todos los campos obligatorios deben estar completos.")
            return

        try:
            rpc = Presence(client_id)
            rpc.connect()
            print("Conectado a Discord.")

            rpc.update(
                large_image=large_image,
                large_text=large_text,
                details=details,
                start=int(time.time()),
                state=state,
                buttons=[{"label": button_label_1, "url": button_url_1}] if button_label_1 and button_url_1 else None
            )

            button.config(text="Is running", bg="#B22D4A", activebackground="#7A1F37")
            running = True
        except Exception as e:
            print(f"No se pudo conectar a Discord: {e}")
    else:  # Si ya está activo, detener el estado
        try:
            if rpc:
                rpc.close()
                rpc = None
                print("Desconectado de Discord.")
            button.config(text="Update status", bg="#E03657", activebackground="#9F3657")
            running = False
        except Exception as e:
            print(f"Error al desconectar de Discord: {e}")