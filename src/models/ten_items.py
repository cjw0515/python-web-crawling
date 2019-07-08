from dataclasses import dataclass


@dataclass
class TenItem:
    imageURL: str = None
    itemCode: int = None
    itemName: str = None
    itemid_1300k: int = None