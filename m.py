# 設定文字檔路徑
file_path = "test3.txt"  # 將 "data.txt" 替換為實際的檔案路徑

# 從文字檔讀取資料並處理
with open(file_path, "r") as f:
    data = [line.strip().strip("[]").replace("'", "").split(",") for line in f]

# 建立 Mermaid 語法
graph = "graph TD\n"
for row in data:
    row = [item.strip() for item in row]  # 去除額外的空白
    end_point = row[-1]  # 取得終點
    for start_point in row[:-1]:  # 除了終點的所有起點
        graph += f"    {start_point} --- {end_point}\n"

# 輸出結果
print(graph)

# 可將生成的 Mermaid 語法存入檔案
output_path = "output.mmd"  # 生成的 Mermaid 語法文件路徑
with open(output_path, "w") as f:
    f.write(graph)

print(f"Mermaid 語法已儲存至 {output_path}")
