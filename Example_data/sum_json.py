import json

# 병합하려는 파일 이름들을 리스트에 넣습니다.
file_paths = ['./json_files_new/P1.json','./json_files_new/P2.json']

merged_data = []

for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        merged_data += data

# 병합된 데이터를 새로운 파일에 저장
with open('./json_sum/train.json', 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile,ensure_ascii=False, indent=4)

with open(f'./json_sum/train.jsonl', 'w', encoding='utf-8') as outfile:
    for entry in merged_data:
        json.dump(entry, outfile ,ensure_ascii=False)
        outfile.write('\n')

