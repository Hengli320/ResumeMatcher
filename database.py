import psycopg2
import sys
import boto3
import os

ENDPOINT="ece1779-project-db.c3400sk0g9qa.us-east-2.rds.amazonaws.com"
PORT="5432"
USER="postgres"
REGION="us-east-2a"
DBNAME="ece1779-project-db"
PASSWORD="Ll20010101"

def get_job_requirements(job_title):
    conn = psycopg2.connect(
        host=ENDPOINT,
        database=USER,
        user=USER,
        password=PASSWORD,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM public.jobs WHERE job_title = %s", (job_title,))
    rows = cur.fetchall()
    conn.close()
    # print(type(rows))
    # print(rows)
    return rows if rows else None


