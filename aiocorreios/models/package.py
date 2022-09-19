from typing import Union
from dataclasses import dataclass
from .package_type import PackageType


@dataclass
class Package:
    """
    Package model
    """
    package_type: int = PackageType.TYPE_BOX
    width: Union[int, float] = 0
    heigth: Union[int, float] = 0
    length: Union[int, float] = 0
    diameter: Union[int, float] = 0
    weight: Union[int, float] = 0
