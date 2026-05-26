from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from src.config import PROJECT_ROOT


class BaseExtractor(ABC):
    name: str = "base"

    def output_path(self, suffix: str = "") -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.name}_{ts}{f'_{suffix}' if suffix else ''}.json"
        path = PROJECT_ROOT / "data" / "raw" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @abstractmethod
    async def extract(self, **kwargs) -> Path:
        """Run extraction and return path to the raw output file."""
        ...
