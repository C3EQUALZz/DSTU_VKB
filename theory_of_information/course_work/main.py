#!/usr/bin/python3
import argparse

# Amazon S3 settings.
# AWS_ACCESS_KEY_ID  in ~/.aws/credentials
# AWS_SECRET_ACCESS_KEY in ~/.aws/credentials
import datetime
import gzip
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from shutil import move
from tempfile import mkstemp

import boto3
import psycopg2
from botocore.config import Config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.settings.config import get_settings

AWS_BUCKET_NAME = "backup.mydomain.com"
AWS_BUCKET_PATH = "postgres/"
BACKUP_PATH = r"D:/PycharmProjects/DSTU_VKB/theory_of_information/course_work/example-of-use/tmp/"


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",  # или https для SSL
        aws_access_key_id="your_username",  # Логин MinIO
        aws_secret_access_key="your_pasword",  # Пароль MinIO
        config=Config(signature_version="s3v4"),  # Требуется для MinIO
        region_name="us-east-1",  # Может быть любым для MinIO
    )


def upload_to_s3(file_full_path, dest_file):
    """
    Upload a file to an AWS S3 bucket.
    """
    s3_client = get_s3_client()

    try:
        s3_client.upload_file(file_full_path, "dump-database", AWS_BUCKET_PATH + dest_file)
        os.remove(file_full_path)
    except boto3.exceptions.S3UploadFailedError as exc:
        print(exc)
        exit(1)


def download_from_s3(backup_s3_key, dest_file):
    """
    Upload a file to an AWS S3 bucket.
    """
    s3_client = boto3.resource("s3")
    try:
        s3_client.meta.client.download_file(AWS_BUCKET_NAME, backup_s3_key, dest_file)
    except Exception as e:
        print(e)
        exit(1)


def list_available_backup():
    key_list = []
    s3_client = boto3.client("s3")
    s3_objects = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=AWS_BUCKET_PATH)

    for key in s3_objects["Contents"]:
        key_list.append(key["Key"])
    return key_list


