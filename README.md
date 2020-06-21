

# 基于PyQt5的网上书店管理系统

[toc]

## 界面设计

### 登陆界面

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607200922.png)

由于是管理系统所以不设置注册

功能：

- 当用户名与密码不符时，保留用户名，清除密码栏

### 主页

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607201220.png)

功能：

- 提供管理图书信息的接口
- 提供查看会员信息的接口（由于是管理端，所以对会员信息的修改，在客户端，管理端不提供接口）
- 提供查看购买记录的接口

### 图书信息管理页

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607201601.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607202313.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607202535.png)

功能：

- 实现分页操作
- 提供进货的接口
- 提供出货的接口
- 提供修改图书信息的接口
- 查询图书信息（当查询失败时，发出提示信息，展现所有图书）
- 返回主页
- 内容居中
- 相邻行颜色深浅不同
- 不可编辑

### 进货页面

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607201831.png)

功能：

- 购入图书
- 智能补全，当图书名称、作者、出版社在数据库中存在（即书店中存在这种书）时智能补全图书种类与销售价格，当图书名称、作者、出版社在数据库中不存在时（即书店从未进过这本书）补全图书种类、销售价格与购入数目由用户输入

### 出货页面

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607202706.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607202904.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607203338.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607203442.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607203458.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607203628.png)

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607204537.png)

功能

- 智能检查：检查书店存在此图书以及电话号码是否合法
- 采用下拉框智能补全，通过出售书名来补全，作者信息栏，通过出售书名来补全出版社，以确保书名，作者，出版社一一对应；通过买方手机号来补全默认配送地址，配送地址可随改
- 智能提示：提示书名与电话号码填写问题
- 第二遍确认

### 修改图书页

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607204627.png)

功能：

- 修改图书信息（按下修改，使其一行可以修改，其余行不可修改，且不同行按钮处于冻结状态，按下完成按钮修改内容同步至数据库）
- 翻页
- 返回上一级
- 查询

### 查看会员信息

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607205033.png)

功能：

- 不可编辑
- 分页
- 查询
- 返回主页

### 查看购买记录

![](https://gowi-picgo.oss-cn-shenzhen.aliyuncs.com/picgo/20200607205146.png)

功能

- 查询
- 分页
- 按时间排序
- 不可编辑

## 文件结构

```
.
├── Add_bookUI.py
├── Book_informationUI.py
├── Buy_OrderUI.py
├── Change_bookUI.py
├── Controller.py
├── LoginUI.py
├── MainUI.py
├── Member_informationUI.py
└── Sell_bookUI.py

0 directories, 9 files
```

使用模块

- PyQt5
- pymmsql
- sys

## 数据库设计

SQL Server2017

```sql
use Course_Design
create table Book_Information
(
    Book_no               char(8) primary key, --书籍编号
    Book_name             nchar(10) not null,  --书籍名称
    Book_author           nchar(10) not null,  --书籍作者
    Book_Publishing_house nchar(20) not null,  --出版社
    Book_kind             nchar(10) not null,  --书籍种类
)

create table Book_storage
(
    Book_no    char(8) primary key, --书籍编号
    Book_price money not null,      --价格
    Book_stock int   not null,      --库存
    constraint FK_Book_no foreign key (Book_no) references Book_Information (Book_no),
)

create table Member_Information
(

    Member_no      char(8) primary key,                                                --会员编号
    Member_name    nchar(8)  not null,                                                 --会员姓名
    Member_sex     nchar(2)  not null default N'男' check (Member_sex in (N'男', N'女')), --会员性别
    Member_address nchar(20) not null,                                                 --会员住址
    Member_phone   char(11)  not null,                                                 --会员电话
)
create table Buy_Book
(
    Number    tinyint       not null primary key,
    Member_no char(8)       not null,
    Book_no   char(8)       not null,
    Buy_num   tinyint       not null,
    Delivery  nchar(2)      not null default N'否' check (Delivery in (N'是', N'否')), --是否配送
    Buytime   smalldatetime not null,                                               --购买时间
)
```

