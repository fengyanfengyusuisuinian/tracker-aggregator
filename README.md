&lt;div align="center"&gt;
&lt;h1&gt;Tracker 订阅聚合&lt;/h1&gt;
  &lt;p&gt;
    tracker 规则订阅器，整合不同来源的规则，帮助你快速构建属于自己的规则集~
  &lt;/p&gt;
&lt;!-- Badges --&gt;
&lt;p&gt;
  &lt;img src="https://img.shields.io/github/last-commit/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="last update" /&gt;
  &lt;img src="https://img.shields.io/github/forks/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="forks" /&gt;
  &lt;img src="https://img.shields.io/github/stars/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="stars" /&gt;
  &lt;img src="https://img.shields.io/github/issues/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="open issues" /&gt;
  &lt;img src="https://img.shields.io/github/license/fengyanfengyusuisuinian/tracker-aggregator?style=flat-square" alt="license" /&gt;
&lt;/p&gt;

&lt;h4&gt;
    &lt;a href="#a"&gt;项目说明&lt;/a&gt;
  &lt;span&gt; · &lt;/span&gt;
    &lt;a href="#c"&gt;规则订阅&lt;/a&gt;
  &lt;span&gt; · &lt;/span&gt;
    &lt;a href="#d"&gt;问题反馈&lt;/a&gt;
  &lt;/h4&gt;
&lt;/div&gt;

[English](README_en.md) | 中文

&lt;h2 id="a"&gt;📔 项目说明&lt;/h2&gt;
Tracker aggregator Subscriber 是一个用于聚合和管理 BitTorrent Tracker 列表的工具。  
受 &lt;a href="https://github.com/fordes123/ad-filters-subscribe"&gt;fordes123/ad-filters-subscribe&lt;/a&gt; 启发，经过优化与重构。

#### **本次更新亮点**
- ✅ 自动识别**任意合法协议头**（`udp://` / `wss://` / `wdp://` …）并拆分为独立行  
- ✅ **字符串完全相等去重**（区分大小写、协议、端口）  
- ✅ 无法访问的源自动记入 `TrackerServer/bad_tracker.txt`，便于后续排查  
- ✅ 零额外依赖，GitHub Actions 每日自动更新，开箱即用

#### **GitHub Action**
- fork 本项目  
- 自定义规则订阅（可选）  
  - 修改 tracker 源文件：`sources.list`  
  - 修改工作流配置：`.github/workflows/sync.yml`  
- 打开 `GitHub Actions` 页面 → 左侧 `Update Filters` → 授权 Workflow 定时执行（⚠ 重要）  
- 点击 `Run workflow` 或等待自动执行；结果将推送至 `release` 分支

#### **Codespaces**
- 登录 GitHub → 右上角 `Code` → 创建 `Codespaces`  
- 启动完成后即可在线调试与运行

&lt;details&gt;
&lt;summary&gt;点击查看上游规则&lt;/summary&gt;
&lt;ul&gt;
  &lt;li&gt;&lt;a href="https://newtrackon.com/api/all"&gt;newtrackon.com/api/all&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://trackerslist.com/all.txt"&gt;trackerslist.com/all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://newtrackon.com/api/stable"&gt;newtrackon.com/api/stable&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://at.raxianch.moe/AT_all.txt"&gt;at.raxianch.moe/AT_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://gcore.jsdelivr.net/gh/XIU2/TrackersListCollection/all.txt"&gt;gcore.jsdelivr.net/gh/XIU2/TrackersListCollection/all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_best.txt"&gt;cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_best.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://cf.trackerslist.com/all.txt"&gt;cf.trackerslist.com/all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all.txt"&gt;cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/1265578519/OpenTracker/master/tracker.txt"&gt;raw.githubusercontent.com/1265578519/OpenTracker/master/tracker.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt"&gt;raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt"&gt;raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://down.adysec.com/trackers_best.txt"&gt;down.adysec.com/trackers_best.txt&lt;/a&gt;&lt;/li&gt;
&lt;/ul&gt;
&lt;/details&gt;

&lt;h2 id="c"&gt;🎯 规则订阅&lt;/h2&gt;

| 文件              | 说明           | GitHub 直链 | GitWarp 加速 |
| ----------------- | :------------- | :---------- | :----------- |
| `tracker.txt`     | 聚合去重结果   | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt) |
| `bad_tracker.txt` | 无法拉取的源   | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt) |

&gt; 本次去重规则：仅当字符串完全相等时视为重复；大小写、协议、端口均严格区分。

&lt;h2 id="d"&gt;💬 问题反馈&lt;/h2&gt;

👉 [开 Issue](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/issues)
