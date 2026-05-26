import json
from datetime import datetime
from pathlib import Path

import polars as pl

from src.config import PROJECT_ROOT


def transform_idealista(raw_path: Path) -> Path:
    """Clean and normalize raw Idealista listings into a structured Parquet file."""
    raw = json.loads(raw_path.read_text())

    records = []
    for listing in raw:
        records.append(
            {
                "property_code": listing.get("propertyCode"),
                "operation": listing.get("operation"),
                "property_type": listing.get("propertyType"),
                "price": listing.get("price"),
                "price_by_area": listing.get("priceByArea"),
                "size": listing.get("size"),
                "rooms": listing.get("rooms"),
                "bathrooms": listing.get("bathrooms"),
                "floor": listing.get("floor"),
                "has_lift": listing.get("hasLift"),
                "is_new_development": listing.get("newDevelopment", False),
                "has_parking": listing.get("parkingSpace", {}).get("hasParkingSpace", False),
                "latitude": listing.get("latitude"),
                "longitude": listing.get("longitude"),
                "address": listing.get("address"),
                "municipality": listing.get("municipality"),
                "district": listing.get("district"),
                "neighborhood": listing.get("neighborhood"),
                "province": listing.get("province"),
                "country": listing.get("country"),
                "description_length": len(listing.get("description", "")),
                "has_photos": len(listing.get("multimedia", {}).get("images", [])) > 0,
                "extracted_at": datetime.now().isoformat(),
            }
        )

    df = pl.DataFrame(records)
    df = df.with_columns(
        pl.when(pl.col("size") > 0)
        .then(pl.col("price") / pl.col("size"))
        .otherwise(None)
        .alias("calculated_price_m2"),
    )

    output = PROJECT_ROOT / "data" / "processed" / f"idealista_{datetime.now():%Y%m%d}.parquet"
    output.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output)
    return output
