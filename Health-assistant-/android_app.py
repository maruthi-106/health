from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock
from datetime import datetime
import json
import os
import google.generativeai as genai
import pandas as pd

# Configure Gemini API
genai.configure(api_key="AIzaSyAdl8m1ff3j1xMQtWjiLGkgNKfXJ5X6JF4")
model = genai.GenerativeModel('gemini-1.5-flash')

# Constants
SERIOUS_SYMPTOMS = [
    "high fever", "chest pain", "difficulty breathing", "severe pain",
    "unconsciousness", "severe bleeding", "stroke", "heart attack"
]

SEASONAL_DISEASES = {
    "Flu": {
        "symptoms": "Fever, cough, sore throat, body aches, fatigue",
        "first_aid": "Rest, stay hydrated, over-the-counter fever reducers",
        "precautions": "Annual flu shot, frequent hand washing, avoid close contact with sick people"
    },
    "Dengue": {
        "symptoms": "High fever, severe headache, joint pain, rash",
        "first_aid": "Rest, stay hydrated, avoid aspirin",
        "precautions": "Use mosquito repellent, eliminate standing water, wear protective clothing"
    },
    "Common Cold": {
        "symptoms": "Runny nose, sore throat, cough, congestion",
        "first_aid": "Rest, stay hydrated, over-the-counter cold medicine",
        "precautions": "Wash hands frequently, avoid close contact with sick people"
    },
    "Allergic Rhinitis": {
        "symptoms": "Sneezing, runny nose, itchy eyes, nasal congestion",
        "first_aid": "Antihistamines, nasal sprays, eye drops",
        "precautions": "Avoid allergens, use air purifiers, keep windows closed during high pollen times"
    },
    "Food Poisoning": {
        "symptoms": "Nausea, vomiting, diarrhea, abdominal pain",
        "first_aid": "Stay hydrated, rest, avoid solid foods initially",
        "precautions": "Practice food safety, wash hands before eating, avoid undercooked food"
    }
}

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Hospital Health Assistant',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        # Login form
        form = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        
        self.username = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        self.password = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        login_btn = Button(
            text='Login',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        login_btn.bind(on_press=self.login)
        
        register_btn = Button(
            text='Register',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.8, 0, 1)
        )
        register_btn.bind(on_press=self.go_to_register)
        
        form.add_widget(self.username)
        form.add_widget(self.password)
        form.add_widget(login_btn)
        form.add_widget(register_btn)
        
        layout.add_widget(title)
        layout.add_widget(form)
        self.add_widget(layout)
    
    def login(self, instance):
        # Load users from file
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
                
            username = self.username.text
            password = self.password.text
            
            if username in users and users[username]['password'] == password:
                App.get_running_app().current_user = username
                self.manager.current = 'main'
            else:
                self.show_error('Invalid username or password')
        else:
            self.show_error('No users found. Please register first.')
    
    def go_to_register(self, instance):
        self.manager.current = 'register'
    
    def show_error(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='New Patient Registration',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        # Registration form
        form = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=400)
        
        self.username = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        self.password = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40
        )
        
        self.age = TextInput(
            hint_text='Age',
            multiline=False,
            input_filter='int',
            size_hint_y=None,
            height=40
        )
        
        self.sex = Spinner(
            text='Select Sex',
            values=('Male', 'Female', 'Other'),
            size_hint_y=None,
            height=40
        )
        
        self.weight = TextInput(
            hint_text='Weight (kg)',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=40
        )
        
        self.height = TextInput(
            hint_text='Height (cm)',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=40
        )
        
        register_btn = Button(
            text='Register',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.8, 0, 1)
        )
        register_btn.bind(on_press=self.register)
        
        back_btn = Button(
            text='Back to Login',
            size_hint_y=None,
            height=40,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        back_btn.bind(on_press=self.go_to_login)
        
        form.add_widget(self.username)
        form.add_widget(self.password)
        form.add_widget(self.age)
        form.add_widget(self.sex)
        form.add_widget(self.weight)
        form.add_widget(self.height)
        form.add_widget(register_btn)
        form.add_widget(back_btn)
        
        layout.add_widget(title)
        layout.add_widget(form)
        self.add_widget(layout)
    
    def register(self, instance):
        username = self.username.text
        password = self.password.text
        age = self.age.text
        sex = self.sex.text
        weight = self.weight.text
        height = self.height.text
        
        if not all([username, password, age, sex]):
            self.show_error('Please fill in all required fields')
            return
        
        # Load existing users
        users = {}
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)
        
        if username in users:
            self.show_error('Username already exists')
            return
        
        # Add new user
        users[username] = {
            'password': password,
            'age': int(age),
            'sex': sex,
            'weight': float(weight) if weight else None,
            'height': float(height) if height else None,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save users
        with open('users.json', 'w') as f:
            json.dump(users, f)
        
        self.show_success('Registration successful! Please login.')
        Clock.schedule_once(lambda dt: self.go_to_login(None), 2)
    
    def go_to_login(self, instance):
        self.manager.current = 'login'
    
    def show_error(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
    
    def show_success(self, message):
        popup = Popup(
            title='Success',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        title = Label(
            text='Hospital Health Assistant',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        user_info = Label(
            text='',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        header.add_widget(title)
        header.add_widget(user_info)
        
        # Navigation buttons
        nav = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        
        log_symptoms_btn = Button(
            text='Log Symptoms',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        log_symptoms_btn.bind(on_press=self.go_to_log_symptoms)
        
        view_log_btn = Button(
            text='View Health Log',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        view_log_btn.bind(on_press=self.go_to_view_log)
        
        advice_btn = Button(
            text='Get Health Advice',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        advice_btn.bind(on_press=self.go_to_advice)
        
        diseases_btn = Button(
            text='Seasonal Diseases',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        diseases_btn.bind(on_press=self.go_to_diseases)
        
        logout_btn = Button(
            text='Logout',
            size_hint_y=None,
            height=40,
            background_color=(1, 0, 0, 1)
        )
        logout_btn.bind(on_press=self.logout)
        
        nav.add_widget(log_symptoms_btn)
        nav.add_widget(view_log_btn)
        nav.add_widget(advice_btn)
        nav.add_widget(diseases_btn)
        nav.add_widget(logout_btn)
        
        self.layout.add_widget(header)
        self.layout.add_widget(nav)
        self.add_widget(self.layout)
        
        # Store references
        self.user_info_label = user_info
    
    def on_enter(self):
        # Update user info when screen is entered
        if hasattr(App.get_running_app(), 'current_user'):
            username = App.get_running_app().current_user
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    users = json.load(f)
                    user_data = users[username]
                    info_text = f'Welcome, {username}\n'
                    info_text += f'Age: {user_data["age"]} | Sex: {user_data["sex"]}'
                    if user_data["weight"]:
                        info_text += f' | Weight: {user_data["weight"]}kg'
                    if user_data["height"]:
                        info_text += f' | Height: {user_data["height"]}cm'
                    self.user_info_label.text = info_text
    
    def go_to_log_symptoms(self, instance):
        self.manager.current = 'log_symptoms'
    
    def go_to_view_log(self, instance):
        self.manager.current = 'view_log'
    
    def go_to_advice(self, instance):
        self.manager.current = 'advice'
    
    def go_to_diseases(self, instance):
        self.manager.current = 'diseases'
    
    def logout(self, instance):
        App.get_running_app().current_user = None
        self.manager.current = 'login'

class LogSymptomsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Log Symptoms',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        # Form
        form = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=400)
        
        self.symptoms = TextInput(
            hint_text='Describe your symptoms',
            multiline=True,
            size_hint_y=None,
            height=200
        )
        
        analyze_btn = Button(
            text='Analyze Symptoms',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        analyze_btn.bind(on_press=self.analyze_symptoms)
        
        back_btn = Button(
            text='Back to Main Menu',
            size_hint_y=None,
            height=40,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        form.add_widget(self.symptoms)
        form.add_widget(analyze_btn)
        form.add_widget(back_btn)
        
        layout.add_widget(title)
        layout.add_widget(form)
        self.add_widget(layout)
    
    def analyze_symptoms(self, instance):
        symptoms = self.symptoms.text
        if not symptoms.strip():
            self.show_error('Please enter your symptoms')
            return
        
        # Get user info
        username = App.get_running_app().current_user
        with open('users.json', 'r') as f:
            users = json.load(f)
            user_info = users[username]
        
        # Analyze symptoms
        age = user_info['age']
        sex = user_info['sex']
        age_group = "child" if age < 18 else "adult" if age < 65 else "elderly"
        
        prompt = f"""As a medical assistant, analyze these symptoms for a {age_group} {sex.lower()} patient aged {age} years and provide:
        1. Possible conditions (considering age and sex-specific factors)
        2. Home remedies (appropriate for the patient's age group)
        3. When to seek medical attention
        4. Age and sex-specific recommendations
        
        Patient Information:
        - Age: {age} years
        - Sex: {sex}
        - Age Group: {age_group}
        
        Symptoms: {symptoms}
        
        Keep the response concise and focused on immediate actions."""
        
        try:
            response = model.generate_content(prompt)
            analysis = response.text
            
            # Log the entry
            log_entry = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'username': username,
                'symptoms': symptoms,
                'analysis': analysis,
                'age_at_log': age,
                'sex_at_log': sex
            }
            
            # Load existing logs
            logs = []
            if os.path.exists('health_log.csv'):
                df = pd.read_csv('health_log.csv')
                logs = df.to_dict('records')
            
            # Add new log
            logs.append(log_entry)
            
            # Save logs
            df = pd.DataFrame(logs)
            df.to_csv('health_log.csv', index=False)
            
            # Show analysis
            self.show_analysis(analysis)
            
        except Exception as e:
            self.show_error(f'Error analyzing symptoms: {str(e)}')
    
    def show_analysis(self, analysis):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=analysis, text_size=(Window.width - 100, None)))
        
        popup = Popup(
            title='Analysis Results',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def show_error(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()
    
    def go_to_main(self, instance):
        self.manager.current = 'main'

class ViewLogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Health Log',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        # Log display
        self.log_display = Label(
            text='No health logs found.',
            text_size=(Window.width - 40, None),
            size_hint_y=None
        )
        
        # Back button
        back_btn = Button(
            text='Back to Main Menu',
            size_hint_y=None,
            height=40,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        layout.add_widget(title)
        layout.add_widget(self.log_display)
        layout.add_widget(back_btn)
        self.add_widget(layout)
    
    def on_enter(self):
        # Update log display when screen is entered
        if os.path.exists('health_log.csv'):
            df = pd.read_csv('health_log.csv')
            username = App.get_running_app().current_user
            user_logs = df[df['username'] == username]
            
            if not user_logs.empty:
                log_text = ''
                for _, log in user_logs.iterrows():
                    log_text += f"Date: {log['date']}\n"
                    log_text += f"Symptoms: {log['symptoms']}\n"
                    log_text += f"Analysis: {log['analysis']}\n"
                    log_text += '-' * 50 + '\n'
                self.log_display.text = log_text
            else:
                self.log_display.text = 'No health logs found.'
        else:
            self.log_display.text = 'No health logs found.'
    
    def go_to_main(self, instance):
        self.manager.current = 'main'

class AdviceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Health Advice',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        # Advice display
        self.advice_display = Label(
            text='Click the button below to get personalized health advice.',
            text_size=(Window.width - 40, None),
            size_hint_y=None
        )
        
        # Buttons
        get_advice_btn = Button(
            text='Get Health Advice',
            size_hint_y=None,
            height=40,
            background_color=(0, 0.7, 1, 1)
        )
        get_advice_btn.bind(on_press=self.get_advice)
        
        back_btn = Button(
            text='Back to Main Menu',
            size_hint_y=None,
            height=40,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        layout.add_widget(title)
        layout.add_widget(self.advice_display)
        layout.add_widget(get_advice_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)
    
    def get_advice(self, instance):
        if not os.path.exists('health_log.csv'):
            self.advice_display.text = 'No health history available for personalized advice.'
            return
        
        df = pd.read_csv('health_log.csv')
        username = App.get_running_app().current_user
        user_logs = df[df['username'] == username]
        
        if user_logs.empty:
            self.advice_display.text = 'No health history available for personalized advice.'
            return
        
        # Get user info
        with open('users.json', 'r') as f:
            users = json.load(f)
            user_info = users[username]
        
        age = user_info['age']
        sex = user_info['sex']
        age_group = "child" if age < 18 else "adult" if age < 65 else "elderly"
        
        # Get recent logs
        recent_logs = user_logs.tail(7)  # Last 7 entries
        symptoms_text = "\n".join(recent_logs['symptoms'].tolist())
        
        prompt = f"""Based on the patient's health history and demographics, provide personalized advice:
        
        Patient Information:
        - Age: {age} years
        - Sex: {sex}
        - Age Group: {age_group}
        
        Recent Symptoms (Last 7 Days):
        {symptoms_text}
        
        Please provide:
        1. Pattern Analysis: Identify any recurring symptoms or patterns
        2. Lifestyle Recommendations: Suggest age and sex-appropriate lifestyle changes
        3. Preventive Measures: Recommend preventive steps based on the patient's demographics
        4. Follow-up Actions: Suggest when to monitor or seek medical attention
        
        Keep the advice practical and focused on the specific symptoms shown."""
        
        try:
            response = model.generate_content(prompt)
            self.advice_display.text = response.text
        except Exception as e:
            self.advice_display.text = f'Error getting advice: {str(e)}'
    
    def go_to_main(self, instance):
        self.manager.current = 'main'

class DiseasesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Seasonal Diseases',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        # Diseases display
        scroll = ScrollView()
        diseases_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        diseases_layout.bind(minimum_height=diseases_layout.setter('height'))
        
        for disease, info in SEASONAL_DISEASES.items():
            disease_box = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=200)
            
            disease_title = Label(
                text=disease,
                size_hint_y=None,
                height=40,
                font_size='18sp',
                bold=True
            )
            
            symptoms = Label(
                text=f"Symptoms:\n{info['symptoms']}",
                size_hint_y=None,
                height=60,
                text_size=(Window.width - 40, None)
            )
            
            first_aid = Label(
                text=f"First Aid:\n{info['first_aid']}",
                size_hint_y=None,
                height=60,
                text_size=(Window.width - 40, None)
            )
            
            precautions = Label(
                text=f"Precautions:\n{info['precautions']}",
                size_hint_y=None,
                height=60,
                text_size=(Window.width - 40, None)
            )
            
            disease_box.add_widget(disease_title)
            disease_box.add_widget(symptoms)
            disease_box.add_widget(first_aid)
            disease_box.add_widget(precautions)
            
            diseases_layout.add_widget(disease_box)
        
        scroll.add_widget(diseases_layout)
        
        # Back button
        back_btn = Button(
            text='Back to Main Menu',
            size_hint_y=None,
            height=40,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(back_btn)
        self.add_widget(layout)
    
    def go_to_main(self, instance):
        self.manager.current = 'main'

class HealthAssistantApp(App):
    def build(self):
        # Set window size for testing
        Window.size = (400, 700)
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(LogSymptomsScreen(name='log_symptoms'))
        sm.add_widget(ViewLogScreen(name='view_log'))
        sm.add_widget(AdviceScreen(name='advice'))
        sm.add_widget(DiseasesScreen(name='diseases'))
        
        return sm

if __name__ == '__main__':
    HealthAssistantApp().run() 