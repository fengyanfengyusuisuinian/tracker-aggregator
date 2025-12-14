<div align="center">
<h1>Tracker订阅聚合</h1>
<p>tracker规则订阅器，整合不同来源的规则，帮助你快速构建属于自己的规则集~</p>
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
Tracker aggregator Subscriber 是一个用于聚合和管理 BitTorrent Tracker 列表的工具。该项目受 <a href="https://github.com/fordes123/ad-filters-subscribe">fordes123的广告过滤规则订阅器</a> 启发，经过优化和重构。

#### **功能**
- 自动抓取多个 Tracker 源
- 去重与排序
- 生成可用 Tracker 列表
- 记录无法访问的源到 `TrackerServer/bad_tracker.txt`
- 支持 GitHub Actions 自动更新

#### **Github Action**
1. Fork 本项目
2. 自定义规则订阅（可选）
   - 修改 tracker 源文件：`sources.list`
   - 修改工作流配置：`.github/workflows/sync.yml`
3. 打开 `Github Action` 页面，选中左侧 `Update Filters` 授权 `Workflow` 定时执行（⚠ 重要步骤）
4. 点击 `Run workflow` 或等待自动执行。执行完成后规则将生成在 `release` 分支

#### **Codespaces**
- 登录 `Github`，点击本仓库右上角 `Code` 按钮，选择并创建新的 `Codespaces`
- 等待 `Codespaces` 启动，即可直接对本项目进行调试

<details>
<summary>点击查看上游规则</summary>
<ul>
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
<li><a href="https://down.adysec.com/trackers_best.txt">down.adysec.com/trackers_best.txt</a>（<a href="https://github.com/adysec/tracker">项目地址</a>）</li>
</ul>
</details>

<h2 id="c">🎯 规则订阅</h2>

| 文件 | 说明 | github | gitwarp |
| ---- | ---- | ---- | ---- |
| `tracker.txt` | 聚合后最终可用列表（已排序） | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt) |
| `trackers_merged.txt` | 合并+去重后完整列表（未检测） | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_merged.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_merged.txt) |
| `trackers_alive.txt` | 通过存活检测的可用列表（需开启检测） | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_alive.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_alive.txt) |
| `sources_failed.txt` | 数据源拉取失败记录 | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/sources_failed.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/sources_failed.txt) |
| `bad_tracker.txt` | 兼容旧版无法拉取记录 | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt) |

<h2 id="d">💬 问题反馈</h2>
<a href="https://github.com/fengyanfengyusuisuinian/tracker-aggregator/issues">issues</a>
