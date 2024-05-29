from openai import OpenAI

client = OpenAI()
# 需要有代码来生成需要的数据
file_response = client.files.create(
  file=open("Inputs/batch_abc123.jsonl", "rb"),
  purpose="batch"
)

batch_responses = client.batches.create(
    input_file_id=file_response.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
        "batch_description": "practice batch"
    }
)

# 在控制台下载结果
