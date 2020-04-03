import datetime
import re
import time
from logging import getLogger
from random import randint, gauss, random

import pandas as pd

from .external import DataframeLoader

log = getLogger(__name__)


class PrimarySchoolClasses(DataframeLoader):
    DISABLE_CACHE = False

    def __init__(self, pupils, present=None):
        self._present = present
        super().__init__(pupils)

    def data(self) -> pd.DataFrame:
        """Return locations for all the classes in the supplied primary schools. Simple approximation: only one class 
        per pupil-age, even if 80 pupils in one class..."""

        def rows():
            i = 0
            seen = set()
            # for row in self._source.itertuples(name='Segment'):  Does not work! No column headings!
            for index, row in self._source.iterrows():
                for cell in row.items():
                    r = re.match('leeftijd_(\d+)', cell[0])
                    if not r:
                        continue
                    age = int(r.group(1))
                    if (row.brin_nummer, age) in seen:
                        continue
                    seen.add((row.brin_nummer, age))
                    i += 1
                    yield {'location_id': i,
                           'postcode_target': row.postcode_target}

        return pd.DataFrame((row for row in rows()), columns=('location_id', 'postcode_target'))
