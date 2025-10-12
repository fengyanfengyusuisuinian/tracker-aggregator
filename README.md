<div align="center">
<h1>AD Filter Subscriber</h1>
  <p>
    tracker规则订阅器，整合不同来源的规则，帮助你快速构建属于自己的规则集~
  </p>
<!-- Badges -->
<p>
  <img src="https://img.shields.io/github/last-commit/fordes123/ad-filters-subscriber?style=flat-square" alt="last update" />
  <img src="https://img.shields.io/github/forks/fordes123/ad-filters-subscriber?style=flat-square" alt="forks" />
  <img src="https://img.shields.io/github/stars/fordes123/ad-filters-subscriber?style=flat-square" alt="stars" />
  <img src="https://img.shields.io/github/issues/fordes123/ad-filters-subscriber?style=flat-square" alt="open issues" />
  <img src="https://img.shields.io/github/license/fordes123/ad-filters-subscriber?style=flat-square" alt="license" />
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
#### 支持的规则格式
- [x] easylist
- [x] dnsmasq
- [x] clash
- [x] smartdns
- [x] hosts

#### 注意事项
1. 仅支持基本规则转换，即域名、通配域名构成的规则，对形如 `||example.org^$popup` 等规则无法转换(合并、去重不受影响) 
2. 接受不可避免的缩限，如 `||example.org^` 将拦截 example.org 及其所有子域，但将其转换为 hosts 格式时，将无法匹配子域名。
3. 规则有效性检测基于域名解析，因此仅支持基本规则 (只能检测当前域有效性，而无法检测其是否存在有效子域，故此功能可能存在误杀)。

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
