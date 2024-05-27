"""需要训练一下我给的数据集，也就是音标和单词之间的对应关系训练一个模型，然后用该模型去做预测"""
import json
from openai import OpenAI

# -------------------------------------------训练数据处理为jsonl文件--------------------------------------------------------
words_list = [['k æ n ʌ n', 'c a n n o n'], ['m ʌ ʃ i n', 'm a c h i n e'],
              ['k oʊ p', 'c o p e'],
              ['ɪ ɡ z ɪ b ɪ t', 'e x h i b i t'], ['m i t', 'm e e t'], ['ʌ l aɪ v', 'a l i v e'],
              ['l aɪ b r ɛ r i', 'l i b r a r y'],
              ['dʒ ɝ n ʌ l', 'j o u r n a l'], ['z ɪ r oʊ', 'z e r o'],
              ['ɪ n v aɪ t', 'i n v i t e'], ['ɡ ʊ d b aɪ', 'g o o d b y e'], ['ɪ n f ɝ', 'i n f e r'],
              ['w i k l i', 'w e e k l y'], ['f aɪ v', 'f i v e']]
#
# # 转换为系统、用户、助手格式
# train_data = []
# for phonemes, word in words_list:
#     entry = {
#         "messages": [
#             {"role": "system", "content": "You are an assistant specialized in phonetic transcriptions."},
#             {"role": "user", "content": f"Phonemes: {phonemes}"},
#             {"role": "assistant", "content": word}]
#     }
#     train_data.append(entry)
#
#
# # 保存微调数据到JSONL文件
# with open('inputs/word_list.jsonl', 'w') as f:
#     for entry in train_data:
#         json.dump(entry, f)
#         f.write('\n')
#
# print("Data has been converted and saved to word_list.jsonl")

# -------------------------------------------训练模型--------------------------------------------------------


client = OpenAI()

# file_response = client.files.create(
#   file=open("inputs/word_list.jsonl", "rb"),
#   purpose="fine-tune"
# )
#
# fine_tune_response = client.fine_tuning.jobs.create(
#   training_file=file_response.id,
#   model="gpt-3.5-turbo",
#   suffix="StudentAgent"
# )
# print("Fine-tuning job response:", fine_tune_response)
#

completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal:studentagent:9TbYh5oE",
  messages=[
    {"role": "system", "content": "You are an assistant specialized in phonetic transcriptions"},
    {"role": "user", "content": 'l aɪ b r ɛ r i'}
  ]
)

print(completion.choices[0].message.content)
