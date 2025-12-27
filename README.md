# CudaText plugin for 'ShellCheck' tool integration

## 🎯 What is ShellCheck?

ShellCheck is a **static analysis tool for shell scripts** that finds bugs in your sh/bash scripts. It's the **industry standard** for shell script linting and helps you:

- ✅ Find syntax errors and bugs
- ✅ Detect dangerous code patterns
- ✅ Follow best practices
- ✅ Improve code quality
- ✅ Learn shell scripting properly

Used by major projects and recommended by shell script developers worldwide.

## 📦 Installation

### Install the Plugin
1. In CudaText: **Plugins > Addon Manager > Install**
2. Search for "ShellCheck" and install

### Install ShellCheck
- **Windows**: Download `shellcheck.exe` from [releases](https://github.com/koalaman/shellcheck/releases) → place in `CudaText/tools/ShellCheck` folder
- **Linux**: `sudo apt install shellcheck` or `dnf install ShellCheck`
- **macOS**: `brew install shellcheck`

ShellCheck must be in system PATH or in `CudaText/tools/ShellCheck` folder (portable mode).

## ✨ Plugin Features

### Core Functionality
- 🔌 **Full CudaLint integration** - Works seamlessly with the existing framework
- 🔍 **Smart executable detection** - Finds ShellCheck in PATH or uses bundled version (portable mode)
- ⚙️ **JSON configuration** - Easy to configure ignore rules with validation
- 🌍 **Cross-platform** - Windows, Linux, macOS fully supported
- 📊 **Diagnostic logging** - Helpful console output for debugging

### User Experience
- 🎯 **KISS principle** - Simple, clean code with minimal complexity
- 🔴 **Smart severity mapping** - Errors show as red, warnings/notes as yellow
- 🏷️ **Clear error messages** - Shows SC codes for easy lookup
- 📖 **Comprehensive help** - Built-in documentation with common codes
- 📦 **Portable-ready** - Works great with CudaText portable installations

## 🚀 Usage

### Menu Commands
- **Options > Settings-plugins > ShellCheck > Config** - Configure ignore rules
- **Options > Settings-plugins > ShellCheck > Help** - Show help

### Configuration
Create `settings/shellcheck_config.json` to customize ignore rules:
```json
{
  "ignore_codes": [
    "SC2034",
    "SC2154",
    "SC2086"
  ]
}
```

### Common Ignore Codes
- **SC2034**: Variable appears unused
- **SC2154**: Variable referenced but not assigned
- **SC2086**: Quote to prevent word splitting
- **SC2046**: Quote command substitutions to prevent word splitting

## 📚 Additional Info
- **ShellCheck project**: https://github.com/koalaman/shellcheck
- **ShellCheck wiki**: https://github.com/koalaman/shellcheck/wiki
- **Author**: Bruno Eduardo
- **License**: MIT
