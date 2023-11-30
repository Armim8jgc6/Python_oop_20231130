from datetime import datetime, timedelta

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalva = []

    def foglal(self, datum):
        self.foglalva.append(datum)

    def lemond(self, datum):
        if datum in self.foglalva:
            self.foglalva.remove(datum)
            return True
        return False

    def elerheto(self, datum):
        return datum not in self.foglalva

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, ar=22500)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam, ar=35000)

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def szabad_szobak_listazasa(self, datum):
        szabad_szobak = [szoba for szoba in self.szobak if szoba.elerheto(datum)]
        return szabad_szobak

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam and szoba.elerheto(datum):
                szoba.foglal(datum)
                return Foglalas(szoba, datum)
        return None

    def lemondas(self, foglalas):
        szoba = foglalas.szoba
        datum = foglalas.datum
        if szoba.lemond(datum):
            return "Lemondás sikeres."
        return "Nincs ilyen foglalás."

    def foglalasok_listazasa(self):
        foglalasok = []
        for szoba in self.szobak:
            for datum in szoba.foglalva:
                foglalasok.append((szoba.szobaszam, szoba.ar, datum))
        return foglalasok

def datum_beolvasas():
    while True:
        datum_str = input("Adja meg a dátumot (YYYY-MM-DD formátumban): ")
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
            return datum
        except ValueError:
            print("Hibás dátum formátum. Próbálja újra.")

# Szálloda és szobák létrehozása
hotel = Szalloda("Best Hotel")
szoba1 = EgyagyasSzoba(101)
szoba2 = EgyagyasSzoba(102)
szoba3 = KetagyasSzoba(201)

hotel.szoba_hozzaadas(szoba1)
hotel.szoba_hozzaadas(szoba2)
hotel.szoba_hozzaadas(szoba3)

# Foglalások létrehozása
datum1 = datetime(2023, 1, 1)
datum2 = datetime(2023, 1, 2)
datum3 = datetime(2023, 1, 3)
datum4 = datetime(2023, 1, 4)
datum5 = datetime(2023, 1, 5)

foglalas1 = hotel.foglalas(101, datum1)
foglalas2 = hotel.foglalas(201, datum2)
foglalas3 = hotel.foglalas(102, datum3)
foglalas4 = hotel.foglalas(201, datum4)
foglalas5 = hotel.foglalas(103, datum5)

# Lemondás
hotel.lemondas(foglalas3)

# Felhasználói interfész
while True:
    print("\nVálassz műveletet:")
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")

    valasztas = input("Választás: ")

    if valasztas == "1":
        print("\nElérhető szobák:")
        szabad_szobak = hotel.szabad_szobak_listazasa(datetime.now() + timedelta(days=1))
        for i, szoba in enumerate(szabad_szobak, start=1):
            print(f"{i}. Szoba {szoba.szobaszam} - Ár: {szoba.ar}")

        szoba_idx = int(input("Válassz szobát sorszám alapján: "))
        valasztott_szoba = szabad_szobak[szoba_idx - 1]

        print("Adja meg a foglalás dátumát:")
        foglalasi_datum = datum_beolvasas()

        if foglalasi_datum >= datetime.now() + timedelta(days=1):
            foglalas = hotel.foglalas(valasztott_szoba.szobaszam, foglalasi_datum)
            if foglalas:
                print(f"Foglalás sikeres. Szoba: {foglalas.szoba.szobaszam}, Ár: {foglalas.szoba.ar}, Dátum: {foglalas.datum}")
            else:
                print("A kiválasztott szoba már foglalt ezen a napon.")
        else:
            print("A foglalás dátuma érvénytelen.")

    elif valasztas == "2":
        foglalas_szobaszam = input("Adja meg a lemondandó foglalás szobaszámát: ")
        lemondasi_datum = datum_beolvasas()

        lemondas_eredmeny = hotel.lemondas(Foglalas(Szoba(foglalas_szobaszam, 0), lemondasi_datum))
        print(lemondas_eredmeny)

    elif valasztas == "3":
        print("\nFoglalások:")
        for foglalas in hotel.foglalasok_listazasa():
            print(f"Szoba: {foglalas[0]}, Ár: {foglalas[1]}, Dátum: {foglalas[2]}")

    elif valasztas == "4":
        print("Kilépés...")
        break

    else:
        print("Érvénytelen választás. Kérlek, válassz újra.")