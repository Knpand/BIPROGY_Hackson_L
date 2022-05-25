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

### ## 仮想環境の構築

#### 環境の作成
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

#### パッケージのインストール
```
$ pip install -r requirements.txt
```

※新たなパッケージを追加するときは`requirement.txt`に追記する．
