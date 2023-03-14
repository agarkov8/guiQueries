# Importieren die benötigten Python-Packages
import pandas as pd
import numpy as np
from ms_active_directory import ADDomain
import getpass
from tkinter import *
from tkinter import messagebox
from shutil import copyfile
import os

print("Bitte warten!")

# Die entsprechende CSV-Tabelle wird in eine DataFrame umgewandelt.
# Alle Spalten werden umbenannt und die, die nicht gebraucht werden, werden entfernt.
copyfile('E:/Transfer/Sample/file.csv', 'C:/temp/file.csv')
df = pd.read_csv(r'C:\temp\ file.csv', sep=',', dtype='str', encoding='latin-1')
df.columns = ['Opcode', 'Spalte2', 'ID', 'RollenID', 'Funktion', 'Spalte6', 'BASEUSRC-IMPORT', 'BASEUSRC-PE-EXCL',
              'BASEUSRC-TILL', 'BASEUSRC-COMMENT', 'BASEUSRC-CUST', 'BASEUSRC-SAMEXP', 'BASEUSRC-F-ASSIGN',
              'BASEUSRC-F-CMT-ID']
df = df.drop(df.columns[[0, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13]], axis=1)
df = df.drop(index=0)

# Leere Listen
email_list = []
surname_list = []
fname_list = []

# DataFrame wird bereinigt, da die Daten drin sehr inkonsistent sind
df['ID'] = df['ID'].str[2:-5]
df['RollenID'] = df['RollenID'].str.strip('GEN_F_')
df['RollenID'] = df['RollenID'].str.strip('GEN_B_')
df['RollenID'] = df['RollenID'].str.strip('GEN_R_')
df['RollenID'] = df['RollenID'].str.strip('OE_')
df['RollenID'] = df['RollenID'].str.strip('_U')
df['Funktion'] = df['Funktion'].replace('AC_Funktion', '1')
df['Funktion'] = df['Funktion'].replace('AC_WF-free', '1')
df['Funktion'] = df['Funktion'].replace('AC_Rolle', '1')
df['Funktion'] = df['Funktion'].replace('AC_Interne_Rolle', '2')

# Einige Zeilen werden entfernt, da die keine sinnvolle Bedeutung haben(Buchstaben, Sonderzeichen)
digits = df['RollenID'].str.len()
df.loc[digits > 8, 'RollenID'] = np.nan
df.loc[df['ID'] == 'BASEUS-SAM-ID', 'ID'] = np.nan
df.loc[df['Funktion'] == 'BASEUSRC-IS-CODE', 'Funktion'] = np.nan
df_dropped = df.dropna()


# Diese Funktion füllt die leeren Listen mit den Daten jedes Mitarbeiters, der die gewünschte Rolle hat.
def find_user_info(pnumber, session):
    user = session.find_user_by_name(pnumber,
                                     ['displayName', 'givenName', 'mail', 'sAMAccountName', 'sn', 'telephoneNumber'])
    group_name = 'operations managers'

    email_list.append(user.get('mail'))
    surname_list.append(user.get('sn'))
    fname_list.append(user.get('givenName'))


# Die Funktion gibt eine neue CSV-Datei(das Endergebnis) zurück.
# Parameters:
# rollenID (str): Die RollenID, die man braucht, wird abgerufen.
# fileName (str): Der Name der neuen CSV-Datei wird automatisch eingegeben.
# Es wird eine for-Schleife erstellt, die über jede Personalnummer in der Spalte ergebnis['ID'] iteriert
# Bei jeder Iteration wird die find_user_info-Funktion aufgerufen.
# Für jede einzelne Liste werden neue DataFrames erstellt und am Ende werden alle DataFrames gemerged.
# Return:
# 'df_final' ist das Endergebnis-DataFrame dieser Funktion und
# eine CSV-Datei wird mit den neuen benötigten Daten erstellt.
def abfrage(roll_id, filePath, session):
    session_p = session
    ergebnis = df_dropped[df_dropped['RollenID'] == str(roll_id)]
    pnumber_array = np.array(ergebnis['ID'])

    for pnumber in ergebnis['ID']:
        find_user_info(pnumber, session_p)

    df_email = pd.DataFrame({
        'ID': pnumber_array,
        'E-mail': email_list
    })

    df_surname = pd.DataFrame({
        'ID': pnumber_array,
        'Surname': surname_list
    })

    df_givenName = pd.DataFrame({
        'ID': pnumber_array,
        'GivenName': fname_list
    })

    df_email_surname = pd.merge(df_email, df_surname, on='ID')
    df_email_surname_givenName = pd.merge(df_email_surname, df_givenName, on='ID')
    df_final = pd.merge(ergebnis, df_email_surname_givenName, on='ID')
    df_final.drop_duplicates(subset=['RollenID', 'Surname', 'E-mail', 'Funktion'], keep='last', inplace=True)
    df_final.to_csv(filePath, sep=';', index=False,
                    columns=['RollenID', 'Surname', 'GivenName', 'ID', 'E-mail', 'Funktion'],
                    header=['Role', 'Surname', 'GivenName', 'SamAccountName', 'EmailAddress', 'UserClass'])
    messagebox.showinfo("Abfrage",
                        "Eine Datei wurde für Sie erstellt!\nDie Datei wurde in X:\Abfragen gespeichert.")
    email_list.clear()
    surname_list.clear()
    fname_list.clear()


