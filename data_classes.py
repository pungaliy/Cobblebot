class Times:

    def __init__(self, first_time):
        self.string_times = []
        self.add_time(first_time)

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

    # noinspection PyDictCreation
    def add_time(self, time_name):
        if time_name not in self.string_times:
            self.string_times.append(time_name)


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