import pywhatkit
import pandas as pd
import time
import re
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
try:
    from colorama import init, Fore, Style
    init()  # Initialize colorama for Windows compatibility
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    Fore = Style = type('MockColor', (), {'RED': '', 'GREEN': '', 'YELLOW': '', 'CYAN': '', 'RESET_ALL': ''})()

# Configuration and Logging Setup
def load_config() -> dict:
    """Load configuration from config.json file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.YELLOW}⚠️ Config file not found, using default settings{Style.RESET_ALL}")
        return {
            "default_settings": {
                "max_contacts": 50,
                "min_interval_seconds": 5,
                "max_retries": 3,
                "log_level": "INFO",
                "enable_logging": True,
                "log_file": "whatsapp_bot.log"
            }
        }
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}❌ Error parsing config file: {e}{Style.RESET_ALL}")
        return {}

def setup_logging(config: dict) -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger('whatsapp_bot')
    
    if config.get('default_settings', {}).get('enable_logging', True):
        log_level = getattr(logging, config.get('default_settings', {}).get('log_level', 'INFO'))
        log_file = config.get('default_settings', {}).get('log_file', 'whatsapp_bot.log')
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.setLevel(log_level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Global variables
config = load_config()
logger = setup_logging(config)

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
    """Validate phone number format with enhanced validation."""
    try:
        pattern = config.get('validation', {}).get('phone_pattern', r"^\+\d{10,15}$")
        is_valid = re.match(pattern, number) is not None
        
        if not is_valid:
            logger.warning(f"Invalid phone number format: {number}")
            print(f"{Fore.YELLOW}⚠️ Invalid format for {number}! Use + followed by country code and number.{Style.RESET_ALL}")
        else:
            logger.info(f"Valid phone number: {number}")
            
        return is_valid
    except Exception as e:
        logger.error(f"Error validating phone number {number}: {e}")
        return False

def get_scheduled_time() -> Tuple[int, int]:
    """Get and validate scheduled time for message delivery."""
    max_retries = config.get('default_settings', {}).get('max_retries', 3)
    retries = 0
    
    while retries < max_retries:
        try:
            hour = int(input(f"{Fore.CYAN}Enter the hour (24-hour format, e.g., 14 for 2 PM): {Style.RESET_ALL}"))
            minute = int(input(f"{Fore.CYAN}Enter the minute: {Style.RESET_ALL}"))
            
            # Validate hour and minute ranges
            if not (0 <= hour <= 23):
                print(f"{Fore.RED}⚠️ Hour must be between 0-23!{Style.RESET_ALL}")
                retries += 1
                continue
                
            if not (0 <= minute <= 59):
                print(f"{Fore.RED}⚠️ Minute must be between 0-59!{Style.RESET_ALL}")
                retries += 1
                continue

            now = datetime.now()
            scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the scheduled time is in the past, move it to the next day
            if scheduled_time < now:
                scheduled_time += timedelta(days=1)
                print(f"{Fore.YELLOW}ℹ️ Time is in the past, scheduling for tomorrow at {hour:02d}:{minute:02d}{Style.RESET_ALL}")

            logger.info(f"Scheduled time set: {hour:02d}:{minute:02d}")
            return scheduled_time.hour, scheduled_time.minute
            
        except ValueError as e:
            retries += 1
            logger.warning(f"Invalid time input attempt {retries}: {e}")
            print(f"{Fore.RED}⚠️ Invalid input! Please enter numeric values for hour and minute.{Style.RESET_ALL}")
            
    logger.error("Maximum retries exceeded for time input")
    print(f"{Fore.RED}❌ Maximum retries exceeded. Using default time (current hour + 1){Style.RESET_ALL}")
    now = datetime.now()
    return (now.hour + 1) % 24, now.minute

def validate_media_file(file_path: str) -> bool:
    """Validate media file exists and has supported format."""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False
            
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        max_size = config.get('validation', {}).get('max_file_size_mb', 16)
        
        if file_size_mb > max_size:
            logger.error(f"File too large: {file_size_mb:.2f}MB (max: {max_size}MB)")
            print(f"{Fore.RED}❌ File too large! Maximum size: {max_size}MB{Style.RESET_ALL}")
            return False
            
        ext = os.path.splitext(file_path)[1].lower()
        supported_formats = (config.get('validation', {}).get('supported_image_formats', []) + 
                           config.get('validation', {}).get('supported_video_formats', []))
        
        if supported_formats and ext not in supported_formats:
            logger.error(f"Unsupported file format: {ext}")
            print(f"{Fore.RED}❌ Unsupported file format: {ext}{Style.RESET_ALL}")
            return False
            
        logger.info(f"Media file validated: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error validating media file {file_path}: {e}")
        return False

def get_phone_numbers() -> Optional[List[str]]:
    """Get a list of phone numbers from user input or CSV file."""
    numbers = []
    max_contacts = config.get('default_settings', {}).get('max_contacts', 50)
    
    choice = input(f"{Fore.CYAN}Do you want to upload a CSV file with numbers? (yes/no): {Style.RESET_ALL}").strip().lower()

    if choice in ["yes", "y"]:
        file_path = input(f"{Fore.CYAN}Enter the path to the CSV file: {Style.RESET_ALL}").strip()
        
        if os.path.exists(file_path):
            try:
                logger.info(f"Loading contacts from CSV: {file_path}")
                df = pd.read_csv(file_path)
                
                # Try different possible column names for phone numbers
                phone_column = None
                for col in ['Phone', 'phone', 'Number', 'number', 'Mobile', 'mobile', 'Contact', 'contact']:
                    if col in df.columns:
                        phone_column = col
                        break
                        
                if phone_column is None:
                    print(f"{Fore.RED}❌ No phone number column found. Expected columns: Phone, Number, Mobile, Contact{Style.RESET_ALL}")
                    logger.error(f"No phone column found in CSV: {list(df.columns)}")
                else:
                    raw_numbers = df[phone_column].dropna().astype(str).tolist()
                    
                    # Validate each number
                    for num in raw_numbers[:max_contacts]:  # Limit contacts
                        if validate_phone_number(num):
                            numbers.append(num)
                    
                    print(f"{Fore.GREEN}✅ Loaded {len(numbers)} valid contacts from CSV (out of {len(raw_numbers)} total).{Style.RESET_ALL}")
                    logger.info(f"Successfully loaded {len(numbers)} contacts from CSV")
                    
            except Exception as e:
                logger.error(f"Error reading CSV {file_path}: {e}")
                print(f"{Fore.RED}❌ Error reading CSV: {e}{Style.RESET_ALL}")
        else:
            logger.warning(f"CSV file not found: {file_path}")
            print(f"{Fore.RED}❌ File not found. Switching to manual entry.{Style.RESET_ALL}")
    
    if not numbers:
        print(f"\n{Fore.CYAN}📞 Enter phone numbers (with country code). Type 'done' when finished:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️ Maximum {max_contacts} contacts allowed.{Style.RESET_ALL}")
        
        while len(numbers) < max_contacts:
            number = input(f"{Fore.CYAN}Enter number (e.g., +1234567890): {Style.RESET_ALL}").strip()
            if number.lower() == "done":
                break
            if validate_phone_number(number):
                numbers.append(number)
                print(f"{Fore.GREEN}✅ Added: {number} ({len(numbers)}/{max_contacts}){Style.RESET_ALL}")
            # Error message is handled in validate_phone_number function
                
        if len(numbers) >= max_contacts:
            print(f"{Fore.YELLOW}⚠️ Maximum contact limit reached ({max_contacts}){Style.RESET_ALL}")
            logger.warning(f"Maximum contact limit reached: {max_contacts}")
    
    if numbers:
        logger.info(f"Total valid numbers collected: {len(numbers)}")
        
    return numbers if numbers else None

def get_message_type() -> int:
    """Ask user whether to send text, image, or video."""
    max_retries = config.get('default_settings', {}).get('max_retries', 3)
    retries = 0
    
    while retries < max_retries:
        try:
            choice = input(f"{Fore.CYAN}What do you want to send? (1) Text (2) Image (3) Video: {Style.RESET_ALL}").strip()
            if choice in ["1", "2", "3"]:
                logger.info(f"Message type selected: {['Text', 'Image', 'Video'][int(choice)-1]}")
                return int(choice)
            else:
                retries += 1
                print(f"{Fore.RED}⚠️ Invalid choice! Enter 1, 2, or 3. ({retries}/{max_retries}){Style.RESET_ALL}")
        except Exception as e:
            retries += 1
            logger.error(f"Error getting message type: {e}")
            print(f"{Fore.RED}⚠️ Invalid input! ({retries}/{max_retries}){Style.RESET_ALL}")
    
    logger.warning("Maximum retries exceeded for message type, defaulting to text")
    print(f"{Fore.YELLOW}⚠️ Maximum retries exceeded. Defaulting to Text message.{Style.RESET_ALL}")
    return 1

def get_media_path() -> Optional[str]:
    """Ask for image or video path with validation."""
    max_retries = config.get('default_settings', {}).get('max_retries', 3)
    retries = 0
    
    while retries < max_retries:
        path = input(f"{Fore.CYAN}Enter the file path: {Style.RESET_ALL}").strip()
        
        if validate_media_file(path):
            logger.info(f"Media file selected: {path}")
            return path
        else:
            retries += 1
            print(f"{Fore.RED}❌ File validation failed! Try again. ({retries}/{max_retries}){Style.RESET_ALL}")
    
    logger.error("Maximum retries exceeded for media path")
    print(f"{Fore.RED}❌ Maximum retries exceeded for media file selection.{Style.RESET_ALL}")
    return None

def main():
    """Enhanced main function with comprehensive error handling."""
    try:
        welcome_msg = config.get('messages', {}).get('welcome', '📲 **Automated WhatsApp Message Sender** 📩')
        print(f"\n{Fore.GREEN}{welcome_msg}{Style.RESET_ALL}\n")
        logger.info("WhatsApp Bot started")

        # Get list of phone numbers
        numbers = get_phone_numbers()
        if not numbers:
            print(f"{Fore.RED}⚠️ No valid numbers provided! Exiting.{Style.RESET_ALL}")
            logger.warning("No valid phone numbers provided")
            return

        # Get message type
        msg_type = get_message_type()

        if msg_type == 1:  # Text message
            message = input(f"{Fore.CYAN}Enter the message you want to send: {Style.RESET_ALL}").strip()
            if not message:
                print(f"{Fore.RED}⚠️ Message cannot be empty!{Style.RESET_ALL}")
                logger.error("Empty message provided")
                return
            media_path = None
        else:  # Image or Video message
            media_path = get_media_path()
            if not media_path:
                print(f"{Fore.RED}⚠️ No valid media file selected! Exiting.{Style.RESET_ALL}")
                logger.error("No valid media file selected")
                return
        message = input(f"{Fore.CYAN}Enter the caption for the media (or press Enter to skip): {Style.RESET_ALL}").strip()

        # Get per-contact scheduling
        print(f"\n{Fore.CYAN}⏳ Scheduling messages for each contact...{Style.RESET_ALL}")
        schedule_times = {}
        for mobile in numbers:
            print(f"\n{Fore.YELLOW}⏰ Set time for {mobile}{Style.RESET_ALL}")
            hour, minute = get_scheduled_time()
            schedule_times[mobile] = (hour, minute)

        # Get number of repetitions
        min_interval = config.get('default_settings', {}).get('min_interval_seconds', 5)
        
        while True:
            try:
                repeat_count = int(input(f"{Fore.CYAN}Enter how many times you want to send the message: {Style.RESET_ALL}"))
                if repeat_count <= 0:
                    print(f"{Fore.RED}⚠️ Please enter a valid number greater than 0.{Style.RESET_ALL}")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}⚠️ Please enter a valid number.{Style.RESET_ALL}")

        # Get interval between messages (in seconds)
        while True:
            try:
                interval = int(input(f"{Fore.CYAN}Enter time interval between messages (min {min_interval}s): {Style.RESET_ALL}"))
                if interval < min_interval:
                    print(f"{Fore.RED}⚠️ Please enter an interval of at least {min_interval} seconds.{Style.RESET_ALL}")
                else:
                    break
            except ValueError:
                print(f"{Fore.RED}⚠️ Please enter a valid number.{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}📤 Sending messages to {len(numbers)} contacts...{Style.RESET_ALL}\n")
        logger.info(f"Starting message delivery to {len(numbers)} contacts")

        # Send messages with progress tracking
        total_messages = len(numbers) * repeat_count
        sent_count = 0
        failed_count = 0

        for mobile in numbers:
            hour, minute = schedule_times[mobile]
            print(f"{Fore.CYAN}📨 Sending messages to {mobile} starting at {hour:02d}:{minute:02d}...{Style.RESET_ALL}")

            for i in range(repeat_count):
                try:
                    print(f"{Fore.YELLOW}📨 Sending message {i+1}/{repeat_count} to {mobile}...{Style.RESET_ALL}")

                    if msg_type == 1:
                        pywhatkit.sendwhatmsg(mobile, message, hour, minute)
                    elif msg_type == 2:
                        pywhatkit.sendwhats_image(mobile, media_path, message)
                    elif msg_type == 3:
                        pywhatkit.sendwhats_video(mobile, media_path, message)

                    sent_count += 1
                    logger.info(f"Message sent to {mobile} ({sent_count}/{total_messages})")
                    print(f"{Fore.GREEN}✅ Message {i+1} sent successfully to {mobile}{Style.RESET_ALL}")
                    
                    time.sleep(interval)  # User-defined delay between messages
                    
                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to send message to {mobile}: {e}")
                    print(f"{Fore.RED}❌ Failed to send message {i+1} to {mobile}: {e}{Style.RESET_ALL}")

        # Final summary
        success_msg = config.get('messages', {}).get('success', '✅ All messages successfully sent!')
        print(f"\n{Fore.GREEN}{success_msg}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Summary: {sent_count} sent, {failed_count} failed out of {total_messages} total{Style.RESET_ALL}")
        logger.info(f"Message delivery completed: {sent_count} sent, {failed_count} failed")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Operation cancelled by user{Style.RESET_ALL}")
        logger.warning("Operation cancelled by user")
    except Exception as e:
        error_msg = f"{config.get('messages', {}).get('error_prefix', '❌ Error:')} {e}"
        print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
        logger.error(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    logo()
    main()
