import datetime
import re
import time
import datetime
from logging import getLogger
from random import randint, gauss, random

import pandas as pd

from .external import DataframeLoader

log = getLogger(__name__)


class Population(DataframeLoader):

    def data(self) -> pd.DataFrame:
        """Return a representative population based on the numbers per gender, age and postcode.
        82% of women is a parent, 72% of men. The fields is_child and is_parent are used to set the households."""

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
                            print(i, datetime.datetime.now())
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


class HousedPopulation(DataframeLoader):
    DISABLE_CACHE = False

    def __init__(self, source, distribution):
        self._distribution = distribution
        super().__init__(source)

    def data(self) -> pd.DataFrame:
        """Get the distribution of households per postcode, apply it to the people and assign them to a house.
        At this moment very crude: only round robin assignment of children and simple assignment of mothers and fathers.
        """

        def rows():
            # Set the extra column
            self._source['house'] = 0
            counter = 0
            house_cnt = 0
            for index, row in self._distribution.iterrows():
                # Get each postcode area and set up the houses for families, singles and groups
                people = self._source.loc[self._source.postcode == row.postcode]
                people.sort_values('age', inplace=True)
                houses = {}
                for key, num in (('singles', row.eenpersoonshuishoudens),
                                 ('multiple', row.meerpersoonshuishoudens_zonder_kinderen),
                                 ('families', row.meerpersoonshuishoudens_met_kinderen)):
                    houses[key] = [{'index': i, 'inhabitants': []} for i in range(house_cnt, house_cnt + num)]
                    house_cnt += num
                # First get a pool of children who live at home. 
                children = people[people.is_child]
                parents = people[people.is_parent]
                others = people[~people.is_child & ~people.is_parent]
                # First very simple: just assign children to houses until they are all assigned, in a round robin way.
                fam_houses = houses['families']
                if fam_houses:
                    # Only house children and parents when houses are available. If not, they stay on the street...
                    for i, (index, row1) in enumerate(children.iterrows()):
                        fam_houses[i % len(fam_houses)]['inhabitants'].append(row1)
                    # now assign the parents mothers bottom up and fathers top down
                    # ToDo: reverse sort fathers, because this way 
                    for gender, direction in (('female', 1), ('male', -1)):
                        for i, (index, row1) in enumerate(parents[parents.gender == gender].iterrows()):
                            house_index = i % len(fam_houses) if direction > 0 else (len(fam_houses) - i - 1) % len(fam_houses)
                            houses['families'][house_index]['inhabitants'].append(row1)
                # populate single houses:
                others.sort_values('age', inplace=True)
                single_houses = houses['singles']
                for group, houses_list in ((others.iloc[-len(single_houses):], houses['singles']),
                                           (others.iloc[:-len(single_houses)], houses['multiple'])):
                    if houses_list:
                        for i, (index, row1) in enumerate(group.iterrows()):
                            houses_list[i % len(houses_list)]['inhabitants'].append(row1)
                # Assign the houses back to the source
                for key, house_list in houses.items():
                    for house in house_list:
                        for row2 in house['inhabitants']:
                            row2['house'] = house['index']
                            if counter % 100000 == 0:
                                print(counter, datetime.datetime.now())
                            counter += 1
                            yield row2

        return pd.DataFrame((row for row in rows()), columns=list(self._source.columns) + ['house'])

