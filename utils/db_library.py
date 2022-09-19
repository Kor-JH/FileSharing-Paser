import sqlite3
from typing import Dict, Optional


def make_contact_table(out_path):
    with sqlite3.connect(out_path) as conn:
        cur = conn.cursor()

        try:
            cur.execute("DROP table contact_list")
        except:
            pass

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_list(
            Platform TEXT, 
            ContactTime TEXT,
            DeviceName TEXT,
            DeviceType TEXT, 
            MACAddr TEXT
            )
        """
        )
        conn.commit()



def insert_contacted_data(row: Dict[str, Optional[str]], out_path):
    conn = sqlite3.connect(out_path)
    with conn:
        cursor = conn.cursor()
        sql = f"""
            INSERT OR REPLACE INTO contact_list VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(
            sql,
            (
                row["platform"],
                row["time"],
                row["name"],
                row["type"],
                row["mac"]
            ),
        )
        conn.commit()


def make_nbu_sharing(out_path):
    with sqlite3.connect(out_path) as conn:
        cur = conn.cursor()

        try:
            cur.execute("DROP table nbu_sharing")
        except:
            pass

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS nbu_sharing(
            EventTime TEXT,
            Event TEXT,
            Device_name TEXT,
            FilePath TEXT,
            FileName TEXT,
            MIMEType TEXT,
            Description TEXT,
            FileSize TEXT
            )
        """
        )
        conn.commit()


def insert_nbu_sharing(row: Dict[str, Optional[str]], out_path):
    conn = sqlite3.connect(out_path)
    with conn:
        cursor = conn.cursor()
        sql = f"""
            INSERT OR REPLACE INTO nbu_sharing VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(
            sql,
            (
                row["time"],
                row["event"],
                row["device_name"],
                row['filepath'],
                row['filename'],
                row['mimetype'],
                row["description"],
                row['filesize']
            ),
        )
        conn.commit()


def make_qs_sharing(out_path):
    with sqlite3.connect(out_path) as conn:
        cur = conn.cursor()

        try:
            cur.execute("DROP table quick_sharing")
        except:
            pass

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS quick_sharing(
            EventTime TEXT,
            Event TEXT,
            Device_id TEXT,
            Device_name TEXT,
            Share_id TEXT,
            FileName TEXT,
            MIMEType TEXT,
            FileSize TEXT,
            Statue TEXT
            )
        """
        )
        conn.commit()


def insert_qs_sharing(row: Dict[str, Optional[str]], out_path):
    conn = sqlite3.connect(out_path)
    with conn:
        cursor = conn.cursor()
        sql = f"""
            INSERT OR REPLACE INTO quick_sharing VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(
            sql,
            (
                row["time"],
                row["event"],
                row["device_id"],
                row['device_name'],
                row['share_id'],
                row['filename'],
                row['mimetype'],
                row['filesize'],
                row['status']
            ),
        )
        conn.commit()




def make_ps_sharing(out_path):
    with sqlite3.connect(out_path) as conn:
        cur = conn.cursor()

        try:
            cur.execute("DROP table ps_sharing")
        except:
            pass

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS ps_sharing(
            EventTime TEXT,
            Event TEXT,
            FileName TEXT,
            FileKey TEXT       
            )
        """
        )
        conn.commit()


def insert_ps_sharing(row: Dict[str, Optional[str]], out_path):
    conn = sqlite3.connect(out_path)
    with conn:
        cursor = conn.cursor()
        sql = f"""
            INSERT OR REPLACE INTO ps_sharing VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(
            sql,
            (
                row["time"],
                row["event"],
                row["filename"],
                row["filekey"]
            ),
        )
        conn.commit()


def make_total_sharing(out_path):
    with sqlite3.connect(out_path) as conn:
        cur = conn.cursor()

        try:
            cur.execute("DROP table total_sharing")
        except:
            pass

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS total_sharing(
            Service TEXT,
            EventTime TEXT,
            Event TEXT,
            Device_name TEXT,
            FileName TEXT
            )
        """
        )
        conn.commit()

def insert_total_sharing(row: Dict[str, Optional[str]], out_path):
    conn = sqlite3.connect(out_path)
    with conn:
        cursor = conn.cursor()
        sql = f"""
            INSERT OR REPLACE INTO total_sharing VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        """
        cursor.execute(
            sql,
            (
                row['service'],
                row["time"],
                row["event"],
                row["device_name"],
                row["filename"]
            ),
        )
        conn.commit()
