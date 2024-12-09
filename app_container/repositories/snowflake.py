import snowflake.connector
import pandas as pd

from config.database_config import snowflake_schema, snowflake_password, snowflake_account, snowflake_database,snowflake_username, snowflake_warehouse


def createClient():
    conn = snowflake.connector.connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    cur = conn.cursor()

    return conn, cur

conn, cur = createClient()
def create(db, collection, document):
    global conn, cur
    columns = str(tuple([i for i in document.keys()])).replace("'","")
    values = tuple(document.values())
    try:
        cur.execute(f"""
            INSERT INTO {collection}
            {columns}
            VALUES {values}
        """)
        conn.commit()
        return get(db, collection, document)
    except Exception as e:
        conn.rollback()
        print(e)
        return {"error": str(e), "status": 500}
    # cur.execute(f"""INSERT INTO 
    #             {collection} 
    #             {str([i for i in document.keys()]).replace('[','(').replace(']',')')}
    #             VALUES {str([i for i in document.values()]).replace('[','(').replace(']',')')}
    # """)
    


def get(db, collection, condition):
    global conn, cur
    query = f"""
        SELECT * FROM {collection} 
        WHERE {" AND ".join([ str([ j for j in condition.keys()][i])+" = " + "'"+str([j for j in condition.values()][i])+"'" for i in  range(len([ j for j in condition.keys()])) ])}
    """
    print(query)
    res = pd.read_sql(query,con=conn).iloc[0].to_dict()
    return res


def fetch(db, collection, condition):
    global conn,cur
    query = f"""
        SELECT * FROM {collection} 
        WHERE {" AND ".join([ str([ j for j in condition.keys()][i])+" = " + "'"+str([j for j in condition.values()][i])+"'" for i in  range(len([ j for j in condition.keys()])) ])}
    """
    print(query)
    res = pd.read_sql(query,con=conn).to_dict(orient="records")
    return res

def fetch_account_queries(db, collection, condition):
    global conn,cur
    query = f"""
        SELECT * FROM {collection} 
        INNER JOIN ORGANIZATION ON ORGANIZATION.ORGANIZATION_ID = DATASOURCE.ORGANIZATION_ID
        WHERE {" AND ".join([ str([ j for j in condition.keys()][i])+" = " + "'"+str([j for j in condition.values()][i])+"'" for i in  range(len([ j for j in condition.keys()])) ])}
        AND DATASOURCE.ORGANIZATION_ID = {condition['organization_id']}
    """
    print(query)
    res = pd.read_sql(query,con=conn).to_dict(orient="records")
    return res

def update(db, collection, document):
    global conn,cur
    return


