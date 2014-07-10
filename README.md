# Variational Bayesian Kalman Filter
---------------------------------------

[Särkkä, S., & Nummenmaa, A. (2009). Recursive noise adaptive Kalman filtering by variational Bayesian approximations.IEEE Transactions on Automatic Control, 54(3).](http://www.lce.hut.fi/~ssarkka/pub/vb-akf-ieee.pdf)

Pythonで実装したもの。通常のカルマンフィルタでは不可能な、時間変化する観測信号のノイズの分散を推定出来ます

だた個人的な感覚では、分散の推定精度はそんなに良くはなく（真の分散値に至るまでけっこうな数のイテレーションを要する、ばらつきも大きい）、しかもヘタすると発散する…

普通のカルマンフィルタも一緒に入ってる

## メモ

* 論文の通りにやったら上手く行かなかったので一部更新式に修正が入ってる
* なぜ上手く行かないのかったのかはわかってない
* 論文著者のページでmatlabコードは公開されている（2013年くらいに確認したときは少なくとも）

ミスがあったら教えて下さい…
