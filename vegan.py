
import urllib
import re

words_regex = "[\\w\\\/\(\\) -]*"
newline = "\n"


acceptable_allergens = {
    ''
    , 'Vegan'
    , 'Vegetarian'
    , 'Food Not Analyzed for Allergens'
    # , 'Peanuts'
    # , 'Dairy'
    # , 'Eggs'
    # , 'Fish'
    # , 'Pork'
    # , 'Sesame'
    # , 'Shellfish'
    # , 'Soy'
    # , 'Tree Nuts'

    # , 'Wheat / Gluten'
}

unacceptable_allergens = {
    'Pork'
    # , 'Eggs'
    # , 'Fish'
    # , 'Food Not Analyzed for Allergens'
    # , 'Peanuts'
    # , 'Dairy'
    # , 'Sesame'
    # , 'Shellfish'
    # , 'Soy'
    # , 'Tree Nuts'
    # , 'Vegan'
    # , 'Vegetarian'
    # , 'Wheat / Gluten'
}

exclude_sections = {
    "Crepes",
    "Deli Bar",
    "Plant Based - Mezze Bar"
}


def get_from_tags(tag, tomatch, tagclass = ""):
    if tagclass != "":
        tagclass = " class={}".format(tagclass)
    return "<{tag}{tagclass}>({tomatch})<\\/{tag}>".format(tag=tag, tagclass=tagclass, tomatch=tomatch)



meal_time_pattern = re.compile("<div class=\"hsp-accordian-container\"><h2 class=\"fw-accordion-title ui-state-active" + \
                               "\"><span class=\"ui-accordion-header-icon ui-icon ui-icon-triangle-1-s\"><\\/span>" + \
                               "<span class=\"fw-accordion-title-inner\">([a-zA-Z0-9, -]*)<\\/span>(.*?)" + \
                               "<\\/div><\\/div><\\/div>")
dining_hall_pattern = re.compile(get_from_tags("div", ".*?", "\"col-sm-6 col-md-4\""))
menu_area_pattern = re.compile(get_from_tags("h4", words_regex) +
                               get_from_tags("ul", ".*?", "\'menu-item-list\'"))
menu_item_pattern = re.compile(get_from_tags("li", ".*?"))

html_vals = urllib.urlopen("http://hospitality.usc.edu/residential-dining-menus/").read()

for meal_name, meal_html in re.findall(meal_time_pattern, html_vals):
    print meal_name
    for dining_hall_html in re.findall(dining_hall_pattern, meal_html):
        print (re.findall(
            re.compile("<h3 class=\"menu-venue-title\">([\\w'& ]*)<\\/h3>"),
            dining_hall_html
        ))[0]
        for menu_area_name, menu_area_html in re.findall(menu_area_pattern, dining_hall_html):
            if menu_area_name not in exclude_sections:
                print menu_area_name
                for menu_item_html in re.findall(menu_item_pattern, menu_area_html):
                    # print menu_item_html
                    item_name = re.findall(re.compile("({})<span ".format(".*?")), menu_item_html)
                    # print item_name[0]
                    allergens = set(re.findall(re.compile(get_from_tags("span", words_regex)), menu_item_html))
                    if (len(allergens) == 0):
                        allergens = {''}
                    # print allergens

                    if len(acceptable_allergens & allergens) > 0 and len(unacceptable_allergens & allergens) == 0:
                        print item_name[0]
                        # print allergens
                print newline
    print newline



