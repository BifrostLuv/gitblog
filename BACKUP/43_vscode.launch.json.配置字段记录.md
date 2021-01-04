# [vscode launch.json 配置字段记录](https://github.com/chaleaoch/gitblog/issues/43)


Table of Contents
=================

         * ["justMyCode": false](#justmycode-false)
         * ["console": "integratedTerminal"](#console-integratedterminal)
         * ["env": {"PYTHONPATH": "${workspaceFolder}/django"}](#env-pythonpath-workspacefolderdjango)
         * ["cwd": "${workspaceFolder}/contrib/role_and_menu/"](#cwd-workspacefoldercontribrole_and_menu)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
### "justMyCode": false

### "console": "integratedTerminal"

输出在vscode terminal, 调试信息在调试控制台

    - "console": "internalConsole" -- 调试信息和输出信息都在调试控制台

### "env": {"PYTHONPATH": "${workspaceFolder}/django"}

需要其他环境变量的话.很重要.

### "cwd": "${workspaceFolder}/contrib/role_and_menu/"

当前工作目录, os.getcwd()

