# 📸 Multimodal AI Desktop Assistant (Voice & Vision) 🤖🔊

An advanced Python desktop application built with Tkinter, utilizing the modern Google Gemini API to process both images and text inputs simultaneously. It features native speech synthesis (text-to-speech) to read back AI responses aloud.

## ✨ Features
* **Vision & Image Understanding:** Upload any image (PNG/JPG) and ask the AI specific questions about its content.
* **Voice Synthesis (TTS):** Integrated with `pyttsx3` to automatically convert the AI's textual responses into spoken voice.
* **Modern GUI Design:** A clean, dark-themed responsive interface optimized for a smooth user experience.

## 🛠️ Tech Stack
* **Language:** Python
* **GUI Library:** Tkinter
* **Image Processing:** Pillow (PIL)
* **Text-to-Speech:** pyttsx3
* **AI Engine:** Google GenAI SDK (`gemini-2.5-flash`)

## 🚀 How to Run the Project
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   ```
2. **Install requirements:**
   ```bash
   pip install google-genai pillow pyttsx3
   ```
3. **Configure API Key:**
   Replace `"YOUR_GEMINI_API_KEY_HERE"` in `multimodal_ai_app.py` with your key from Google AI Studio.
4. **Run application:**
   ```bash
   python multimodal_ai_app.py
   ```

---
*Developed as a capstone project for my AI programming portfolio.*
