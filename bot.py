import pywhatkit
import pandas as pd
import time
import re
import os
import logging
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(filename='whatsapp_bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to display banner
def show_banner():
    banner = r"""
                       ______
                    .-"      "-.
                   /  *ViRuS*   \
       _          |              |          _
      ( \         |,  .-.  .-.  ,|         / )
       > "=._     | )(_0_/\_0_)( |     _.=" <
      (_/"=._"=._ |/     /\     \| _.="_.="\_)
             "=._ (_     ^^     _)"_.="
                 "=\__|IIIIII|__/="
                _.="| \IIIIII/ |"=._
      _     _.="_.="\          /"=._"=._     _
     ( \_.="_.="     `--------`     "=._"=._/ )
      > _.="                            "=._ <
     (_/                                    \_)
 ____________________________________________________
 ----------------------------------------------------        
        #  Whatsapp-Bot
        #  Author : The-Real-Virus
        #  https://github.com/The-Real-Virus
 ____________________________________________________
 ----------------------------------------------------
"""
    print(banner)

# Show banner at script startup
show_banner()

# Ask user for input
choice = input("\nPress 'y' to continue or 'n' to exit: ").strip().lower()

if choice == 'n':
    print("\nExiting the script. Goodbye!")
    exit()
elif choice == 'y':
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen on Linux/Mac ('clear') or Windows ('cls')
else:
    print("\nInvalid choice. Exiting the script.")
    exit()

def logo():
    logo = r"""
██╗    ██╗██╗  ██╗ █████╗ ████████╗███████╗ █████╗ ██████╗ ██████╗       ██████╗  ██████╗ ████████╗
██║    ██║██║  ██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗      ██╔══██╗██╔═══██╗╚══██╔══╝
██║ █╗ ██║███████║███████║   ██║   ███████╗███████║██████╔╝██████╔╝█████╗██████╔╝██║   ██║   ██║   
██║███╗██║██╔══██║██╔══██║   ██║   ╚════██║██╔══██║██╔═══╝ ██╔═══╝ ╚════╝██╔══██╗██║   ██║   ██║   
╚███╔███╔╝██║  ██║██║  ██║   ██║   ███████║██║  ██║██║     ██║           ██████╔╝╚██████╔╝   ██║   
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝           ╚═════╝  ╚═════╝    ╚═╝   
                                                                                                                                                                               
"""
    print(logo)

def validate_phone_number(number: str) -> bool:
    """Validate phone number format (basic validation for international format)."""
    pattern = r"^\+\d{10,15}$"  # Matches + followed by 10-15 digits
    return re.match(pattern, number) is not None

def get_scheduled_time():
    """Ensure the user enters a valid future time for message scheduling."""
    while True:
        try:
            hour = int(input("Enter the hour (24-hour format, e.g., 14 for 2 PM): "))
            minute = int(input("Enter the minute: "))

            now = datetime.now()
            scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the scheduled time is in the past, move it to the next day
            if scheduled_time < now:
                scheduled_time += timedelta(days=1)

            return scheduled_time.hour, scheduled_time.minute
        except ValueError:
            print("⚠️ Invalid input! Please enter numeric values for hour and minute.")

def get_phone_numbers():
    """Get a list of phone numbers from user input or CSV file."""
    numbers = []
    choice = input("Do you want to upload a CSV file with numbers? (yes/no): ").strip().lower()

    if choice == "yes":
        file_path = input("Enter the path to the CSV file: ").strip()
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                numbers = df['Phone'].dropna().astype(str).tolist()
                print(f"✅ Loaded {len(numbers)} contacts from CSV.")
            except Exception as e:
                print(f"❌ Error reading CSV: {e}")
        else:
            print("❌ File not found. Switching to manual entry.")
    
    if not numbers:
        print("\n📞 Enter phone numbers (with country code). Type 'done' when finished:")
        while True:
            number = input("Enter number (e.g., +1234567890): ").strip()
            if number.lower() == "done":
                break
            if validate_phone_number(number):
                numbers.append(number)
            else:
                print("⚠️ Invalid format! Use + followed by country code and number.")
    
    return numbers if numbers else None

def get_message_type():
    """Ask user whether to send text, image, or video."""
    while True:
        choice = input("What do you want to send? (1) Text (2) Image (3) Video: ").strip()
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("⚠️ Invalid choice! Enter 1, 2, or 3.")

def get_media_path():
    """Ask for image or video path if needed."""
    while True:
        path = input("Enter the file path: ").strip()
        if os.path.exists(path):
            return path
        print("❌ File not found! Try again.")

def main():
    print("\n📲 **Automated WhatsApp Message Sender** 📩\n")

    # Get list of phone numbers
    numbers = get_phone_numbers()
    if not numbers:
        print("⚠️ No valid numbers provided! Exiting.")
        return

    # Get message type
    msg_type = get_message_type()

    if msg_type == 1:  # Text message
        message = input("Enter the message you want to send: ").strip()
        if not message:
            print("⚠️ Message cannot be empty!")
            return
        media_path = None
    else:  # Image or Video message
        media_path = get_media_path()
        message = input("Enter the caption for the media (or press Enter to skip): ").strip()

    # Get per-contact scheduling
    print("\n⏳ Scheduling messages for each contact...")
    schedule_times = {}
    for mobile in numbers:
        print(f"\n⏰ Set time for {mobile}")
        hour, minute = get_scheduled_time()
        schedule_times[mobile] = (hour, minute)

    # Get number of repetitions
    while True:
        try:
            repeat_count = int(input("Enter how many times you want to send the message: "))
            if repeat_count <= 0:
                print("⚠️ Please enter a valid number greater than 0.")
            else:
                break
        except ValueError:
            print("⚠️ Please enter a valid number.")

    # Get interval between messages (in seconds)
    while True:
        try:
            interval = int(input("Enter time interval between messages (in seconds): "))
            if interval <= 0:
                print("⚠️ Please enter a valid interval greater than 0 seconds.")
            else:
                break
        except ValueError:
            print("⚠️ Please enter a valid number.")

    print(f"\n📤 Sending messages to {len(numbers)} contacts...\n")

    try:
        for mobile in numbers:
            hour, minute = schedule_times[mobile]
            print(f"📨 Sending messages to {mobile} starting at {hour}:{minute}...")

            for i in range(repeat_count):
                print(f"📨 Sending message {i+1}/{repeat_count} to {mobile}...")

                try:
                    if msg_type == 1:
                        pywhatkit.sendwhatmsg(mobile, message, hour, minute)
                    elif msg_type == 2:
                        pywhatkit.sendwhats_image(mobile, media_path, message)
                    elif msg_type == 3:
                        pywhatkit.sendwhats_video(mobile, media_path, message)
                    logging.info(f"Message {i+1} sent to {mobile}")
                except Exception as e:
                    logging.error(f"Failed to send message {i+1} to {mobile}: {e}")
                    print(f"❌ Error sending to {mobile}: {e}")

                time.sleep(interval)  # User-defined delay between messages
        print("\n✅ All messages successfully sent!")
        logging.info("All messages sent successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"General error: {e}")

if __name__ == "__main__":
    logo()
    main()
