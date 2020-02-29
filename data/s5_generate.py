#!/usr/bin/env python3

print("""============================
s5: S5
	osm     https://www.openstreetmap.org/node/3752879366
	address Krijgslaan 281, 9000 Gent
	website https://www.ugent.be/student/nl/meer-dan-studeren/resto/restos/restocampussterre.htm
============================""")

# Paste menu from https://www.ugent.be/student/nl/meer-dan-studeren/resto/broodjes/overzicht.htm
# here
MENU = [l.split("\t") for l in """
Spring break	Erwten-munt spread, komkommer, radijs, sla, croutons, cocktailsaus	€ 1,50	€ 2,40
Groentespread	Weekelijks wisselende groentespread	€ 1,60	€ 2,60
Brie	Brie, honing, pijnboompitten, sla	€ 1,50	€ 2,50
Geitenkaas	Geitenkaas, appel, honing en sla	€ 1,70	€ 2,60
Kaas	Kaas, ei, komkommer, sla, tomaat en mayonaise	€ 1,40	€ 2,10
Kruidenkaas	Kruidenkaas, ei, komkommer, sla en tomaat	€ 1,40	€ 2,10
Tomaat-mozzarella	Mozzarella, tomaat, basilicumpesto en sla	€ 1,70	€ 2,60
Kip curry	Kip curry, ei, komkommer, sla en tomaat	€ 1,50	€ 2,20
Kip curry Hawaï	Kip curry, ananas, ei, komkommer, sla en tomaat	€ 1,50	€ 2,20
Caesar	Kippenreepjes, Gran Moravia kaasschilfers, croutons, sla en caesardressing	€ 1,50	€ 2,50
Gerookte zalm met kruidenkaas	Gerookte zalm, kruidenkaas en ui	€ 1,60	€ 2,60
Vissalade	Duurzame vissalade, tomaat, sla, komkommer en ei	€ 1,50	€ 2,30
Ham	Ham, ei, komkommer, sla, tomaat en mayonaise	€ 1,50	€ 2,30
Preparé	Preparé, ei, komkommer, sla en tomaat	€ 1,50	€ 2,30
Martino	Preparé, augurk, tomaat, mosterd en tabasco	€ 1,60	€ 2,40
Hoevebroodje	Geitenkaas, appel, honing, gebakken spek en sla	€ 1,70	€ 2,60
Maison	Ham, kaas, augurk, ei, sla, tomaat, cocktailsaus en mayonaise	€ 1,60	€ 2,40
Tropical	Ham, kaas, ananas, ei, sla, cocktailsaus	€ 1,60	€ 2,40
Toscane	Mozzarella, prosciutto ham, sla en tomatensalsa	€ 1,60	€ 2,70
Argenteuil	Ham, asperge, ei, komkommer, sla, tomaat en mayonaise	€ 1,50	€ 2,40
""".strip().split("\n")]
# Sort by price. This fails if price is not always exactly "€ x,xx" but whatever
MENU.sort(key=lambda dish: dish[2] + dish[3])

SANDWICHES = [
    [ # First price
        ("small_white", "Klein wit  "),
        ("small_brown", "Klein bruin"),
    ],
    [ # Second price
        ("large_white", "Groot wit  "),
        ("large_brown", "Groot bruin"),
        ("quattro", "    Quattro    "),
    ]
]

def name_to_id(name):
    return "".join(filter(
        lambda c: ord("a") <= ord(c) <= ord("z"),
        name.lower().replace("é", "e")
    ))

for dish in MENU:
    print()
    name, description = dish[0], dish[1]
    prices = [p.replace(",", ".") for p in dish[2:]]

    print("dish sandwich_{}: Broodje {} -- {}".format(name_to_id(name), name, description))
    print("\tsingle_choice sandwich: Broodje")
    for sandwiches, price in zip(SANDWICHES, prices):
        for sw_id, sw_name in sandwiches:
            print("\t\t{}: {} {}".format(sw_id, sw_name, price))

print("""
dish yoghurt:             Natuuryoghurt           € 0.4
dish yofu:                Plantaardige yofu       € 1
dish yoghurt_muesli:      Yoghurt met muesli      € 1
dish greek_fruit_yoghurt: Griekse vruchtenyoghurt € 1.4
dish chocolate_mousse:    Chocomousse             € 1.4
dish speculoos_mousse:    Speculaasmousse         € 1.4
dish soy_dessert:         Soja dessert            € 0.7
dish tiramisu:            Tiramisu                € 1.4
dish muffin:              Muffin                  € 1
dish donut:               Donut                   € 1
dish ice_variation:       IJsvariatie             € 2.3
dish fruit:               Fruit                   € 0.5
dish nuts_fruit:          Nuts & fruit            € 1.5

dish chocolate_milk: Koude chocolademelk        € 0.8
dish juice:          Fruitsap 20 cl Fair Trade  € 0.8
dish water:          Bruisend water 50 cl       € 0.8
dish perfumed_water: Gearomatiseerd water 50 cl € 1
dish bionade:        Bionade                    € 1.5
dish finley:         Finley                     € 1
dish iced_coffee:    IJskoffie                  € 2
dish iced_tea:       IJsthee                    € 2
dish smoothie:       Smoothie                   € 2""")
