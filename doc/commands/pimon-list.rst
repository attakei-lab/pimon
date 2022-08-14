``pimon list`` コマンド
=======================

概要
----

取得済みのメッセージ一覧を表示します。

引数
----

-ws, --workspace
  (任意)対象となるワークスペース。

  もし指定がない場合は、次のように決定されます。また、 :doc:`./pimon-init` で初期化済みである必要があります。

  - Linuxの場合は、 ``$HOME/.config/pimon``

利用例
------

OSデフォルトのワークスペースで運用している場合。

.. code-block:: console

   pimon list

特定フォルダをワークスペースとして運用している場合。

.. code-block:: console

   pimon list --workspace=/PATH/TO/WORKSPACE
