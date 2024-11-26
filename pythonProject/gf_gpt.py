import openai
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import scrolledtext

load_dotenv(dotenv_path="C:/Users/USER/Desktop/pythonProject/OPENAI_API_KEY.env")

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("API키가 설정되지 않음")
else:
    print('API키 확인')

class MyGirlFriend:
    def __init__(self, model="gpt-4o-mini", system_message="너는 여고생 말투로 대답하는 나의 여자친구야. 그리고 너는 나를 엄청 좋아해. 너의 이름은 권지연, 너랑 나는 동갑인 17살이야."):
        self.model = model
        self.system_message = system_message

    def get_response(self, user_input: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=200,
                temperature=0.9
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f'오류 발생: {e}'

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("나만의 여자친구")
        self.gf = MyGirlFriend()

        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled", height=20, width=60)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.user_input = tk.Entry(self.root, width=50, font=("Malgun Gothic", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="전송", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def update_chat_history(self, message: str, sender: str):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        self.chat_history.yview(tk.END)
        self.chat_history.config(state='disabled')

    def send_message(self, event=None):
        user_input = self.user_input.get().strip()
        if not user_input: return

        self.update_chat_history(user_input, "나")
        self.user_input.delete(0, tk.END)

        response = self.gf.get_response(user_input)
        self.update_chat_history(response, "여자친구")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    chat_ui = UI()
    chat_ui.run()