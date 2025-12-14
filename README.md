&lt;div align="center"&gt;
&lt;h1&gt;Tracker订阅聚合&lt;/h1&gt;
  &lt;p&gt;
    tracker规则订阅器，整合不同来源的规则，帮助你快速构建属于自己的规则集~
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
Tracker aggregator Subscriber 是一个用于聚合和管理 BitTorrent Tracker 列表的工具。该项目受 fordes123的广告过滤规则订阅器 https://github.com/fordes123/ad-filters-subscribe  项目启发经过优化和重构。

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
  - 修改修改配置文件: `.github/workflows/sync.yml`
- 打开 `Github Action` 页面，选中左侧 `Update Filters` 授权 `Workflow` 定时执行(⚠ 重要步骤)
- 点击 `Run workflow` 或等待自动执行。执行完成后规则将生成在 `release` 分支

#### **Codespaces**

- 登录 `Github`，点击本仓库右上角 `Code` 按钮，选择并创建新的 `Codespaces`
- 等待 `Codespaces` 启动，即可直接对本项目进行调试


&lt;details&gt;
&lt;summary&gt;点击查看上游规则&lt;/summary&gt;
&lt;ul&gt;
   &lt;!--  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt "&gt;AdGuard 基础过滤器&lt;/a&gt;&lt;/li&gt; --&gt;
  &lt;li&gt;&lt;a href="https://newtrackon.com/api/all "&gt;newtrackon.com/api/all&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://trackerslist.com/all.txt "&gt;trackerslist.com/all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://newtrackon.com/api/stable "&gt;newtrackon.com/api/stable&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://at.raxianch.moe/AT_all.txt "&gt;at.raxianch.moe/AT_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://gcore.jsdelivr.net/gh/XIU2/TrackersListCollection/all.txt "&gt;gcore.jsdelivr.net/gh/XIU2/TrackersListCollection/all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_best.txt "&gt;cdn.jsdelivr.net/gh/ngosang/trackerslist/trackers_best.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://cf.trackerslist.com/all.txt "&gt;cf.trackerslist.com/all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all.txt "&gt;cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/1265578519/OpenTracker/master/tracker.txt "&gt;raw.githubusercontent.com/1265578519/OpenTracker/master/tracker.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt "&gt;raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt "&gt;raw.githubusercontent.com/DeSireFire/animeTrackerList/master/AT_all.txt&lt;/a&gt;&lt;/li&gt;
  &lt;li&gt;&lt;a href="https://down.adysec.com/trackers_best.txt "&gt;https://github.com/adysec/tracker?tab=readme-ov-file &lt;/a&gt;&lt;/li&gt;
&lt;/ul&gt;
&lt;/details&gt;



&lt;h2 id="c"&gt;🎯 规则订阅&lt;/h2&gt;

| 文件 | 说明 | github | gitwarp |
|----|----|----|----|
| `tracker.txt` | 聚合后最终可用列表（已排序） | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/tracker.txt) |
| `trackers_merged.txt` | 合并+去重后完整列表（未检测） | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_merged.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_merged.txt) |
| `trackers_alive.txt` | 通过存活检测的可用列表（需开启检测） | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_alive.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/trackers_alive.txt) |
| `sources_failed.txt` | 数据源拉取失败记录 | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/sources_failed.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/sources_failed.txt) |
| `bad_tracker.txt` | 兼容旧版无法拉取记录 | [link](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt) | [link](http://hk-yd-proxy.gitwarp.com:6699/https://github.com/fengyanfengyusuisuinian/tracker-aggregator/blob/main/TrackerServer/bad_tracker.txt) |



&lt;h2 id="d"&gt;💬 问题反馈&lt;/h2&gt;

- 👉 [issues](https://github.com/fengyanfengyusuisuinian/tracker-aggregator/issues )
