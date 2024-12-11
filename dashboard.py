import hashlib
import customtkinter as ctk
import tkinter.messagebox as tkmb


# File-based authentication system
def validate_login(username, password):
    try:
        with open('accounts.txt', 'r') as account_file:
            accounts = {
                line.strip().split(';')[0]: line.strip().split(';')[1]
                for line in account_file.readlines()
            }
    except FileNotFoundError:
        accounts = {}

    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    return accounts.get(username) == hashed_password


def create_account(username, password):
    try:
        with open('accounts.txt', 'r') as account_file:
            accounts = {
                line.strip().split(';')[0]
                for line in account_file.readlines()
            }
    except FileNotFoundError:
        accounts = set()

    if username in accounts:
        return False, "Deze gebruikersnaam is al in gebruik."

    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    with open('accounts.txt', 'a') as account_file:
        account_file.write(f"{username};{hashed_password}\n")

    return True, "Het account is succesvol aangemaakt!"


# Tkinter-based UI
def launch_dashboard():
    dashboard = ctk.CTkToplevel()
    dashboard.geometry("1300x700")
    dashboard.title("Dashboard")

    ctk.CTkLabel(
        master=dashboard,
        text="Welkom bij het dashboard!",
        font=ctk.CTkFont(size=16, weight="bold"),
    ).pack(pady=20)

    ctk.CTkLabel(
        master=dashboard,
        text="Welkom bij Steam",
    ).pack(pady=20)


def login_action():
    username = user_entry.get()
    password = user_pass.get()

    if validate_login(username, password):
        tkmb.showinfo("Succes", "Je bent succesvol ingelogd!")
        app.withdraw()  # Hide the login window
        launch_dashboard()
    else:
        tkmb.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord!")


def signup_action():
    username = user_entry.get()
    password = user_pass.get()

    if (
            ';' in password
            or len(password) < 8
            or not any(char.isdigit() for char in password)
            or not any(char.isupper() for char in password)
    ):
        tkmb.showerror(
            "Fout",
            "Het wachtwoord moet:\n"
            "- Geen ; bevatten\n"
            "- Minimaal 8 tekens lang zijn\n"
            "- Minimaal 1 cijfer en 1 hoofdletter bevatten",
        )
        return

    success, message = create_account(username, password)
    if success:
        tkmb.showinfo("Succes", message)
    else:
        tkmb.showerror("Fout", message)


# Tkinter App UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("Modern Login UI with File-Based Authentication")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

ctk.CTkLabel(master=frame, text="Login of Registreer", font=ctk.CTkFont(size=16)).pack(
    pady=12, padx=10
)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Gebruikersnaam")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Wachtwoord", show="*")
user_pass.pack(pady=12, padx=10)

login_button = ctk.CTkButton(master=frame, text="Login", command=login_action)
login_button.pack(pady=12, padx=10)

signup_button = ctk.CTkButton(master=frame, text="Registreren", command=signup_action)
signup_button.pack(pady=12, padx=10)

app.mainloop()
