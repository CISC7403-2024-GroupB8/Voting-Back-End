import os
from flask import Flask, request, jsonify
import json
import psycopg2
import logging
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_connection():
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    db_name = os.environ.get("POSTGRES_DB")

    conn = psycopg2.connect(
        host="localhost", database=db_name, user=user, password=password
    )
    return conn


app = Flask(__name__)


def initialize_database():
    """
    初始化数据库，创建表并插入初始数据
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # 创建表的SQL语句
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS votes (
        option_name VARCHAR(50) PRIMARY KEY,
        vote_number INT NOT NULL,
        last_vote TIMESTAMP NOT NULL
    );
    """
    cur.execute(create_table_sql)

    # 插入初始数据的SQL语句
    insert_data_sql = """
    INSERT INTO votes (option_name, vote_number, last_vote) VALUES
    ('Cats', 0, '2024-10-10 00:00:00'),
    ('Dogs', 0, '2024-10-10 00:00:00');
    """
    cur.execute(insert_data_sql)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    option = data["option"]  # 获取投票选项（'cats'或'dogs'等）

    # 连接数据库并更新投票数据
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE votes SET vote_number = vote_number + 1, last_vote = NOW() WHERE name = %s",
        (option,),
    )
    conn.commit()

    # 记录投票日志
    logger.info(f"Vote received for {option} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    cur.close()
    conn.close()

    return jsonify({"message": "Vote successfully recorded."})


@app.route("/results", methods=["GET"])
def get_results():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM votes")
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
                "total_votes": total_votes,  # 新增，可根据需求决定是否保留在返回结果中
            }
        )

    return jsonify(result_data)


if __name__ == "__main__":
    print("啟動API服務器中...")

    # 初始化数据库
    initialize_database()

    app.run(host="0.0.0.0", port=8000, debug=False)
