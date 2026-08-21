import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class LiveSportsApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Header
        self.layout.add_widget(Label(text="[b]Live Premier League Predictor[/b]", markup=True, font_size='20sp'))

        # API Key Input
        self.layout.add_widget(Label(text="Enter your football-data.org API Key:"))
        self.api_input = TextInput(hint_text="Paste API key here", multiline=False, font_size='14sp', size_hint_y=None, height=40)
        self.layout.add_widget(self.api_input)

        # Fetch Button
        self.fetch_btn = Button(
            text="Fetch Upcoming Matches", 
            font_size='16sp', 
            background_color=(0, 0.6, 1, 1), 
            size_hint_y=None, 
            height=45
        )
        self.fetch_btn.bind(on_press=self.get_live_matches)
        self.layout.add_widget(self.fetch_btn)

        # Output Area
        self.result_label = Label(
            text="Tap 'Fetch' to load matches live from API", 
            font_size='14sp',
            size_hint_y=None,
            height=300
        )
        
        # Scroll View for long data
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_label)
        self.layout.add_widget(scroll)

        return self.layout

    def get_live_matches(self, instance):
        api_key = self.api_input.text.strip()
        if not api_key:
            self.result_label.text = "Please enter a valid API Key first!"
            return

        self.result_label.text = "Connecting to API... Please wait."
        
        # Endpoint for Premier League
        url = "https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED"
        headers = {"X-Auth-Token": api_key}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])[:5] # Get top 5 matches
                
                output = "--- UPCOMING FIXTURES ---\n\n"
                for m in matches:
                    home = m["homeTeam"]["name"]
                    away = m["awayTeam"]["name"]
                    date = m["utcDate"][:10]
                    output += f"• {home} vs {away}\n  Date: {date}\n\n"
                
                self.result_label.text = output if matches else "No scheduled matches found."
            else:
                self.result_label.text = f"API Error {response.status_code}: Check your key."
        except Exception as e:
            self.result_label.text = f"Connection failed: {str(e)}"

if __name__ == '__main__':
    LiveSportsApp().run()
  
