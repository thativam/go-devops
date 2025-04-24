from nicegui import ui # type: ignore
import requests

API_BASE_URL = 'http://your-api.com/users'  # Replace with your real endpoint

user_list_container = None  # Placeholder for our list section

# --- Function to get users from API ---
def load_users():
    user_list_container.clear()
    try:
        response = requests.get(API_BASE_URL)
        if response.ok:
            users = response.json()
            for user in users:
                with user_list_container:
                    ui.label(f'{user["id"]}: {user["name"]}')
        else:
            with user_list_container:
                ui.label('⚠️ Failed to load users.')
    except Exception as e:
        with user_list_container:
            ui.label(f'⚠️ Error: {e}')

# --- Function to create user ---
def create_user(name_input):
    name = name_input.value.strip()
    if not name:
        ui.notify('Please enter a name')
        return

    try:
        response = requests.post(API_BASE_URL, json={'name': name})
        if response.ok:
            ui.notify('✅ User created')
            name_input.value = ''
            load_users()
        else:
            ui.notify('❌ Failed to create user')
    except Exception as e:
        ui.notify(f'❌ Error: {e}')

# --- UI Layout ---
ui.label('👥 User List').classes('text-2xl font-bold')

user_list_container = ui.column()
load_users()

ui.separator()

ui.label('➕ Create New User').classes('text-xl')
name_input = ui.input('Name')
ui.button('Create', on_click=lambda: create_user(name_input))

ui.run(port=5000)
