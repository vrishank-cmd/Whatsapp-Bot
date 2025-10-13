# Whatsapp-Bot

> A simple **Python-based WhatsApp automation bot** built with **PyWhatKit**. It allows you to send **messages**, **images**, and **videos** to individuals or groups — either **scheduled** or **instantly**. This repository is a clean, refactored fork of a similar project and is licensed under MIT.

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Desktop%20%7C%20Laptop-lightgrey">
</p>

## ✨ Features

- Send **text messages** to phone numbers or groups.  
- Send **images** (with optional captions).  
- **Schedule** messages for specific times or send **instantly**.  
- Supports **multiple recipients** (simple list-based looping).  
- Works via **WhatsApp Web**, no Business API required.

> Note: PyWhatKit controls your browser to open `web.whatsapp.com`, select a chat, type, and send messages. Instant-send features may depend on your browser and system automation permissions.

---

## 📦 Requirements

- **Python 3.8+**
- **Google Chrome** or supported default browser
- Already logged into **WhatsApp Web**
- Stable internet connection
- Python package: `pywhatkit` (and dependencies such as `pyautogui`)

---

## 🚀 Installation

```bash
# 1) Clone the repo
git clone https://github.com/ricoagista/Whatsapp-Bot.git
cd Whatsapp-Bot

# 2) (Optional) Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3) Install dependencies
pip install -r Requirements.txt
```

---

## 🧪 Quick Usage

### 1) Send **Instant Message**
```python
import pywhatkit as pwk

pwk.sendwhatmsg_instantly(
    phone_no="+6281234567890",
    message="Hello from Whatsapp-Bot! 🎉",
    wait_time=10,
    tab_close=True,
    close_time=5
)
```

### 2) Send **Scheduled Message**
```python
import pywhatkit as pwk

pwk.sendwhatmsg(
    phone_no="+6281234567890",
    message="Reminder: Meeting at 09:00",
    time_hour=8,
    time_min=59,
    wait_time=15,
    tab_close=True,
    close_time=5
)
```

### 3) Send **Image with Caption**
```python
import pywhatkit as pwk

pwk.sendwhats_image(
    receiver="+6281234567890",
    img_path="poster.png",
    caption="Poster for LSO Kaliber Event 📣",
    wait_time=10,
    tab_close=True,
    close_time=5
)
```

### 4) Send to **Multiple Contacts**
```python
import pywhatkit as pwk
numbers = ["+628111111111", "+628222222222", "+628333333333"]
for no in numbers:
    pwk.sendwhatmsg_instantly(no, "Hello! Bulk message from Whatsapp-Bot.", 10, tab_close=True, close_time=5)
```

---

## 🗂️ Project Structure

```
Whatsapp-Bot/
├─ bot.py              # main script (can be turned into CLI)
├─ Requirements.txt    # dependencies
└─ LICENSE             # MIT License
```

---

## ⚙️ Best Practices

- **Keep screen awake** during scheduled sends.  
- **Include country code** (e.g., `+62` for Indonesia).  
- **Browser focus** may be needed for send confirmation.  
- **Test with your own number** before bulk sending.  
- Add **retry logic** for mass sending to avoid failed deliveries.

---

## ❗ Limitations

- Uses **UI automation** on WhatsApp Web — UI changes may affect functionality.  
- Some users report instant send stopping after typing; pressing Enter manually may help.  
- Use responsibly and comply with **WhatsApp Terms of Service**.

---

## 🧰 Future Plans

- [ ] Add CLI support (`python bot.py --file contacts.csv --msg "..." --mode instant`)
- [ ] Add message templates (`{name}`, `{date}`, etc.)
- [ ] Random delay generator to mimic human typing
- [ ] Logging & success/failure reports

---

## 🤝 Contribution

1. Fork this repo & create a new branch: `git checkout -b feat/new-feature`  
2. Commit changes: `git commit -m "feat: add something"`  
3. Push to branch: `git push origin feat/new-feature`  
4. Create a Pull Request.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

## 🙏 Credits

- **PyWhatKit** – main library for WhatsApp Web automation  
- This repo is a cleaned-up, extended fork

---

## 🔗 References

- [PyWhatKit GitHub](https://github.com/Ankit404butfound/PyWhatKit)
- [PyPI – PyWhatKit](https://pypi.org/project/pywhatkit/)
- [Documentation](https://github.com/Ankit404butfound/PyWhatKit/wiki)
