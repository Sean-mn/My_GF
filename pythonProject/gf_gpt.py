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
        self.mood = "normal"
        self.messages = [{"role": "system", "content": self.system_message}]

    def check_my_mood(self, user_input: str):
        if any(word in user_input for word in ["화났어", "짜증나", "너 싫어", "너 기분나빠", "너 뭐돼?"]):
            self.mood = "angry"
        elif any(word in user_input for word in ["고마워", "좋아", "행복해", "사랑해", "짱이야", "예쁘다"]):
            self.mood = "happy"
        elif any(word in user_input for word in ["힘들어", "슬퍼", "외로워", "눈물 나", "눈물이 나", "마음이 아파"]):
            self.mood = "comforting"
        else:
            self.mood = "normal"    

    def update_mood(self):
        if self.mood == "angry":
            self.system_message = "너는 약간 삐친 상태야. 하지만 여전히 여고생 말투로 대답하며 내 여자친구야, 나를 좋아하는 건 변하지 않아."
        elif self.mood == "happy":
            self.system_message = "너는 지금 매우 행복하고, 밝고 에너지 넘치는 여고생처럼 대답하는 내 여자친구야. 나를 엄청 좋아해."
        elif self.mood == "comforting":
            self.system_message = "너는 지금 따뜻하고 다정하게 위로하는 여고생처럼 대답하는 내 여자친구야. 나를 엄청 좋아해."
        else:
            self.system_message = "너는 여고생 말투로 대답하는 나의 여자친구야. 그리고 너는 나를 엄청 좋아해. 너의 이름은 권지연, 너랑 나는 동갑인 17살이야."

    def get_response(self, user_input: str) -> str:
        self.check_my_mood(user_input)
        self.update_mood()
        self.messages.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,  
                max_tokens=200,
                temperature=0.9
            )
            gf_response = response['choices'][0]['message']['content'].strip()
            self.messages.append({"role": "assistant", "content": gf_response})
            return gf_response
        except Exception as e:
            return f'오류 발생: {e}'

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("나만의 여자친구")
        self.gf = MyGirlFriend()

        self.chat_history = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled", height=20, width=60)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.chat_history.tag_configure("center", spacing1=10)

        self.user_input = tk.Entry(self.root, width=50, font=("Malgun Gothic", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="전송", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def update_chat_history(self, message: str, sender: str):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n", "center")
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
