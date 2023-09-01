# tagless code block

sed或awk脚本通常在命令行下调用时是sed -e '命令'或者awk '命令'。在Bash脚本中嵌入这些命令会让它们在调用时很简单，并且能够被重用。使用这种方法可以将sed和awk的优势统一起来，比如将sed命令处理的结果通过管道传递给awk继续处理。将这些保存成为一个可执行文件，你可以重复调用它的原始版本或者修改版本，而不用在命令行里反复敲冗长的命令。

## Example 36-1. shell wrapper

```
#!/bin/bash
# 这个脚本功能是去除文件中的空白行
# 没有做参数检查
#
# 也许你想添加下面的内容：
#
# E_NOARGS=85
# if [ -z "$1" ]
# then
#  echo "Usage: `basename $0` target-file"
#  exit $E_NOARGS
# fi
sed -e /^$/d "$1"
# 就像这个命令
#    sed -e '/^$/d' filename
# 通过命令行调用
# '-e'意思是后面为编辑命令（这个选项可省略）。
# '^'代表行首，'$'代表行尾。
# 这个正则表达式表示要匹配出所有行首位没有内容的行，就是空白行。
# 是删除命令（译注：就是把刚才选出来的空白行删掉）
# 将文件名中的特殊字符和空白进行转译
# 这个脚本并不会真正的修改目标文件，如果想对目标文件真正的修改，请将输出重定向
exit
```

## Example 36-2. 稍微复杂一点的 shell wrapper

```
#!/bin/bash
#  subst.sh: 在文件中进行替换字符串的脚本
#  例如 "sh subst.sh Smith Jones letter.txt"
#  letter.txt 中的所有 Jones 都被替换为 Smith。
ARGS=3         # 这个脚本需要三个参数
E_BADARGS=85   # 传给脚本的参数数量不正确
if [ $# -ne "$ARGS" ]
then
    echo "Usage: `basename $0` old-pattern new-pattern filename"
    exit $E_BADARGS
fi
old_pattern=$1
new_pattern=$2
if [ -f "$3" ]
then
    file_name=$3
else
    echo "File \"$3\" does not exist."
    exit $E_BADARGS
fi
# -----------------------------------------------
# 这里是最核心的部分
sed -e "s/$old_pattern/$new_pattern/g" $file_name
# -----------------------------------------------
# 's' 是sed中的替换命令
# /pattern/调用地址匹配
# 'g' 表示要对文件中的所有匹配项目都进行替换操作，而不是仅对第一个这样干。
# 如果需要深入了解，请阅读sed命令的相关文档。
exit $?  # 将这个脚本的输出重定向到一个文件即可记录真正的结果
```

## Example 36-3. 一个通用的写日志文件的 shell wrapper

```
#!/bin/bash
#  logging-wrapper.sh
#  一个通用的shell wrapper，在进行操作的同时对操作进行日志记录
DEFAULT_LOGFILE=logfile.txt
# 设置下面两个变量的值
OPERATION=
# 可以是任意操作，比如一个awk脚本或者用管道连接的复杂命令
LOGFILE=
if [ -z "$LOGFILE" ]
    then     # 如果没有设置日志文件，则使用默认文件名
      LOGFILE="$DEFAULT_LOGFILE"
      fi
# 对于操作命令的参数（可选）
OPTIONS="$@"
# 日志记录
echo "`date` + `whoami` + $OPERATION "$@"" >> $LOGFILE
# 进行操作动作
exec $OPERATION "$@"
# 要在真正执行操作之前写日志
# 思考下为什么要先写日志，后操作。
```

## Example 36-4. 关于awk脚本的 shell wrapper

```
#!/bin/bash
# pr-ascii.sh: 打印ASCII码表格
START=33   # 可打印的ASCII码范围（十进制）
END=127    # 不会输出不可打印的ASCII码
echo " Decimal   Hex     Character"   # 表头
echo " -------   ---     ---------"
for ((i=START; i<=END; i++))
do
    echo $i | awk '{printf("  %3d       %2x         %c\n", $1, $1, $1)}'
# Bash内置的printf命令无法完成下面的操作: （译注：所以这使用awk脚本来实现输出）
#     printf "%c" "$i"
done
exit 0
#  Decimal   Hex     Character
#  -------   ---     ---------
#    33       21         !
#    34       22         "
#    35       23         #
#    36       24         $
#
#    . . .
#
#   122       7a         z
#   123       7b         {
#   124       7c         |
#   125       7d         }
# 将输出重定向到文件
# 或者用管道传递给"more":  sh pr-asc.sh | more
```

subsequent contents

# bash code block

```bash
#!/bin/bash
# get-commandline.sh
# 获得进程的命令行参数。
OPTION=cmdline
# 识别 PID。
pid=$( echo $(pidof "$1") | awk '{ print $1 }' )
# 只获取                     ^^^^^^^^^^^^^^^^^^ 多个实例的第一个。
echo
echo "Process ID of (first instance of) "$1" = $pid"
echo -n "Command-line arguments: "
cat /proc/"$pid"/"$OPTION" | xargs -0 echo
#   格式化输出               ^^^^^^^^^^^^^^^
#   （感谢 Han Holl 修复问题！）
echo; echo
# 例如：
# sh get-commandline.sh xterm
```

