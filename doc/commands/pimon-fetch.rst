``pimon fetch`` コマンド
========================

概要
----

pimonで管理されているアカウントごとにIMAPサーバーへ接続し、受信箱のメール情報を一括取得します。

引数
----

-ws, --workspace
  (任意)対象となるワークスペース。

  もし指定がない場合は、次のように決定されます。また、 :doc:`./pimon-init` で初期化済みである必要があります。

  - Linuxの場合は、 ``$HOME/.config/pimon``

--name
  (任意)取得対象のアカウント。

  この引数を指定した場合は、指定したアカウントからのみメール情報を取得します。

利用例
------

単純に全アカウントから取得する場合。

.. code-block:: console

   pimon fetch

特定アカウント *example* だけ取得したい場合。

.. code-block:: console

   pimon fetch --name=example

ワークスペースがデフォルトの場所ではない場合。

.. code-block:: console

   pimon fetch --workspace=/PATH/TO/WORKSPACE
