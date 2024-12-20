import re
import matplotlib.pyplot as plt
import networkx as nx

def find_shared_nodes(file_path):
    """
    從指定文件中提取 NODE_NAME，並檢查是否有節點同時屬於多個 NET_NAME。

    條件：
    1. NET_NAME 的值以 P 或 V 開頭 (忽略 ')。
    2. NODE_NAME 的節點名稱以 L、U 或 Q 開頭。

    如果一個節點名稱出現在多個 NET_NAME 中，輸出 [NET_NAME1, NET_NAME2, NODE_NAME] 格式。
    只輸出和條件 1 相符的 NET_NAME。

    Args:
        file_path (str): 文件路徑。

    Returns:
        list: 篩選後的結果，每個元素為 ["NET_NAME1", "NET_NAME2", "NODE_NAME"] 格式的 list。
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    net_name = ""
    node_to_net_map = {}  # 用於記錄每個節點屬於哪些 NET_NAME
    shared_nodes = []  # 使用 list 來儲存結果

    # 遍歷文件行，提取 NET_NAME 和 NODE_NAME
    for i, line in enumerate(lines):
        if "NET_NAME" in line:
            net_name = lines[i + 1].strip()
            net_name = net_name.replace("'", "")  # 移除 ' 符號

            # 確保 NET_NAME 符合條件才處理 NODE_NAME
            if not (re.search(r"^P.*V.*", net_name) or re.search(r"^V.*", net_name)) or \
               re.search(r"VR|_FB|_SW|_BST|_NTC|SENSE|SEN|_ZCD|_EN|PWRGD|PG|_SR|_ILM|HOT|ALERT|PWM|COMP", net_name):
                net_name = None

        if line.startswith("NODE_NAME") and net_name:
            for word in line.split():
                if word.startswith(("L", "U", "Q", "CONN", "P", "FB", "R")):
                    if word not in node_to_net_map:
                        node_to_net_map[word] = []
                    node_to_net_map[word].append(net_name)
                    break

    # 處理節點屬於多個 NET_NAME 的情況
    for node, nets in node_to_net_map.items():
        if node.startswith(("R")) and len(nets) > 1:  # 針對 R 開頭的節點，只有當它屬於多個 NET_NAME 才加入 shared_nodes
            unique_nets = list(set(nets))
            shared_nodes.append(unique_nets + [node])  # 將結果儲存為 list
        elif not node.startswith(("R")) and len(nets) > 0:  # 其他情況，只要屬於至少一個 NET_NAME 就加入 shared_nodes
            unique_nets = list(set(nets))
            shared_nodes.append(unique_nets + [node])  # 將結果儲存為 list

    def natural_sort(item):
        # 提取排序關鍵字
        key = item[-1]  # 直接使用最後一個元素作為排序關鍵字
        # 將字串中的數字部分轉換為整數，以便進行自然排序
        return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', key)]

    shared_nodes.sort(key=natural_sort)  # 使用自然排序

    return shared_nodes  # 返回 list

def draw_tree(data):
    """
    使用樹狀圖呈現資料

    Args:
        data (list): 每筆資料的 list，例如 ["NET_NAME1", "NET_NAME2", "NODE_NAME"]
    """
    graph = nx.DiGraph()
    graph.add_edges_from([(data[i], data[-1]) for i in range(len(data) - 1)])
    
    # 設定圖形樣式
    pos = nx.spring_layout(graph, seed=42)  # 使用 spring_layout 排版
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, 
            font_color="black", font_weight="bold", arrowsize=20, arrowstyle='->')
    plt.title("樹狀圖呈現")
    plt.show()

# 測試
file_path = "test2.txt"  # 替換為您的文件路徑
result = find_shared_nodes(file_path)

# 逐筆繪製樹狀圖
for item in result:
    draw_tree(item)