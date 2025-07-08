from engine.qa_engine import MyVanna
from config import DB_CONFIG
import pymysql

def ask(question: str):
    vn = MyVanna()
    sql = vn.ask(question)
    print("🧠 生成SQL:", sql)

    conn = pymysql.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
    conn.close()
    return result

# 测试入口
if __name__ == '__main__':
    q = input("请输入你的问题: ")
    print(ask(q))