"""
脚本名称：export_doc_txt.py
功能描述：用于从数据库中自动导出所有表名、表注释、字段名、字段注释，生成 data/doc.txt 文本，供后续训练使用。

作者：wyl
创建日期：2025-07-08
"""

import pymysql
import os
from config import DB_CONFIG

OUTPUT_FILE = "data/doc.txt"

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
    SELECT table_name, table_comment
    FROM information_schema.tables
    WHERE table_schema = %s;
""", (DB_CONFIG["database"],))
tables = cursor.fetchall()

os.makedirs("data", exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for table_name, table_comment in tables:
        f.write(f"表 {table_name} {table_comment or '无说明'}\n")

        cursor.execute("""
            SELECT column_name, column_comment
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s;
        """, (DB_CONFIG["database"], table_name))
        columns = cursor.fetchall()

        for column_name, column_comment in columns:
            f.write(f"- {column_name} {column_comment or '无说明'}\n")

        f.write("\n")

cursor.close()
conn.close()
print(f"✅ 已生成 doc.txt 到 {OUTPUT_FILE}")