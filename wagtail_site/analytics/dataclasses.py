import dataclasses


@dataclasses.dataclass(frozen=True)
class IPInfo:
    """Class for holding IP information"""
    ip: str
    country: str
    city: str
    region: str
    loc: str
    org: str
    timezone: str
    hostname: str

