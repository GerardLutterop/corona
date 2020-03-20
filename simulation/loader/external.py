from pathlib import Path
import re
import os
from logging import getLogger

import pandas as pd

log = getLogger(__name__)

class Loader:
    """Generic loader for data, source can be file or url or whatever"""

    def __init__(self, source):
        self._source = source
        self._df = self.from_source()

    def from_source(self):
        raise NotImplementedError

    def __call__(self):
        return self._df

    @staticmethod
    def normalize_fieldname(name: str) -> str:
        name = re.sub('\W', '_', name.strip())
        if not re.match('[a-zA-Z_].*', name):
            name = '_' + name
        return name


class FileLoader(Loader):
    DATA_ROOT = Path(os.getcwd()) / '..' / '..' / 'data'
    DATA_ROOT_CACHE = DATA_ROOT / 'cache'
    FILENAME = NotImplemented
    DISABLE_CACHE = False

    def __init__(self, filename=None):
        super().__init__(filename or self.FILENAME)

    def from_source(self):
        if self.DISABLE_CACHE \
                or not self.filename_cache.exists() \
                or self.filename_cache.stat().st_mtime < self.filename_data.stat().st_mtime:
            df = self.from_file()
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
            return df
        # Cache present, read it and return
        try:
            return pd.read_feather(self.filename_cache)
        except Exception as e:
            try:
                self.filename_cache.unlink()
            except:
                pass
            return self.from_file()

    def from_file(self) -> pd.DataFrame:
        raise NotImplementedError

    @property
    def filename_data(self) -> Path:
        return Path(self.DATA_ROOT) / self._source

    @property
    def filename_cache(self) -> Path:
        Path(self.DATA_ROOT_CACHE).mkdir(parents=True, exist_ok=True)
        return Path(self.DATA_ROOT_CACHE) / (self._source + '.feather')


class PostcodeLocation(FileLoader):
    FILENAME = "4pp.csv"

    def from_file(self):
        return pd.read_csv(self.filename_data, sep=',')


class PopulationPostcode(FileLoader):
    FILENAME = "BevolkingPerPostcode_1januari2018.xls"
    DISABLE_CACHE = False

    def from_file(self):
        df = pd.read_excel(self.filename_data)
        df.columns = ['postcode'] + list(df.iloc[2].values[1:64]) + list(df.iloc[1].values[64:])
        df.columns = [self.normalize_fieldname(e) for e in df.columns]
        # Now extract ages, numbers and household sizes:
        males = pd.concat([df.iloc[5:, [0]], df.iloc[5:, 23:43]], axis=1)
        females = pd.concat([df.iloc[5:, [0]], df.iloc[5:, 44:64]], axis=1)
        households = pd.concat([df.iloc[5:, [0]], df.iloc[5:, 68:72]], axis=1)
        return males
        return males, females, households

if __name__ == '__main__':
    pcl = PostcodeLocation()()
    pcp = PopulationPostcode()()
    print(pcl, pcp)
