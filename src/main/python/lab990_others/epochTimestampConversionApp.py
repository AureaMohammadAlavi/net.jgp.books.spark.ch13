"""
 Use of from_unixtime() and unix_timestamp().

 @author rambabu.posa
"""
import time
import random
from pyspark.sql import (SparkSession, functions as F)
from pyspark.sql.types import (StructType, StructField,
                               StringType, IntegerType)

# Creates a session on a local master
spark = SparkSession.builder.appName('Timestamp conversion') \
    .master('local[*]').getOrCreate()

#spark.conf.set("spark.sql.session.timeZone", "GMT")

schema = StructType([
    StructField('event', IntegerType(), False),
    StructField('original_ts', StringType(), False)
])

now = int(time.time())

data = []

# Building a df with a sequence of chronological timestamps
for i in range(0,1000):
    data = data + [(i, now)]
    now = now + (random.randint(1,3) + 1)

df = spark.createDataFrame(data, schema)
df.show()
df.printSchema()

# Turning the timestamps to Timestamp datatype
# timestamp, format='yyyy-MM-dd HH:mm:ss')
df = df.withColumn('date', F.from_unixtime(df.original_ts).cast('timestamp'))
df.show(truncate=False)
df.printSchema()

# Turning back the timestamps to epoch
df = df.withColumn('epoch', F.unix_timestamp(df.date))
df.show(truncate=False)
df.printSchema()

# Collecting the result and printing out
timeRows = [row for row in df.collect()]

for row in timeRows:
    print("{} : {} ({})".format(row[0], row[1], row[2]))

spark.stop()