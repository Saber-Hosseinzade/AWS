import awswrangler as wr
from urllib.parse import unquote_plus


def lambda_handler(event=None, context=None):
    
    
    # Get the source bucket and object name as passed to the Lambda function

    for record in event['Records']:
        
        bucket = record['s3']['bucket']['name']

        key = unquote_plus(record['s3']['object']['key'])

  
    # We will set the DB and table name based on the last two elements of

    # the path prior to the file name. If key = 'dms/sakila/film/LOAD01.csv',

    # then the following lines will set db to sakila and table_name to 'film'

    key_list = key.split("/")

    print(f'key_list: {key_list}')

    db_name = key_list[len(key_list)-3]

    table_name = key_list[len(key_list)-2]
    
    file_name = key_list[len(key_list)-1].split('.')[0]
    
    print(f'Bucket: {bucket}')

    print(f'Key: {key}')

    print(f'DB Name: {db_name}')

    print(f'Table Name: {table_name}')
    
    print(f'File Name: {file_name}')

    

    input_path = f"s3://{bucket}/{key}"

    print(f'Input_Path: {input_path}')

    output_path = f"s3://{bucket}/clean_zone/{db_name}/{table_name}/{file_name}.parquet"
    


    print(f'Output_Path: {output_path}')
    
    
    input_df = wr.s3.read_csv([input_path])
    
    input_df['first_name']  = input_df.name.apply(lambda x: x.split(" ")[0])
    input_df['last_name']  = input_df.name.apply(lambda x: x.split(" ")[1])
    input_df['email'] = input_df[['first_name','last_name','mail_suffix']].apply(lambda x : f'{x[0]}.{x[1]}@{x[2]}', axis=1)
    input_df.drop(['name','mail_suffix'],axis=1, inplace=True)
    

    

    current_databases = wr.catalog.databases()

    
    if db_name not in current_databases.values:

        print(f'- Database {db_name} does not exist ... creating')

        wr.catalog.create_database(db_name)    
    else:

        print(f'- Database {db_name} already exists')
        
    
    result = wr.s3.to_parquet(

        df=input_df,

        path=output_path,

        dataset=True,

        database=db_name,

        table=table_name,

        mode="overwrite")
        

        
        

    print("RESULT: ")

    print(f'{result}')

    

    return result


