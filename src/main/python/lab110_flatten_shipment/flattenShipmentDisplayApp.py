"""
 Processing of invoices formatted using the schema.org format.

 @author rambabu.posa
"""
import os
from pyspark.sql import (SparkSession, functions as F)

current_dir = os.path.dirname(__file__)
relative_path = "../../../../data/json/shipment.json"
absolute_file_path = os.path.join(current_dir, relative_path)

# Creates a session on a local master
spark = SparkSession.builder.appName("Flatenning JSON doc describing shipments") \
    .master("local[*]").getOrCreate()

# Reads a JSON, stores it in a dataframe
# Dataset[Row] == DataFrame
df = spark.read.format("json") \
        .option("multiline", True) \
        .load(absolute_file_path)

df = df \
    .withColumn("supplier_name", F.col("supplier.name")) \
    .withColumn("supplier_city", F.col("supplier.city")) \
    .withColumn("supplier_state", F.col("supplier.state")) \
    .withColumn("supplier_country", F.col("supplier.country")) \
    .drop("supplier") \
    .withColumn("customer_name", F.col("customer.name")) \
    .withColumn("customer_city", F.col("customer.city")) \
    .withColumn("customer_state", F.col("customer.state")) \
    .withColumn("customer_country", F.col("customer.country")) \
    .drop("customer") \
    .withColumn("items", F.explode(F.col("books")))

df = df \
    .withColumn("qty", F.col("items.qty")) \
    .withColumn("title", F.col("items.title")) \
    .drop("items") \
    .drop("books")

# Shows at most 5 rows from the dataframe (there's only one anyway)
df.show(5, False)
df.printSchema()

df.createOrReplaceTempView("shipment_detail")

sqlQuery = "SELECT COUNT(*) AS bookCount FROM shipment_detail"
bookCountDf = spark.sql(sqlQuery)

bookCountDf.show()

spark.stop()