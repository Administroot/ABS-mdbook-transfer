#!/bin/env python3
'''
@Author: Administroot <1474668090@qq.com>
@Repository: https://gitee.com/administroot/ABS-mdbook-transfer OR
             https://github.com/Administroot/ABS-mdbook-transfer
@Date: 2023/8/28
'''

import subprocess
import os
import shutil
import re

SUBMODULE = "Advanced-Bash-Scripting-Guide-in-Chinese/"
PATH_EXCHANGE = {SUBMODULE+"source/": "src",
                 SUBMODULE + "SUMMARY.md": "src/SUMMARY.md"}
MDPATH = os.path.abspath('src/') + '/'


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


# 检查是否存在SUBMODULE
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


class mdfile:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.file_ctx = self.read(file_path)

    def read(self, path: str) -> str:
        try:
            with open(path, "r", encoding='utf-8') as fp:
                return fp.read()
        except Exception:
            format_print("ERROR", f"无法读取{path}。程序终止")
            exit(62)
 
    def write(self, path: str) -> None:
        try:
            with open(path, "w", encoding='utf-8') as fp:
                fp.write(self.file_ctx)
        except Exception:
            format_print("ERROR", f"无法写入{path}。程序终止")
            exit(63)

    def global_replace(self, origin_words: str, replaced_words: str) -> None:
        aft_ctx = self.file_ctx.replace(origin_words, replaced_words)
        if aft_ctx != self.file_ctx:
            format_print("INFO", f"『{self.file_path}』:  \"{origin_words}\" --> \"{replaced_words}\"")
        self.file_ctx = aft_ctx
        # print("file_ctx= ", self.file_ctx)
        self.write(self.file_path)

    def partial_replacement(self) -> None:
        # 内容转为切片
        line_ls = self.file_ctx.split('\n')
        
        # 遍历，找到关键词并触发策略
        new_ls = list()
        new_line = str()
        res = tuple()
        hint_flag = -1
        for elem in line_ls:
            # 遇到hint style 就变为0并开始递增； 遇到endhint就重新变成-1
            # 转换hint style
            res = self.hint_trans(hint_flag, elem)
            hint_flag = res[0]
            new_line = res[1]

            if hint_flag >= 0:
                hint_flag += 1
            
            # TODO: 转换raw

            if new_line == "":
                continue
            new_ls.append(new_line)


        # 重新写入文件
        self.file_ctx = "\n".join(new_ls)
        self.write(self.file_path)

    # 转换hint style
    def hint_trans(self, flag: int, line: str) -> (int, str):
        # TODO: output logs <FILE LINENO>
        if re.match(r"{% hint style=\"(.*)\" %}", line):
            line = ""
            flag = 0
        elif re.match(r"{% endhint %}", line):
            line = ""
            return (-1, '\n')
        
        # 下一行
        if flag == 1:
            if line != "":
                line = "\n" + "> ![note](https://tldp.org/LDP/abs/images/tip.gif)" + "\n> \n> " + line
            else:
                line = "> ![note](https://tldp.org/LDP/abs/images/tip.gif)" + line
        elif flag > 1:
            # 其他所有内容均添加 "> "
            line = "> " + line
        
        return (flag, line)



# 更改SUMMARY.md索引格式
def update_summary(summary: mdfile) -> None:
    format_print("INFO", "正在修改SUMMARY.md索引格式")
    summary.global_replace(origin_words="source/", replaced_words="")


# 格式转换
def transform(path: str) -> bool:
    files = list()
    for item in os.scandir(path):
        if item.is_file():
            files.append(item.path)
        else:
            transform(item)

    for file in files:
        # 创建对象
        new_file = mdfile(file)

        # TODO: 处理对象
        new_file.partial_replacement()

        # 删除对象
        del new_file


# Main function
if __name__ == '__main__':
    cmd = "rustc"
    arg = "--version"

    format_print("INFO", "程序正常启动")

    if not check_rust_install(cmd + " " + arg):
        format_print("ERROR", f"mdbook必需{cmd}环境才能运行\n您可能未安装{cmd}环境或未设置全局变量，请检查！")
        exit(60)

    install_mdbook()

    essential_files = PATH_EXCHANGE.keys()

    if not check_existence(essential_files):
        format_print("ERROR", f"缺少 “{SUBMODULE}” 相关文件，请检查！")
        exit(61)

    cp_files(PATH_EXCHANGE)

    # 释放内存
    del PATH_EXCHANGE
    del essential_files

    format_print("INFO", "格式转换中......")

    sum_file = mdfile(MDPATH + "SUMMARY.md")
    update_summary(sum_file)
    del sum_file

    transform(MDPATH)