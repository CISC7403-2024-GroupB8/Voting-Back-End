from flask import Flask, request, jsonify
import json
import psycopg2
import logging
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

    cur.close()
    conn.close()

    return jsonify({"message": "Vote successfully recorded."})


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
        percentage = (vote_number / total_votes) * 100 if total_voves > 0 else 0
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


if __name__ == "__main__":
    print("啟動API服務器中...")
    app.run(host="0.0.0.0", port=8000, debug=False)