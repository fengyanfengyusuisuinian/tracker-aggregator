<div align="center">
<h1>Tracker aggregator  Subscriber</h1>
  <p>
   A tracker rule subscriber that integrates rules from different sources to help you quickly build your own rule set~
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
    <a href="#a">Project Description</a>
  <span> · </span>
    <a href="#c">Rule Subscription</a>
  <span> · </span>
    <a href="#d">Feedback</a>
  </h4>
</div>

English | [中文](README.md)

<h2 id="a">📔 Project Description</h2>
Tracker Aggregator Subscriber is a tool for aggregating and managing BitTorrent Tracker lists. This project is inspired by fordes123's ad filtering rule subscriber project (https://github.com/fordes123/ad-filters-subscribe) with optimizations and refactoring.


#### **Features**

- Automatically fetch multiple Tracker sources
- Deduplication and sorting
- Generate available Tracker lists
- Record inaccessible sources in `TrackerServer/bad_tracker.txt`
- Support automatic updates via GitHub Actions

#### **Github Action**

- Fork this project
- Customize rule subscriptions (optional)
  - Modify the tracker source file: `sources.list`
  - Modify the configuration file: `.github/workflows/sync.yml`
- Open the `Github Action` page, select `Update Filters` on the left, and authorize the `Workflow` to execute regularly (⚠ Important step)
- Click `Run workflow` or wait for automatic execution. After completion, the rules will be generated in the `release` branch

#### **Codespaces**

 Log in to `Github`, click the `Code` button in the upper right corner of this repository, select and create a new `Codespaces`
- Wait for `Codespaces` to start, then you can directly debug this project


<details>
<summary>Click to view upstream rules</summary>
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
| `tracker.txt`     |  Aggregated rules        |     [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt)                       |     [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt)                       |
| `bad_tracker.txt` | Unreachable rules| [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt)                       | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt)                       |



<!-- **⚠ 本仓库不再提供规则订阅，我们更推荐 fork 本项目自行构建规则集.** -->

<!-- 下面是使用了本项目进行构建的规则仓库，可在其中寻找合适的规则订阅: -->
<!-- <details> -->
<!-- <summary>点击查看</summary> -->
<!-- <ul> -->
<!--     <br/> -->
<!--     <li><a href="https://github.com/xndeye/adblock_list/">xndeye/adblock_list</a></li> -->
<!-- </ul> -->
<!-- </details> -->

<h2 id="d">💬 Feedbac</h2>

- 👉 [issues](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/issues)
