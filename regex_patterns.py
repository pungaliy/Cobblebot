import re

words_regex = "[\\w\\\/\(\\) -]*"
newline = "\n"


def get_from_tags(tag, to_match, tag_class =""):
    if tag_class != "":
        tag_class = " class={}".format(tag_class)
    return "<{tag}{tag_class}>({to_match})<\\/{tag}>".format(tag=tag, tag_class=tag_class, to_match=to_match)


meal_time_pattern_string = "<div class=\"hsp-accordian-container\"><h2 class=\"fw-accordion-title ui-state-active" + \
               "\"><span class=\"ui-accordion-header-icon ui-icon ui-icon-triangle-1-s\"><\\/span>" + \
               "<span class=\"fw-accordion-title-inner\">([a-zA-Z0-9, -]*)<\\/span>(.*?)" + \
               "<\\/div><\\/div><\\/div>"
meal_time_pattern = re.compile(meal_time_pattern_string)


dining_hall_html_pattern = re.compile(get_from_tags("div", ".*?", "\"col-sm-6 col-md-4\""))
dining_hall_name_pattern = re.compile("<h3 class=\"menu-venue-title\">([\\w'& ]*)<\\/h3>")
menu_area_pattern = re.compile(get_from_tags("h4", words_regex) +
                               get_from_tags("ul", ".*?", "\'menu-item-list\'"))
menu_item_pattern = re.compile(get_from_tags("li", ".*?"))
item_name_pattern = re.compile("({})<span ".format(".*?"))
allergen_pattern = re.compile(get_from_tags("span", words_regex))