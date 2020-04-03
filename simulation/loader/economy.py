import datetime
import re
import time
from logging import getLogger
from random import randint, gauss, random

import pandas as pd

from .external import DataframeLoader

log = getLogger(__name__)


class Companies(DataframeLoader):
    """Based on the distribution of company sizes, primary schools per postcode and the population:
     generate a list of companies and company size per postcode. Assign all working people to a location, based on
     the distribution of the primary school pupils.
     Companies are created from large to smaller companies, until all working people have a job at a company."""

    def __init__(self, branch_size: pd.DataFrame, primary_schools: pd.DataFrame, population: pd.DataFrame):
        self._branch_size = branch_size
        self._primary_schools = primary_schools
        self._population = population
        super().__init__(branch_size)  # Have to set _source for naming etc. Also kicks off getting data

    def data(self) -> pd.DataFrame:
        """Return a population with all working people assigned to a company, which has a postcode."""

        # First make a list of schools with number of postcodes from which the pupils come.
        schools = self._primary_schools
        school_region_cnt = schools.groupby([schools.postcode_target, schools.brin_nummer, schools.vestigingsnummer]).postcode_target.count()
        
        def rows():
            i = 0
            # for row in self._source.itertuples(name='Segment'):  Doe not work! No column headings!
            for index, row in self._source.iterrows():
                for cell in row.items():
                    r = re.match('.+?(\d+)\D+?(\d+)', cell[0])
                    if not r:
                        r = re.match('\D+?(\d+)', cell[0])
                    if not r:
                        continue
                    ages = [int(e) for e in r.groups()]
                    if len(ages) == 1:
                        ages.append(ages[0] + 6)
                    ages[-1] -= 1
                    for _ in range(cell[1]):
                        if i % 100000 == 0:
                            print(i, time.time())
                        i += 1
                        age = randint(*ages)
                        is_child = age < 18 or age < gauss(18, 4)
                        is_parent = not is_child and age > gauss(30, 4) and age < gauss(55, 4)
                        if is_parent and \
                                (row.gender == 'male' and random() > .72) or \
                                (row.gender == 'female' and random() > .82):
                            is_parent = False
                        yield {'postcode': row.postcode,
                               'gender': row.gender,
                               'age': age,
                               'is_child': is_child,
                               'is_parent': is_parent}

        return pd.DataFrame((row for row in rows()), columns=('postcode', 'gender', 'age', 'is_child', 'is_parent'))