# Nimmt den Wert von dem RollenID-Eingabefeld
def fill_roll_id_input(rollenID, session):
    session_r = session
    roll_id = str(rollenID.get())
    # FileName
    file_name = 'MemberRole-' + roll_id + '.csv'
    file_path = 'X:/Abfragen/' + str(file_name)
    abfrage(roll_id, file_path, session_r)


# Die Login-Funktion wird ausgeführt und ein neues Fenster wird geöffnet
def login():
    try:
        pID = str(pID_user.get())
        username = str(pID_user.get()) + '@sample.de'
        user_pw = str(password_user.get())
        domain = ADDomain('sample.de')
        session = domain.create_session_as_user(username, user_pw)
        user = session.find_user_by_name(pID, ['displayName', 'givenName', 'mail', 'sAMAccountName', 'sn',
                                               'telephoneNumber'])
        print('Hallo, ' + user.get('givenName'))
        fenster.destroy()

        # Create new frame
        neuesFenster = Tk()
        neuesFenster.title("Abfragen")
        neuesFenster.geometry("340x340")
        POSX = 550
        POSY = 200
        neuesFenster.geometry("+%d+%d" % (XPOS, YPOS))

        # Benutzername-Label
        benutzername1_label = Label(neuesFenster, text="Bitte RollenID eingeben :")
        benutzername1_label.grid(row=0, column=0)

        # RollenID-Entry
        rollenID = Entry(neuesFenster)
        rollenID.grid(row=0, column=2, columnspan=2)

        # Suche-Button
        OK_button = Button(neuesFenster, text="Suche", command=lambda: fill_roll_id_input(rollenID, session))
        OK_button.grid(row=2, column=2)
        # Abbrechen-Button
        exit1_button = Button(neuesFenster, text="Abbrechen", command=neuesFenster.destroy)
        exit1_button.grid(row=2, column=3)
        neuesFenster.mainloop()
    except Exception:
        messagebox.showinfo("Abfrage", "Der Benutzername oder das Kennwort ist falsch! Bitte versuchen Sie es erneut.")


def callback(event):
    login_button = login()


# Frame erstellen
fenster = Tk()
fenster.title("Anmeldemaske")
fenster.geometry("260x100")
XPOS = 550
YPOS = 250
fenster.geometry("+%d+%d" % (XPOS, YPOS))

# Benutzername-Label
benutzername_label = Label(fenster, text="Benutzername :")
benutzername_label.grid(row=0, column=0, padx=5, pady=5)
# Benutzername-ENTRY
pID_user = Entry(fenster)
pID_user.grid(row=0, column=1, padx=5, pady=5)

# Passwort-Label
passwort_label = Label(fenster, text="Passwort :")
passwort_label.grid(row=1, column=0, padx=5, pady=5)
# Passwort-Entry
password_user = Entry(fenster, show="*")
password_user.grid(row=1, column=1, padx=5, pady=5)

# Login-Label
login_label = Label(fenster, text="Login")
# Login-Button
login_button = Button(fenster, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=1)
# Exit-Label
exit_button = Button(fenster, text="Abbrechen", command=fenster.destroy)
exit_button.grid(row=2, column=1)
fenster.bind('<Return>', callback)
fenster.mainloop()
os.remove("C:/temp/file.csv")