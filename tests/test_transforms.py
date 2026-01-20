import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as spark_max, count, lit

@pytest.fixture(scope="session")
def spark():
    """Create a local Spark session for testing."""
    return SparkSession.builder \
        .master("local[*]") \
        .appName("pytest-tests") \
        .getOrCreate()

def test_feeder_aggregation(spark):
    """Test utility1 feeder aggregation logic (group by feeder, max HC, segment count)."""
    # Mock segment data
    data = [
        ("feeder1", 10.5, "2022-10-01"),
        ("feeder1", 12.0, "2022-10-01"),
        ("feeder2", 8.0, "2022-10-02"),
        ("feeder2", 9.5, "2022-10-02")
    ]
    df = spark.createDataFrame(data, ["NYHCPV_csv_NFEEDER", "NYHCPV_csv_NMAXHC", "NYHCPV_csv_FHCADATE"])

    # Your aggregation logic (from notebook)
    aggregated = df.groupBy("NYHCPV_csv_NFEEDER") \
        .agg(
            spark_max("NYHCPV_csv_NMAXHC").alias("max_hosting_capacity_mw"),
            count("*").alias("segment_count")
        )

    result = aggregated.collect()
    
    assert len(result) == 2, "Should have 2 feeders"
    assert result[0]["max_hosting_capacity_mw"] == 12.0, "feeder1 max HC wrong"
    assert result[0]["segment_count"] == 2, "feeder1 segment count wrong"
    assert result[1]["max_hosting_capacity_mw"] == 9.5, "feeder2 max HC wrong"

def test_der_status_filter(spark):
    """Test basic DER status filtering (installed vs planned)."""
    data = [
        ("f1", "Solar", 5.0, "installed"),
        ("f1", "Battery", 10.0, "planned"),
        ("f2", "Wind", 15.0, "installed")
    ]
    df = spark.createDataFrame(data, ["feeder_id", "der_type", "mw", "status"])

    installed_count = df.filter(col("status") == "installed").count()
    planned_count = df.filter(col("status") == "planned").count()

    assert installed_count == 2, "Wrong installed count"
    assert planned_count == 1, "Wrong planned count"

def test_env_schema_generation():
    """Test dynamic schema naming logic (no Spark needed)."""
    env = "qa"
    bronze = f"iedr_{env}_bronze"
    silver = f"iedr_{env}_silver"
    
    assert bronze == "iedr_qa_bronze"
    assert silver == "iedr_qa_silver"
