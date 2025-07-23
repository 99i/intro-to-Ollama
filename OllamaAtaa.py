import flet as ft
import pandas as pd
import ollama


DB_FILE = 'Rooms.csv'
OLLAMA_MODEL = "HotelAssistant2" 

def get_ollama_response(user_query: str):
    df = pd.read_csv(DB_FILE)
    prompt = f" بيانات الغرف التي قد تحتاجها: {df.to_string(index=False)}\nطلب: {user_query}"
    
    response = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, stream=False)
    
    return response['response']


def main(page: ft.Page):
    page.title = "مساعد فندق العطاء"
    page.vertical_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 700
    page.window.height = 800
    page.window.resizable = False
    page.rtl = True

    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True, padding=10)
    new_message = ft.TextField(hint_text="اكتب هنا...", expand=True)

    def send_message(e):
        user_text = new_message.value
        if not user_text:
            return
            
        chat.controls.append(ft.Text(f"أنت: \n{user_text}", weight="bold"))
        new_message.value = ""
        
        loading_indicator = ft.Row([ft.ProgressRing(width=16, height=16, stroke_width=2)], alignment=ft.MainAxisAlignment.CENTER)
        chat.controls.append(loading_indicator)
        page.update()

        response_text = get_ollama_response(user_text)
        chat.controls.remove(loading_indicator)
        chat.controls.append(ft.Text(f"المساعد: \n {response_text}"))
        page.update()

    new_message.on_submit = send_message

    page.add(
        ft.Container(content=chat,border=ft.border.all(1, "#444444"),border_radius=10,padding=10,expand=True,margin=10,)
        ,
        ft.Row(controls=[new_message,ft.IconButton(icon="send_rounded",tooltip="إرسال",on_click=send_message,icon_color="#FFD700"),]
        ,alignment=ft.MainAxisAlignment.CENTER,spacing=10,))

if __name__ == "__main__":
    ft.app(target=main)
