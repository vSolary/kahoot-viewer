import requests
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Design Tokens (Premium Palette)
BG_COLOR = get_color_from_hex("#0f172a")
ACCENT_BLUE = get_color_from_hex("#3b82f6")
ACCENT_GREEN = get_color_from_hex("#10b981")
TEXT_WHITE = (1, 1, 1, 1)

Window.clearcolor = BG_COLOR

# --- CONFIGURAZIONE ---
# DOPO che hai caricato 'index.html' su GitHub, metti il tuo link qui:
BASE_WEB_URL = "https://vSolary.github.io/kahoot-viewer/"

class KahootMasterApp(App):
    def build(self):
        self.title = "Kahoot! Global Master"
        
        root = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Header
        root.add_widget(Label(
            text="Kahoot! Global Master",
            font_size='28sp',
            bold=True,
            size_hint_y=None, height=60,
            color=ACCENT_BLUE
        ))
        
        # Search Area
        search_box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=120)
        
        self.search_input = TextInput(
            hint_text="Titolo del Quiz...",
            multiline=False,
            size_hint_y=None, height=55,
            padding=[15, 15],
            background_color=(0.15, 0.2, 0.3, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=ACCENT_BLUE,
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        search_box.add_widget(self.search_input)
        
        search_btn = Button(
            text="CERCA NEL DATABASE",
            bold=True,
            size_hint_y=None, height=60,
            background_normal='',
            background_color=ACCENT_BLUE
        )
        search_btn.bind(on_press=self.search_database)
        search_box.add_widget(search_btn)
        
        root.add_widget(search_box)
        
        # Results
        self.results_layout = GridLayout(cols=1, spacing=15, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll.add_widget(self.results_layout)
        
        root.add_widget(scroll)
        
        return root

    def search_database(self, instance):
        query = self.search_input.text
        if not query: return
        
        self.results_layout.clear_widgets()
        self.results_layout.add_widget(Label(text="Interrogazione API globale...", size_hint_y=None, height=50))
        
        try:
            url = f"https://create.kahoot.it/rest/kahoots/?query={query}&limit=15"
            r = requests.get(url, timeout=10)
            data = r.json()
            entities = data.get('entities', [])
            
            self.results_layout.clear_widgets()
            
            if not entities:
                self.results_layout.add_widget(Label(text="Nessun quiz pubblico trovato.", color=(1,0,0,1)))
                return
            
            for item in entities:
                card = item.get('card', item)
                title = card.get('title', 'Unknown')
                uuid = card.get('uuid')
                
                # Card Layout for each result
                item_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=130, padding=10)
                
                # Title Label
                item_layout.add_widget(Label(
                    text=title,
                    bold=True,
                    halign='left',
                    size_hint_y=None, height=40,
                    text_size=(Window.width - 80, None)
                ))
                
                # Action Buttons
                btn_row = BoxLayout(spacing=10, size_hint_y=None, height=50)
                
                # Button: Vedi qui
                v_btn = Button(
                    text="Apri sul PC",
                    background_color=(0.2, 0.2, 0.2, 1)
                )
                v_btn.bind(on_press=lambda inst, u=uuid: self.open_link(u))
                
                # Button: Genera Link
                g_btn = Button(
                    text="Genera Link Web",
                    background_color=ACCENT_GREEN,
                    bold=True
                )
                g_btn.bind(on_press=lambda inst, u=uuid, t=title: self.share_link(u, t))
                
                btn_row.add_widget(v_btn)
                btn_row.add_widget(g_btn)
                item_layout.add_widget(btn_row)
                
                # Separator line
                self.results_layout.add_widget(item_layout)

        except Exception as e:
            self.results_layout.add_widget(Label(text=f"Errore: {e}", color=(1,0,0,1)))

    def open_link(self, uuid):
        # Apre direttamente nel browser del PC
        webbrowser.open(f"https://create.kahoot.it/details/{uuid}")

    def share_link(self, uuid, title):
        # Genera il link per il viewer universale
        final_url = f"{BASE_WEB_URL}?uuid={uuid}"
        
        # Mostra il link in un "finto" popup (label)
        self.results_layout.clear_widgets()
        self.results_layout.add_widget(Label(
            text=f"LINK COPIABILE:\n\n{final_url}",
            color=ACCENT_GREEN,
            bold=True,
            font_size='14sp',
            halign='center'
        ))
        
        # Copia negli appunti (se possibile su Android, altrimenti stampiamo)
        print(f"LINK GENERATO per {title}: {final_url}")
        
        restart_btn = Button(text="TORNA ALLA RICERCA", size_hint_y=None, height=50)
        restart_btn.bind(on_press=self.search_database)
        self.results_layout.add_widget(restart_btn)

if __name__ == '__main__':
    KahootMasterApp().run()
