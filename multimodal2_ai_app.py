import customtkinter as ctk
from tkinter import filedialog
from google import genai
from PIL import Image, ImageTk
import pyttsx3
import os
import threading

# ⚠️ ضع المفتاح السري الخاص بك هنا:
API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# إعداد ثيم الواجهة الحديث (مظهر داكن ولون أزرق مريح)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

client = genai.Client(api_key=API_KEY)
selected_image_path = None

# إعداد محرك نطق الصوت
engine = pyttsx3.init()

def speak_text(text):
    # تشغيل الصوت في خيط منفصل (Thread) لضمان عدم تجميد الواجهة الحديثة
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

def select_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        selected_image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((120, 120))
        img_tk = ImageTk.PhotoImage(img)
        image_label.configure(image=img_tk, text="")
        image_label.image = img_tk
        
        chat_history.configure(state="normal")
        chat_history.insert("end", f"📸 Loaded Image: {os.path.basename(file_path)}\n\n")
        chat_history.configure(state="disabled")
        chat_history.see("end")

def send_message():
    global selected_image_path
    user_text = user_input.get("1.0", "end").strip()
    if not user_text and not selected_image_path:
        return
    
    chat_history.configure(state="normal")
    if user_text:
        chat_history.insert("end", f"You: {user_text}\n\n")
    user_input.delete("1.0", "end")
    chat_history.configure(state="disabled")
    
    # إظهار مؤشر تحميل (Loading) بسيط للمستخدم
    send_button.configure(state="disabled", text="Thinking... 🤖")
    
    def fetch_ai_response():
        global selected_image_path
        try:
            contents = [user_text] if user_text else []
            if selected_image_path:
                img = Image.open(selected_image_path)
                contents.append(img)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
            )
            ai_response = response.text
        except Exception as e:
            ai_response = f"Error: {str(e)}"

        # تحديث الواجهة بعد استقبال الرد
        root.after(0, lambda: update_ui_with_response(ai_response))

    threading.Thread(target=fetch_ai_response, daemon=True).start()

def update_ui_with_response(ai_response):
    global selected_image_path
    chat_history.configure(state="normal")
    chat_history.insert("end", f"Gemini AI:\n{ai_response}\n\n")
    chat_history.configure(state="disabled")
    chat_history.see("end")
    
    # إعادة تهيئة أزرار الواجهة
    selected_image_path = None
    image_label.configure(image="", text="No image selected")
    send_button.configure(state="normal", text="Send & Listen 🚀 🔊")
    
    # نطق الرد صوتياً
    speak_text(ai_response)

# --- بناء الواجهة العصرية باستخدام CustomTkinter ---
root = ctk.CTk()
root.title("Gemini Multimodal AI Assistant")
root.geometry("600x700")

# عنوان النافذة العلوي الفخم
title_label = ctk.CTkLabel(root, text="🤖 Gemini Multimodal AI Assistant", font=ctk.CTkFont(size=20, weight="bold"))
title_label.pack(pady=15)

# صندوق عرض المحادثة المطور والناعم
chat_history = ctk.CTkTextbox(root, width=560, height=380, font=ctk.CTkFont(size=13), activate_scrollbars=True)
chat_history.pack(padx=20, pady=10, fill="both", expand=True)
chat_history.configure(state="disabled")

# منطقة معاينة الصورة المرفوعة
image_label = ctk.CTkLabel(root, text="No image selected", width=560, height=40, fg_color="#2b2b36", corner_radius=8)
image_label.pack(padx=20, pady=10)

# الأزرار والتحكم بتصميم دائري عصري
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(fill="x", padx=20, pady=5)

img_button = ctk.CTkButton(btn_frame, text="📸 Upload Image", command=select_image, font=ctk.CTkFont(weight="bold"), fg_color="#e67e22", hover_color="#d35400")
img_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

user_input = ctk.CTkTextbox(root, width=560, height=60, font=ctk.CTkFont(size=13))
user_input.pack(padx=20, pady=10, fill="x")

send_button = ctk.CTkButton(root, text="Send & Listen 🚀 🔊", command=send_message, font=ctk.CTkFont(size=15, weight="bold"), height=40)
send_button.pack(padx=20, pady=(0, 20), fill="x")

root.mainloop()