from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class GlobalInfo(BaseModel):
    alpha2: str
    alpha3: str
    numeric_code: str
    region: str
    subregion: str
    region_code: str
    subregion_code: str
    world_region: str
    continent_name: str
    continent_code: str

class DialInfo(BaseModel):
    calling_code: str
    national_prefix: str
    international_prefix: str

class Currency(BaseModel):
    symbol: str
    code: str
    name: str
    numeric: int
    minor_unit: int

class CountryModule(BaseModel):
    latitude: float
    longitude: float
    common_name: str
    official_name: str
    capital: str
    flag: str
    area: int
    landlocked: bool
    independent: bool
    global_info: GlobalInfo
    dial: DialInfo
    currencies: List[Currency]
    languages: Dict[str, str]

class SunTimes(BaseModel):
    time: int
    astronomical: int
    civil: int
    nautical: int

class SunModule(BaseModel):
    rise: SunTimes
    set: SunTimes
    transit: int

class TimezoneModule(BaseModel):
    name: str
    offset_sec: int
    offset_string: str

class LocationData(BaseModel):
    latitude: float
    longitude: float
    type: str
    name: str
    number: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    confidence: float
    region: str
    region_code: str
    county: str
    locality: str
    administrative_area: Optional[str] = None
    neighbourhood: Optional[str] = None
    country: str
    country_code: str
    continent: str
    label: str
    bbox_module: List[float]
    country_module: CountryModule
    sun_module: SunModule
    timezone_module: TimezoneModule

class LocationResponse(BaseModel):
    data: List[LocationData] 