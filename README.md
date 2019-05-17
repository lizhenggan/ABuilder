# 前言
Python开发的mysql链式操作，ABuilder告别繁琐的模型定义，节省开发时间，几乎没有任何要求，导入直接使用。与常规模型不同ABuilder不需要预先定义表字段、字段类型、字段长度等繁琐的设置，当然那样做有它的优点这里就不说了～，各具所长取舍看个人。ABuilder支持入直接使用，简单、快速、便捷

# 快速开始
- 安装 a-sqlbuilder
```python
pip3 install a-sqlbuilder
```
- 设置数据配置文件（参照数据库配置文件说明）
- 开始使用
```python
from ABuilder.ABuilder import ABuilder

model = ABuilder()
data = model.table('tar_user').field("username,id").where({"username": ["like", "%M-萌%"]}).limit(0, 1).query()
```
# 使用文档

## 第三方库要求
- pymysql
- logging
## 数据库配置文件
我们需要开发者在项目更目录中加入`database.py` 数据库配置文件

确保`from database import database`能获取到数据库配置项

配置文件实例:
```python
class Config(object):
    pass

class Proconfig(Config):
    pass


class Devconfig(Config):
    debug = True
    DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/target'
    data_host = '127.0.0.1' 
    data_pass = 'root'
    data_user = 'root'
    database = 'target'
    data_port = 3306
    charset = 'utf8mb4'


database = Devconfig
```
## 支持函数
目前项目只支持一些简单用法具体如下
- table 查询表
- where where条件
- where_or 设置or条件
- field 查询字段 
- limit 查询条数
- group 分组
- order 排序
- join 连表查询
- first 查询单条
- query 查询多条
- pluck 查询单个字段
- insert 插入
- update 修改
- delete 删除
- select 执行原生查询
- commit 事物提交
- rollback 事物回滚
- get_last_sql 获取执行sql
- get_insert_id 获取插入id
### table
> 设置查询表
```python
from ABuilder.ABuilder import ABuilder
data = ABuilder().table('user').limit(0,1).query()
print(data)
```
### where
> 设置where条件
```python
from Amo.ABuilder import ABuilder
ABuilder().table('user').where({"id":["=",3]}).first()
```
多个where条件
```python
ABuilder().table('user').where({"id":['<=',10],"sex":["=","男"]}).query()
# 或则多个where拼接
ABuilder().table('user').where({"id":['<=',10]}).where({"sex":["=","男"]}).query()
```
比较符号支持 `=,<>,<,>,<=,>=,in,like`等
### where_or
> 设置or条件
`where_or`使用方法与where大同小异
```python
from Amo.ABuilder import ABuilder
ABuilder().table('user').where_or({"id":["=",3]}).query()
```
比较符号支持 `=,<>,<,>,<=,>=,in,like`等
### field
> 设置查询字段
```python
ABuilder().table("user").field("user_id,sex,user_name").query()
# 举例count使用
ABuilder().table("user").field("count(*) as count").query()
```
不设置field默认查询全部字段 `*`,查询字段使用`,`隔开,支持`count(),sum()`等

注意：不支持类似`DATE_FORMAT(NOW(),'%m-%d-%Y')`这类带有`%`的函数
### limit
>查询数
```python
ABuilder().table("user").limit(0,10).query()
```
> `limit` 第一个参数为开始查询位置，第二个参数为获取多少条
### group
>分组
```python
# 按照性别分组
ABuilder().table("user").field("count(*) as count").group('sex').query()

# 多个分组使用
ABuilder().table("user").field("count(*) as count").group('sex').group('age').query()
# sql为：select count(*) as count from user group by sex,age
```
### order
> 排序
```python
ABuilder().table("user").order("user_id","desc").query()

# 多个排序值
ABuilder().table("user").order("user_id","desc").order("sex",'asc').query()
# sql为：select * from tar_user order by user_id desc,sex asc
```
`order by`先后顺序：遵循从左到右
### join
> 连表查
```python
ABuilder().table('user as u').field('u.id,b.name').join('book b', 'u.id=b.user_id','INNER').where({"u.id": ['=', 1]}).query()

# sql为：select u.id,b.name from user as u INNER JOIN book b on u.id=b.user_id where u.id = 1
```
join三个参数说明
- 表名
- 列表条件 支持 `and,or`
- join类型：`INNER,LEFT,RIGHT,FULL` 默认INNER

