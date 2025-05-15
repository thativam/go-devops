from nicegui import ui  # type: ignore
import requests
import os as OS

css = """
main {
    align-content: center;
}
body {
    background-color: #f8fafc;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;  /* Adicione esta linha */
}

.container {
    max-width: 900px; 
    min-width: 400px;
    min-height: 500px;  
    max-height: 90vh;
    width: 90%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: auto;
    padding: 2.5rem;
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.07);
    overflow: hidden;
}

.header {
    font-size: 2rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2rem;
    text-align: center;
    letter-spacing: -0.025em;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-title::before {
    content: "";
    display: block;
    width: 6px;
    height: 1.2rem;
    background: #3b82f6;
    border-radius: 3px;
}

.input-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    width: 100%;
}

.input-field {
    flex-grow: 1;
    padding: 0.875rem 1.25rem;
    font-size: 1rem;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    transition: all 0.2s ease;
}

.input-field:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
    outline: none;
}

.btn {
    background: #3b82f6;
    color: #ffffff;
    padding: 0.875rem 2rem;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    box-shadow: 0 4px 6px rgba(59, 130, 246, 0.15);
    margin-left: auto;
}

.btn:hover {
    background: #2563eb;
    transform: translateY(-1px);
    box-shadow: 0 6px 12px rgba(59, 130, 246, 0.2);
}

.user-list {
    background-color: #f8fafc;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    min-height: 120px;
    max-height: 250px;
    overflow-y: auto;
    border: 1px dashed #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}

.empty-state {
    color: #64748b;
    text-align: center;
    padding: 2rem 0;
    font-size: 0.95rem;
    width: 100%;
}

.user-entry {
    background-color: #ffffff;
    border: 1px solid #f1f5f9;
    padding: 1rem 1.25rem;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
    width: 100%;
}

.user-entry:hover {
    border-color: #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.user-name {
    font-weight: 600;
    color: #0f172a;
}

.user-id {
    font-size: 0.875rem;
    color: #64748b;
    background: #f1f5f9;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
}

.error-message {
    background-color: #fee2e2;
    color: #b91c1c;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    font-weight: 500;
    margin: 1rem 0;
    width: 100%;
    box-sizing: border-box;
}
"""


class rest_api():
    def __init__(self):
        api_host = OS.getenv('API_HOST', 'localhost')
        api_port = OS.getenv('API_PORT', '8080')
        self.api_base_url = f'http://{api_host}:{api_port}'
        self.users_base_api = f'{self.api_base_url}/users'
        print(f'API Hosted: {self.api_base_url}')

    def get_api_base_url(self):
        return self.api_base_url

    def get_users(self):
        response = requests.get(self.users_base_api)
        if not response.ok:
            raise Exception(f"Failed to fetch users: {response.status_code}")
        users = response.json()
        print(users)
        return users

    def create_user(self, json_name):
        response = requests.post(self.users_base_api, json=json_name)
        if not response.ok:
            raise Exception(f"Failed to create user: {response.status_code}")
        user = response.json()
        return user


class apiMock():
    users = [
        {'id': 1, 'name': 'John Doe'},
        {'id': 2, 'name': 'Jane Smith'},
        {'id': 3, 'name': 'Alice Johnson'},
    ]

    def __init__(self):
        self.api_base_url = ''

    def get_users(self):
        print(self.users)
        return self.users

    def create_user(self, json_name):
        name = json_name['name']
        if not name:
            raise ValueError("Name cannot be empty")
        new_user = {'id': len(self.users) + 1, 'name': name}
        self.users.append(new_user)
        return new_user


class Frontend():
    def __init__(self, api, port):
        self.api = api
        self.user_list_container = None
        self.port = port

    def load_users(self):
        self.user_list_container.clear()
        try:
            users = self.api.get_users()
            if not users:
                with self.user_list_container:
                    ui.label('No users found').classes('empty-state')
            else:
                for user in users:
                    with self.user_list_container:
                        with ui.row().classes('user-entry'):
                            ui.label(user['name']).classes('user-name')
                            ui.label(f"ID: {user['id']}").classes('user-id')
        except Exception as e:
            with self.user_list_container:
                ui.label(f'Connection error: {str(e)}').classes('error-message').style('width: 100%')

    def create_user(self, name_input):
        name = name_input.value.strip()
        if not name:
            ui.notify('Please enter a name', type='negative', position='top')
            return
        try:
            self.api.create_user({'name': name})
            ui.notify('User created successfully', type='positive', position='top')
            name_input.value = ''
            self.load_users()
        except Exception as e:
            ui.notify(f'Failed to create user {str(e)}', type='negative', position='top')


    def startUI(self):
        ui.add_head_html(f'<style>{css}</style>')

        with ui.column().classes('container'):
            ui.label('User Management').classes('header')

            with ui.column().classes('w-full'):
                ui.label('User List').classes('section-title')
                self.user_list_container = ui.column().classes('user-list')
                self.load_users()

            with ui.column().classes('w-full'):
                ui.label('Create New User').classes('section-title')
                with ui.row().classes('input-row'):
                    name_input = ui.input(placeholder='Enter user name').classes('input-field').props('autofocus')
                    
                    def handle_key(e):
                        if e.args['key'] == 'Enter':
                            self.create_user(name_input)
                    name_input.on('keydown.enter', handle_key)
                    
                    
                    ui.button('CREATE USER', on_click=lambda: self.create_user(name_input)).classes('btn')

        ui.run(port=self.port)


MOCK_API = apiMock()
realApi = rest_api()
client = Frontend(realApi, 5000)
#client = Frontend(MOCK_API, 5000)
client.startUI()