# [poetry入门](https://github.com/chaleaoch/gitblog/issues/45)


Table of Contents
=================

   * [安装和更新](#安装和更新)
   * [基本使用](#基本使用)
      * [配置虚拟环境](#配置虚拟环境)
      * [新建或初始化](#新建或初始化)
      * [添加依赖](#添加依赖)
      * [进入虚拟环境](#进入虚拟环境)
      * [切换虚拟环境](#切换虚拟环境)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
poetry -- 一个环境,依赖管理和打包工具. 

> I built Poetry because I wanted a single tool to manage my Python projects from start to finish. I wanted something reliable and intuitive that the community could use and enjoy.

# 安装和更新

```text
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/env

$ poetry --version
Poetry version 1.1.4

# 更新自己
$ poetry self update
You are using the latest version

# auto completion
# Bash
poetry completions bash > /etc/bash_completion.d/poetry.bash-completion
```

# 基本使用

## 配置虚拟环境

```text
$ poetry config --list
cache-dir = "/root/.cache/pypoetry"
experimental.new-installer = true
installer.parallel = true
virtualenvs.create = true
virtualenvs.in-project = null
virtualenvs.path = "{cache-dir}/virtualenvs"  # /root/.cache/pypoetry/virtualenvs
```

## 新建或初始化

```text
poetry new poetry-demo # 新建项目
或者
poetry init poetry-demo # 既存项目新建poetry
```

```text
root@vpn:~/test/poetry-demo 
$ tree
.
├── poetry_demo
│   └── __init__.py
├── pyproject.toml
├── README.rst
└── tests
    ├── __init__.py
    └── test_poetry_demo.py
```

## 添加依赖

```text
$ poetry add pendulum
Creating virtualenv poetry-demo-hAszOqab-py3.9 in /root/.cache/pypoetry/virtualenvs
Using version ^2.1.2 for pendulum
==============================================================================================
root@vpn:~/.cache/pypoetry/virtualenvs/poetry-demo-hAszOqab-py3.9/lib/python3.9/site-packages 
$ ls pendulum
constants.py  datetime.py  exceptions.py  formatting  __init__.py  mixins     parsing    __pycache__  time.py  utils
date.py       duration.py  _extensions    helpers.py  locales      parser.py  period.py  py.typed     tz       __version__.py

```

## 进入虚拟环境

```text
root@vpn:~/test/poetry-demo 
$ poetry shell
Spawning shell within /root/.cache/pypoetry/virtualenvs/poetry-demo-hAszOqab-py3.9
. /root/.cache/pypoetry/virtualenvs/poetry-demo-hAszOqab-py3.9/bin/activate

root@vpn:~/test/poetry-demo 
$ . /root/.cache/pypoetry/virtualenvs/poetry-demo-hAszOqab-py3.9/bin/activate

[poetry-demo-hAszOqab-py3.9] root@vpn:~/test/poetry-demo 

```

## 切换虚拟环境

```text
root@vpn:~/test/poetry-demo2 
$ cat pyproject.toml 
[tool.poetry]
name = "poetry-demo2"
version = "0.1.0"
description = ""
authors = ["zhicfeng <zhicfeng@cisco.com>"]

[tool.poetry.dependencies]
python = ">=3.6"
 # 注意这里

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"


$ poetry env use python3.6
Creating virtualenv poetry-demo2-olXfc6F_-py3.6 in /root/.cache/pypoetry/virtualenvs
Using virtualenv: /root/.cache/pypoetry/virtualenvs/poetry-demo2-olXfc6F_-py3.6
```

