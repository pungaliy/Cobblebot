
import urllib
import smtplib
from cobblebot_regex_patterns import *

names = {
    "pungaliy@usc.edu": "Shray",
    "hyunhste@usc.edu": "Stephanie",
    "voter@usc.edu": "Ben",
    "kbchandr@usc.edu": "Katrina"
}
to_find_backwards = {"Sliced Almonds": ["pungaliy@usc.edu"],
                     "Cherry Cobbler": ["pungaliy@usc.edu"],
                     "Strawberry Cobbler": ["pungaliy@usc.edu"],
                     "Peach Cobbler": ["pungaliy@usc.edu"]}

emails = {"pungaliy@usc.edu": [], "kbchandr@usc.edu": []}




# html_vals = urllib.urlopen("http://hospitality.usc.edu/residential-dining-menus/").read()

html_vals = urllib.urlopen("http://hospitality.usc.edu/residential-dining-menus/?menu_date=January+4%2C+2018").read()


class Times:
    def __init__(self, first_time):
        self.string_times = []
        self.add_time(first_time)

    # noinspection PyDictCreation
    def add_time(self, time_name):
        if time_name not in self.string_times:
            self.string_times.append(time_name)

    def __str__(self):

        l = len(self.string_times)
        if l == 1:
            return self.string_times[0]
        elif l == 2:
            return " and ".join(self.string_times)
        else:
            last = l - 1
            s = self.string_times[last]
            rest = self.string_times[:last]
            return ", ".join(rest) + ", and " + s

    def to_string(self):
        return self.__str__()


class MenuItem:
    def __init__(self, item_name, dining_hall, timings, menu_area, allergens):
        self.item_name = item_name
        self.dining_hall = dining_hall
        self.timings = timings
        self.menu_area = menu_area
        self.allergens = allergens

    def __str__(self):
        return "{item_name} in the {menu_area} at {dining_hall} for {times}".\
            format(item_name=self.item_name, menu_area=self.menu_area,
                   dining_hall=self.dining_hall, times=self.timings.to_string())

    def to_string(self):
        return self.__str__()


def create_searchable_menu(html_vals):
    unordered_menu = {}
    for full_meal_name, meal_html in re.findall(meal_time_pattern, html_vals):
        meal_time = full_meal_name.split()[0]
        for dining_hall_html in re.findall(dining_hall_html_pattern, meal_html):
            dining_hall_name = re.findall(dining_hall_name_pattern, dining_hall_html)[0]
            for menu_area_name, menu_area_html in re.findall(menu_area_pattern, dining_hall_html):
                for menu_item_html in re.findall(menu_item_pattern, menu_area_html):
                    item_name = re.findall(item_name_pattern, menu_item_html)[0]
                    allergens = re.findall(allergen_pattern, menu_item_html)
                    if item_name in unordered_menu:
                        added = False
                        for item_in_dining_hall in unordered_menu[item_name]:
                            if item_in_dining_hall.dining_hall == dining_hall_name:
                                item_in_dining_hall.timings.add_time(meal_time)
                                added = True
                        if not added:
                            unordered_menu[item_name].append(MenuItem(
                                item_name, dining_hall_name, Times(meal_time), menu_area_name, allergens))

                    else:
                        unordered_menu[item_name] = [MenuItem(
                            item_name, dining_hall_name, Times(meal_time), menu_area_name, allergens)]

    return unordered_menu
    # return OrderedDict(sorted(unordered_menu.items(), key=lambda t: t[0]))


def create_email_list():
    menu = create_searchable_menu(html_vals)  ## Unordered dictionary
    menu_item_names = set(menu.keys())
    desired_item_names = set(to_find_backwards.keys())
    for item_name in (menu_item_names & desired_item_names):
        for email in to_find_backwards[item_name]:
            emails[email] += menu[item_name]


def generate_email(email_addr, food_items):

    print food_items

    message = "Hello {name}!\n\n".format(name=names[email_addr])

    if len(food_items) == 0:
        message += "Unfortunately, none of the items you flagged are available in the dining halls today :("
    elif len(food_items) == 1:
        message += "The following item that you flagged is available in the dining hall today:\n\n{item}".format(
            item=food_items[0].to_string())
    else:
        message += "The following items that you flagged are available in the dining halls today:\n\n"
        for item in food_items:
            print item
            message += item.to_string() + "\n"

    message += "\n\nHave a nice day!\n-Cobblebot"

    return message

def send_email(email_address, msg):
    username = 'usccobblebot@gmail.com'
    password = 'villagedininghall'
    toaddrs = email_address
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(username, toaddrs, msg)
    server.quit()


def gen_and_send_all_emails():
    create_email_list()
    for email, menu_items in emails.iteritems():
        message = generate_email(email, menu_items)
        print email
        print message
        print "\n"
        # send_email(email, message)


gen_and_send_all_emails()