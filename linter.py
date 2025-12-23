"""ShellCheck linter plugin for CudaText with CudaLint integration."""

from cuda_lint import Linter
import os
import shutil
import json
from cudatext import *

# Plugin loaded (lazy loading via on_lexer/on_open)
print("ShellCheck: Plugin initialized")

class ShellCheck(Linter):
    """ShellCheck linter interface for CudaLint framework.

    Supports Bash/Shell scripts with configurable ignore rules and
    automatic executable detection (PATH or bundled version).
    """

    syntax = ('Bash script', 'Bash', 'Shell script')
    CONFIG_FILE = 'shellcheck_config.json'

    # Default values required by CudaLint framework
    executable = 'shellcheck'
    cmd = ('shellcheck', '-f', 'gcc', '-')

    # Regex for ShellCheck GCC format: filename:line:col: type: message
    regex = (
        r'^.+:(?P<line>\d+):(?P<col>\d+): '
        r'(?:(?P<error>error)|(?P<warning>warning|note)): '
        r'(?P<message>.+)'
    )

    multiline = False
    tempfile_suffix = 'sh'

    def __init__(self, view):
        super().__init__(view)

        # Find ShellCheck executable
        self.shellcheck_path = self._find_executable()
        if not self.shellcheck_path:
            # Ensure valid state even when executable not found
            self.ignore_codes = []
            return

        # Load ignore configuration
        self.ignore_codes = self._load_config()

        # Update with actual values
        self.executable = self.shellcheck_path
        self.cmd = self._build_cmd()

        # Show diagnostic information
        self._log_status()

    def _find_executable(self):
        """Locate ShellCheck: system PATH first, then bundled version."""
        # Try system PATH (cross-platform)
        if path := shutil.which('shellcheck'):
            print(f"ShellCheck: Found in PATH: {path}")
            return path

        # Try bundled version
        try:
            base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            exe = 'shellcheck.exe' if os.name == 'nt' else 'shellcheck'
            bundled = os.path.join(base, 'ShellCheck', exe)

            if os.path.isfile(bundled):
                print(f"ShellCheck: Using bundled version: {bundled}")
                return bundled

            print(f"ShellCheck: WARNING - Not found in PATH or: {bundled}")
        except (NameError, AttributeError) as e:
            print(f"ShellCheck: WARNING - Cannot locate bundled version: {e}")

        return None

    def _load_config(self):
        """Load ignore codes from JSON config, supporting comments."""
        path = os.path.join(app_path(APP_DIR_SETTINGS), self.CONFIG_FILE)

        # Guard clause: config file doesn't exist
        if not os.path.isfile(path):
            return []

        # Read and parse config file
        content = self._read_config_file(path)
        if not content:
            return []

        # Parse and validate codes
        return self._parse_and_validate_codes(content)

    def _read_config_file(self, path):
        """Read config file with comment stripping and encoding fallback."""
        try:
            # Try UTF-8 first (standard)
            with open(path, 'r', encoding='utf-8') as f:
                lines = [ln for ln in f if (s := ln.strip()) and not s.startswith(('//', '#'))]
                return ''.join(lines).strip()

        except UnicodeDecodeError:
            # Fallback to system default encoding (legacy Windows, etc)
            try:
                with open(path, 'r') as f:
                    lines = [ln for ln in f if (s := ln.strip()) and not s.startswith(('//', '#'))]
                    return ''.join(lines).strip()
            except Exception as e:
                print(f"ShellCheck: ERROR - Failed to read config with fallback encoding: {e}")
                return None

        except Exception as e:
            print(f"ShellCheck: ERROR - Failed to read config: {e}")
            return None

    def _parse_and_validate_codes(self, content):
        """Parse JSON and validate SC code format."""
        try:
            config = json.loads(content)

            # Guard clause: config must be a dict (JSON object)
            if not isinstance(config, dict):
                print("ShellCheck: ERROR - Config must be JSON object, not array/string")
                return []

            codes = config.get('ignore_codes', [])

            # Guard clause: ignore_codes must be a list (JSON array)
            if not isinstance(codes, list):
                print("ShellCheck: ERROR - 'ignore_codes' must be array")
                return []

            # Validate format: must be string starting with 'SC' followed by digits
            valid = [c for c in codes if isinstance(c, str) and c.startswith('SC') and c[2:].isdigit()]

            # Warn about invalid codes
            if len(valid) != len(codes):
                invalid = [c for c in codes if c not in valid]
                print(f"ShellCheck: Warning - Invalid codes ignored: {invalid}")

            # Log loaded codes
            if valid:
                print(f"ShellCheck: Loaded ignore codes: {valid}")

            return valid

        except json.JSONDecodeError as e:
            print(f"ShellCheck: ERROR - Invalid JSON in config: {e}")
            return []

    def _build_cmd(self):
        """Build command with ignore flags."""
        cmd = [self.shellcheck_path, '-f', 'gcc', '-']

        for code in self.ignore_codes:
            cmd.extend(['-e', code])

        print(f"ShellCheck: Command: {' '.join(cmd)}")
        return tuple(cmd)

    def _log_status(self):
        """Print diagnostic information."""
        count = len(self.ignore_codes)
        print(f"ShellCheck: Active with {count} ignore rule{'s' if count != 1 else ''}")
        if self.ignore_codes:
            print(f"ShellCheck: Ignoring: {', '.join(self.ignore_codes)}")

    def tmpfile(self, cmd, code, suffix=''):
        """Ensure .sh extension for proper ShellCheck detection."""
        _, ext = os.path.splitext(self.filename)
        return super().tmpfile(cmd, code, ext or '.sh')


