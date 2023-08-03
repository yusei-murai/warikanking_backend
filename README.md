# warikanking_backend
## 概要
割り勘精算の自動計算アプリ。複数人でイベントを作成し、それぞれの建て替えを管理することができる。建て替えもイベント参加者なら誰でも行うことができる。
## 使用技術
### 言語
Dart(Flutter), Python(Django REST Framework)
### データストア
MySQL, Redis(キャッシュ)
### 環境
Docker
## 設計
クリーンアーキテクチャを元に設計。DTOは使用しておらず、views.pyで入力はentityのオブジェクトに変換され、usecaseに渡される構成。
### apiv1
views.pyにハンドラメソッドが書かれている。views.pyは、presenterとcontrollerの役割を果たし、入出力の整形、型式の(jsonになっているかなど)バリデーションを行う。
urls.pyにurlが書かれている。
### core
#### entities
entityが書かれている。ビジネスロジックとデータの格納をしている。値オブジェクトで型は定義されている。
#### factories
abstract factoryパターンに基づいて、repositoryのインスタンス化を行う。
#### services
複数のDBを操作するときなどにつかう。entityにのみ依存する
#### use_cases
ユースケースが書かれている。原則一つのハンドラメソッドにつき一つのPythonファイルが格納される。「（アクター）が〇〇する」と言い換えられるもの。entity、serviceに依存する
#### i_repositories
DBのCRUDを行うrepositoryを抽象化したものを書く。
### data_model
DjangoのORMを使うためのデータモデルが格納される。
### repositories
DBのCRUDを行う。i_repositoryの実装。
### serializers
データ変換をする。
