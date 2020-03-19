from .general import Object, Objects
import datetime

GENDERS = {'female', 'male'}
STATES = ('susceptible', 'exposed', 'infected', 'recovered', 'dead')
SYMPTOMS = {'cough', 'fever', 'stomach ache'}
PRE_EXISTING_CONDITIONS = {'cardiovascular disease', 'diabetes', 'chronic respiratory disease', 'hypertension', 'cancer'}

class Person(Object):
    """Age and gender are important predictors for mortality. Age is a static field."""
    __slots__ = ('age', 'gender', 'state', 'state_start', 'contagiousness', 'symptoms', 'pre_existing_conditions')
    def __init__(self, age=21, gender='female', state=STATES[0], state_start=datetime.datetime.now(),
                 pre_existing_conditions=None):
        self.age = age
        self.state = state
        self.state_start = state_start        
        self.symptoms = set()
        self.gender = gender
        if pre_existing_conditions:
            self.pre_existing_conditions = set(pre_existing_conditions) if isinstance(pre_existing_conditions, (list, tuple)) else {pre_existing_conditions}
        else:
            self.pre_existing_conditions = set()
        self.compute_contagiousness()

    def compute_contagiousness(self):
        """Depending on the age and other features like symptoms, compute the grade of contagiousness, from 0 to 1"""
        if self.age < 20:
            self.contagiousness = .0001  # No documented transmissions, but cannot be excluded
        elif self.age < 25:
            self.contagiousness = ((25 - 20) / 5) * .5
        elif self.age < 27:
            self.contagiousness = .5 + ((27 - 25) / 2) * .5
        else:
            self.contagiousness = 1
        # Limit the contagiousness between 0 and 1, to prevent possible calc errors:
        self.contagiousness = min(max(self.contagiousness, 0), 1)

    def move(self):
        for _ in range(100):
            self.age += 1

class Role(Object):
    pass

class Persons(Objects):
    CLASS = Person
    def move(self):
        for i, person in enumerate(self):
            person.move()
            if i % 100000 == 0:
                print(i)

