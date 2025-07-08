import json
from engine.qa_engine import MyVanna

vn = MyVanna()

# 加载训练数据
with open('../data/ddl.sql') as f:
    vn.train(ddl=f.read())

with open('../data/doc.txt') as f:
    docs = [line.strip() for line in f if line.strip()]
    vn.train(documentation=docs)

with open('../data/examples.json') as f:
    examples = json.load(f)
    vn.train(sql=examples)

vn.save()
print("✅ 训练完成并保存")