# HLDS data format

HLDS is the Haldis Language for Describing Servings. It defines the menu you see when ordering in
Haldis.

There is syntax highlighting support for editors in `etc/` in the Haldis repository.

## Indentation
Indentation requires hard **tabs**. Spaces will not work.

## Identifiers
You must choose an identifier for each location, dish, choice and option. Identifiers may consist
of numbers, hyphens, underscores and lowercase letters.

* Good: `my_identifier-007`
* Bad: ~~`My Identifié 007`~~

## Locations

A HLDS file consists of one or more locations. Each location starts with a header, which enclosed
in "fences" of at least three equal signs. The first line of the header contains the ID and name of
the location.  Further lines contain the metadata of the location, such as the phone number and
OpenStreetMap element. In the future, the phone number and such will be fetched from OpenStreetMap.

```hlds
==========================
ocean_garden: Ocean Garden
	osm     https://www.openstreetmap.org/node/2275105003
	phone   +32 9 222 72 74
	address Zwijnaardsesteenweg 399, 9000 Gent
	website http://oceangarden.byethost3.com/
	# Comments are allowed too!
==========================
```

## Dishes

A location consists of dishes. Spaces can be used to align the elements of your dish (but that's
not required).

```hlds
dish cheeseburger: Cheeseburger € 2.9
dish assortment:   Twijfelaar   € 3
```

## Inline choices
Dishes can contain choices. There are two types:
* `single_choice` is a required choice where the user must choose one option.
* `multi_choice` is an optional choice where the user can choose zero or more options.

```hlds
dish fries: Frietjes
	single_choice size: Formaat
		extra_small: Extra small € 1.8
		small:       Small       € 2
		medium:      Medium      € 2.5
		large:       Large       € 3.3
	multi_choice sauce: Saus
		ketchup: Ketchup        € 1.4
		mayo:    Mayonaise      € 1.4
		bicky:   Bickysaus      € 1.4
		stew:    Stoofvleessaus € 1.9
```

## Common choices
Choices that are used more than once, can be declared once and referenced in multiple dishes.

```hlds
bami_nasi: Bami of nasi
	bami: Bami
	nasi: Nasi

dish wok3: Studentenwok 3 kip bami/nasi zonder saus € 6
	single_choice bami_nasi

dish wok5: Studentenwok 5 babi pangang € 6
	single_choice bami_nasi
```

## Descriptions
You can add descriptions to dishes, choices and options. Separate name and description with ` -- `.

```hlds
dish dishid: Name -- This is a description € 3
```

## Tags

**Note:** HLDS tags are not supported in Haldis yet. You can ignore them.

You can add tags after ` :: `. Tags are `{identifier}`. You can use tags to attach more information
about a dish or option in a structured way. For example: `{has_meat}` signals to vegetarians that
they should avoid this.

The order is always id, name, description, tags, price (not all have to be present of course).

```hlds
dish dishid: Name -- This is a description :: {has_meat} € 3
```
