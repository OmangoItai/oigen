# OI Gen

Data generator for OI.

一款准备做得专业化的微型框架，用于算法竞赛的出题工作。

OI Gen 拥有友好的交互、报错支持，支持灵活的小功能组合，3 分钟一个 python 脚本，告别**所有**市面上繁琐的劣质 GUI 和系统脚本编写。

## 快速开始

首先，配置 OI Gen。包括题目用到的参数 `args`，标准程序（AC 代码可执行文件）路径 `stdFilePath` 和 io 数据生成路径 `ioFilePath`

```py
from oigen import OI
from oigen.oitypes import CppType

oi = OI({
    "args": {
        "n": CppType.Int
    },
    "stdFilePath": "./ac.exe",
    "ioFilePath": "./test",
})
```

使用`@oi.handler`装饰器向 OI Gen 挂载一个 handler，用于数据生成。这里挂载一个序列生成的方法

```py
from oi.values import randInt
# 注意：randInt(l, r) 会返回一个随机值的生成器，即返回 random.randint(l, r) 的函数签名
# 要返回值需要 randInt(l, r)()
@oi.handler("seq")
def anyNameIsOK(n: int):
    text = ''
    text += f"{n}\n"
    for i in range (1, n+1):
        text += str(randInt(114, 514)()) + ' ' 
    return text
```

生成 4 组数据，指定 handler 并填写题目参数的范围

```py
oi.gen(4, "seqh", {
    "n": randInt(1,10)
})
```

随机值生成器 `randInt` 会应用在每轮数据中，为你自动生成范围内的值

