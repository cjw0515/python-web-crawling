from dataclasses import dataclass


@dataclass
class SearchResultItem:
    itemCode: int = None
    ItemName: str = None
    brandEName: str = None
    brandKName: str = None
    imgURL1: str = None
    imgURL2: str = None
    itemTag: str = None