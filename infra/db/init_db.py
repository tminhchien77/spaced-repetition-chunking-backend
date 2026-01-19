from psycopg2 import connect
import os
from dotenv import load_dotenv
import csv
load_dotenv()

def create_schema(database_url=None):
    conn = connect(database_url)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE SCHEMA IF NOT EXISTS application;
    CREATE SCHEMA IF NOT EXISTS  masterdata;


    CREATE TABLE IF NOT EXISTS  "application"."app_user_chunk" (
    "user_chunk_id" serial4 NOT NULL,
    "user_id" int4,
    "chunk_id" int4,
    "chunk_state" varchar(10) COLLATE "pg_catalog"."default",
    "interval_days" float8,
    "ease_factor" float8,
    "recall_streak" int4,
    "forget_count" int4,
    "last_reviewed_at" timestamp(6),
    "next_review_at" timestamp(6),
    "created_user" varchar(20) COLLATE "pg_catalog"."default",
    "created_at" timestamp(6) DEFAULT now(),
    "updated_user" varchar(20) COLLATE "pg_catalog"."default",
    "updated_at" timestamp(6),
    CONSTRAINT "app_user_chunk_pkey" PRIMARY KEY ("user_chunk_id"),
    CONSTRAINT "idx_user_chunk_unique" UNIQUE ("user_id", "chunk_id")
    );


    CREATE TABLE IF NOT EXISTS "masterdata"."md_chunk" (
    "chunk_id" serial4 NOT NULL,
    "chunk" varchar(200) COLLATE "pg_catalog"."default",
    "frequency" int4,
    "createduser" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 'admin'::character varying,
    "createddate" timestamp(6) DEFAULT now(),
    "updateduser" varchar(20) COLLATE "pg_catalog"."default",
    "updateddate" timestamp(6),
    "deleteduser" varchar(20) COLLATE "pg_catalog"."default",
    "deleteddate" timestamp(6),
    "isdeleted" bool DEFAULT false,
    CONSTRAINT "md_chunkphrase_pkey" PRIMARY KEY ("chunk_id")
    );

    CREATE TABLE IF NOT EXISTS  "masterdata"."md_chunk_syntagm" (
    "chunk_syntagm_id" serial4 NOT NULL,
    "chunk_id" int4,
    "keyword" varchar(50) COLLATE "pg_catalog"."default",
    "syntagmid" int4,
    "createduser" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 'admin'::character varying,
    "createddate" timestamp(6) DEFAULT now(),
    "updateduser" varchar(20) COLLATE "pg_catalog"."default",
    "updateddate" timestamp(6),
    "deleteduser" varchar(20) COLLATE "pg_catalog"."default",
    "deleteddate" timestamp(6),
    "isdeleted" bool DEFAULT false,
    CONSTRAINT "md_chunk_syntagm_pkey" PRIMARY KEY ("chunk_syntagm_id")
    );


    CREATE TABLE IF NOT EXISTS  "masterdata"."md_syntagm" (
    "syntagm_id" int4 NOT NULL,
    "syntagm_name" varchar(50) COLLATE "pg_catalog"."default",
    "target_part_of_speech" varchar(50) COLLATE "pg_catalog"."default",
    "createduser" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 'admin'::character varying,
    "createddate" timestamp(6) DEFAULT now(),
    "updateduser" varchar(20) COLLATE "pg_catalog"."default",
    "updateddate" timestamp(6),
    "deleteduser" varchar(20) COLLATE "pg_catalog"."default",
    "deleteddate" timestamp(6),
    "isdeleted" bool DEFAULT false,
    CONSTRAINT "md_syntagm_pkey" PRIMARY KEY ("syntagm_id")
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

def init_data(database_url=None):
    conn = connect(database_url)
    cursor = conn.cursor()

    with open('../../data/md_chunk.csv', 'r') as chunk_file:
        reader = csv.DictReader(chunk_file)
        chunks = list(reader)

        cursor.executemany("""
        INSERT INTO "masterdata"."md_chunk" ("chunk_id", "chunk", "frequency")
        VALUES (%(chunk_id)s, %(chunk)s, %(frequency)s)
        ON CONFLICT (chunk_id) DO NOTHING;
        """, chunks)

    with open('../../data/md_chunk_syntagm.csv', 'r') as chunk_syntagm_file:
        reader = csv.DictReader(chunk_syntagm_file)
        chunks = list(reader)

        cursor.executemany("""
        INSERT INTO "masterdata"."md_chunk_syntagm" ("chunk_syntagm_id", "chunk_id", "keyword", "syntagmid")
        VALUES (%(chunk_syntagm_id)s, %(chunk_id)s, %(keyword)s, %(syntagmid)s)
        ON CONFLICT (chunk_syntagm_id) DO NOTHING;
        """, chunks)

    with open('../../data/md_syntagm.csv', 'r') as syntagm_file:
        reader = csv.DictReader(syntagm_file)
        chunks = list(reader)

        cursor.executemany("""
        INSERT INTO "masterdata"."md_syntagm" ("syntagm_id", "syntagm_name", "target_part_of_speech")
        VALUES (%(syntagm_id)s, %(syntagm_name)s, %(target_part_of_speech)s)
        ON CONFLICT (syntagm_id) DO NOTHING;
        """, chunks)

    conn.commit()
    cursor.close()
    conn.close()

def init_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")

    create_schema(DATABASE_URL)
    init_data(DATABASE_URL)