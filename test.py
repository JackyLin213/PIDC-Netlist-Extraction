def process_data(data):
    """
    處理資料列表，將包含相同字串的資料重組成新的列表。
    """
    merged_data = []
    for i in range(0, len(data) - 1):
        for j in range(i + 1, len(data)):
            col1 = data[i]
            col2 = data[j]

            # 找到 col1 和 col2 中的共同字串
            common_str = set(col1) & set(col2)

            # 如果有共同字串，則進行重組
            if common_str:
                common_str = common_str.pop()  # 取出共同字串
                connector = col2[-1] if len(col2) == 3 else col1[-1]  # 判斷連接點
                first_item = col2[0] if len(col2) == 3 else col1[0]  # 判斷第一個元素
                last_item = col1[-1] if len(col2) == 3 else col2[-1]  # 判斷最後一個元素

                # 判斷是否為終點
                is_endpoint = len(col1) == 2 if len(col2) == 3 else len(col2) == 2

                merged_data.append([first_item, connector, common_str, last_item, is_endpoint])
    return merged_data

# 範例資料
data = [
    ['P_5V_USB1', 'CONN1'],
    ['P5V_S', 'P_5V_USB1', 'U25'],
    ['P_5V_USB2', 'CONN2'],
    ['P1_CTRLAVDD', 'P1_NIC_3V3', 'FB1'],
    ['P5V_S', 'P_5V_USB2', 'U12']
]

# 呼叫函數
result = process_data(data)

# 打印結果
for row in result:
    print(row)