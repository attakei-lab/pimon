============
セットアップ
============

必要環境
========

次の環境を前提としています。

* Linux OS
* 接続対象となるIMAPサーバーへProxy等を伴わずに直接接続できること
* Python 3.10.x系

インストール
============

``pimon`` はPythonパッケージプロダクトですが、PyPI上にアップロードしていません。
そのため、次のいずれかの手段を取る必要があります。

* GitHub上のビルド済みwheelをインストール (推奨）
* GitHubリポジトリをclone後にソースをインストール

wheelインストール
-----------------

インストール先の環境を用意した上で、ターミナル上で以下のコマンドを実行してください。

.. code-block:: console

   pip install --find-links=https://github.com/attakei-lab/pimon/releases pimon

GitHubリポジトリからインストール
--------------------------------

.. code-block:: console

   git clone https://github.com/attakei-lab/pimon.git
   pip install ./pimon

準備
====

``pimon init`` でローカル環境のセットアップを、
``pimon accounts:add`` でIMAPサーバー接続用のアカウントの登録を行います。

.. code-block:: console

   pimon init
   pimon accounts:add

受信
====

``pimon fetch`` でサーバーから受信箱上のEメール情報を取得します。
また、特定のアカウントのみを対象にしたい場合は、 ``--name`` オプションを利用できます。

.. code-block:: console

   pimon fetch
