
# unidbg-jd-sign
某东sign app version 11.0.2

### 使用方式:
1.加载到idea

2.add 个maven工程

3.运行 `UnidbgServerApplication.java` 即可启动服务

### 修改配置和代码
通过 `application.properties` 自行修改服务的地址(默认`0.0.0.0`就行)和端口(默认是`8888`)

修改绝对路径为你的apk所在的文件夹

apk.path = F:/jd/jd.apk

so.path = F:/jd/libjdbitmapkit.so

（apk不提供自行网上下载最新版）

（so文件提取 把apk重命名为.zip 用压缩软件打开\lib\armeabi-v7a下面即可找到so文件）

### 打jar包
配置好maven环境的前提下，项目主目录执行
````java
 mvn clean package -Dmaven.test.skip=true  
````
使用maven的package即可，之后会发现生成一个target目录其中里面就有jar包了。
```
mvn package
```
把application.properties 复制到 jar包所在目录 方便修改
### 使用jar包
```
java -jar target\unidbg-server-0.0.2.jar 
```
### 调用示例
```
查看 根目录 忒星59-20.py
```

