# Biprogy Hackson Group L

# Getting Started

## # 環境構築

### ## 導入

以下を順に実行する．
保険のため、mainブランチへのpushはできないようにする．
```
$ git clone https://github.com/Knpand/BIPROGY_Hackson_L.git
$ cd BIPROGY_Hackson_L
$ git config --local core.hooksPath .github/hooks
$ chmod -R +x .github/hooks
```

### ## 環境構築

#### 仮想環境の作成
```
$ python3 -m venv venv
```

#### Activate(仮想環境に入る)

##### Mac
```
$ source venv/bin/activate
```

##### Windows
```
$ .\[newenvname]\Scripts\activate
```

#### Deactivate(仮想環境から抜ける)
```
$ deactivate
```

#### 環境変数の設定(.zshrcなどに書くと、ターミナルを閉じても環境変数が残る)
##### Mac(zshの場合)
```
$ echo 'export FLASK_APP=api' >> ~/.zshrc
$ echo 'export FLASK_ENV=development' >> ~/.zshrc
$ source ~/.zshrc
```

##### Windows
```
$
```
#### パッケージのインストール
```
$ pip install -r requirements.txt
```

※新たなパッケージを追加するときは`requirement.txt`に追記する．

### ## 開発サーバーを起動
```
$ flask run
```
