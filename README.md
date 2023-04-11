# Practice-of-Information-Systems-1st
情報学研究科の情報システム論実習の前半プロジェクトです

# 環境構築
```
git clone https://github.com/K-Hayashi884/Practice-of-Information-Systems-1st
cd ./Practice-of-Information-Systems-1st
conda create -n <好きな仮想環境名> python=3.9
conda activate <仮想環境名>
conda env create -f requirements.yaml
git checkout -b <好きなブランチ名>
```

# パッケージインストールしたら
`conda install`をした後には必ず`conda env export > requirements.yaml`を走らせてください。

# 参考文献
- [データベース操作](https://engineer-lifestyle-blog.com/code/python/flask-tutorial-web-app-with-database/)
