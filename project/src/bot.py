import spacy

nlp = spacy.load("pl_core_news_sm")

def extract_street_name(description):
    doc = nlp(description)
    for ent in doc.ents:
        print(ent.text, ent.label_)

    streets = [ent.text for ent in doc.ents if ent.label_ == 'LOC']
    return streets

description = "3 pokoje | 1 piętro | komórka lokatorska + miejsce postojowe w hali garażowej </p><p></p><p>Stan realizacji: obecnie budynek skończony, deweloper czeka na pozwolenie na użytkowanie (planowane w maju) - umowy przenoszące własność od końca maja, początku czerwca. </p><p></p><p>Zapraszam do zapoznania się z możliwością nabycia ekskluzywnego trzypokojowego mieszkania o powierzchni 55,79 m2 - powierzchnia bez ścian podana przez dewelopera (z powierzchnią użytkową 54,44 m2 - powierzchnia ze ścianami dodanymi przez dewelopera) w nowoczesnej inwestycji znajdującej się w dzielnicy Warszawa Włochy, przy ulicy Jutrzenki. Mieszkanie usytuowane jest na pierwszym piętrze oraz oferowane jest w stanie deweloperskim, co zapewnia możliwość indywidualnej aranżacji według preferencji przyszłego właściciela.</p><p></p><p>Lokalizacja: Inwestycja zapewnia doskonałą komunikację zarówno w obrębie Warszawy, jak i w kierunku innych dużych miast Polski. Bliskość stacji WKD Raków oraz licznych przystanków autobusowych ułatwia codzienne podróże, a obecność centrum handlowego oraz różnorodnych udogodnień sprawia, że mieszkanie staje się idealną przestrzenią dla osób ceniących wygodę i funkcjonalność.</p><p></p><p>Inwestycja: Projekt został zrealizowany w 95%, a zakończenie prac budowlanych planowane jest do połowy marca 2024 roku. Przewidywane przekazanie kluczy nastąpi od końca kwietnia do połowy maja 2024 roku. Na terenie inwestycji znajdują się liczne ścieżki spacerowe, obszary zieleni oraz fontanna, tworząc przyjazne i estetyczne otoczenie. Dodatkowo, mieszkańcom zapewniono ochronę 24/7, komfortowe lobby, miejsce parkingowe z ładowarką dla samochodów elektrycznych, darmową siłownię oraz klub fitness.</p><p></p><p>Mieszkanie: Przestrzeń mieszkalna składa się z salonu z aneksem kuchennym, dwóch sypialni, przedpokoju oraz łazienki z WC. Do mieszkania przynależy balkon o powierzchni 6,18 m2, który stanowi idealne miejsce do relaksu na świeżym powietrzu. Dodatkowo, oferta obejmuje obligatoryjny zakup miejsca postojowego w hali garażowej (60 000 złotych) oraz komórki lokatorskiej (25 000 złotych).</p><p></p><p>Standard wykończenia mieszkania obejmuje tynki gipsowe na ścianach (z wyjątkiem łazienki), parapety z konglomeratu kamiennego, instalacje telewizji kablowej, wentylację mechaniczną, okna PCV, drzwi antywłamaniowe oraz podłogi z wylewek. Woda ciepła dostarczana jest z MPEC.</p><p></p><p>Niezwłocznie skorzystaj z tej unikalnej okazji, by stać się właścicielem luksusowego mieszkania w dynamicznie rozwijającej się części Warszawy!</p><p></p><p>Zapraszam do kontaktu"
street_names = extract_street_name(description)

print("Znalezione nazwy ulic:", street_names)