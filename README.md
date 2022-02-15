# WP Generate

個人用のWordpressサイトのテーマを生成するために作成した、業務効率向上のためのPythonスクリプトです。

HTMLで作成されたテンプレートのページにHTMLのコメント形式でアノテーションを入れて、スクリプトを実行すると、Wordpressテーマが生成されます。
仕組みは結構強引で、HTMLをパースして、実行時にjinjaテンプレートを生成、それをレンダリングしてphpファイルを生成するという二段階方式になっています。
もともと、複数のWordpressサイトをサクサク作りたくて「自分用」に作ったものなので、公開することを考慮していませんが、一応動作はします。
数年前に作ったものなので、現行のWordpressの仕様に照らし合わせて、妥当なテンプレートが生成されるかは不明です
（私は既にサイトを閉鎖しているので、Wordpressは数年前から追いかけていません）。

# フォルダと構成

wp_generateフォルダには、スクリプト本体のほか、スクリプトが生成した「Venom」ワードプレステーマのサンプルファイルが格納されています。

## プログラム本体
meta_templates - PHPコードのマクロテンプレート
pretty.py - HTMLの書式を整えるクラスのモジュール。PHPが混じっていてもそれなりに奇麗な書式になる（はず）なのがミソです。
maketheme.py - Wordpressテンプレート生成用スクリプト本体。

## Venomサンプル用定義ファイル
venom.ini - 「Venom」テーマのサンプル設定ファイル。
venom_template - サンプルテーマ「Venom」用アノテーション付きHTML一式。

## 自動生成済みVenomテーマ
venom_meta_template - 自動生成される「Venom」サンプルテーマ生成用中間ファイル。
venom - 自動生成された「Venom」テーマが格納されているフォルダ。

# 使用法

大抵の人の役には立たないと思いますが、一応、使用方法を記述します。

## HTMLでサイトのテンプレートを作る

まず、HTMLでhomeやarchive、index、single、search...等々おなじみのWordpressテンプレートのphpに対応するページをHTMLでおもむろに生成します。
それすら面倒くさいという方は、html_genereateというHTMLページのたたき台を作るスクリプトが私のリポジトリにありますので、興味があればご使用ください。
ページが出来たら、HTMLのコメント形式でアノテーションを入れるのですが、使用を細かく説明するのが面倒なので、簡単に例を示します。

### HTMLヘッダの例

<!-- %PAGE:
    page_type           = 'archive',
    has_comment         = False,
    has_navigation      = True,
    template            = '_main.jinja',
    content_template    = 'template-parts/content',
    content_type        = 'archive'
-->

これはarchive.phpを生成するための雛形archive.htmlに書くべきヘッダの例です。
必ずこの書式で、HTMLファイルの先頭に書いてください。

### タグの置き換え

<!-- %inline: post_thumbnail() -->
　<img style="max-width: 100%" src="img/thumbnail.jpeg">
<!-- %end_inline -->




maketheme.pyをシェルなどから直接実行します。
ただし、作りかけのため、テンプレート生成用の設定ファイル名がスクリプトにハードコードされたままです。

メイン処理（if __name__ == '__main__'以降）


