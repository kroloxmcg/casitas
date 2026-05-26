import json
import tempfile
from pathlib import Path

from src.transformers.idealista import transform_idealista
from src.transformers.ine import transform_ine


def test_transform_idealista_basic():
    raw = [
        {
            "propertyCode": "123",
            "operation": "sale",
            "propertyType": "flat",
            "price": 200000,
            "size": 80,
            "rooms": 3,
            "bathrooms": 1,
            "floor": "2",
            "latitude": 40.42,
            "longitude": -3.70,
            "municipality": "Madrid",
            "district": "Centro",
            "neighborhood": "Sol",
            "province": "Madrid",
            "country": "es",
            "description": "Piso en el centro",
            "multimedia": {"images": [{"url": "img.jpg"}]},
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(raw, f)
        raw_path = Path(f.name)

    output = transform_idealista(raw_path)
    assert output.exists()
    assert output.suffix == ".parquet"

    import polars as pl

    df = pl.read_parquet(output)
    assert len(df) == 1
    assert df["price"][0] == 200000
    assert df["calculated_price_m2"][0] == 2500.0

    raw_path.unlink()
    output.unlink()


def test_transform_ine_basic():
    raw = {
        "ipv_general": [
            {"periodo": "2024T4", "valor": 112.5},
            {"periodo": "2024T3", "valor": 110.2},
        ],
        "ipv_nueva": [
            {"periodo": "2024T4", "valor": 115.0},
        ],
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(raw, f)
        raw_path = Path(f.name)

    output = transform_ine(raw_path)
    assert output.exists()

    import polars as pl

    df = pl.read_parquet(output)
    assert len(df) == 3
    assert set(df["category"].to_list()) == {"ipv_general", "ipv_nueva"}

    raw_path.unlink()
    output.unlink()
