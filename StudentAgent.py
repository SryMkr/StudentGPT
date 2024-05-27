"""能够给出具体的拼写"""
# a = [['k æ n ʌ n', 'c a n n o n'], ['m ʌ ʃ i n', 'm a c h i n e'], ['ɑ f l i', 'a w f u l l y'], ['k oʊ p', 'c o p e'],
# ['ɪ ɡ z ɪ b ɪ t', 'e x h i b i t'], ['m i t', 'm e e t'], ['ʌ l aɪ v', 'a l i v e'], ['l aɪ b r ɛ r i', 'l i b r a r y'],
# ['dʒ ɝ n ʌ l', 'j o u r n a l'], ['f ɔ r t i n', 'f o u r t e e n'], ['z ɪ r oʊ', 'z e r o'],
# ['ɪ n v aɪ t', 'i n v i t e'], ['ɡ ʊ d b aɪ', 'g o o d b y e'], ['ɪ n f ɝ', 'i n f e r'],
# ['w i k l i', 'w e e k l y'], ['f aɪ v', 'f i v e']]


from openai import OpenAI


class StudentAssistant:
    def __init__(self):
        self.client = OpenAI()
        self.assistant = self.create_assistant()

    def create_assistant(self):

        return self.client.beta.assistants.create(
            # model="gpt-4o",
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
            tools=[{"type": "code_interpreter"}],
            temperature=0,
            top_p=1
        )

    def get_spelling(self, phonemes, answer_length):
        try:
            thread = self.client.beta.threads.create()

            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=f"The phonemes are {phonemes}, and the answer length is {answer_length}"
            )

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=self.assistant.id,
                instructions="The response must be only conclude the spelling of English words without any other information, or symbols, or expression."
            )

            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                for message in messages:
                    return message.content[0].text.value.lower()
            else:
                return f"Run status: {run.status}"
        except Exception as e:
            return f"An error occurred: {e}"

    def generate_picture(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url


if __name__ == "__main__":
    student_agent = StudentAssistant()
    words_list = [['k æ n ʌ n', 'c a n n o n'], ['m ʌ ʃ i n', 'm a c h i n e'],
                  ['k oʊ p', 'c o p e'],
                  ['ɪ ɡ z ɪ b ɪ t', 'e x h i b i t'], ['m i t', 'm e e t'], ['ʌ l aɪ v', 'a l i v e'],
                  ['l aɪ b r ɛ r i', 'l i b r a r y'],
                  ['dʒ ɝ n ʌ l', 'j o u r n a l'], ['z ɪ r oʊ', 'z e r o'],
                  ['ɪ n v aɪ t', 'i n v i t e'], ['ɡ ʊ d b aɪ', 'g o o d b y e'], ['ɪ n f ɝ', 'i n f e r'],
                  ['w i k l i', 'w e e k l y'], ['f aɪ v', 'f i v e']]

    for task in words_list:
        answer = student_agent.get_spelling(task[0], len(''.join(task[1].split(' '))))
        print(answer)
        # url = student_agent.generate_picture(answer)
        # print(url)


