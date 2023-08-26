#!/bin/env python3
'''
@Author: Administroot <1474668090@qq.com>
@Repository: https://gitee.com/administroot/ABS-mdbook-transfer OR
             https://github.com/Administroot/ABS-mdbook-transfer
@Date: 2023/8/25
'''

import subprocess
import os
import shutil

# TODO: 格式化输出

# 检查安装环境
def check_rust_install(command: str) -> bool:
    try:
        # 执行命令，捕获输出结果，但不需要输出到终端
        subprocess.run(command, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

# TODO: 安装Mdbook


# 检查是否存在submodule
def check_existence(path: list) -> bool:
    for rel_path in path:
        dir_file_path = os.path.join(os.getcwd(), rel_path)
        if not os.path.exists(dir_file_path):
            return False
        else:
            return True


# 准备Markdown文本环境
def cp_files(trans: dict) -> None:
    for src, dst in trans.items():
        if os.path.isdir(src):
            # 目录
            try:
                shutil.copytree(src, dst)
            except FileExistsError:
                print(src, "已存在，程序已停止。")
                exit(62)
        else:
            # 文本文件
            try:
                shutil.copyfile(src, dst)
            except FileExistsError:
                print(src, "已存在，程序已停止。")
                exit(62)


# Main function
if __name__ == '__main__':
    cmd = "rustc"
    arg = "--version"
    submodule = "Advanced-Bash-Scripting-Guide-in-Chinese/"
    change_paths = {submodule+"source/": "src",
                    submodule + "SUMMARY.md": "src/SUMMARY.md"}

    if not check_rust_install(cmd + " " + arg):
        print(f"mdbook必需{cmd}环境才能运行\n您可能未安装{cmd}环境或未设置全局变量，请检查！")
        exit(60)

    essential_files = change_paths.keys()
    print(essential_files)

    if not check_existence(essential_files):
        print(f"您缺少 “{submodule}” 相关文件，请检查！")
        exit(61)

    cp_files(change_paths)

    # 释放内存
    del change_paths
    del essential_files
