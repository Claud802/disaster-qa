# engine/qa_engine.py
from vanna.chromadb import ChromaDB_VectorStore
from engine.llm.llm_deepseek import DeepSeekChat
from config import CHROMADB_CONFIG
from config import DB_CONFIG
import pymysql
import pandas as pd
import re

# 自定义 MySQL Connector
class MySQL_Connector:
    def __init__(self, config):
        self.config = config

    def run_sql(self, sql):
        connection = pymysql.connect(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

class MyVanna(ChromaDB_VectorStore):
    def __init__(self):
        ChromaDB_VectorStore.__init__(self, config={
            "path": CHROMADB_CONFIG["save_path"],   # ✅ 必须是 path
            "collection_name": "disaster-qa",
            "persist": True
        })
        self.llm = DeepSeekChat()
        # ✅设置数据库连接器,使用自定义的 MySQL Connector
        self.db_connector = MySQL_Connector(config=DB_CONFIG)
        self.run_sql = self.db_connector.run_sql

    def extract_sql(self, llm_response):
        # 正常实现，比如用正则提取 SQL
        import re
        matches = re.findall(r"```sql\n(.*?)\n```", llm_response, re.DOTALL)
        if matches:
            return matches[0].strip()
        else:
            return llm_response.strip().splitlines()[-1]

    def ask(self, question: str) -> str:
        # Step 1: 获取最相似的训练数据
        similar_qs = self.get_similar_question_sql(question)

        if similar_qs:
            best_match = similar_qs[0]
            template_sql = best_match.get("sql")
            reference_question = best_match.get("question")

            # Step 2: 让 LLM 替换 SQL 模板变量为真实语句
            messages = [
                self.system_message(
                    "你是一个SQL生成助手。用户会提供一个问题和一个SQL模板。请直接返回最终SQL，不要加任何解释，不要使用<think>标签。"),
                self.user_message(f"用户提问: {question}\n相似问题: {reference_question}\nSQL模板: {template_sql}")
            ]
            generated_sql = self.submit_prompt(messages).strip()

            # Step 3: 执行 SQL 查询并返回最终回答
            try:
                result = self.run_sql(generated_sql)

                # ✅ 格式化返回为用户能理解的自然语言
                if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                    count = list(result[0].values())[0]
                    return f"{question} 答案是：{count} 次"
                else:
                    return f"查询结果：{result}"

            except Exception as e:
                return f"⚠️ 执行SQL时出错：{str(e)}\n\nSQL: {generated_sql}"

        # Step 4: fallback（完全无训练数据）
        return self.submit_prompt([
            self.system_message("你是一个SQL生成助手，请根据提问生成SQL查询语句。"),
            self.user_message(question)
        ])

    def generate_summary(self, question, df):
        # 如果 df 是 list（如 [{"count(*)": 4}]），转成 DataFrame
        if isinstance(df, list):
            df = pd.DataFrame(df)

        messages = [
            {"role": "system", "content": "你是一个善于总结数据的助手。"},
            {"role": "user",
             "content": f"请基于以下数据总结回答这个问题：{question}\n\n{df.head(10).to_markdown(index=False)}"}
        ]
        result = self.llm.submit_prompt(messages)

        if isinstance(result, tuple):
            return result[0]['content']
        elif isinstance(result, str):
            return result
        elif isinstance(result, dict) and 'content' in result:
            return result['content']
        else:
            return str(result)

    def user_message(self, msg): return self.llm.user_message(msg)
    def system_message(self, msg): return self.llm.system_message(msg)
    def assistant_message(self, msg): return self.llm.assistant_message(msg)

    def submit_prompt(self, messages, **kwargs):
        return self.llm.submit_prompt(messages, **kwargs)