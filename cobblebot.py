
import urllib
import re
import smtplib

names = {
    "pungaliy@usc.edu": "Shray",
    "hyunhste@usc.edu": "Stephanie",
    "voter@usc.edu": "Ben",
}

to_find = {
    "voter@usc.edu": {
        "Peach Cobbler",
        "Apple Cobbler",
        "Tortellini"
    },
    "hyunh@usc.edu": {
        "Ramen"
    },
    "pungaliy@usc.edu": {
        "Buckwheat Pancakes"
    }
}


def send_mail(email, food_items):
    # from_addr = 'usccobblebot@gmail.com'
    toaddrs = email
## TODO: Fix this (or at least understand it)
    for foods in food_items:
        if len(foods) == 1:
            food_string = foods[0]
        elif len(food_items) == 2:
            food_string = foods[0] + " and " + foods[1]
        else:
            foods[len(foods)-1] = "and " + foods[len(foods)-1]
            food_string = str(foods).strip('[]').replace("'", "")

    # food_string =
    # food_string = str(food_items).strip('[]').replace("'", "")
    msg = 'Hello {}!\n\nThe Village Dining Hall has {} today. Hoorah!\n\n-Cobblebot'.\
        format(names[email], food_string)


    username = 'usccobblebot@gmail.com'
    password = 'villagedininghall'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(username, toaddrs, msg)
    server.quit()

    print "SENT to {}".format(names[email])


html_vals = urllib.urlopen("http://hospitality.usc.edu/residential-dining-menus/").read()

for email, personal_choices in to_find.iteritems():
    available_foods = []
    for item in personal_choices:
        pattern = re.compile("({})".format(item), re.I)
        found_item = re.findall(pattern, html_vals)
        if found_item:
            available_foods.append(item)
    if available_foods:
        send_mail(email, available_foods)


