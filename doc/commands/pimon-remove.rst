``pimon remove`` コマンド
=========================

概要
----

pimon内で管理されているメッセージに対して削除処理を行います。
この削除処理は「ローカル環境」と「サーバー環境の【受信箱】」からの削除のみを行い、メールの削除は基本的に行いません。

引数
----

``ACCOUNT`` と ``UID`` については、あらかじめ :doc:`./pimon-list` で確認してください。

ACCOUNT
  取得対象のアカウント。

UID
  削除対象のUID。

-ws, --workspace
  (任意)対象となるワークスペース。

  もし指定がない場合は、次のように決定されます。また、 :doc:`./pimon-init` で初期化済みである必要があります。

  - Linuxの場合は、 ``$HOME/.config/pimon``


利用例
------

.. code-block:: console

   pimon remove example 11111