```sh
> poetry run python test.py
Oi Gen 0.1.0 initialized.
[06:31:36] "1.in", "1.out" done.
           "2.in", "2.out" done.
           "3.in", "3.out" done.
           "4.in", "4.out" done.
Gnerating... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

完毕

## 配置 OI Gen

将本题需要的数据填写进 `args` 中，并填入你的**标准程序（std）路径**和**题目数据路径**

标程是你的正解代码所生成的**二进制文件**，**暂不支持源码编译自动执行！！不要填写源代码路径！**

题目数据路径是 **批量生成`*.in`，`*.out`** 的路径，请单独安排，避免污染文件夹

```py
oi = OI(config = {
    "args": {
        "n": CppType.Int,
        "m": CppType.Int,
    },
    "stdFilePath": "std.exe",
    "ioFilePath": "test/",
})
```

## 生成数据

使用装饰器 `@oi.handler()` 向 OI Gen 挂载数据生成方法，该方法返回字符串作为题目数据文件的内容

```py
@oi.handler("seq")
def wirteSeq(n: int, m: int):
    # randInt 返回的是一个随机数生成器（函数），需要调用一次
    seq = [randInt(1, n//2)() for _ in range(n)]
    text = f"{n} {m}\n"
    text += " ".join( map(str, seq) )
    return text
```

生成 2 组数据

记得指定**已挂载的**生成方法 handler，并填写参数范围

支持**字面量**和**随机生成器**两种挂载方法（随机值生成器在 `oigen.values` 中）

```py
oi.gen(2, "seq", {
    "n": randInt( 5, 10 ),
    "m": 0,
})
```

再来 4 组更大范围数据

```py
oi.gen(4, "seq", {
    "n": randInt( 1000, 9999 ),
    "m": randInt( 5, 20 ),
})
oi.gen( 4, "seq" )
```

数据们将按序排列好 

```sh
1.in 1.out
2.in 2.out
3.in 3.out
4.in 4.out
5.in 5.out
6.in 6.out
```

……OI Gen 会记录数据批次，方便你生成不同规模的数据

## 测试工具

如果你想单纯测试 **标准程序（std）** 的输出结果，可以使用`run`

```py
oi.debug.run()
```

你可以手动打开 `printOnly` 开关，在终端查看结果，防止更改 `*.out` 文件；

默认对所有`.in`和`.out`文件进行测试，也可以手动指定测试的数据编号

```py
oi.debug.run(targetIO = [1,2,3,4], printOnly = True )
oi.debug.run(targetIO = range(6,10+1), printOnly = False )
```

OI Gen 还提供比较工具，方便你对比两份代码的差异

`debug.compareRun` 会在结果相同时，返回 `True`；在结果有差异时，返回一个**问题数据列表**

你可以选择是否在终端查看它们，`isPrint` 开关默认为 `False`

默认对所有`.in`和`.out`文件进行测试，也可以手动指定对比的数据编号

```py
oi.debug.compareRun( 'wrongAanswer.exe', targetIO = [7, 8, 9, 10], isPrint = True )
```

```sh
============= 7.in =================
std.exe:
23

pusu.exe:
0

============ 10.in ==================
std.exe:
39

pusu.exe:
0
```

## 养蛊

你当然可以利用 debug 工具中的 `debug.compareRun` 来反复测试数据强度，而无需手动构造复杂数据。

比如对一个分阶段数据，前 50 分送了，后 50 分高强度。假设我们有一个 **simple** 和一个 **hack** 做法：

```py
...
@oi.handler('matrix')
def ...

oi.gen( 5, 'matrix', {
    ... # some simple data
})

while True:
    oi.setCurrentBatch(6) # begein at 6.in
    oi.gen( 5, 'matrix')
    if oi.debug.compareRun('simple.exe', range(6, 10+1)) == True or oi.debug.compareRun('hack.exe', range(6, 10+1)) == True:
        continue
    else
        break

```

这样就能不停养蛊，直到同时产生后 5 组高强度数据。虽然但是，我还是建议你一组组强化养蛊，否则挺难凑巧同时出现 5 组强数据……

## 挖坑

由于作者深知这些搞 ACM 和 OI 的人对于工业的偏见有多深，以及他们可怜的工业水平（好多区域金选手甚至去私企实验室了若干年**连编译和工具链都不会**！），虽然贴了 MIT 协议，但作者几乎放弃了用开源社区把该项目做正规的想法……因此，只能长期低频地亲自更新。

对于该项目为什么要叫 OI 而不是 ACM，大概是因为名字短。

以后可能会涉及到的优化：

- 加强`debug.compareRun`自动养蛊策略，对于同一批次的强数采取据保留而非直接重写
- ✅~~加个数据生成的进度条~~优化了所有界面，保证弱智也能看懂报错和提示
- 支持源码编译到执行，包括一些主流语言（cpp、py、java）
- 添加沙盒保护
- 添加对于常规题目类型的自定义**自动模板**`handler`，比如`@oi.sequence`、`@oi.matrix()`装饰器
- 引入一下机器学习，试试 ai 养蛊
- 搞个前端，在线化服务 ~~，开始恰烂钱~~
- 加入 pip 套餐，未来使用 pip 安装

作者很穷，为了不给大厂卖沟子，已经吃了超过 12 月的一天两顿 `(泡面，面包)` 了，长期处于拖着房租不交的状态。

所以，慢点催（即便没人催 orz）……

## 不该说的话……

选手们即便拿了金，若干年退役后，请问是从头开始学 现代工业算法、AI 算法，还是转工业界学现代工业标准和思路呢？到头来还不是发现竞赛打过头了，越到尖端赛场对于知识的收益逐渐趋 0……

很巧，作者从大一开始搞学术（纯算法到 AI、数据库研究），后面转基建（系统级编程、编译器、虚拟机之类），再到后来转工业界跟着做前后端开发（Node 全家桶、Go 之类），可以说几乎都见识过算法竞赛对于这些方向的 **“帮助”**——比赛越难，越没帮助。

虽然作者现在在承接一些 ACM/OI 机构的教练、出题等烂活儿，也知道教练这口屎难吃——谁会闲的没事做，人为给学生制造问题，还把学生一路带向职业化竞赛的道路呢？

> 作者也算有个二专，哲学能到研一研二水平。  
> 后来在教青少年的时候，有机会都愿意和他们讲讲形式语言、谓词逻辑、哲学体系、简单数学体系等……很多知识并非竞赛市场的劣质教练们提一嘴就过了，把这些联通了讲，不仅极大简化了学生整合知识的时间，也是彻底不让知识沦为**魔法和封建迷信**——竞赛教练们为了速度，知其然而不知其所以然，稀里糊涂就教了，美其名曰“这是数学，你学不懂，别再问了”——这在竞赛市场太严重了。 
> 我完全知道，当下，要么采用我事必躬亲的**贵族教育**，要么采用工业化的办法，用知识垃圾批量制造工业人口——如果没有彻底的教育革命的话……  

大家肯定要怪大环境，怪CCF……CCF 的丑事想必各位教练都知道：为了捞钱从改 csp 赛制到演都不演，直接让小学生考级，每年 4 次，批量产生报名费需求的同时又批量生产 noi 教练证（非常水的证书）。

我想说的是：

> 我知道，没有哪个具体的人，改变得了大环境。  
> 不管你对现行教育制度是否嗤之以鼻，是否为此昂首奔走呼号过，是否为此垂首泣不成声过  
> 也许好用点的 OI Gen 能让你多些时间，和孩子们说说真话，把他们往正路，而不是资本主义给自己制造的，由假问题们构成的死路上引  
> 但愿，我们能一点点地救回孩子们……  