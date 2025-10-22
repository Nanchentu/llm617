import pandas as pd
import json
from pathlib import Path

# === 路径设置 ===
base = Path(".")  # 当前目录
files = [base / f"topic_{i}.jsonl" for i in range(1, 7)]
rows = []

# === 合并所有 topic 文件 ===
for file in files:
    if not file.exists():
        print(f"⚠️ 跳过未找到的文件: {file}")
        continue

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                topic_id = data.get("topic_id")
                pair_type = str(data.get("pair_type"))
                topic_statement = data.get("topic_statement", "")

                agents = data.get("agents", [])
                A = agents[0] if len(agents) > 0 else {}
                B = agents[1] if len(agents) > 1 else {}

                rounds = data.get("rounds", [])
                round_dict = {}
                for i, r in enumerate(rounds, 1):
                    round_dict[f"round{i}_A"] = r.get("A", "")
                    round_dict[f"round{i}_B"] = r.get("B", "")

                reflection = data.get("reflection", {})
                reflection_A = reflection.get("A", "")
                reflection_B = reflection.get("B", "")

                row = {
                    "topic_id": topic_id,
                    "pair_type": pair_type,
                    "topic_statement": topic_statement,
                    "A_occupation": A.get("occupation", ""),
                    "A_region": A.get("region", ""),
                    "A_pref": A.get("pref", ""),
                    "B_occupation": B.get("occupation", ""),
                    "B_region": B.get("region", ""),
                    "B_pref": B.get("pref", ""),
                    **round_dict,
                    "reflection_A": reflection_A,
                    "reflection_B": reflection_B,
                }
                rows.append(row)
            except Exception as e:
                print(f"Error parsing line in {file.name}: {e}")

# === 生成 CSV ===
df = pd.DataFrame(rows)
output_path = base / "debate_results_llama3.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 合并完成，共 {len(df)} 条记录。已保存至：{output_path.resolve()}")
