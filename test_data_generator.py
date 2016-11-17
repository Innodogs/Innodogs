"""
Dirty "AGILE" test data generator
"""

import random
import os
from datetime import datetime, timedelta

__author__ = 'Xomak'

locations_count = 100
dogs_count = 1000
custom_significant_events_count = 4
custom_events_counts = 10
users_count = 500
inpayments_count = 250
expenditures_count = 500
add_requests_count = 100
folder = "big_dump"


def clear_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def add_to_file(filename, line):
    with open("{}/{}.sql".format(folder, filename), "a") as text_file:
        text_file.write(line + "\n")


def generate_location(location_index, parent_id):
    query = "INSERT INTO public.location (name, description, parent_id) VALUES ('{name}', '{description}', {parent_id});".format(
        name="Location %s" % location_index,
        description="Description of %s location" % location_index,
        parent_id=parent_id
    )
    add_to_file("innodogs_public_location", query)


def generate_dog(dog_index, is_adopted, location_id):
    query = "INSERT INTO public.dog (is_hidden, name, sex, description, is_adopted, location_id) VALUES ({is_hidden}, '{name}', '{sex}', '{description}', {is_adopted}, {location_id});".format(
        is_hidden="FALSE",
        name="Dog %s" % dog_index,
        description="Description for dog %s" % dog_index,
        sex="male" if random.randint(0, 1) == 1 else "female",
        is_adopted=is_adopted,
        location_id=location_id
    )
    add_to_file("innodogs_public_dog", query)


def generate_event(dog_id, type_id, expenditure_id, datetime):
    query = "INSERT INTO public.event (datetime, description, expenditure_id, event_type_id, dog_id) VALUES ('{datetime}', '{comment}', {expenditure_id}, {type_id}, {dog_id});".format(
        datetime=datetime,
        type_id=type_id,
        comment="Description of event for dog %s with type %s" % (dog_id, type_id),
        dog_id=dog_id,
        expenditure_id=expenditure_id
    )
    add_to_file("innodogs_public_event", query)


def generate_user(user_index):
    query = "INSERT INTO public.\"user\" (google_id, is_volunteer, is_admin, _is_active, name, email) VALUES ('{google_id}', {is_volunteer}, {is_admin}, {is_active}, '{name}', '{email}');".format(
        google_id="googleidforuser%s" % user_index,
        is_volunteer="FALSE",
        is_admin="FALSE",
        is_active="FALSE",
        name="User %s" % user_index,
        email="user%s@example.com" % user_index
    )
    add_to_file("innodogs_public_user", query)


def generate_inpayment(payment_index, user_id, datetime):
    query = "INSERT INTO public.inpayment (amount, datetime, comment, user_id) VALUES ('{amount}', '{datetime}', '{comment}', {user_id});".format(
        amount=random.randint(100, 10000),
        datetime=datetime,
        payment_index=payment_index,
        comment="Inpayment #%s" % payment_index,
        user_id=user_id
    )
    add_to_file("innodogs_public_inpayment", query)


def generate_event_type(type_name, is_significant):
    query = "INSERT INTO public.event_type (type_name, is_significant) VALUES ('{type_name}', {is_significant});" \
        .format(
        type_name=type_name,
        is_significant=is_significant
    )
    add_to_file("innodogs_public_event_type", query)


def generate_expenditure(expenditure_index, datetime):
    query = "INSERT INTO public.expenditure (amount, datetime, comment) VALUES ({amount}, '{datetime}', '{comment}');" \
        .format(
        amount=random.randint(1, 5000),
        datetime=datetime,
        comment="Expenditure #%s" % expenditure_index
    )
    add_to_file("innodogs_public_expenditure", query)


