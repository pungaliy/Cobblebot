import urllib
import smtplib
from regex_patterns import *
import data_classes
import config
import people_and_items


def create_searchable_menu(html_vals):
    """Create and return a menu (dict of {food_item_name: MenuItem})"""
    unordered_menu = {}
    # Nested for loops for each meal time, dining hall, menu area, and item
    for full_meal_name, meal_html in re.findall(meal_time_pattern, html_vals):
        meal_time = full_meal_name.split()[0]
        for dining_hall_html in re.findall(dining_hall_html_pattern, meal_html):
            dining_hall_name = re.findall(dining_hall_name_pattern, dining_hall_html)[0]
            for menu_area_name, menu_area_html in re.findall(menu_area_pattern, dining_hall_html):
                for menu_item_html in re.findall(menu_item_pattern, menu_area_html):
                    item_name = re.findall(item_name_pattern, menu_item_html)[0]
                    allergens = re.findall(allergen_pattern, menu_item_html)
                    add_item_to_menu(allergens, dining_hall_name, item_name, meal_time, menu_area_name, unordered_menu)

    return unordered_menu


def add_item_to_menu(allergens, dining_hall_name, item_name, meal_time, menu_area_name, unordered_menu):
    """Add an item to the menu
    If it already exists in the same dining hall, add the specific time
    Otherwise, if it exists, but in a different dining hall, add to the list of MenuItem's under the item name
    If it doesn't exist at all in the dict, add the item_name as well as a new MenuItem as it's value"""
    if item_name in unordered_menu:
        added = False
        for item_in_dining_hall in unordered_menu[item_name]:
            if item_in_dining_hall.dining_hall == dining_hall_name:
                item_in_dining_hall.timings.add_time(meal_time)
                added = True
        if not added:
            unordered_menu[item_name].append(data_classes.MenuItem(
                item_name, dining_hall_name, data_classes.Times(meal_time), menu_area_name, allergens))

    else:
        unordered_menu[item_name] = [data_classes.MenuItem(
            item_name, dining_hall_name, data_classes.Times(meal_time), menu_area_name, allergens)]


def create_email_list():
    """Create the list of people to email, and the menu items each email will be sent"""
    emails_to_items = dict((email, []) for email in people_and_items.emails_to_names.iterkeys())
    html_vals = urllib.urlopen(config.menu_website).read()
    menu = create_searchable_menu(html_vals)
    menu_item_names = set(menu.keys())
    desired_item_names = set(people_and_items.items_to_emails.keys())
    for item_name in (menu_item_names & desired_item_names):
        for email in people_and_items.items_to_emails[item_name]:
            emails_to_items[email] += menu[item_name]

    return emails_to_items


def generate_email(email_address, food_items):
    """Generate the email's message given the food items. Take their quantity into account for correct grammar"""
    message = "Hello {name}!\n\n".format(name=people_and_items.emails_to_names[email_address])

    if len(food_items) == 0:
        message += "Unfortunately, none of the items you flagged are available in the dining halls today :("
    elif len(food_items) == 1:
        message += "The following item that you flagged is available in the dining hall today:\n\n{item}".format(
            item=food_items[0].to_string())
    else:
        message += "The following items that you flagged are available in the dining halls today:\n\n"
        for item in food_items:
            message += item.to_string() + "\n"

    message += "\n\nHave a nice day!\n-Cobblebot"

    return message


def send_email(to_address, msg):
    """Send an email given the recipient and message"""
    server = smtplib.SMTP(config.smtp_server_name)
    server.starttls()
    server.login(config.email_username, config.email_password)
    server.sendmail(config.email_username, to_address, msg)
    server.quit()


def gen_and_send_all_emails():
    """Main function
    Create the list of emails and associated MenuItem's
    Generate the message and send it"""
    emails_to_items = create_email_list()
    for email, menu_items in emails_to_items.iteritems():
        message = generate_email(email, menu_items)

        # --- Comment out these lines to remove IO ---
        print email
        print message
        print "\n"
        # --------------------------------------------
        
        # Uncomment the next line to actually send emails
        # send_email(email, message)


gen_and_send_all_emails()
