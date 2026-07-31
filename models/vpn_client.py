from dataclasses import dataclass
from typing import Optional


@dataclass
class VPNClient:
    id: str
    client_name: str
    protocol: str
    config: Optional[str]
    expires_at: Optional[int]