<div align="center">
<h1>Tracker aggregator  Subscriber</h1>
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
    <a href="#c">规则订阅</a>
  <span> · </span>
    <a href="#d">问题反馈</a>
  </h4>
</div>

[English](README_en.md) | 中文

<h2 id="a">📔 项目说明</h2>
Tracker aggregator Subscriber 是一个用于聚合和管理 BitTorrent Tracker 列表的工具。该项目受 fordes123的广告过滤规则订阅器 https://github.com/fordes123/ad-filters-subscribe 项目启发经过优化和重构。

#### **功能**

- 自动抓取多个 Tracker 源
- 去重与排序
- 生成可用 Tracker 列表
- 记录无法访问的源到 `TrackerServer/bad_tracker.txt`
- 支持 GitHub Actions 自动更新

#### **Github Action**

- fork 本项目
- 自定义规则订阅 (可选)
  - 修改tracker源文件: `sources.list`
  - 修改修改配置文件: `config/sync.yml`
- 打开 `Github Action` 页面，选中左侧 `Update Filters` 授权 `Workflow` 定时执行(⚠ 重要步骤)
- 点击 `Run workflow` 或等待自动执行。执行完成后规则将生成在 `release` 分支

#### **Codespaces**

- 登录 `Github`，点击本仓库右上角 `Code` 按钮，选择并创建新的 `Codespaces`
- 等待 `Codespaces` 启动，即可直接对本项目进行调试


<details>
<summary>#### **点击查看上游规则**</summary>
<ul>
   <!--  <li><a href="https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt">AdGuard 基础过滤器</a></li> -->
  <li><a href="https://newtrackon.com/api/all">newtrackon.com/api/all</a></li>
  <li><a href="https://trackerslist.com/all.txt">trackerslist.com/all.txt</a></li>
  <li><a href="https://newtrackon.com/api/stable">newtrackon.com/api/stable</a></li>
  <li><a href="https://at.raxianch.moe/AT_all.txt">at.raxianch.moe/AT_all.txt</a></li>
  <li><a href="https://gcore.jsdelivr.net/gh/XIU2/TrackersListCollection/all.txt">gcore.jsdelivr.net/gh/XIU2/TrackersListCollection/all.txt</a></li>
  <li><a href="https://cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_best.txt">cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_best.txt</a></li>
  <li><a href="https://cf.trackerslist.com/all.txt">cf.trackerslist.com/all.txt</a></li>
  <li><a href="https://cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all.txt">cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all.txt</a></li>
  <li><a href="https://raw.githubusercontent.com/1265578519/OpenTracker/master/tracker.txt">raw.githubusercontent.com/1265578519/OpenTracker/master/tracker.txt</a></li>
  <li><a href="https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt">raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt</a></li>
  <li><a href="https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt">raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt</a></li>
</ul>
</details>



<h2 id="c">🎯 规则订阅</h2>

| 文件              | 说明           |                                                               github                                                               |                                                                                 gitwarp                                                                                 |
| ----------------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| `tracker.txt`     | 聚合规则       |     [link][tracker-github](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt)]     |     [link][tracker-gitwarp](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt)]     |
| `bad_tracker.txt` | 无法拉取的规则 | [link][bad_tracker-github](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt)] | [link][bad_tracker-gitwarp](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt)] |



<!-- **⚠ 本仓库不再提供规则订阅，我们更推荐 fork 本项目自行构建规则集.** -->

<!-- 下面是使用了本项目进行构建的规则仓库，可在其中寻找合适的规则订阅: -->
<!-- <details> -->
<!-- <summary>点击查看</summary> -->
<!-- <ul> -->
<!--     <br/> -->
<!--     <li><a href="https://github.com/xndeye/adblock_list/">xndeye/adblock_list</a></li> -->
<!-- </ul> -->
<!-- </details> -->

<h2 id="d">💬 问题反馈</h2>

- 👉 [issues](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/issues)
