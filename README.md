# code-monkey
## 介绍
本代码库是我学习各种量化策略的源码实现以及心得体会。代码采用了RQalpha框架进行回测，有关RQalpha的内容请参考:[https://github.com/ricequant/rqalpha](https://github.com/ricequant/rqalpha)

## 目录结构
每个目录就是一种量化策略，目录里包含以下几个文件：
- README.MD 策略相关介绍分析
- 目录名.py 策略源码主代码文件
- config.yml 策略快速验证的配置文件
- backtest.py 策略完整回测的测试代码

## 使用方法
### 准备工作
按照RQalpha的指导配置好RQalpha并更新RQalpha的回测数据存放在默认位置
### 快速验证
在相应策略目录下执行
> rqalpha run

### 完整验证
在相应策略目录下执行
> python ./backtest.py

## 策略列表
- [二八策略](https://github.com/ShekiLyu/code-monkey/tree/master/two-eight)
- [Dual Thrust策略](https://github.com/ShekiLyu/code-monkey/tree/master/dual-thrust)
- 海龟策略
- Long/Short 策略
- 资产配置
