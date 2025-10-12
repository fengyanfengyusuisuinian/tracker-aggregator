<div align="center">
<h1>tracker aggregator  Subscriber</h1>
  <p>
    tracker规则订阅器，整合不同来源的规则，帮助你快速构建属于自己的规则集~
  </p>
<!-- Badges -->
<p>
  <img src="https://img.shields.io/github/last-commit/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="last update" />
  <img src="https://img.shields.io/github/forks/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="forks" />
  <img src="https://img.shields.io/github/stars/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="stars" />
  <img src="https://img.shields.io/github/issues/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="open issues" />
  <img src="https://img.shields.io/github/license/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="license" />
</p>

<h4>
    <a href="#a">项目说明</a>
  <span> · </span>
    <a href="#b">快速开始</a>
  <span> · </span>
    <a href="#c">规则订阅</a>
  <span> · </span>
    <a href="#d">问题反馈</a>
  </h4>
</div>

[English](./README_en.md) | 中文
<h2 id="a">📔 项目说明</h2>

本项目旨在聚合不同的tracker服务器
#### **主要文件**

- sync.yml
- main.py
- sources.list----------tracker服务器列表
#### **Github Action**

- fork 本项目
- 自定义规则订阅 (可选)
    - 参照[示例配置](./config/application-example.yaml)，修改配置文件: `config/application.yaml`
- 打开 `Github Action` 页面，选中左侧 `Update Filters` 授权 `Workflow` 定时执行(⚠ 重要步骤)
- 点击 `Run workflow` 或等待自动执行。执行完成后规则将生成在 `release` 分支

#### **Codespaces**

- 登录 `Github`，点击本仓库右上角 `Code` 按钮，选择并创建新的 `Codespaces`
- 等待 `Codespaces` 启动，即可直接对本项目进行调试

<h2 id="c">🎯 规则订阅</h2>

**⚠ 本仓库不再提供规则订阅，我们更推荐 fork 本项目自行构建规则集.**

下面是使用了本项目进行构建的规则仓库，可在其中寻找合适的规则订阅:
<details>
<summary>点击查看</summary>
<ul>
    <br/>
    <li><a href="https://github.com/xndeye/adblock_list/">xndeye/adblock_list</a></li>
</ul>
</details>



# Tracker Aggregator

Tracker Aggregator 是一个用于聚合和管理 BitTorrent Tracker 列表的工具。  
该文件**基于 [www.baidu.com](https://www.baidu.com) 的原始项目修改**，经过优化和重构，现已成为独立工具。

## 功能

- 自动抓取多个 Tracker 源
- 去重与排序
- 生成可用 Tracker 列表
- 记录无法访问的源到 `TrackerServer/bad_tracker.txt`
- 支持 GitHub Actions 自动更新

## 使用方法

1. 克隆仓库：
   ```bash
   git clone https://github.com/your-username/tracker-aggregator.git
   cd tracker-aggregator
