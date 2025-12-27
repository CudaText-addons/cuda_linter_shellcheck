Linter for CudaLint plugin.
It adds support for Bash script lexer.
It uses "ShellCheck".

'ShellCheck' must be in your system PATH or in the ShellCheck folder (portable use) inside CudaText directory.

ShellCheck is a static analysis tool for shell scripts:
https://github.com/koalaman/shellcheck

For example, to install it on Windows, download shellcheck.exe from GitHub releases and place it in tools/ShellCheck folder inside CudaText directory.
On Linux: sudo apt install shellcheck
On Mac: brew install shellcheck

Access configuration via menu: Options > Settings-plugins > ShellCheck > Config
Access help via menu: Options > Settings-plugins > ShellCheck > Help

To ignore specific warnings, create settings/shellcheck_config.json with:
{
  "ignore_codes": [
    "SC2034",
    "SC2154"
  ]
}

Author: Bruno Eduardo

License: MIT
