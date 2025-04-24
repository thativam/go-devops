# Getting Started with Python

## Setting Up the Environment

1. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    ```

2. **Activate the Virtual Environment**:
    - On Linux/MacOS:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      .\venv\Scripts\activate
      ```

3. **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

## Adding a New Dependency

1. **Install the Dependency**:
    ```bash
    pip install <package-name>
    ```

2. **Update `requirements.txt`**:
    ```bash
    pip freeze > requirements.txt
    ```

3. **Share the Updated `requirements.txt`**:
    Ensure the updated file is committed to version control for others to use.

## Deactivating the Environment

To deactivate the virtual environment, simply run:
```bash
deactivate
```