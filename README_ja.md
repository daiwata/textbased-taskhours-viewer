# テキストベースのタスク時間ビューア

このツールはテキスト形式で入力された予定と実際の日々の作業時間を表示するシンプルなウェブベースのツールで、それらを表形式にまとめます。

![](capt.png)

## 特徴

- カテゴリー、ファイルベース、日次、月次によるタスク時間の集計します。
- 集計データをHTML形式で出力・表示します。
- テキストが変更されると、集計データをリアルタイムに更新し表示します。

## 必要なもの

- [Git](https://git-scm.com/)
- [Python 3.11](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## インストール

プロジェクトをクローンします：

```bash
git clone https://github.com/daiwata/textbased-tasktime-view.git
```

プロジェクトのディレクトリに移動します：

```bash
cd textbased-taskhours-viewer
```

仮想環境を作成し、それを有効化します：

```bash
python -m venv venv
source venv/bin/activate
```

必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

## アプリケーションの実行

srcディレクトリに移動してmain.pyファイルを実行します：

```bash
cd src
python main.py
```

## Windows用にEXEファイルを作成

追加のパッケージをインストールします：

```bash
pip install pyinstaller
pip install git+https://github.com/bottlepy/bottle.git
```

appディレクトリに移動してアプリケーションをコンパイルします：

```bash
cd app
pyinstaller -wF --add-data="web/*;web/" main.py --clean --distpath . -n TaskhoursView.exe
```

## EXEの実行（Windows）

"Code -> Download ZIP"からこのプロジェクトをダウンロードし、解凍します。

エクスプローラでアプリディレクトリに移動し、"TaskhourView.exe" ファイルをダブルクリックします。

## コントリビューション

プルリクエストは大歓迎です。大きな変更の場合は、まず問題を開いて変更したい内容について議論してください。

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細については、LICENSE.txtファイルをご覧ください。
