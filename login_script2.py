name: Run Login Script  # 运行登录脚本

on:
  workflow_dispatch:  # 允许手动触发这个工作流
  schedule:
    - cron: "0 0 */3 * *"  # 每三天运行一次，可以根据需求调整时间
  push:
    branches:
      - main  # 仅在 `main` 分支有代码推送时运行工作流

jobs:
  login:
    runs-on: ubuntu-latest  # 使用最新版本的 Ubuntu 作为运行环境

    steps:
      - name: Checkout 仓库代码  # 检出仓库代码
        uses: actions/checkout@v2  # 使用 GitHub Actions 的 checkout 动作来拉取代码

      - name: 设置 Python 环境  # 设置 Python 环境
        uses: actions/setup-python@v2  # 使用 GitHub Actions 的 setup-python 动作来设置 Python 版本
        with:
          python-version: '3.x'  # 设置你希望使用的 Python 版本，建议使用稳定版本

      - name: Create accounts.json from environment variable  # 从环境变量创建 accounts.json 文件
        run: echo "$ACCOUNTS_JSON" > accounts.json  # 将环境变量 ACCOUNTS_JSON 的值写入到 accounts.json 文件
        env:
            ACCOUNTS_JSON: ${{ secrets.ACCOUNTS_JSON }}  # 从 GitHub Secrets 中获取 ACCOUNTS_JSON 环境变量

      - name: 安装依赖  # 安装依赖
        run: |
          python -m pip install --upgrade pip  # 升级 pip
          pip install pyppeteer aiofiles requests  # 安装所需的 Python 包
          pip install --upgrade pyppeteer  # 升级 pyppeteer

      - name: 运行登录脚本  # 运行登录脚本
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}  # 从 GitHub Secrets 中获取 TELEGRAM_BOT_TOKEN
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}  # 从 GitHub Secrets 中获取 TELEGRAM_CHAT_ID
          ACCOUNTS_JSON: ${{ secrets.ACCOUNTS_JSON }}  # 从 GitHub Secrets 中获取 ACCOUNTS_JSON
        run: |
          python login_script.py  # 运行 login_script.py 脚本
