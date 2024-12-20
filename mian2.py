import re

def find_shared_nodes(file_path):
    """
    從指定文件中提取 NODE_NAME，並檢查是否有節點同時屬於多個 NET_NAME。

    條件：
    1. NET_NAME 的值以 'P 或 'V 開頭。
    2. NODE_NAME 的節點名稱以 L、U 或 Q 開頭。

    新功能：
    如果一個節點名稱出現在多個 NET_NAME 中，輸出 [NET_NAME1, NET_NAME2, NODE_NAME] 格式。
    只輸出和條件 1 相符的 NET_NAME。

    Args:
        file_path (str): 文件路徑。

    Returns:
        str: 篩選後的結果，每行為 "[NET_NAME1, NET_NAME2, NODE_NAME]" 格式。
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    net_name = ""
    node_to_net_map = {}  # 用於記錄每個節點屬於哪些 NET_NAME

    # 遍歷文件行，提取 NET_NAME 和 NODE_NAME
    for i, line in enumerate(lines):
        if "NET_NAME" in line:
            net_name = lines[i + 1].strip()

        if line.startswith("NODE_NAME") and net_name:
            if (re.search(r"'P.*V.*", net_name) or re.search(r"'V.*", net_name)) and not re.search(r"VR|FB|SW|BST|NTC|SENSE|ZCD|EN|PWRGD|PG|SR|ILM|HOT|ALERT|PWM|COMP", net_name):  # 只處理符合條件的 NET_NAME
                for word in line.split():
                    if word.startswith(("L", "U", "Q", "FB", "CONN", "CN", "R")):
                        if word not in node_to_net_map:
                            node_to_net_map[word] = []
                        node_to_net_map[word].append(net_name)
                        break

    # 處理節點屬於多個 NET_NAME 的情況
    shared_nodes = set()  # 使用 set 來儲存 shared_nodes，避免重複
    for node, nets in node_to_net_map.items():
        if len(nets) > 1:
            unique_nets = list(set(nets))  # 去除 nets 中的重複 NET_NAME
            shared_nodes.add(f"{', '.join(unique_nets)}, {node}")

    # 格式化輸出為字串
    output_str = "\n".join(shared_nodes)  # 將 set 轉回 list
    return output_str

# 測試
file_path = "test.txt"  # 替換為您的文件路徑
result = find_shared_nodes(file_path)
print(result):