import random
from faker import Faker
import string

fake = Faker()

def generate_rand_date():
    year = random.randint(2000, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Assuming all months have 28 days to simplify
    return f"{month:02d}/{day:02d}/{year}"

def generate_num(n):
    return str(random.randint(10**(n-1), 10**n - 1))

def generate_company_name():
    return fake.company()

def generate_ein():
    return f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}"

def generate_ssn():
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"

def generate_person_name():
    return fake.name()

def generate_address():
    return fake.address()

def generate_city_state():
    return f"{fake.city()}, {fake.state_abbr()}"

def generate_state():
    return fake.state_abbr()

def generate_alphanum_code():
        length = random.randint(1, 5)
        choices = string.ascii_letters + string.digits
        return ''.join(random.choice(choices) for _ in range(length))
