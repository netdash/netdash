from typing import TypeVar, Generic, List, Dict, Any
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class SourceValue(Generic[T]):
    source: str
    value: T

    def __str__(self):
        return f'{self.source}: {str(self.value)}'


@dataclass
class MergedColumn(Generic[T]):
    values: List[SourceValue[T]]

    @property
    def valid(self):
        return all(v.value == self.values[0].value for v in self.values[1:])

    def __str__(self):
        return self.values[0].value if self.valid else '\n'.join(self.values)


class MergedRow:
    columns: Dict[str, MergedColumn[Any]]

    def __init__(self, **kwargs):
        self.columns = {}
        for source, row in kwargs.items():
            self.merge(source, row)

    def merge(self, source, row):
        for column, val in row.items():
            if self.columns.get(column, None):
                self.columns[column].values.append(SourceValue(source, val))
            else:
                self.columns[column] = MergedColumn([SourceValue(source, val)])
