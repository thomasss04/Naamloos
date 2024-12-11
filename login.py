import hashlib
def account_aanmaken():
    with open('accounts.txt', 'r+') as account:
        lines = account.readlines()

        used = [line.strip().split(';')[0] for line in lines]
        gebruikersnaam = input('Gebruikersnaam: ')
        while gebruikersnaam == '' or ';' in gebruikersnaam:
            print('Het veld mag niet leeg zijn of een ; bevatten.')
            gebruikersnaam = input('Gebruikersnaam: ')


        while gebruikersnaam in used:
            print('Deze gebruikersnaam is al in gebruik.')
            gebruikersnaam = input('Gebruikersnaam: ')
        wachtwoord = input('Wachtwoord: ')
        while ';' in wachtwoord or len(wachtwoord)<8 or not any(char.isdigit() for char in wachtwoord) or not any(char.isupper() for char in wachtwoord):
            print(f'Fout, probeer het nog een keer. \nHet wachtwoord mag geen ; bevatten.\nHet wachtwoord moet 8 characters lang zijn.\nHet wachtwoord moet minimaal 1 cijfer en 1 hoofdletter bevatten.')
            wachtwoord = input('voer een wachtwoord in:')
        check_wachtwoord = input('voer het wachtwoord nog een keer in:')
        while wachtwoord != check_wachtwoord:
            check_wachtwoord = input('Het wachtwoord was niet hetzelfde, voer het wachtwoord nog een keer in:')
        var = wachtwoord.encode('utf-8')
        hashed_var = hashlib.sha1(var).hexdigest()



        account.writelines(f'{gebruikersnaam};{hashed_var}\n')
        return print('Het aanmaken van het account is gelukt!')



def account_inloggen():
    with open('accounts.txt', 'r') as account:
        lines = account.readlines()
        gebruikersnaam = input('Gebruikersnaam: ')
        wachtwoord = input('Wachtwoord: ')
        var = wachtwoord.encode('utf-8')
        hashed_var = hashlib.sha1(var).hexdigest()
        print(type(hashed_var))
        while f'{gebruikersnaam};{hashed_var}\n' not in lines:
            print('De gebruikersnaam of het wachtwoord is niet correct.')
            gebruikersnaam = input('Gebruikersnaam: ')
            wachtwoord = input('Wachtwoord: ')
        return print('Het inloggen is gelukt!')


keuze = int(input('1: Sign in\n2: Sign up'))
if keuze == 1:
    print(account_inloggen())
if keuze == 2:
    print(account_aanmaken())