```bash
devfile="/proc/bus/usb/devices"
text="Spd"
USB1="Spd=12"
USB2="Spd=480"
bus_speed=$(fgrep -m 1 "$text" $devfile | awk '{print $9}')
#                 ^^^^ Stop after first match.
if [ "$bus_speed" = "$USB1" ]
then
  echo "USB 1.1 port found."
  # Do something appropriate for USB 1.1.
fi
```

甚至有可能通过发送到 `/proc` 目录的命令来控制某些外围设备。

这会打开某些型号 IBM/Lenovo Thinkpad 的 *Thinklight*。（可能不会在所有 Linux 发行版上生效。）
当然，在写入 `/proc` 时应谨慎。
`/proc` 目录包含一些不寻常的以数字为名的子目录。每一个名称都映射到当前运行的进程的进程 ID。在每一个子目录内，有一些文件保存着与对应进程有关的有用信息。`stat` 和 `status` 文件维护进程运行时的统计数据，`cmdline` 文件保存了进程被调用时的命令行参数，`exe` 文件是一个链接到调用进程的完整路径名称的符号链接。还有一些类似的文件，但前面这些是从编写脚本的角度来说最为感兴趣的。
**例 29-3. 找到与 PID 关联的进程**

```bash
#!/bin/bash
# pid-identifier.sh:
# 给出与 PID 关联的进程的完整路径名称。
ARGNO=1  # 脚本预期的参数数量。
E_WRONGARGS=65
E_BADPID=66
E_NOSUCHPROCESS=67
E_NOPERMISSION=68
PROCFILE=exe
if [ $# -ne $ARGNO ]
then
  echo "Usage: `basename $0` PID-number" >&2  # 错误信息 >stderr.
  exit $E_WRONGARGS
fi  
pidno=$( ps ax | grep $1 | awk '{ print $1 }' | grep $1 )
# 在“ps”列表，第一个字段中检查 pid。
# 然后确认这是个真实的进程，而不是被这个脚本调用的进程。
# 最后的 “grep $1”排除了这种可能性。
#
#    pidno=$( ps ax | awk '{ print $1 }' | grep $1 )
#    也可以，如 Teemu Huovila 指出。
if [ -z "$pidno" ]  #  如果，在所有过滤之后，结果是长度为 0 的字符串，
then                #+ 那么就没有与给定 pid 对应的运行进程。
  echo "No such process running."
  exit $E_NOSUCHPROCESS
fi  
# 另一种方法：
#   if ! ps $1 > /dev/null 2>&1
#   then                # 没有与给定 pid 对应的运行进程。
#     echo "No such process running."
#     exit $E_NOSUCHPROCESS
#    fi
# 要简化整个过程，可以使用 “pidof”。
if [ ! -r "/proc/$1/$PROCFILE" ]  # 检查读权限。
then
  echo "Process $1 running, but..."
  echo "Can't get read permission on /proc/$1/$PROCFILE."
  exit $E_NOPERMISSION  # 普通用户无法访问 /proc 中的某些文件。
fi  
# 最后两条测试可以用下面替换：
#    if ! kill -0 $1 > /dev/null 2>&1 # '0' 不是一个信号，但
                                      # 会测试是否可以向进程
                                      # 发送信号。
#    then echo "PID doesn't exist or you're not its owner" >&2
#    exit $E_BADPID
#    fi
exe_file=$( ls -l /proc/$1 | grep "exe" | awk '{ print $11 }' )
# 或者      exe_file=$( ls -l /proc/$1/exe | awk '{print $11}' )
#
#  /proc/pid-number/exe 是一个链接到调用进程的完整路径名的符号链接。
if [ -e "$exe_file" ]  #  如果 /proc/pid-number/exe 存在，
then                   #+ 那么对应进程就存在。
  echo "Process #$1 invoked by $exe_file."
else
  echo "No such process running."
fi  
#  
#  这个复杂的脚本可以*几乎*用下面的命令替代
#       ps ax | grep $1 | awk '{ print $5 }'
#  但是，这不会生效……
#+ 因为“ps”的第 5 个字段是进程的 argv[0]，而不是可执行文件的路径。
#
# 不过，下面的方法都是可行的。
#       find /proc/$1/exe -printf '%l\n'
#       lsof -aFn -p $1 -d txt | sed -ne 's/^n//p'
# Stephane Chazelas 的补充评论。
exit 0
```

# shell code block

```shell
bash$ lsusb
Bus 001 Device 001: ID 0000:0000  
 Device Descriptor:
   bLength                18
   bDescriptorType         1
   bcdUSB               1.00
   bDeviceClass            9 Hub
   bDeviceSubClass         0 
   bDeviceProtocol         0 
   bMaxPacketSize0         8
   idVendor           0x0000 
   idProduct          0x0000

   . . .
```

### lspci

列出目前所有的*pci*总线。

```shell
bash$ lspci
00:00.0 Host bridge: Intel Corporation 82845 845
 (Brookdale) Chipset Host Bridge (rev 04)
 00:01.0 PCI bridge: Intel Corporation 82845 845
 (Brookdale) Chipset AGP Bridge (rev 04)
 00:1d.0 USB Controller: Intel Corporation 82801CA/CAM USB (Hub #1) (rev 02)
 00:1d.1 USB Controller: Intel Corporation 82801CA/CAM USB (Hub #2) (rev 02)
 00:1d.2 USB Controller: Intel Corporation 82801CA/CAM USB (Hub #3) (rev 02)
 00:1e.0 PCI bridge: Intel Corporation 82801 Mobile PCI Bridge (rev 42)

   . . .
```
