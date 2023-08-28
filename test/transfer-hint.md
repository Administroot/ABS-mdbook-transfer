# 单行info hint

## 注记1

{% hint style="info" %}
[1] 这些操作和选项被称为内建命令（builtin），是shell的内部特征。

[2] 虽然递归可以在shell脚本中实现，但是它的效率很低且实现起来很复杂、不具有美感。

[3] 首字母缩略词是由每一个单词的首字母拼接而成的易读的代替短语。这不是一个好习惯，通常会引起一些不必要的麻烦。

[4] ksh88中的许多特性，甚至一些ksh93的特性都被合并到Bash中了。

[5] 按照惯例，用户编写的Bourne shell脚本应该在文件名后加上`.sh`的扩展名。而那些系统脚本，比如在`/etc/rc.d`中的脚本通常不遵循这种规范。
{% endhint %}

## 注记2

{% hint style="info" %}
[1] 在文献中更常见的形式是she-bang或者sh-bang。它们都来源于词汇sharp(#)和bang(!)的连接。

[2] 一些UNIX的衍生版（基于4.2 BSD）声称他们使用四字节的幻数，在#!后增加一个空格，即`#! /bin/sh`。而[Sven Mascheck](http://www.in-ulm.de/~mascheck/various/shebang/#details)指出这是虚构的。

[3] 命令解释器首先将会解释#!这一行，而因为#!以#打头，因此解释器将其视作注释。起始行作为调用解释器的作用已经完成了。

事实上即使脚本中含有不止一个#!,bash也会将除第一个`#!`以外的解释为注释。

```bash
#!/bin/bash

echo "Part 1 of script."
a=1

#!/bin/bash
# 这并不会启动新的脚本

echo "Part 2 of script."
echo $a  # $a的值仍旧为1
```

[4] 这里允许使用一些技巧。

```bash
#!/bin/rm
# 自我删除的脚本

# 当你运行这个脚本，除了这个脚本本身消失以外并不会发生什么。

WHATEVER=85

echo "This line will never print (betcha!)."

exit $WHATEVER  # 这没有任何关系。脚本将不会从这里退出。
                # 尝试在脚本终止后打印echo $a。
                # 得到的值将会是0而不是85.
```

当然你也可以建立一个起始行是`#!/bin/more`的README文件，并且使它可以执行。结果就是这个文件成为了一个可以打印本身的文件。（查看样例 19-3，使用`cat`命令的here document也许是一个更好的选择）

[5] 可移植操作系统接口（POSIX）尝试标准化类UNIX操作系统。POSIX规范可以在[Open Group site](http://www.opengroup.org/onlinepubs/007904975/toc.htm)中查看。

[6] 为了避免这种情况的发生，可以使用`#!/bin/env bash`作为起始行。这在bash不在`/bin`的UNIX系统中会有效果。

[7] 如果bash是系统默认shell，那么脚本并不一定需要#!作为起始行。但是当你在其他的shell中运行脚本，例如tcsh，则需要使用#!。
{% endhint %}

## 连结的info hint

## 注记3

{% hint style="info" %}
[1] 在文献中更常见的形式是she-bang或者sh-bang。它们都来源于词汇sharp(#)和bang(!)的连接。

[2] 一些UNIX的衍生版（基于4.2 BSD）声称他们使用四字节的幻数，在#!后增加一个空格，即`#! /bin/sh`。而[Sven Mascheck](http://www.in-ulm.de/~mascheck/various/shebang/#details)指出这是虚构的。

[3] 命令解释器首先将会解释#!这一行，而因为#!以#打头，因此解释器将其视作注释。起始行作为调用解释器的作用已经完成了。

事实上即使脚本中含有不止一个#!,bash也会将除第一个`#!`以外的解释为注释。
{% endhint %}

# warning hint

{% hint style="warning" %}

使用内建命令 `declare` 还可以限制变量的 [作用域]()。

```bash
foo ()
{
FOO="bar"
}

bar ()
{
foo
echo $FOO
}

bar   # 输出 bar。
```

但是...

```bash
foo(){
declare FOO="bar"
}

bar ()
{
foo
echo $FOO
}

bar  # 什么都不会输出。


# 感谢 Michael Iatrou 指出这点。
```

{% endhint %}
