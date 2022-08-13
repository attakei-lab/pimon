``pimon upgrade`` コマンド
==========================

概要
----

ワークスペースの環境を、コマンド実行したpimonのバージョンに追従します。

引数
----

-ws, --workspace
  (任意)対象となるワークスペース。

  もし指定がない場合は、次のように決定されます。また、 :doc:`./init` で初期化済みである必要があります。

  - Linuxの場合は、 ``$HOME/.config/pimon``

利用例
------

OSデフォルトのワークスペースで運用している場合。

.. code-block:: console

   pimon upgrade

特定フォルダをワークスペースとして運用している場合。

.. code-block:: console

   pimon upgrade --workspace=/PATH/TO/WORKSPACE
