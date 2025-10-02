# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/vrishank-cmd/Whatsapp-Bot.git
cd Whatsapp-Bot
```

### 2. Install Dependencies

#### Using pip (Recommended)
```bash
pip install -r requirements.txt
```

#### Manual Installation
```bash
pip install pywhatkit>=5.4
pip install pandas>=1.5.0
pip install colorama>=0.4.6
```

### 3. Configuration (Optional)

The bot includes a `config.json` file for customization:

- `max_contacts`: Maximum number of contacts allowed (default: 50)
- `min_interval_seconds`: Minimum interval between messages (default: 5)
- `max_retries`: Maximum retry attempts for user input (default: 3)
- `enable_logging`: Enable/disable logging (default: true)
- `log_file`: Log file name (default: "whatsapp_bot.log")

## Platform-Specific Instructions

### Windows
```powershell
# Install Python from python.org
# Open PowerShell or Command Prompt
pip install -r requirements.txt
python bot.py
```

### Linux/Ubuntu
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
python3 bot.py
```

### macOS
```bash
# Install Python using Homebrew
brew install python3
pip3 install -r requirements.txt
python3 bot.py
```

## Troubleshooting

### Common Issues

1. **Module Not Found Error**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Permission Denied**
   - Linux/macOS: Use `pip3 install --user -r requirements.txt`
   - Windows: Run Command Prompt as Administrator

3. **Colorama Issues on Windows**
   ```bash
   pip install --upgrade colorama
   ```

### WhatsApp Web Setup

1. The bot uses WhatsApp Web, so ensure you have:
   - A stable internet connection
   - Chrome browser installed
   - WhatsApp Web access

2. On first run, the bot will open WhatsApp Web - scan the QR code with your phone

### CSV File Format

If using CSV file for contacts, ensure the format:
```csv
Phone
+1234567890
+9876543210
```

Supported column names: Phone, phone, Number, number, Mobile, mobile, Contact, contact

## Running the Bot

```bash
python bot.py
```

Follow the interactive prompts to:
1. Choose message type (text/image/video)
2. Enter contacts (manual or CSV)
3. Schedule delivery times
4. Set repetition and intervals

## Support

For issues or questions, please check the [GitHub Issues](https://github.com/vrishank-cmd/Whatsapp-Bot/issues) page.