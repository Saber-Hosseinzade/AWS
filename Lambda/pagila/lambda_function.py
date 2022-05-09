import json
import awswrangler as wr
import logging
from urllib.parse import unquote_plus
import sql_create_tables

logger = logging.getLogger()
logger.setLevel(logging.INFO)

con = wr.postgresql.connect("saber-rds-pagila")

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    logger.info(f"---> Bucket name is {bucket}")
    logger.info(f"---> Object key is {key}")
    
    input_path = f"s3://{bucket}/{key}"
    
    key_list = key.split("/")
    database_name = key_list[len(key_list)-2]
    table_name = key_list[len(key_list)-1].split('.')[0]

    output_path = f"s3://{bucket}/staging_zone/{database_name}/{table_name}.parquet"
    logger.info(f"--->  output path is {output_path}")
    
    
    input_df = wr.s3.read_csv([input_path])
    
    database_list = wr.catalog.databases()
    
    if database_name in database_list.values:
        logger.info(f'---> Database {database_name} was already in Glue Catalog')
    else:
        logger.info(f'---> Creating database {database_name}')
        wr.catalog.create_database(database_name) 
        
    
    table_exist = wr.catalog.does_table_exist(database=database_name, table=table_name)
    
    
    result = wr.s3.to_parquet(
        df=input_df,
        path=output_path,
        dataset=True,
        database=database_name,
        table=table_name,
        mode="overwrite"
        )


    with con.cursor() as cursor:
        if table_exist:
            logger.info(f'---> Table {table_name} was already created')
        else:
            logger.info(f'---> Creating table {table_name}')
            cursor.execute(sql_create_tables.sql_dict[f'{table_name}'])
            con.commit()
            
        
        tuples = list(set([tuple(x) for x in input_df.to_numpy()]))
        
        # Comma-separated dataframe columns
        cols = ','.join(list(input_df.columns)) 
        input_cols = ','.join(['%s']*len(list(input_df.columns)))
        
        # SQL query to execute
        query = f"INSERT INTO myschema.{table_name}({cols}) VALUES({input_cols})"

        try:
            cursor.executemany(query, tuples)
            con.commit()

        except Exception as error:
            logger.error(f'---> Error: {error}')
            con.rollback()
    
    logger.info(f"---> SUCCESS: table {table_name} is transfered to postgres")

