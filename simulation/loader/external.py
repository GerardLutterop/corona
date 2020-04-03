import re
import time
from logging import getLogger
from pathlib import Path

import pandas as pd

log = getLogger(__name__)


class Loader:
    """Generic loader for data, source can be file or url or whatever"""

    def __init__(self, source):
        self._source = source
        self._df = self.from_source()

    def from_source(self) -> pd.DataFrame:
        raise NotImplementedError

    def __call__(self):
        return self._df

    @classmethod
    def normalized_fieldname(cls, name: str) -> str:
        name = re.sub('\W', '_', name.strip().lower())
        if not re.match('[a-zA-Z_].*', name):
            name = '_' + name
        return name

    @classmethod
    def normalized_fieldnames(cls, names: list) -> list:
        return [cls.normalized_fieldname(name) for name in names]


class CachedLoader(Loader):
    DATA_ROOT_CACHE = Path(__file__).parent / '..' / '..' / 'data' / 'cache'
    DISABLE_CACHE = False

    def from_source(self) -> pd.DataFrame:
        if self.DISABLE_CACHE \
                or not self.filename_cache.exists() \
                or self.filename_cache.stat().st_mtime < self.mtime():
            df = self.data()
            if not self.DISABLE_CACHE:
                try:
                    df.to_feather(self.filename_cache)
                except ValueError:
                    # No indexing supprted; try again:
                    df.reset_index(0, drop=True, inplace=True)
                    try:
                        df.to_feather(self.filename_cache)
                    except:
                        pass
                except Exception as e:
                    log.error(f'Error when saving as feather: {e}')
            df.loader = self
            return df
        # Cache present, read it and return
        try:
            df = pd.read_feather(self.filename_cache)
            df.loader = self
            return df
        except Exception as e:
            try:
                self.filename_cache.unlink()
            except:
                pass
            df = self.data()
            df.loader = self
            return df

    def mtime(self):
        """Modification time of the source. In case of a file, it is mtime, depends on source."""
        return time.time()

    def data(self) -> pd.DataFrame:
        raise NotImplementedError

    @property
    def filename_cache(self) -> Path:
        Path(self.DATA_ROOT_CACHE).mkdir(parents=True, exist_ok=True)
        name = self._source
        if not isinstance(name, str):
            name = type(name).__name__
        return Path(self.DATA_ROOT_CACHE) / f'{name}.{self.__class__.__name__}.feather'


class DataframeLoader(CachedLoader):
    """Source of the loader is another dataframe, for cascading operations."""

    def __init__(self, source):
        self._source: pd.DataFrame = source
        self._df: pd.DataFrame = self.from_source()


    def mtime(self):
        return self._source.loader.mtime()


class FileLoader(CachedLoader):
    DATA_ROOT = Path(__file__).parent / '..' / '..' / 'data'
    FILENAME = NotImplemented

    def __init__(self, filename=None):
        super().__init__(filename or self.FILENAME)

    def mtime(self):
        return self.filename.stat().st_mtime

    def data(self) -> pd.DataFrame:
        raise NotImplementedError('Write file loader')

    @property
    def filename(self) -> Path:
        return Path(self.DATA_ROOT) / self._source


class PostcodeLocation(FileLoader):
    FILENAME = "4pp.csv"

    def data(self):
        return pd.read_csv(self.filename, sep=',')


class PopulationPostcode(FileLoader):
    FILENAME = "BevolkingPerPostcode_1januari2018.xls"

    def df(self):
        df = pd.read_excel(self.filename)
        df.columns = ['postcode'] + list(df.iloc[2].values[1:64]) + list(df.iloc[1].values[64:])
        df.columns = self.normalized_fieldnames(df.columns)
        return df

    def data(self):
        # Now extract ages, gender and numbers:
        df = self.df()
        males = pd.concat([df.iloc[5:, [0]],
                           pd.DataFrame([['male'] for _ in range(len(df.index))], columns=['gender']).iloc[5:, [0]],
                           df.iloc[5:, 23:43]], axis=1)
        females = pd.concat([df.iloc[5:, [0]],
                             pd.DataFrame([['female'] for _ in range(len(df.index))], columns=['gender']).iloc[5:, [0]],
                             df.iloc[5:, 44:64]], axis=1)
        population = females.append(males)
        return population[population.postcode < 10000]


class HouseholdPostcode(PopulationPostcode):
    FILENAME = "BevolkingPerPostcode_1januari2018.xls"

    def data(self):
        df = self.df()
        households = pd.concat([df.iloc[5:, [0]], df.iloc[5:, 68:72]], axis=1)
        return households[households.postcode < 10000]

class DensityPostcode(FileLoader):
    """The number of addresses per postcode-area, the house worth and number of 'uitkeringen' can be retrieved in other sources."""
    FILENAME = "161010-Kenmerken-postcode-mw.xlsx"

    def data(self):
        df: pd.DataFrame = pd.read_excel(self.filename, 'Tabel 1')
        df = df.iloc[4:-2]
        df.columns = ('postcode', 'density')
        return pd.Series(df.density.values, df.postcode, name='density', dtype=float)

class PrimarySchools(FileLoader):
    FILENAME = "03-alle-vestigingen-bo.xls"

    def data(self):
        df = pd.read_excel(self.filename)
        columns = self.normalized_fieldnames(df.columns)
        columns[columns.index('postcode')] = 'postcode_full'
        df.columns = columns
        df['postcode'] = df['postcode_full'].apply(lambda v: int(v[:4]))
        return df

class PrimarySchoolPupils(FileLoader):
    FILENAME = "03-leerlingen-po-totaaloverzicht-2018-2019.csv"

    def data(self):
        df = pd.read_csv(self.filename, sep=';', encoding='ANSI')
        columns = self.normalized_fieldnames(df.columns)
        columns[columns.index('postcode_leerling')] = 'postcode'
        df.columns = columns
        df['postcode_target'] = df['postcode_vestiging'].apply(lambda v: int(v[:4]))
        return df

class EconomyBranchSize(FileLoader):
    FILENAME = "Bedrijven__bedrijfstak_23032020_155149.csv"
    
    def data(self):
        """Return only non-aggregated rows (no totals/subtotals) and skip last two columns (are wrong categories)"""
        df = pd.read_csv(self.filename, sep=';')
        df.columns = self.normalized_fieldnames(df.columns)
        return df[df.apply(lambda row: bool(re.match('[A-Z]\s.*', row.iloc[0])), axis=1)].iloc[:,:-2]