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
            {"anyo": 2024, "periodo_id": 22, "valor": 112.5, "fecha": 1735686000000},
            {"anyo": 2024, "periodo_id": 21, "valor": 110.2, "fecha": 1727733600000},
        ],
        "ipv_nueva": [
            {"anyo": 2024, "periodo_id": 22, "valor": 115.0, "fecha": 1735686000000},
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
    assert df.filter(pl.col("period") == "2024Q4")["value"][0] == 112.5

    raw_path.unlink()
    output.unlink()
