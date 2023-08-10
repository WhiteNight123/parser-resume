# 智能简历解析系统

## 简介

​    这是一个智能简历解析系统，用户可以上传简历（支持**docx，pdf，png和txt**）或者**手动输入**简历信息，系统可以自动解析用户上传的简历。当输入简历个数为1条时，系统自动提取简历中的关键信息，提取的内容包括**姓名，出生年月，年龄，政治面貌，学历，电话，毕业院校**，然后根据提取的信息进行人才画像构建，分析出**选手标签，预计薪酬，匹配岗位及匹配优先级**，提升招聘效率。当上传简历为多条时，系统进行简历信息统计分析，输出可视化图表，包括**学历统计，年龄统计，毕业院校统计和工作年限统计**，方便企业了解求职者的总体水平。

​    项目基于python语言，客户端部分使用的**OyQt6**，服务端部分使用的是**paddle模型**和自己的**微调模型**，模型是在移动**九天·毕昇**平台上跑出来的。

## 运行

1. 创建并激活一个python虚拟环境。

```sh
$ cd rprename_project/
$ python3 -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. 安装依赖包。

```sh
(venv) $ pip install -r requirements.txt
```

3. 运行程序

```sh
(venv) $ python3 main.py
```

**注意:** 这个应用在 Python 3.10.11 and PyQt 6.4.2上编译并测试通过。

## 项目架构

**系统模块图**

<p align="center"><img src="https://s2.loli.net/2023/07/16/SnRdYvACDWjfL6E.png" alt="image-20230716084200977" width="700px" /></p>

**系统用例模型图**

<p align="center"><img src="https://s2.loli.net/2023/07/16/BIoZCywhA9vJduk.png" alt="image-20230716084400646" width="500px" /></p>

**系统流程图**

<p align="center"><img src="https://s2.loli.net/2023/07/16/sDib4QZk2YlIPEA.png" alt="image-20230716084220419" width="500px" /></p>

**系统时序图**

<p align="center"><img src="https://s2.loli.net/2023/07/16/ehf7OX8yFAJSGQK.png" alt="image-20230716084301767" width="500px" /></p>

## 界面运行结果

**文件上传界面**
<p align="center"><img src="https://s2.loli.net/2023/07/15/xobhWt7NiD9QTZU.png" alt="界面1" width="300px" /></p>

**手动输入界面**
<p align="center"><img src="https://s2.loli.net/2023/07/15/QpEFk7MB1NIA2Oi.png" alt="界面2" width="300px" /></p>

**基本信息界面**
<p align="center"><img src="https://s2.loli.net/2023/07/15/K7ExgRjbIFqCndt.png" alt="界面3" width="300px"/></p>

**人才画像界面**
<p align="center"><img src="https://s2.loli.net/2023/07/15/ZYlsaJKOjV5zXrD.png" alt="界面4" width="300px" /></p>

**统计可视化界面**
<p align="center"><img src="https://s2.loli.net/2023/07/15/X4nlO7RgAqszWIU.png" alt="界面5" width="300px"/></p>

<p align="center"><img src="https://s2.loli.net/2023/07/15/usRgjdGKIWL5SAt.png" alt="界面6" width="300px" /></p>
