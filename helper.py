from datetime import datetime
import re
class Item:
    def __init__(self, villeDepart, villeArrive, classe, nbreEscale, prix, duree, departDate, retourDate, heureDepart, heureDepartName, heureArrive, heureArriveName, compagnie):
        self.villeDepart = villeDepart
        self.villeArrive = villeArrive
        self.classe = classe
        self.nbreEscale = nbreEscale
        self.prix = prix
        self.duree = duree
        self.departDate = departDate
        self.retourDate = retourDate
        self.heureDepart = heureDepart
        self.heureDepartName = heureDepartName
        self.heureArrive = heureArrive
        self.heureArriveName = heureArriveName
        self.compagnie = compagnie

    def to_dict(self):
        return {
            'villeDepart': self.villeDepart,
            'villeArrive': self.villeArrive,
            'classe': self.classe,
            'nbreEscale': self.nbreEscale,
            'prix': self.prix,
            'duree': self.duree,
            'departDate': self.departDate,
            'retourDate': self.retourDate,
            'heureDepart': self.heureDepart,
            'heureDepartName': self.heureDepartName,
            'heureArrive': self.heureArrive,
            'heureArriveName': self.heureArriveName,
            'compagnie': self.compagnie
        }
    
time_slots = {
    "Early_Morning": (4, 8),
    "Morning": (8, 12),
    "Afternoon": (12, 17),
    "Evening": (17, 21),
    "Night": (21, 24),
    "Late_Night": (0, 4)
}


def clean_price(price):
    if not price:
        return ""
    # Supprimer le symbole euro et les espaces
    price = price.replace('€', '')
    # Supprimer tous les types d'espaces
    price = re.sub(r'\s+', '', price)
    
    return price
def convert_duration_to_hours(duration_str):
    parts = duration_str.split()
    hours = 0
    minutes = 0
    for i, part in enumerate(parts):
        if 'h' in part:
            hours_str = part.replace('h', '').strip()
            if hours_str:
                hours = int(hours_str)
            else:
                hours = int(parts[i - 1])
        if 'min' in part:
            minutes_str = part.replace('min', '').strip()
            if minutes_str:
                minutes = int(minutes_str)
            else:
                minutes = int(parts[i - 1])
    return hours + minutes / 60

def parse_time(time_str):
    if '+' in time_str:
        time_str = time_str.split('+')[0]
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60

def get_time_slot(hour_decimal):
    for slot, (start, end) in time_slots.items():
        if start < end:
            if start <= hour_decimal < end:
                return slot
        else:
            if hour_decimal >= start or hour_decimal < end:
                return slot
    return "Unknown"

def convert_escale(escale_str):
    if escale_str == 'Sans escale':
        return 1
    elif escale_str == '1 escale':
        return 2
    else:
        return 3
