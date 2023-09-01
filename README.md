# ABS Mdbook本地部署转换器

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)[![GitBook](https://img.shields.io/badge/GitBook-read-blue)](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/)

> 主体功能已完善，部分格式影响较大的正在逐一手动修复中

**ABS-Mdbook-Converter**是基于[Mdbook](https://rust-lang.github.io/mdBook/)（源代码仓库部署方式为[Gitbook](https://www.gitbook.com/)）的项目[《Bash脚本进阶指南》第十次修订本中文版](https://github.com/LinuxStory/Advanced-Bash-Scripting-Guide-in-Chinese)（简称ABS）的<em>**本地部署**</em>工具。

本工具用于将Markdown格式由Gitbook转换为Mdbook，并快速启动本地Mdbook服务器。

## 快速开始

### 一、环境准备

- Mdbook依赖[**Rust**编译环境](https://www.rust-lang.org/)

- 建议[**Python3.6**](https://www.python.org/downloads/)以上解释器

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

![note](http://tldp.org/LDP/abs/images/note.gif) 首先，网络条件允许的情况下建议<code>*在线*</code>学习。

那对于<code>*离线*</code>版本来说：
[原翻译项目](https://github.com/LinuxStory/Advanced-Bash-Scripting-Guide-in-Chinese)使用Gitbook作为在线文档工具。它拥有丰富的插件生态，有着良好的展示效果。但是存在若干难以克服的问题：

1. 首要问题就是Gitbook已经终止了离线版的维护

2. Gitbook相较别的在线文档工具启动速度极慢

3. Gitbook以及[Nodejs](https://nodejs.org/)的版本兼容问题（当然，这可以用[Docker](https://docker.com)来解决。但是，国内[Dockerhub](https://hub.docker.com)域名被污染力，悲）

Mdbook能够避开以上的问题，可以作为<em>**本地部署**</em>的首选项！但是，部分的Markdown语法并不兼容，且观感较差。

于是，便有了该项目。如果您想要将[ABS](tldp.org/LDP/abs/html/)作为一本工具书、自查手册、操作指南等等。那么，本项目定能助你一臂之力！

## 注记

翻译作品位于[Gitbook](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/)上，欢迎指正！

也欢迎对Shell感兴趣的你参与到我们的[翻译项目](https://github.com/LinuxStory/Advanced-Bash-Scripting-Guide-in-Chinese)中来！
