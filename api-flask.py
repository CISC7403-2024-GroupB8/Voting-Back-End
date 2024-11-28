import psycopg2
# 需要使用 pip install psycopg2-binary
from flask import Flask, request
import logging
import json
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="your_database_name",
        user="your_username",
        password="your_password",
    )
    return conn


# 投票微服务API
# 处理投票请求
app = Flask(__name__)


@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    option = data["option"]  # 获取投票选项（'cats'或'dogs'等）

    # 连接数据库并更新投票数据
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE your_table_name SET vote_number = vote_number + 1, last_vote = NOW() WHERE name = %s",
        (option,),
    )
    conn.commit()

    # 记录投票日志
    logger.info(f"Vote received for {option} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 数据库操作等其他代码...

    cur.close()
    conn.close()

    return "Vote successfully recorded."


# 结果微服务API
@app.route("/results", methods=["GET"])
def get_results():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM your_table_name")
    results = cur.fetchall()
    cur.close()
    conn.close()

    total_votes = sum(row[1] for row in results)
    result_data = []
    for row in results:
        option_name = row[0]
        vote_number = row[1]
        percentage = (vote_number / total_votes) * 100 if total_votes > 0 else 0
        last_vote = row[2]
        result_data.append(
            {
                "option": option_name,
                "vote_number": vote_number,
                "percentage": percentage,
                "last_vote": last_vote,
            }
        )

    return jsonify(result_data)


@app.route("/", methods=["GET"])
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    print("啟動API服務器中...")
    # 記得允許防火墻開放端口：sudo ufw allow 6111
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=6111, reload=False)
