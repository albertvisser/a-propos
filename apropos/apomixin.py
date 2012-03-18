import os, pickle
apofile = "apropos.ini"
info = """\
Apropos by Albert Visser
To regain your a propos when you've lost it

Ctrl-N          - new tab
Ctrl-right      - next tab
Ctrl-left       - previous tab
Ctrl-W          - close tab
Ctrl-S          - save all
Ctrl-L          - reload all
Ctrl-Q, Esc     - close and exit
Ctrl-H          - hide in system tray

F1              - this (help)information
F2              - edit tab title
"""
info_dutch = """\
Apropos door Albert Visser
Om je a propos terug te kunnen vinden
als je de draad even kwijt bent

Ctrl-N          - nieuwe tab
Ctrl-rechts     - volgende tab
Ctrl-links      - vorige tab
Ctrl-W          - sluit tab
Ctrl-S          - alles opslaan
Ctrl-L          - alles opnieuw laden
Ctrl-Q, Esc     - opslaan en sluiten
Ctrl-H          - verbergen in system tray

F1              - deze (help)informatie
F2              - wijzig tab titel
"""

hide_text = [
    """\
Apropos wil now go to sleep in the System tray
An icon will appear that you can click on to revive it""",
    "Don't show this message again"
    ]

hide_text_dutch = [
    """\
Apropos gaat nu slapen in de System tray
Er komt een icoontje waarop je kunt klikken om hem weer wakker te maken""",
    "Deze melding niet meer laten zien"
    ]

ask_title = 'New title for current tab:'
ask_title_dutch = 'Nieuwe titel voor de huidige tab:'

class Apomixin(object):
    def load_notes(self):
        if os.path.exists(apofile):
            try:
                with open(apofile, 'rb') as f:
                    self.apodata = pickle.load(f)
            except ValueError:
                with open(apofile, 'r') as f:
                    self.apodata = pickle.load(f)
        else:
            self.apodata = {}

    def save_notes(self):
        f = open(apofile, 'wb')
        pickle.dump(self.apodata, f)
        f.close()
