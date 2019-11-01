from typing import TypeVar, Generic, List, Dict, Any, Set
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class SourceValue(Generic[T]):
    source: str
    value: T


@dataclass
class MergedCell(Generic[T]):
    values: List[SourceValue[T]]

    @property
    def valid(self):
        return all(v.value == self.values[0].value for v in self.values[1:])


class MergedRow:
    cells: Dict[str, MergedCell[Any]]

    def __init__(self, **kwargs):
        self.cells = {}
        for source, row in kwargs.items():
            if row:
                self.merge(source, row)

    def merge(self, source, row):
        for column, val in row.items():
            if self.cells.get(column, None):
                self.cells[column].values.append(SourceValue(source, val))
            else:
                self.cells[column] = MergedCell([SourceValue(source, val)])


Row = Dict[str, Any]
K = TypeVar('K')


class MergedTable:
    columns: Set[str]
    rows: Dict[K, MergedRow]

    @staticmethod
    def _create_merged_rows(keys: Set[K], indexed_data_sources: Dict[str, Dict[str, Any]]) -> Dict[K, MergedRow]:
        rows = {}
        for k in keys:
            correlating_rows = {
                source: indexed_data_sources[source].get(k)
                for source in indexed_data_sources.keys()
            }
            rows[k] = MergedRow(**correlating_rows)
        return rows

    def __init__(self, pk: str, **data_sources: Dict[str, List[Row]]):
        self.columns = set()
        keys = set()
        indexed_data_sources = {}
        for (source, data) in data_sources.items():
            indexed_data_sources[source] = {}
            for row in data:
                self.columns = self.columns | row.keys()
                keys.add(row[pk])
                indexed_data_sources[source][row[pk]] = row
        self.rows = self._create_merged_rows(keys, indexed_data_sources)
