#!/bin/env python3
'''
@Author: Administroot <1474668090@qq.com>
@Repository: https://gitee.com/administroot/ABS-mdbook-transfer OR
             https://github.com/Administroot/ABS-mdbook-transfer
@Date: 2023/8/26
'''

import subprocess
import os
import shutil


# 格式化输出
def format_print(status: str, msg: str) -> None:
    if status == "ERROR":
        print(f"\033[31m[{status}]\033[0m {msg}")
    elif status == "WARN":
        print(f"\033[33m[{status}]\033[0m {msg}")
    elif status == "INFO":
        print(f"\033[34m[{status}]\033[0m {msg}")


# 检查安装环境
def check_rust_install(command: str) -> bool:
    format_print("INFO", "检查Rust环境")
    try:
        # 执行命令，捕获输出结果，但不需要输出到终端
        subprocess.run(command, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


# 安装Mdbook
def install_mdbook() -> None:
    format_print("INFO", "检查并安装Mdbook")
    try:
        subprocess.run("cargo install mdbook")
    except Exception:
        format_print("ERROR", "未知错误，程序退出")


# 检查是否存在submodule
def check_existence(path: list) -> bool:
    format_print("INFO", "检查ABS环境")
    for rel_path in path:
        dir_file_path = os.path.join(os.getcwd(), rel_path)
        if not os.path.exists(dir_file_path):
            return False
        else:
            return True


# 准备Markdown文本环境
def cp_files(trans: dict) -> None:
    format_print("INFO", "拷贝源文件")
    for src, dst in trans.items():
        # print("src=", src, "\n\n", "dst=", dst)
        if os.path.isdir(src):
            # 目录
            try:
                shutil.copytree(src, dst)
            except FileExistsError:
                format_print("WARN", dst + "/目录已存在，将覆盖。")
                shutil.rmtree(dst)
                shutil.copytree(src, dst)
        else:
            # 文本文件
            try:
                shutil.copyfile(src, dst)
            except FileExistsError:
                format_print("WARN", dst + "文件已存在，将覆盖。")
                os.remove(dst)
                shutil.copyfile(src, dst)

# 更改SUMMARY.md索引
def update_summary() -> None:
    format_print("INFO", "修改SUMMARY.md索引格式")
    content = str()
    try:
        stage = "读取"
        with open("src/SUMMARY.md", "r", encoding='utf-8') as fp:
            content = fp.read()
            content = content.replace("source/", "")

        stage = "写入"
        with open("src/SUMMARY.md", "w", encoding='utf-8') as fp:
            fp.write(content)
    except Exception:
        format_print("ERROR", f"无法{stage}SUMMARY.md。程序终止")
        exit(62)

# TODO: 转换Markdown格式


# Main function
if __name__ == '__main__':
    cmd = "rustc"
    arg = "--version"
    submodule = "Advanced-Bash-Scripting-Guide-in-Chinese/"
    change_paths = {submodule+"source/": "src",
                    submodule + "SUMMARY.md": "src/SUMMARY.md"}

    format_print("INFO", "程序正常启动")

    if not check_rust_install(cmd + " " + arg):
        format_print("ERROR", f"mdbook必需{cmd}环境才能运行\n您可能未安装{cmd}环境或未设置全局变量，请检查！")
        exit(60)

    install_mdbook()

    essential_files = change_paths.keys()

    if not check_existence(essential_files):
        format_print("ERROR", f"缺少 “{submodule}” 相关文件，请检查！")
        exit(61)

    cp_files(change_paths)

    # 释放内存
    del change_paths
    del essential_files

    update_summary()