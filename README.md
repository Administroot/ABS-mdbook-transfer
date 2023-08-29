# ABS Mdbook本地部署转换器

>  <em>开发中，敬请期待</em>

---
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

**ABS-Mdbook-Converter**是基于[Mdbook](https://rust-lang.github.io/mdBook/)（源代码仓库部署方式为[Gitbook](https://www.gitbook.com/)）的[《Bash脚本进阶指南》第十次修订本中文版](https://github.com/LinuxStory/Advanced-Bash-Scripting-Guide-in-Chinese)（简称ABS）的<em>**本地部署**</em>工具。

本工具用于将Markdown格式由[Gitbook](https://www.gitbook.com/)转换为[Mdbook](https://rust-lang.github.io/mdBook/)，并快速启动本地[Mdbook]([Introduction - mdBook Documentation](https://rust-lang.github.io/mdBook/))服务器。

## 快速开始

### 一、准备环境

由于Mdbook需要**Rust**编译环境，请前往[Rust官网](https://www.rust-lang.org/)下载并安装。
本软件需要[Python3.5](https://www.python.org/downloads/)以上解释器

```shell
git clone https://github.com/Administroot/ABS-mdbook-transfer.git ABS-mdbook-transfer --recursive
cd ABS-mdbook-transfer && pip install -r requirements.txt
```

### 二、启动ABS-Mdbook-Converter

```shell
python abs_mdbook_transfer.py
```

### 三、启动Mdbook

在当前目录执行

```shell
mdbook serve
```

## 为什么需要ABS-Mdbook-Converter

目前，我正在进行[ABS](tldp.org/LDP/abs/html/)的翻译工作。在翻译和开发中使用[Gitbook](https://www.gitbook.com/)作为在线文档工具。它拥有丰富的插件生态，有着良好的展示效果。但是存在若干难以克服的问题：

1. 首要问题就是[Gitbook](https://www.gitbook.com/)已经终止了离线版的维护，您应该很清楚这意味着什么

2. [Gitbook](https://www.gitbook.com/)相较别的在线文档工具启动速度极慢

3. [Gitbook](https://www.gitbook.com/)以及[Nodejs](https://nodejs.org/)的版本兼容问题（当然，这可以用[Docker](https://docker.com)来解决。但是，国内[dockerhub](https://hub.docker.com)域名被污染力，悲）

[Mdbook](https://rust-lang.github.io/mdBook/)能够完美解决以上的问题，可以作为<em>**本地部署**</em>的首选项！但是，部分的Markdown语法并不兼容。

[ABS](tldp.org/LDP/abs/html/)的翻译作品位于[Gitbook](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/)上，不过网络响应速度较慢。

于是，便有了该项目。如果您想要将[ABS](tldp.org/LDP/abs/html/)作为一本工具书、自查手册、操作指南等等。那么，本项目定能助你一臂之力！

## 注记

翻译作品位于[Gitbook](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/)上，欢迎指正！

也欢迎对Shell感兴趣的你参与到我们的[翻译项目](https://github.com/LinuxStory/Advanced-Bash-Scripting-Guide-in-Chinese)中来！
