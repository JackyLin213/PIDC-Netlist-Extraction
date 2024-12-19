import re


def extract_and_filter_with_shared_nodes(file_path):
    """
    從指定文件中提取符合條件的 NET_NAME 和節點，並檢查是否有節點同時屬於多個 NET_NAME。

    條件：
    1. NET_NAME 的值以 'P 或 'V 開頭。
    2. NODE_NAME 的節點名稱以 L、U 或 Q 開頭。
    3. NET_NAME 必須同時包含至少一個 L* 和一個 U* 的節點。

    新功能：
    如果一個節點名稱出現在多個 NET_NAME 中，輸出 [NET_NAME1, NET_NAME2, NODE_NAME] 格式。

    Args:
        file_path (str): 文件路徑。

    Returns:
        str: 篩選後的結果，每行為 "NET_NAME, 節點名稱" 或 "[NET_NAME1, NET_NAME2, NODE_NAME]" 格式。
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    net_name = ""
    result = []
    net_name_data = {}  # 不需要 L 和 U 的標記變數
    node_to_net_map = {}  # 用於記錄每個節點屬於哪些 NET_NAME

    # 遍歷文件行，提取 NET_NAME 和 NODE_NAME
    for i, line in enumerate(lines):
        if "NET_NAME" in line:
            net_name = lines[i + 1].strip()
            if re.search(r"'P.*V.*", net_name) or re.search(r"'V.*", net_name):
                net_name_data[net_name] = {'nodes': []}  # 只保留 nodes

        if line.startswith("NODE_NAME") and net_name in net_name_data:
            for word in line.split():
                if word.startswith(("L", "U", "Q", "FB", "CONN", "CN")):
                    if word not in node_to_net_map:
                        node_to_net_map[word] = []
                    node_to_net_map[word].append(net_name)
                    net_name_data[net_name]['nodes'].append(word)
                    break

    # 篩選出同時包含 L 和 U 節點的 NET_NAME
    for net_name, data in net_name_data.items():
        has_l = any(node.startswith("L") for node in data['nodes'])  # 檢查是否有 L* 節點
        has_u = any(node.startswith("U") for node in data['nodes'])  # 檢查是否有 U* 節點
        if has_l and has_u:
            for node in data['nodes']:
                result.append([net_name, node])

    # 處理節點屬於多個 NET_NAME 的情況
    shared_nodes = set()  # 使用 set 來儲存 shared_nodes，避免重複
    for node, nets in node_to_net_map.items():
        if len(nets) > 1:
            unique_nets = list(set(nets))  # 去除 nets 中的重複 NET_NAME
            shared_nodes.add(f"{', '.join(unique_nets)}, {node}")

    # 過濾重複項目
    filtered_result = []
    for item in result:
        if item not in filtered_result:
            filtered_result.append(item)

    # 格式化輸出為字串
    result_lines = [f"{item[0]}, {item[1]}" for item in filtered_result] + list(shared_nodes)  # 將 set 轉回 list
    output_str = "\n".join(result_lines)
    return output_str

# 測試
file_path = "test.txt"  # 替換為您的文件路徑
result = extract_and_filter_with_shared_nodes(file_path)
print(result)