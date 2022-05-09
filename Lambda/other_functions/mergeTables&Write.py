import boto3
import awswrangler as wr
from urllib.parse import unquote_plus
import pandas as pd

conn = wr.postgresql.connect("rds-connection-saber")

def lambda_handler(event=None, context=None):
    
    df_table1 = wr.s3.read_parquet(path='s3://learnit2022-saber-hosseinzade/clean_zone/learnit2022-db/customer-table/customer.parquet/')
    df_table2 = wr.s3.read_parquet(path='s3://learnit2022-saber-hosseinzade/clean_zone/learnit2022-db/city-table/city.parquet/')
    
    df_merge = pd.merge(
        df_table1,
        df_table2,
        how="left",
        left_on='country_id',
        right_on='city_id',
    )
    
    df_merge.drop(['country_id','city_id'],axis=1, inplace=True)
    
    item_count = 0

    with conn.cursor() as cur:

        tuples = list(set([tuple(x) for x in df_merge.to_numpy()]))
        table = 'customers'
        # Comma-separated dataframe columns
        cols = ','.join(list(df_merge.columns))
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % (
            table, cols)
    
        try:
            cur.executemany(query, tuples)
            conn.commit()

        except Exception as error:
            print("Error: %s" % error)
            conn.rollback()
            
    
    
    db_name = 'learnit2022-db-curated'
    table_name = 'join-table'
    output_path = 's3://learnit2022-saber-hosseinzade/curated_zone/learnit2022-db-curated/join-table/customers-join.parquet'
    
    current_databases = wr.catalog.databases()

    
    if db_name not in current_databases.values:

        print(f'- Database {db_name} does not exist ... creating')

        wr.catalog.create_database(db_name)    
    else:

        print(f'- Database {db_name} already exists')
        
    
    result = wr.s3.to_parquet(

        df=df_merge,

        path=output_path,

        dataset=True,

        database=db_name,

        table=table_name,

        mode="overwrite")
    
    
    
            
    return 'data is written to RDS'