def generate_add_request(request_index, datetime, user_id):
    status = "new" if get_rand_bool() else ("approved" if get_rand_bool() else "rejected")
    query = "INSERT INTO public.add_request (description, datetime, status, comment, user_id) " \
            "VALUES ('{description}', '{datetime}', '{status}', {comment}, {user_id});".format(
        description="Add request %s" % request_index,
        datetime=datetime,
        status=status,
        comment="'Some comment for %s'" % request_index if status == "rejected" else "NULL",
        user_id=user_id
    )
    add_to_file("innodogs_public_add_request", query)


def generate_dog_picture(url, dog_id, add_request_id, is_main):
    query = "INSERT INTO public.dog_picture (uri, dog_id, request_id, is_main) " \
            "VALUES ('{url}', {dog_id}, {add_request_id}, {is_main});".format(
        url=url,
        dog_id=dog_id,
        add_request_id=add_request_id,
        is_main=is_main
    )
    add_to_file("innodogs_public_dog_picture", query)


def get_rand_bool():
    return random.randint(0, 1) == 1


def random_increase(date):
    return date + timedelta(days=random.randint(1, 20),
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59))


class RandomPicture:
    count = 12
    url_template = "http://xomak.net/files/innodogs/{}.jpg"

    def __init__(self):
        self.given = []

    def get_picture(self):
        picture_id = random.randint(1, self.count)
        while picture_id in self.given:
            picture_id = random.randint(1, self.count)
        return self.url_template.format(picture_id)


def generate_all():
    clear_folder(folder)
    start_date = datetime.strptime("2014-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    generate_event_type("Registered", "FALSE")  # 1
    generate_event_type("Sterilized", "TRUE")  # 2
    generate_event_type("Vaccinated", "TRUE")  # 3
    for event_type_index in range(1, custom_events_counts):
        generate_event_type("Simple event %s" % event_type_index, "FALSE")
    for event_type_index in range(1, custom_significant_events_count):
        generate_event_type("Significant event %s" % event_type_index, "TRUE")

    for location_index in range(1, locations_count):
        rand = random.randint(1, location_index)
        if rand == location_index:
            rand = "NULL"
        generate_location(location_index, rand)

    for user_index in range(1, users_count):
        generate_user(user_index)

    date = start_date
    for inpayment_index in range(1, inpayments_count):
        user_id = random.randint(1, users_count - 1) if get_rand_bool() else "NULL"
        date = random_increase(date)
        generate_inpayment(inpayment_index, user_id, date)

    date = start_date
    for expenditure_index in range(1, expenditures_count):
        date = random_increase(date)
        generate_expenditure(expenditure_index, date)

    date = start_date
    for add_request_index in range(1, add_requests_count):
        date = random_increase(date)
        pictures = RandomPicture()
        for picture_index in range(1, 3):
            generate_dog_picture(pictures.get_picture(), "NULL", add_request_index, "FALSE")

        generate_add_request(add_request_index, date, random.randint(1, users_count - 1))

    for dog_index in range(1, dogs_count):
        is_adopted = "TRUE" if random.randint(0, 1) == 1 else "FALSE"
        location_id = random.randint(1, locations_count - 1)
        generate_dog(dog_index, is_adopted, location_id)
        date = random_increase(start_date)
        pictures = RandomPicture()

        def get_expenditure_id():
            return random.randint(1, expenditures_count - 1) if get_rand_bool() else "NULL"

        generate_event(dog_index, 1, "NULL", date)
        if get_rand_bool():
            date = random_increase(date)
            generate_event(dog_index, 2, get_expenditure_id(), date)
        if get_rand_bool():
            date = random_increase(date)
            generate_event(dog_index, 3, get_expenditure_id(), date)

        generate_dog_picture(pictures.get_picture(), dog_index, "NULL", "TRUE")
        for picture_index in range(1, 5):
            generate_dog_picture(pictures.get_picture(), dog_index, "NULL", "FALSE")

        for event_index in range(1, 5):
            if get_rand_bool():
                date = random_increase(date)
                event_type_id = random.randint(4, custom_significant_events_count + custom_events_counts)
                generate_event(dog_index, event_type_id, get_expenditure_id(), date)


generate_all()
