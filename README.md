RDFZCmsAutoEvaluation
=====================

A simple python script to automatically fill in the faculty evaluations page.

[Info]
这是一个自动完成人大附中cms评价教师系统的程序，使用python 3.4在OSX10.9.4下编写

[Instructions]
由于懒得弄binaries了，所以各位请自行下载python(3.4)及以上运行
rules.txt里是规则，Default 为默认值，可以自行添加条目，非OSX系统建议重新创建此文件
规则格式为“名称＋空格＋选项”，若选项为ABCD中的一个（不区分大小写），则为此名称的老师的每个选项设置为此，若是其它字母则为随机生成选项
如有bug就自己改吧...
