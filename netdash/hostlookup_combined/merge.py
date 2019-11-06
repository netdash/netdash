from typing import TypeVar, Generic, List, Dict, Any, Set, Tuple, Callable, Optional
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class SourceValue(Generic[T]):
    source: str
    value: T


SortOrderFunc = Callable[[Any], int]


@dataclass
class MergedCell(Generic[T]):
    values: List[SourceValue[T]]
    sort_order_func: Optional[SortOrderFunc]

    @property
    def valid(self):
        return all(v.value == self.values[0].value for v in self.values[1:])

    @property
    def sort_order(self):
        if not self.valid:
            return 0
        return (
            self.sort_order_func(self.values[0].value)
            if self.sort_order_func
            else None
        )


class MergedRow:
    cells: Dict[str, MergedCell[Any]]

    def __init__(self, sort_order_funcs: Optional[Dict[str, Optional[SortOrderFunc]]], **kwargs):
        sort_order_funcs = sort_order_funcs or {}
        self.cells = {}
        for source, row in kwargs.items():
            if row:
                self.merge(source, row, sort_order_funcs)

    def merge(self, source, row, sort_order_funcs):
        for column, val in row.items():
            if self.cells.get(column, None):
                self.cells[column].values.append(SourceValue(source, val))
            else:
                self.cells[column] = MergedCell([SourceValue(source, val)], sort_order_funcs.get(column))


Row = Dict[str, Any]
Columns = List[
    Tuple[
        str,  # Key name
        str,  # Display name
        Optional[SortOrderFunc]
    ]
]
K = TypeVar('K')


class MergedTable:
    columns: Set[str]
    rows: Dict[K, MergedRow]
    inner_join: bool

    def _create_merged_rows(self, keys: Set[K], indexed_data_sources: Dict[str, Row]) -> Dict[K, MergedRow]:
        sort_order_funcs = {c[0]: c[2] for c in self.columns if len(c) >= 3}
        rows = {}
        for k in keys:
            correlating_rows = {
                source: indexed_data_sources[source].get(k)
                for source in indexed_data_sources.keys()
            }
            if (
                not self.inner_join or
                not any(True for v in correlating_rows.values() if v is None)
            ):
                rows[k] = MergedRow(sort_order_funcs, **correlating_rows)
        return rows

    def __init__(self, pk: str, columns: Columns, inner_join, **data_sources: Dict[str, List[Row]]):
        self.inner_join = inner_join
        self.columns = columns
        keys = set()
        indexed_data_sources = {}
        for (source, data) in data_sources.items():
            indexed_data_sources[source] = {}
            for row in data:
                keys.add(row[pk])
                indexed_data_sources[source][row[pk]] = row
        self.rows = self._create_merged_rows(keys, indexed_data_sources)
