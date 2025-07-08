import streamlit as st

from engine.qa_engine import MyVanna # 这是你自定义的 Vanna 子类路径
import os, json
import pandas as pd

@st.cache_resource(ttl=3600)
def setup_vanna():
    vn = MyVanna()

    # 加载本地训练数据
    project_root = os.path.dirname(os.path.dirname(__file__))  # 回到项目根目录
    data_dir = os.path.join(project_root, "data")
    ddl_file = os.path.join(data_dir, "ddl.sql")
    doc_file = os.path.join(data_dir, "doc.txt")
    examples_file = os.path.join(data_dir, "examples.json")

    if os.path.exists(ddl_file):
        with open(ddl_file, "r") as f:
            vn.add_ddl(f.read())

    if os.path.exists(doc_file):
        with open(doc_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            vn.add_documentation("\n".join(lines))

    if os.path.exists(examples_file):
        with open(examples_file, "r", encoding="utf-8") as f:
            examples = json.load(f)
            for ex in examples:
                vn.add_question_sql(ex["question"], ex["sql"])

    return vn

@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df):
    vn = setup_vanna()
    # ✅ 转换为 DataFrame，以防是 list
    if isinstance(df, list):
        df = pd.DataFrame(df)
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)