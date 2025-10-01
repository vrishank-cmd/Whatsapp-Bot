# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2024-10-01

### Added
- **Enhanced Configuration System**: Added `config.json` for customizable settings including contact limits, intervals, and logging preferences
- **Comprehensive Logging**: Added detailed logging system with file and console output for better debugging and monitoring
- **Input Validation Improvements**: Enhanced validation for phone numbers, file formats, and user inputs with retry mechanisms
- **Colored Terminal Interface**: Added colorama support for cross-platform colored output to improve user experience
- **Progress Tracking**: Real-time progress tracking during message sending with success/failure counters
- **CSV Import Enhancements**: Flexible column naming support for CSV imports (Phone, Number, Mobile, Contact)
- **File Validation**: Added comprehensive media file validation including size limits and format checking
- **Error Handling**: Robust error handling throughout the application with graceful failure recovery
- **Installation Guide**: Added detailed `INSTALL.md` with platform-specific instructions
- **Example CSV**: Added `example_contacts.csv` template for users

### Changed
- **Requirements Format**: Updated `Requirements.txt` to standard pip requirements format
- **User Interface**: Enhanced all user prompts with colored output and better formatting
- **Contact Limits**: Added configurable maximum contact limits for better resource management
- **Interval Validation**: Added minimum interval validation to prevent spam-like behavior
- **Function Signatures**: Added type hints for better code maintainability

### Improved
- **Code Organization**: Better separation of concerns and modular function design
- **Documentation**: Enhanced README with new features and installation instructions
- **Cross-Platform Compatibility**: Improved compatibility across Windows, Linux, and macOS
- **User Experience**: More intuitive prompts and better error messages

### Security
- **Input Sanitization**: Enhanced input validation to prevent potential security issues
- **File Path Validation**: Added proper file path validation for media uploads

## [Previous] - Original Release

### Features
- Basic WhatsApp message sending functionality
- Support for text, image, and video messages
- Scheduled messaging capability
- Multiple contact support
- CSV file import for contacts