支持多个连表，拼接多个join即可。例如:`table('table as t').join('table1 t1','t1.user_id=t.id').join('table2 t2','t1.id=t2.book_id')`
### first
>查询单条记录
```python
find = ABuilder().table('user').where({"id":["=",3]}).first()
print(find)
```
### query
>查询多条记录
```python
data = ABuilder().table('user').where({"id":["in",(1,2,3,4)]}).query()
print(data)
```
### pluck 
>查询单个字段
```python
user_id = ABuilder().table('user').where({"username":["=",'张三']}).pluck('id')
print(user_id)
```
### insert
> 插入数据
```python
model = ABuilder()
state = model.table("user").insert({"username":"张三","sex":'男',"age":18})
if state:
    print("添加成功！自增id：%" % model.get_insert_id)
else:
    print("添加失败")
```
### update
> 修改记录
```python
state = ABuilder().table("user").where({"username":["=","张三"]}).update({"age":25})
if state:
    print('修改成功')
else:
    print('修改失败')

```
### delete
> 删除记录
```python
state = ABuilder().table("user").where({"username":["=","张三"]}).delete()
if state:
    print('删除成功')
else:
    print('删除失败')
```
### select
>执行原生sql
```python
model = ABuilder()
# 第一种方式
model.select("SELECT username,id FROM user where id=%s", [1])
# 第二种方式
model.select("SELECT username,id FROM user where id=1")
```
### commit，rollback
> 事物操作
```python
model = ABuilder()
state = model.table("user").insert({"username":"张三","sex":'男',"age":18})
if state:
    state = model.table("book").insert({"book_name":'书本昵称',"user_id":model.get_insert_id})
if state:
    # 成功则提交事物
    model.commit()
else:
    # 失败则回滚事物
    model.rollback()
```
操作事物注意事项：请勿实例多个ABuilder否则一部分事物在回滚操作时回滚失败
```python
def fun1():
    model = ABuilder()
    state = model.table("user").insert({"username":"张三","sex":'男',"age":18})
    if state:
        state = fun2()
   
    if state:
        model.commit()
    else:
        model.rollback()

def fun2():
    model = ABuilder()
    return  model.table("book").insert({"book_name":'书本昵称',"user_id":model.get_insert_id})

fun1()
```
这样如果`fun2()`返回失败的是失败状态回滚的只是`fun1()`执行的sql却无法回滚`fun2()`执行的sql，正确做法如下：
```python
def fun1():
    model = ABuilder()
    state = model.table("user").insert({"username":"张三","sex":'男',"age":18})
    if state:
        state = fun2(model)
   
    if state:
        model.commit()
    else:
        model.rollback()

def fun2(model):
    return  model.table("book").insert({"book_name":'书本昵称',"user_id":model.get_insert_id})

fun1()
```
### get_last_sql
> 获取最后一条执行sql
```python
 model = ABuilder()
 find = model.table('user').where({"id":["=",3]}).first()
 print(model.get_last_sql)
```
获取sql注意事项：输出的sql对于字符串没有加上引号，导致拷贝到数据库管理工具里无法执行，处理办法：给予字符串加上单引号或双引号即可，后面维护会优化（抱歉）
### get_insert_id
> 获取插入自增id
```python
model = ABuilder()
model.table("user").insert({"username":"张三","sex":'男',"age":18})
print(model.get_insert_id)
```
## class继承方式使用示例
```python
from ABuilder.ABuilder import ABuilder
class UserModel(ABuilder):

    def __init__(self):
        self.table_name = 'user'
        
    def user_info(self,user_id):
        info = self.table(self.table_name).field("user_id,user_name").where({"user_id":user_id}).first()
        print(self.get_last_sql)
        return info
        
    def login(self):
        pass
        
userInfo = UserModel().user_info(user_id=1)
print(userInfo)
```
## 案例项目
### 目标记账+
!['目标记账+'](http://poto.adooe.com/target_logo.jpg)



记账+。记账与目标结合，随时随地记录每一笔交易，人情来往，多人记账，每日记账实时统计与目标距离，即时了解资金概况资金流向
## 感谢
项目初期是非常第一个简单版本，如有问题，写法不规范的欢迎反馈，千言万语，你懂的，我就不说了