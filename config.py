# LLM配置
# LLM_CONFIG = {
#     "type": "deepseek",  # 可选值："deepseek"、"openai"、"ollama"等
#     "model": "deepseek-r1:32b",
#     "key": "EDD7xftr48cwo/CsLZIq5ou8INh1zPk4Om9+R2UhsEo=",
#     "url": "http://221.219.99.97:11434/v1"
# }
LLM_CONFIG = {
    "type": "aliyun",  # 可选值："deepseek"、"openai"、"ollama"等
    "model": "deepseek-r1-distill-qwen-32b",
    "key": "sk-77f9aa7d5ff64d5aaca4489ebcd79260",
    "url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
}

# ChromaDB 配置
CHROMADB_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "save_path": "/Users/wyl/svn/python/disaster-qa/chroma"
}

# MySQL 配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "disaster42"
}