from openai import OpenAI
import random


def simulate_forgetting(word, noise_level=0.2):
    """ Simulate forgetting by randomly replacing some characters in the word based on the noise level. """
    word_list = list(word)
    num_chars_to_change = int(len(word) * noise_level)  # Calculate how many characters to change based on noise level
    for _ in range(num_chars_to_change):
        index_to_change = random.randint(0, len(word_list) - 1)
        new_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        word_list[index_to_change] = new_char  # Replace character at randomly chosen position
    return ''.join(word_list)


class StudentAssistant:
    def __init__(self):
        self.client = OpenAI()
        self.assistant = self.create_assistant()

    def create_assistant(self):
        return self.client.beta.assistants.create(
            model="ft:gpt-3.5-turbo-0125:personal:studentagent:9TbYh5oE",
            name="Student Agent",
            description=(
                "This assistant provides the most likely spelling of English words based on the given phonetic transcription and the "
                "specified answer length. Ensure that the spelling is accurate and matches the provided phonetic clues."
            ),
            instructions=(
                "You are an assistant specialized in phonetic transcriptions. When given a phonetic transcription of a word and "
                "the desired length of the answer, provide the most likely spelling of the English word. Ensure that:"
                "1. The spelling accurately matches the provided phonetic transcription."
                "2. The length of the answer matches the desired length."
                "3. You must provide one spelling even if it is a guess."
                "4. The response must be only conclude the spelling of English words without any other information, or symbols, or expression."
            ),
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "simulate_forgetting",
                        "description": "This function simulates the forgetting effect by introducing noise into the given word.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "word": {"type": "string"},
                                "noise_level": {"type": "number"}
                            },
                            "required": ["word", "noise_level"]
                        }
                    }
                }
            ],
            temperature=0,
            top_p=1
        )

    def get_spelling(self, phonemes, answer_length):
        thread = self.client.beta.threads.create()
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"The phonemes are {phonemes}, and the answer length is {answer_length}"
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions="Just give the most likely spelling without other any information."
        )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages:
                return message.content[0].text.value.lower()

        elif run.status == "requires_action":
            # Handle required actions for tool calls
            tool_outputs = []
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "simulate_forgetting":
                    # 假设我们需要从 somewhere 获取原始单词和噪声级别
                    messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                    for message in messages:
                        model_generated_word = message.content[0].text.value.lower()
                        break
                    noise_level = 0.3  # or any appropriate level based on your context
                    forgotten_word = simulate_forgetting(model_generated_word, noise_level)
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": forgotten_word  # 实际输出是处理过的单词
                    })

            # Resubmit tool outputs and poll again
            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                output = []
                for message in messages:
                    output.append(message.content[0].text.value.lower())
                return output
            else:
                return f"Run status after resubmission: {run.status}"
        else:
            return f"Run status: {run.status}"


if __name__ == "__main__":
    student_agent = StudentAssistant()
    words_list = [
        ['k æ n ʌ n', 'c a n n o n'], ['m ʌ ʃ i n', 'm a c h i n e'],
        ['k oʊ p', 'c o p e'], ['ɪ ɡ z ɪ b ɪ t', 'e x h i b i t'],
        ['m i t', 'm e e t'], ['ʌ l aɪ v', 'a l i v e'],
        ['l aɪ b r ɛ r i', 'l i b r a r y'], ['dʒ ɝ n ʌ l', 'j o u r n a l'],
        ['z ɪ r oʊ', 'z e r o'], ['ɪ n v aɪ t', 'i n v i t e'],
        ['ɡ ʊ d b aɪ', 'g o o d b y e'], ['ɪ n f ɝ', 'i n f e r'],
        ['w i k l i', 'w e e k l y'], ['f aɪ v', 'f i v e']
    ]

    for task in words_list:
        answer = student_agent.get_spelling(task[0], len(''.join(task[1].split(' '))))
        print(f"information is {answer[1]}, the given answer is {answer[0]}")

        # url = student_agent.generate_picture(answer)
        # print(url)