class Command:
    """Menu commands for ShellCheck plugin."""

    DEFAULT_CONFIG = {
        "ignore_codes": [
            "SC2034",  # unused variable
            "SC2154",  # referenced but not assigned
            "SC2086"   # quote to prevent word splitting
        ]
    }

    def on_lexer(self, ed_self):
        """Trigger plugin loading when Bash lexer is activated."""
        pass

    def on_open(self, ed_self):
        """Trigger plugin loading when Bash file is opened."""
        pass

    def config(self):
        """Open/create configuration file."""
        path = os.path.join(app_path(APP_DIR_SETTINGS), ShellCheck.CONFIG_FILE)

        if not os.path.isfile(path):
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.DEFAULT_CONFIG, f, indent=2)
                print(f"ShellCheck: Created default config: {path}")
            except Exception as e:
                msg_box(f"Failed to create config:\n{e}", MB_OK | MB_ICONERROR)
                print(f"ShellCheck: ERROR - Config creation failed: {e}")
                return

        file_open(path)
        print(f"ShellCheck: Opened config file: {path}")

    def help(self):
        """Display plugin help."""
        msg_box(
            "ShellCheck Linter for CudaText\n\n"
            "FEATURES:\n"
            "- Auto-detection (PATH -> bundled)\n"
            "- Configurable ignore rules (JSON)\n"
            "- Multi-platform support\n"
            "- Diagnostic logging\n\n"
            "CONFIGURATION:\n"
            "Access via: Options > Settings-plugins > ShellCheck > Config\n\n"
            "COMMON IGNORE CODES:\n"
            "- SC2034: variable appears unused\n"
            "- SC2154: variable referenced but not assigned\n"
            "- SC2086: quote to prevent word splitting\n"
            "- SC2046: quote command substitutions\n\n"
            "INSTALLATION:\n"
            "- Windows: Download shellcheck.exe from releases\n"
            "- Linux: sudo apt install shellcheck\n"
            "- macOS: brew install shellcheck\n\n"
            "DOCUMENTATION:\n"
            "https://github.com/koalaman/shellcheck/wiki",
            MB_OK
        )