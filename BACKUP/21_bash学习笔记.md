# [bash学习笔记](https://github.com/chaleaoch/gitblog/issues/21)


Table of Contents
=================



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
```
a=foo
echo $a_file
echo ${a}_file
myvar=USER
echo ${!myvar}
unset NAME ## 不存在的 Bash 变量一律等于空字符串

# export命令用来向子 Shell 输出变量
export NAME=value
# 当前 Shell 的进程 ID
echo $$
# varname存在不为空,返回word
${varname:-word}
# varname存在不为空,将varname设为word,返回word
${varname:=word}
# count存在返回1 否则为空字符串
${count:+1}
# count未定义,就中断执行,报错信息"undefined!"
${count:?"undefined!"}

# 整数可直接进行计算
declare -i val1=12 val2=5 # 这里是否声明无所谓
declare -i result         # 这句关键
result=val1*val2
echo $result

declare -x foo
# 等同于
export foo

#只读
declare -r bar=1
# 等于
readonly foo=1

let foo=1+2
echo $foo
3

#脚本参数
# $0：脚本文件名，即script.sh。
# $1~$9：对应脚本的第一个参数到第九个参数。
# $#：参数的总数。
# $@：全部的参数，参数之间使用空格分隔。
# $*：全部的参数，参数之间使用变量$IFS值的第一个字符分隔，默认为空格，但是可以自定义。

# shift 命令
# 移除脚本当前的第一个参数（$1），使得后面的参数向前一位，即$2变成$1、$3变成$2、$4变成$3，以此类推
# 后面可接参数,一次移出多个参数

#getopts
# while循环不断执行getopts 'lha:' OPTION命令，每次执行就会读取一个连词线参数（以及对应的参数值），
# 然后进入循环体。变量OPTION保存的是，当前处理的那一个连词线参数（即l、h或a）。如果用户输入了没有指定的参数（比如-x），
# 那么OPTION等于?。循环体内使用case判断，处理这四种不同的情况。
# 注意, 不能处理类似这样的情况command foo -l
while getopts 'lha:' OPTION; do # OPTION 是执行的参数个数 和shift 配套食用,效果更佳.
	case "$OPTION" in
	l)
		echo "linuxconfig"
		;;

	h)
		echo "h stands for h"
		;;

	a)
		avalue="$OPTARG" # 保存选项后面的参数值
		echo "The value provided is $OPTARG"
		;;
	?)
		echo "script usage: $(basename $0) [-l] [-h] [-a somevalue]" >&2
		exit 1
		;;
	esac
done
shift "$(($OPTIND - 1))"

# source命令
# 执行脚本,但是并不会新建子shell, source 执行脚本不需要export命令.
# source命令的另一个用途，是在脚本内部加载外部库。
# . .bashrc source 的简写形式

# 条件判断 if
echo -n "输入一个1到3之间的数字（包含两端）> "
read character
if [ "$character" = "1" ]; then
	echo 1
elif [ "$character" = "2" ]; then
	echo 2
elif [ "$character" = "3" ]; then
	echo 3
else
	echo 输入不符合要求
fi

# test
# 写法一
if test -e /tmp/foo.txt; then
	echo "Found foo.txt"
fi

# 写法二
if [ -e /tmp/foo.txt ]; then
	echo "Found foo.txt"
fi

# 写法三
if [[ -e /tmp/foo.txt ]]; then # 支持正则
	echo "Found foo.txt"
fi

# 和文件相关
# [ -a file ]：如果 file 存在，则为true。
# [ -b file ]：如果 file 存在并且是一个块（设备）文件，则为true。
# [ -c file ]：如果 file 存在并且是一个字符（设备）文件，则为true。
# [ -d file ]：如果 file 存在并且是一个目录，则为true。
# [ -e file ]：如果 file 存在，则为true。
# [ -f file ]：如果 file 存在并且是一个普通文件，则为true。
# [ -g file ]：如果 file 存在并且设置了组 ID，则为true。
# [ -G file ]：如果 file 存在并且属于有效的组 ID，则为true。
# [ -h file ]：如果 file 存在并且是符号链接，则为true。
# [ -k file ]：如果 file 存在并且设置了它的“sticky bit”，则为true。
# [ -L file ]：如果 file 存在并且是一个符号链接，则为true。
# [ -N file ]：如果 file 存在并且自上次读取后已被修改，则为true。
# [ -O file ]：如果 file 存在并且属于有效的用户 ID，则为true。
# [ -p file ]：如果 file 存在并且是一个命名管道，则为true。
# [ -r file ]：如果 file 存在并且可读（当前用户有可读权限），则为true。
# [ -s file ]：如果 file 存在且其长度大于零，则为true。
# [ -S file ]：如果 file 存在且是一个网络 socket，则为true。
# [ -t fd ]：如果 fd 是一个文件描述符，并且重定向到终端，则为true。 这可以用来判断是否重定向了标准输入／输出错误。
# [ -u file ]：如果 file 存在并且设置了 setuid 位，则为true。
# [ -w file ]：如果 file 存在并且可写（当前用户拥有可写权限），则为true。
# [ -x file ]：如果 file 存在并且可执行（有效用户有执行／搜索权限），则为true。
# [ file1 -nt file2 ]：如果 FILE1 比 FILE2 的更新时间最近，或者 FILE1 存在而 FILE2 不存在，则为true。
# [ file1 -ot file2 ]：如果 FILE1 比 FILE2 的更新时间更旧，或者 FILE2 存在而 FILE1 不存在，则为true。
# [ FILE1 -ef FILE2 ]：如果 FILE1 和 FILE2 引用相同的设备和 inode 编号，则为true。

# 字符串
# [ string ]：如果string不为空（长度大于0），则判断为真。
# [ -n string ]：如果字符串string的长度大于零，则判断为真。
# [ -z string ]：如果字符串string的长度为零，则判断为真。
# [ string1 = string2 ]：如果string1和string2相同，则判断为真。
# [ string1 == string2 ] 等同于[ string1 = string2 ]。
# [ string1 != string2 ]：如果string1和string2不相同，则判断为真。
# [ string1 '>' string2 ]：如果按照字典顺序string1排列在string2之后，则判断为真。
# [ string1 '<' string2 ]：如果按照字典顺序string1排列在string2之前，则判断为真。

# 整数判断
# [ integer1 -eq integer2 ]：如果integer1等于integer2，则为true。
# [ integer1 -ne integer2 ]：如果integer1不等于integer2，则为true。
# [ integer1 -le integer2 ]：如果integer1小于或等于integer2，则为true。
# [ integer1 -lt integer2 ]：如果integer1小于integer2，则为true。
# [ integer1 -ge integer2 ]：如果integer1大于或等于integer2，则为true。
# [ integer1 -gt integer2 ]：如果integer1大于integer2，则为true

# 这里的整数不一定是declear的整数,
INT=-5

if [ -z "$INT" ]; then
	echo "INT is empty." >&2
	exit 1
fi
if [ $INT -eq 0 ]; then
	echo "INT is zero."
else
	if [ $INT -lt 0 ]; then
		echo "INT is negative."
	else
		echo "INT is positive."
	fi
	if [ $((INT % 2)) -eq 0 ]; then
		echo "INT is even."
	else
		echo "INT is odd."
	fi
fi

# 正则判断
#!/bin/bash
# =~ 是正则运算符
INT=-5

if [[ "$INT" =~ ^-?[0-9]+$ ]]; then
	echo "INT is an integer."
	exit 0
else
	echo "INT is not an integer." >&2
	exit 1
fi

# 与或非
# AND运算：符号&&，也可使用参数-a。
# OR运算：符号||，也可使用参数-o。
# NOT运算：符号!。

# 如果需要加括号,记得\转义
if [ ! \( $INT -ge $MIN_VAL -a $INT -le $MAX_VAL \) ]; then
	echo "$INT is outside $MIN_VAL to $MAX_VAL."
else
	echo "$INT is in range."
fi

# (( ... ))作为算数运算 也可以做if 的 condition
#!/bin/bash

INT=-5

if [[ "$INT" =~ ^-?[0-9]+$ ]]; then
	if ((INT == 0)); then
		echo "INT is zero."
	else
		if ((INT < 0)); then
			echo "INT is negative."
		else
			echo "INT is positive."
		fi
		if ((((INT % 2)) == 0)); then
			echo "INT is even."
		else
			echo "INT is odd."
		fi
	fi
else
	echo "INT is not an integer." >&2
	exit 1
fi

# case
echo -n "输入一个1到3之间的数字（包含两端）> "
read character
case $character in
1)
	echo 1
	;;
2)
	echo 2
	;;
3)
	echo 3
	;;
*) echo 输入不符合要求 ;;
esac

另一个例子
OS=$(uname -s)

case "$OS" in
FreeBSD) echo "This is FreeBSD" ;;
Darwin) echo "This is Mac OSX" ;;
AIX) echo "This is AIX" ;;
Minix) echo "This is Minix" ;;
Linux) echo "This is Linux" ;;
*) echo "Failed to identify this OS" ;;
esac
# 如果条件结尾是;;& 标识不退出条件块

# 以下是一些匹配的例子
# a)：匹配a。
# a|b)：匹配a或b。
# [[:alpha:]])：匹配单个字母。
# ???)：匹配3个字符的单词。
# *.txt)：匹配.txt结尾。
# *)：匹配任意输入，通过作为case结构的最后一个模式。

# 循环
number=0
while [ "$number" -lt 10 ]; do
	echo "Number = $number"
	number=$((number + 1))
done

# for ... in
for i in word1 word2 word3; do
	echo $i
done

# 标识当前目录所有png
for i in *.png; do
	ls -l $i
done

#例子3
count=0
for i in $(cat ~/.bash_profile); do
	count=$((count + 1))
	echo "Word $count ($i) contains $(echo -n $i | wc -c) characters"
done

# in list 省略, 默认值是脚本的所有参数
for filename; do
	echo "$filename"
done

# 等同于

for filename in "$@"; do
	echo "$filename"
done

# C语言for
for ((i = 0; i < 5; i = i + 1)); do
	echo $i
done

#例子2
for (( ; ; )); do
	read var
	if [ "$var" = "." ]; then
		break
	fi
done

# select
select brand in Samsung Sony iphone symphony Walton; do
	echo "You have chosen $brand"
done

# 和用户输入有关联
# $ ./select.sh
# 1) Samsung
# 2) Sony
# 3) iphone
# 4) symphony
# 5) Walton
# #?

echo "Which Operating System do you like?"

select os in Ubuntu LinuxMint Windows8 Windows7 WindowsXP; do
	case $os in
	"Ubuntu" | "LinuxMint")
		echo "I also use $os."
		;;
	"Windows8" | "Windows10" | "WindowsXP")
		echo "Why don't you try Linux?"
		;;
	*)
		echo "Invalid entry."
		break
		;;
	esac
done

#函数
# 第一种
fn() {
	# codes
}

# 第二种
function fn() {
	# codes
}

# 这两种都对
# 函数也可以传参
# 也是$1 $2 $3 ...
function alice() {
	echo "alice: $@"
	echo "$0: $1 $2 $3 $4"
	echo "$# arguments"

}

alice in wonderland # in 是第一个参数, wonderland是第二个参数

# 函数体内声明的变量默认是全局变量
# 如果想声明局部变量 需要使用local

fn() {
	local foo
	foo=1
	echo "fn: foo = $foo"
}

fn
echo "global: foo = $foo"

# 数组
array[0]=val
array[1]=val
array[2]=val
array=(a b c)
array=([2]=c [0]=a [1]=b)

array=(
	a
	b
	c
)

names=(hatter [5]=duchess alice)
names[0]=hatter
names[5]=duchess
names[6]=alice
# 数组默认值是空字符串
# 返回数组全部元素
for i in "${names[@]}"; do # 或 for i in "${names[*]}"; do
	echo $i
done

# 一般倾向于将数组放在双引号中.因为
$ activities=( swimming "water skiing" canoeing "white-water rafting" surfing )
$ for act in ${activities[@]}; \
do \
echo "Activity: $act"; \
done

Activity: swimming
Activity: water
Activity: skiing
Activity: canoeing
Activity: white-water
Activity: rafting
Activity: surfing
################################################################
$ for act in "${activities[@]}"; \
do \
echo "Activity: $act"; \
done

Activity: swimming
Activity: water skiing
Activity: canoeing
Activity: white-water rafting
Activity: surfing

# 获取数组长度
${#array[*]}
${#array[@]}

# 提取数组序号
arr=([5]=a [9]=b [23]=c)
echo ${!arr[@]} # 标识 这些位置有值
5 9 23
echo ${!arr[*]}
5 9 23

arr=(a b c d)

for i in ${!arr[@]};do
  echo ${arr[i]}
done

# 提取部分数组成员
# ${array[@]:position:length}

food=( apples bananas cucumbers dates eggs fajitas grapes )
echo ${food[@]:1:1} # 数组的第一个成员后面数1个
bananas
echo ${food[@]:1:3}
bananas cucumbers dates # 数组的第一个成员后面数3个

# 省略长度, 则一直到最后.
echo ${food[@]:4}
eggs fajitas grapes

# 追加
foo=(a b c)
echo ${foo[@]}
a b c

foo+=(d e f)
echo ${foo[@]}
a b c d e f

# 删除 unset
foo=(a b c d e f)
echo ${foo[@]}
a b c d e f

unset foo[2]
echo ${foo[@]}
a b d e f

# 关联数组 类似哈希?
declare -A colors # 声明
colors["red"]="#ff0000"
colors["green"]="#00ff00"
colors["blue"]="#0000ff"
echo ${colors["blue"]}

# 有些命令不接受管道 需要xargs辅助
# find /sbin -perm +700 |ls -l       #这个命令是错误的
# find /sbin -perm +700 |xargs ls -l   #这样才是正确的
```