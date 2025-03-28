# 💀Whatsapp-Bot💀

## 📜 Description  

This script automates WhatsApp Web messaging using the `pywhatkit` library. It supports:  
✔ **Bulk messaging** (send to multiple contacts).  
✔ **Scheduled or instant messages**.  
✔ **Custom intervals & repetitions**.  
✔ **Media support** (images & videos).  
✔ **CSV import** (upload contact lists).  

It’s designed for automation, making it perfect for reminders, notifications, or announcements!  

## 🚀Step-by-Step Guide in Linux Terminal !

Step 1: Update & upgrade your system  
>sudo apt update  

>sudo apt upgrade  

Step 2: install Dependencies  
>pip install pywhatkit --break-system-packages  

>sudo apt install python3-pandas  

Step 3: Clone the repository  
>git clone https://github.com/The-Real-Virus/Whatsapp-Bot.git  

Step 4: Go to the Tool Directory where u clone it  
>cd Whatsapp-Bot  

Step 5: After Completing the process now u can run script  
>python3 bot.py  

## 🔑 Features  

✅ **Bulk messaging** → Send to multiple contacts.  
✅ **Schedule messages** → Set delivery time per contact.  
✅ **Send images/videos** → Automate media sharing.  
✅ **Instant messaging option** → Send right away.  
✅ **Custom intervals & repetitions** → Avoid spam detection.  
✅ **CSV file support** → Load contact lists easily.  
✅ **Error handling** → Prevents crashes & invalid inputs.  

---

## 💡 Tips !  

- Ensure your **WhatsApp Web is logged in** before running the script.  
- Use **international format** (`+1234567890`) for phone numbers.  
- If using **CSV**, make sure it contains a `Phone` column.  
- **For bulk messaging**, use `sendwhatmsg_instantly()` to avoid long scheduling delays.  
- To send **group messages**, use `sendwhatmsg_to_group()`.  

---

## 🤝 Follow the Prompts !  

### 1️⃣ **Run the Script:**  

### 2️⃣ **Choose Contacts:**
✔ Manually enter numbers **or**  
✔ Upload a CSV file with contacts  

### 3️⃣ **Select Message Type:**  
✔ **Text Message**  
✔ **Image or Video Message**  

### 4️⃣ **Schedule or Send Instantly:**  
✔ Choose time for each contact **or**  
✔ Send instantly with custom delay  

---

## ⚙️ Troubleshooting  

**Issue** | **Solution**  
--- | ---  
Message not sending? | Ensure WhatsApp Web is open and logged in.  
Long delay before sending? | Use `sendwhatmsg_instantly()` instead of `sendwhatmsg()`.  
Error reading CSV? | Ensure the file contains a **"Phone"** column with valid numbers.  
Invalid phone number? | Use **+country_code** (e.g., `+1234567890`).  
Script exits unexpectedly? | Check for missing dependencies (`pip install pywhatkit pandas`).  

---

## 🛠️MODIFICATION 

IF U WANT TO MODIFY OR USE THE SCRIPT IN UR PROJECTs , CONSIDER GIVING CREDITS !  

## 📂 Example Output  

	```
	📞 Enter phone numbers (or type 'done' to finish):  
	+1234567890  
	+9876543210  
	done  

	Enter the message: Hello! This is an automated test message.  
	⏰ Enter the hour (24-hour format, e.g., 14 for 2 PM): 15  
	Enter the minute: 30  
	Enter number of repetitions: 3  
	Enter time interval (in seconds): 10  

	📤 Sending messages...  
	📨 Sending to +1234567890 (Message 1/3)...  
	✅ Message sent successfully!  
	📨 Sending to +9876543210 (Message 1/3)...  
	✅ Message sent successfully!  
	```

# ⚠️Disclaimer !
This tool is intended for ethical and educational use only.  
Do not use it for illegal activities. The author is not responsible for any misuse.  
This script is intended for educational purposes and authorized testing only.  
Unauthorized use of this script is illegal and unethical.  
Ensure you have explicit permission before testing any system.  
- Obtain explicit permission before testing any system.  
- Adhere to all applicable laws and regulations.  
- Respect user privacy and data.  
- By using this script, you agree to take full responsibility for your actions.  
