## 概要
rowmaはロボットをWeb上で管理する事ができるツールで、遠隔操作や監視などが機能に含まれています。
[github.com/asmsuechan/rowma](https://github.com/asmsuechan/rowma)

## プロジェクトリポジトリ
このシステムは現在以下の3つのソフトウェアで構成されています。本リポジトリはドキュメント用になります。

* [ConnectionManager](https://github.com/asmsuechan/rowma_connection_manager)
* [rowma_ros](https://github.com/asmsuechan/rowma_ros)
* [JavaScript SDK](https://github.com/asmsuechan/rowma_js)

## デモ
スマートフォンから/joyにメッセージをpublishして四輪ロボットを操作するデモです。

<iframe width="560" height="315" src="https://www.youtube.com/embed/cOwHWh60PCk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<details><summary>実験環境</summary><div>

以下は実験を行ったシステムのソフトウェア環境です。

|名前|内容|
|:-:|:-:|
|OS|Ubuntu 16.04|
|Python|2.7.15|
|ROS|ROS kinetic|

以下は実験を行ったシステムのハードウェア環境です。

|名前|内容|
|:-:|:-:|
|Laptop|ASUSU ZenBook UX305|
|CPU|Intel(R) Core(TM) i5-6200U CPU @ 2.30GHz|
|RAM|8GB|
|Network|400Mbps程度のWi-Fi|
|Robot|i-cart mini|

</div></details>

## 出来る事
以下の事がインターネット越しにできます。

* roslaunch/rosrunによる任意のROSノードの実行
* 任意のROSノードの停止
* 任意のトピックのPublish/Subscribe

## 使用方法
ロボット管理用のROSノードを動かす事でそのロボットにトピックをPublish/Subscribeします。

まず、ROSが動いているPC上で以下のコマンドを実行します。

```sh
$ cd ~/catkin_ws/src
$ git clone https://github.com/asmsuechan/rowma_ros.git
$ cd ~/catkin_ws
$ catkin_make
$ rosrun rowma_ros rowma
```

なお、デフォルトでは提供されているサーバーに繋ぎに行きます。

次に、サンプル管理画面の `http://ec2-18-176-1-219.ap-northeast-1.compute.amazonaws.com:3000/` にアクセスします。この画面上で上のデモ動画と同じ操作をすれば任意のノードが実行できます。

## なぜ作ったのか
今までの遠隔操作ツールは

* 研究環境に大きく依存して再利用ができない
* セットアップが容易でなく、時間がかかる

ものであり、実装者が思いつくままにシステムを構築していました。

そこで、より**簡単に誰でも使えるシステム**が必要だと感じたのでこのシステムを作りました。

## 使用技術
通信基盤を、[socket.io](https://socket.io/)を用いたWebSocket通信により構築しました。socket.ioを使うことで、自前で全て実装するよりも安定していて高機能なPub/Sub型の通信を容易に実装することが出来ました。

### ConnectionManager
* nodejs v12.8.0
* socket.io
