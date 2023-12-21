import random
import inspect
from utils import (
    generate_num, generate_company_name, generate_ein, generate_ssn, 
    generate_person_name, generate_address, generate_city_state, 
    generate_state, generate_alphanum_code
)

class TextGeneratorFactory:
    def __init__(self):
        # Common generator functions that can be used across different forms
        self.common_generators = {
            'PAYEREIN': lambda _: generate_ein() if random.choice([True, False]) else generate_ssn(),
            'NAMECOMP': lambda _: generate_person_name() if random.choice([True, False]) else generate_company_name(),
            'CITYSTATE': generate_city_state,
            'ADDRESS': generate_address,
            'ALPHANUM': generate_alphanum_code,
            'STABB': generate_state,
            'NUM6': lambda _: generate_num(6),
            'NUM7': lambda _: generate_num(7),
            'NUM50': lambda _: generate_num(50),
            'NUM2': lambda _: generate_num(2),
            'NUM9': lambda _: generate_num(9),
        }

        # Specialized generator functions for specific forms
        # Extend this dictionary when adding new forms, 
        # currently filled with number generation lambda functions, 
        # this is unnecessary and just a placeholder as an example.
        self.form_specific_generators = {
            # 'int1099': {
            #     'NUM6': lambda _: generate_num(6),
            #     'NUM2': lambda _: generate_num(2),
            #     'NUM9': lambda _: generate_num(9),   
            # },
            # 'div1099': {
            #     'NUM6': lambda _: generate_num(6),
            #     'NUM7': lambda _: generate_num(7),
            #     'NUM50': lambda _: generate_num(50),
            #     'NUM2': lambda _: generate_num(2),
            #     'NUM9': lambda _: generate_num(9),  
            # },
            # '1065k1': {
            #     'NUM7': lambda _: generate_num(7),
            #     'NUM9': lambda _: generate_num(9),
                
            # }
            
        }

    def get_generator(self, form_type, keyword):
        # Get the generator function
        generator_function = None
        if keyword in self.form_specific_generators.get(form_type, {}):
            generator_function = self.form_specific_generators[form_type][keyword]
        else:
            generator_function = self.common_generators.get(keyword)

        # Check if the generator function requires an argument
        if generator_function and inspect.signature(generator_function).parameters:
            return lambda _: generator_function(_)
        else:
            return lambda _: generator_function() if generator_function else None