def list_postgres_databases(host, database_name, port, user, password):
    try:
        pg_bin = Path(r"C:\Program Files\PostgreSQL\17\bin")
        psql_path = pg_bin / "psql.exe"

        process = subprocess.Popen(
            [
                str(psql_path),
                f"--dbname=postgresql://{user}:{password}@{host}:{port}/{database_name}",
                "--list",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            print(f"Command failed. Return code : {process.returncode}")
            exit(1)
        return output
    except Exception as e:
        print(e)
        exit(1)


def backup_postgres_db(host, database_name, port, user, password, dest_file, verbose):
    """
    Backup postgres db to a file.
    """
    if verbose:
        pg_bin = Path(r"C:\Program Files\PostgreSQL\17\bin")
        pg_dump_path = pg_bin / "pg_dump.exe"

        try:
            process = subprocess.Popen(
                [
                    str(pg_dump_path),
                    f"--dbname=postgresql://{user}:{password}@{host}:{port}/{database_name}",
                    "-Fc",
                    "-f",
                    dest_file,
                    "-v",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            dest_path = Path(dest_file)
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            output, error = process.communicate()

            if int(process.returncode) != 0:
                print(f"Command failed. Return code : {process.returncode}")
                print("Error output:", error.decode("utf-8"))
                exit(1)
            return output
        except Exception as e:
            print(e)
            exit(1)
    else:
        try:
            process = subprocess.Popen(
                [
                    "pg_dump",
                    f"--dbname=postgresql://{user}:{password}@{host}:{port}/{database_name}",
                    "-f",
                    dest_file,
                ],
                stdout=subprocess.PIPE,
            )
            output = process.communicate()[0]
            if process.returncode != 0:
                print(f"Command failed. Return code : {process.returncode}")
                exit(1)
            return output
        except Exception as e:
            print(e)
            exit(1)


def compress_file(src_file):
    compressed_file = f"{src_file!s}.gz"
    with open(src_file, "rb") as f_in:
        with gzip.open(compressed_file, "wb") as f_out:
            for line in f_in:
                f_out.write(line)
    return compressed_file


def extract_file(src_file):
    extracted_file, extension = os.path.splitext(src_file)
    print(extracted_file)
    with gzip.open(src_file, "rb") as f_in:
        with open(extracted_file, "wb") as f_out:
            for line in f_in:
                f_out.write(line)
    return extracted_file


def remove_faulty_statement_from_dump(src_file):
    temp_file, _ = tempfile.mkstemp()

    try:
        with open(temp_file, "w+") as dump_temp:
            process = subprocess.Popen(["pg_restore", "-l-v", src_file], stdout=subprocess.PIPE)
            output = subprocess.check_output(("grep", "-v", '"EXTENSION - plpgsql"'), stdin=process.stdout)
            process.wait()
            if int(process.returncode) != 0:
                print(f"Command failed. Return code : {process.returncode}")
                exit(1)

            os.remove(src_file)
            with open(src_file, "w+") as cleaned_dump:
                subprocess.call(["pg_restore", "-L"], stdin=output, stdout=cleaned_dump)

    except Exception as e:
        print(f"Issue when modifying dump : {e}")


def change_user_from_dump(source_dump_path, old_user, new_user):
    fh, abs_path = mkstemp()
    with os.fdopen(fh, "w") as new_file:
        with open(source_dump_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(old_user, new_user))
    # Remove original file
    os.remove(source_dump_path)
    # Move new file
    move(abs_path, source_dump_path)


def restore_postgres_db(db_host, db, port, user, password, backup_file, verbose):
    """
    Restore postgres db from a file.
    """

    if verbose:
        try:
            print(user, password, db_host, port, db)
            process = subprocess.Popen(
                [
                    "pg_restore",
                    "--no-owner",
                    f"--dbname=postgresql://{user}:{password}@{db_host}:{port}/{db}",
                    "-v",
                    backup_file,
                ],
                stdout=subprocess.PIPE,
            )
            output = process.communicate()[0]
            if int(process.returncode) != 0:
                print(f"Command failed. Return code : {process.returncode}")

            return output
        except Exception as e:
            print(f"Issue with the db restore : {e}")
    else:
        try:
            process = subprocess.Popen(
                [
                    "pg_restore",
                    "--no-owner",
                    f"--dbname=postgresql://{user}:{password}@{db_host}:{port}/{db}",
                    backup_file,
                ],
                stdout=subprocess.PIPE,
            )
            output = process.communicate()[0]
            if int(process.returncode) != 0:
                print(f"Command failed. Return code : {process.returncode}")

            return output
        except Exception as e:
            print(f"Issue with the db restore : {e}")


def create_db(db_host, database, db_port, user_name, user_password):
    try:
        con = psycopg2.connect(dbname="postgres", port=db_port, user=user_name, host=db_host, password=user_password)

    except Exception as e:
        print(e)
        exit(1)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(f"DROP DATABASE {database} ;")
    except Exception:
        print("DB does not exist, nothing to drop")
    cur.execute(f"CREATE DATABASE {database} ;")
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {user_name} ;")
    return database


def swap_restore_active(db_host, restore_database, active_database, db_port, user_name, user_password):
    try:
        con = psycopg2.connect(dbname="postgres", port=db_port, user=user_name, host=db_host, password=user_password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute(
            "SELECT pg_terminate_backend( pid ) "
            "FROM pg_stat_activity "
            "WHERE pid <> pg_backend_pid( ) "
            f"AND datname = '{active_database}'"
        )
        cur.execute(f"DROP DATABASE {active_database}")
        cur.execute(f'ALTER DATABASE "{restore_database}" RENAME TO "{active_database}";')
    except Exception as e:
        print(e)
        exit(1)


def swap_restore_new(db_host, restore_database, new_database, db_port, user_name, user_password):
    try:
        con = psycopg2.connect(dbname="postgres", port=db_port, user=user_name, host=db_host, password=user_password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute(f'ALTER DATABASE "{restore_database}" RENAME TO "{new_database}";')
    except Exception as e:
        print(e)
        exit(1)


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    args_parser = argparse.ArgumentParser(description="Postgres database management")
    args_parser.add_argument(
        "--action", metavar="action", choices=["list", "list_dbs", "restore", "backup"], required=True
    )
    args_parser.add_argument("--date", metavar="YYYY-MM-dd", help="Date to use for restore (show with --action list)")
    args_parser.add_argument("--dest-db", metavar="dest_db", default=None, help="Name of the new restored database")
    args_parser.add_argument("--verbose", default=True, help="verbose output")

    args = args_parser.parse_args()

    settings = get_settings()

    postgres_host = settings.database.host
    postgres_port = settings.database.port
    postgres_db = settings.database.name
    postgres_restore = f"{postgres_db}_restore"
    postgres_user = settings.database.user
    postgres_password = settings.database.password
    timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"backup-{timestr}-{postgres_db}.dump"
    filename_compressed = f"{filename}.gz"
    restore_filename = "/tmp/restore.dump.gz"
    restore_uncompressed = "/tmp/restore.dump"
    local_file_path = f"{BACKUP_PATH}{filename}"

    # list task
    if args.action == "list":
        logger.info(f"Listing S3 bucket s3://{AWS_BUCKET_NAME}/{AWS_BUCKET_PATH} content :")
        s3_backup_objects = list_available_backup()
        for key in s3_backup_objects:
            logger.info(f"Key : {key}")
    # list databases task
    elif args.action == "list_dbs":
        result = list_postgres_databases(postgres_host, postgres_db, postgres_port, postgres_user, postgres_password)
        for line in result.splitlines():
            logger.info(line)
    # backup task
    elif args.action == "backup":
        logger.info(f"Backing up {postgres_db} database to {local_file_path}")
        result = backup_postgres_db(
            postgres_host, postgres_db, postgres_port, postgres_user, postgres_password, local_file_path, args.verbose
        )
        for line in result.splitlines():
            logger.info(line)

        logger.info("Backup complete")
        logger.info(f"Compressing {local_file_path}")
        comp_file = compress_file(local_file_path)
        logger.info(f"Uploading {comp_file} to Amazon S3...")
        upload_to_s3(comp_file, filename_compressed)
        logger.info(f"Uploaded to {filename_compressed}")
    # restore task
    elif args.action == "restore":
        if not args.date:
            logger.warn(
                'No date was chosen for restore. Run again with the "list" action to see available restore dates'
            )
        else:
            try:
                os.remove(restore_filename)
            except Exception as e:
                logger.info(e)
            all_backup_keys = list_available_backup()
            backup_match = [s for s in all_backup_keys if args.date in s]
            if backup_match:
                logger.info(f"Found the following backup : {backup_match}")
            else:
                logger.error(f"No match found for backups with date : {args.date}")
                logger.info(f"Available keys : {[s for s in all_backup_keys]}")
                exit(1)

            logger.info(f"Downloading {backup_match[0]} from S3 into : {restore_filename}")
            download_from_s3(backup_match[0], restore_filename)
            logger.info("Download complete")
            logger.info(f"Extracting {restore_filename}")
            ext_file = extract_file(restore_filename)
            # cleaned_ext_file = remove_faulty_statement_from_dump(ext_file)
            logger.info(f"Extracted to : {ext_file}")
            logger.info(f"Creating temp database for restore : {postgres_restore}")
            tmp_database = create_db(postgres_host, postgres_restore, postgres_port, postgres_user, postgres_password)
            logger.info(f"Created temp database for restore : {tmp_database}")
            logger.info("Restore starting")
            result = restore_postgres_db(
                postgres_host,
                postgres_restore,
                postgres_port,
                postgres_user,
                postgres_password,
                restore_uncompressed,
                args.verbose,
            )
            for line in result.splitlines():
                logger.info(line)
            logger.info("Restore complete")
            if args.dest_db is not None:
                restored_db_name = args.dest_db
                logger.info(
                    f"Switching restored database with new one : {postgres_restore} > {restored_db_name}"
                )
                swap_restore_new(
                    postgres_host, postgres_restore, restored_db_name, postgres_port, postgres_user, postgres_password
                )
            else:
                restored_db_name = postgres_db
                logger.info(
                    f"Switching restored database with active one : {postgres_restore} > {restored_db_name}"
                )
                swap_restore_active(
                    postgres_host, postgres_restore, restored_db_name, postgres_port, postgres_user, postgres_password
                )
            logger.info("Database restored and active.")
    else:
        logger.warning("No valid argument was given.")
        logger.warning(args)


if __name__ == "__main__":
    main()
