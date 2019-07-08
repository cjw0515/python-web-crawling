from dataclasses import dataclass


@dataclass
class BestItem:
    category: str = None
    rank: int = None
    imageURL: str = None
    itemCode: int = None
    brand: str = None
    itemName: str = None
    price: int = None
    salePrice: int = None
    numOfReview: int = None
    numOfLike: int = None
    regDate: str = None