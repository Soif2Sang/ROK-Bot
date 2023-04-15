import flet as ft
import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = "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"

model_id = 'gpt-3.5-turbo'
# response = openai.Completion.create(model="gpt-3.5-turbo", prompt="Say this is a test", temperature=0, max_tokens=7)
# print(response)

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


class ChatAnswer(ft.Container):
    def __init__(self,text:str, **kwargs):
        super().__init__()
        self.content = ft.Text(
                color="white",
                value=text,
                size=22,
                width= 800,
                selectable=True
            )
        self.bgcolor="#00A67E"
        self.alignment = ft.alignment.center_left
        self.margin = ft.margin.only(right=200)


class ChatQuestion(ft.Container):
    def __init__(self,text:str, **kwargs):
        super().__init__()
        self.content=ft.Text(
                text_align=ft.TextAlign.RIGHT,
                color="white",
                value=text,
                size=22,
                width= 800,
                selectable=True
        )
        self.bgcolor="black"
        self.alignment = ft.alignment.center_right
        self.margin = ft.margin.only(left=200)

class Chat(ft.ListView):
    def __init__(self,**kwargs):
        super().__init__()
        self.height = 850
        self.width = 1000
        self.expand = 0
        self.conversation = []
        self.conversation.append({'role': 'system', 'content': 'How may I help you?'})
        self.conversation = ChatGPT_conversation(self.conversation)

    def add_question(self,text):
        self.controls.append(ChatQuestion(text))
        self.controls.append(ft.Divider())

    def add_answer(self,text):
        self.controls.append(ChatAnswer(text))
        self.controls.append(ft.Divider())

class Prompt(ft.TextField):
    def __init__(self,chat,**kwargs):
        super().__init__()
        self.icon = ft.icons.SEND
        self.chat = chat
        self.label = "Type anything.."
        self.width = 1000
        self.on_submit = lambda e:self.send(e)

    def send(self,e):
        print("On submit trigger")
        self.chat.add_question(
            self.value
        )

        self.chat.update()
        self.chat.conversation.append({'role': 'user', 'content': self.value})
        self.value = ""
        self.update()
        self.chat.conversation = ChatGPT_conversation(self.chat.conversation)
        # print(response["choices"][0]["text"])
        # self.chat.add_answer(response["choices"][0]["text"])
        self.chat.add_answer(self.chat.conversation[-1]['content'].strip())
        self.chat.update()


def main(page:ft.Page):
    page.window_width = 1100
    page.window_height = 1000
    page.chat = Chat()
    page.add(page.chat)
    page.prompt = Prompt(page.chat)
    page.add(page.prompt)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)