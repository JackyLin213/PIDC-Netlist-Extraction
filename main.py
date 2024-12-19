def extract_and_filter(file_path):
    """
    從指定文件中提取符合條件的 NET_NAME 和節點，並過濾重複項目。
    
    條件：
    1. NET_NAME 的值以 'P 或 'V 開頭。
    2. NODE_NAME 的節點名稱以 L 或 U 開頭。
    3. NET_NAME 必須同時包含至少一個 L* 和一個 U* 的節點。

    Args:
        file_path (str): 文件路徑。

    Returns:
        str: 篩選後的結果，每行為 "NET_NAME, 節點名稱" 格式。
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    net_name = ""
    result = []
    net_name_data = {}

    # 遍歷文件行，提取 NET_NAME 和 NODE_NAME
    for i, line in enumerate(lines):
        if "NET_NAME" in line:
            net_name = lines[i + 1].strip()
            if net_name.startswith("'P") or net_name.startswith("'V"):
                net_name_data[net_name] = {'L': False, 'U': False, 'nodes': []}  # 判斷net_name是否有
        
        if line.startswith("NODE_NAME") and net_name in net_name_data:
            for word in line.split():
                if word.startswith("L"):
                    net_name_data[net_name]['L'] = True
                    net_name_data[net_name]['nodes'].append(word)
                elif word.startswith("U"):
                    net_name_data[net_name]['U'] = True
                    net_name_data[net_name]['nodes'].append(word)

    # 篩選出同時包含 L 和 U 節點的 NET_NAME
    for net_name, data in net_name_data.items():
        if data['L'] and data['U']:
            for node in data['nodes']:
                result.append([net_name, node])

    # 過濾重複項目
    filtered_result = []
    for item in result:
        if item not in filtered_result:
            filtered_result.append(item)

    # 格式化輸出為字串
    output_str = "\n".join([f"{item[0]}, {item[1]}" for item in filtered_result])
    return output_str

# 測試
file_path = "test.txt"  # 替換為您的文件路徑
result = extract_and_filter(file_path)
print(result)
