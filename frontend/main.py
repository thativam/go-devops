from nicegui import ui  # type: ignore
import requests

API_BASE_URL = 'http://your-api.com/users'  # Replace with your real endpoint

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
    justify-content: center;
    align-items: center;
}

.container {
    max-width: 800px;  /* Aumentei a largura máxima */
    width: 90%;
    margin: auto;
    padding: 2.5rem;
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.07);
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
    border: 1px dashed #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    width: 100%;  /* Adicionei para ocupar toda a largura */
}

.empty-state {
    color: #64748b;
    text-align: center;
    padding: 2rem 0;
    font-size: 0.95rem;
    width: 100%;  /* Adicionei para ocupar toda a largura */
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
    width: 100%;  /* Adicionei para ocupar toda a largura */
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
    width: 100%;  /* Ocupa toda a largura disponível */
    box-sizing: border-box;  /* Garante que padding não aumente a largura */
}
"""

user_list_container = None

def load_users():
    user_list_container.clear()
    try:
        response = requests.get(API_BASE_URL)
        if response.ok:
            users = response.json()
            if not users:
                with user_list_container:
                    ui.label('No users found').classes('empty-state')
            else:
                for user in users:
                    with user_list_container:
                        with ui.row().classes('user-entry'):
                            ui.label(user['name']).classes('user-name')
                            ui.label(f"ID: {user['id']}").classes('user-id')
        else:
            with user_list_container:
                ui.label('Failed to load users').classes('error-message').style('width: 100%')  # Garante 100% de largura
    except Exception as e:
        with user_list_container:
            ui.label(f'Connection error: {str(e)}').classes('error-message').style('width: 100%')  # Garante 100% de largura

def create_user(name_input):
    name = name_input.value.strip()
    if not name:
        ui.notify('Please enter a name', type='negative', position='top')
        return
    
    try:
        response = requests.post(API_BASE_URL, json={'name': name})
        if response.ok:
            ui.notify('User created successfully', type='positive', position='top')
            name_input.value = ''
            load_users()
        else:
            ui.notify('Failed to create user', type='negative', position='top')
    except Exception as e:
        ui.notify(f'Connection error: {str(e)}', type='negative', position='top')

# UI Layout
ui.add_head_html(f'<style>{css}</style>')

with ui.column().classes('container'):
    ui.label('User Management').classes('header')
    
    with ui.column().classes('w-full'):
        ui.label('User List').classes('section-title')
        user_list_container = ui.column().classes('user-list')
        load_users()

    with ui.column().classes('w-full'):
        ui.label('Create New User').classes('section-title')
        with ui.row().classes('input-row'):
            name_input = ui.input(placeholder='Enter user name').classes('input-field')
            ui.button('CREATE USER', on_click=lambda: create_user(name_input)).classes('btn')

ui.run(port=5000)