# WP Generate

個人用のWordpressサイトのテーマを生成するために作成した、業務効率向上のためのPythonスクリプトです。

HTMLで作成されたテンプレートのページにHTMLのコメント形式でアノテーションを入れて、スクリプトを実行すると、Wordpressテーマが生成されます。
仕組みは結構強引で、HTMLをパースして、実行時にjinjaテンプレートを生成、それをレンダリングしてphpファイルを生成するという二段階方式になっています。
もともと、複数のWordpressサイトをサクサク作りたくて「自分用」に作ったものなので、公開することを考慮していませんが、一応動作はします。
数年前に作ったものなので、現行のWordpressの仕様に照らし合わせて、妥当なテンプレートが生成されるかは不明です
（私は既にサイトを閉鎖しているので、Wordpressは数年前から追いかけていません）。

# 注意事項

例によって、このプログラムを利用したことによって発生したいかなる損害も補償しません。また、メンテするつもりもないです。

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

## 設定ファイルを書く

サンプルのプロジェクトvenomの設定ファイルvenom.iniがあるのでそちらをコピーして修正するのが良いです。
たぶん、設定項目はなんとなくわかると思うのですが、一応、項目についての簡単な説明をします。
なお、設定ファイルは、よりにもよってini形式です…いいんです、これで。自分で使うツールだから。

### Templateセクション

template_dirは、貴方がおつくりになったHTMLテンプレートを格納するディレクトリの名称です。HTMLテンプレートについては、後のセクションでざっくり説明しています。

template_importsには、HTMLテンプレートないで使用するjinjaマクロを記述している、jinjaファイルの名称を記述します。

### Themeセクション
theme_nameにはテーマの名前を記述します。

theme_dirには自動生成されたphpテーマを出力するディレクトリを指定します。

そのほかは、function.phpの先頭のコメントに出力される文字列などです。

### Functions

これらの設定項目に興味がある場合、meta_template/\_functions.phpをご覧ください。おもに、functions.phpに何を記述するかの設定です。

### Sidebar
サイドバーの設定です。お察しください（たぶん、Wordpressのテーマをいじったことのある人なら見当がつくはず）。

### CSS/Script
HTMLテンプレートに含まれるjsとかcssのパスをここに記述します。cssが複数ある時は[CSS_2]のように複数指定することができます。
この設定項目は、たしか、ヘッダのところに<script>、<link>タグとして挿入される内容だったような気がする。

## HTMLでサイトのテンプレートを作る

まず、HTMLでhomeやarchive、index、single、search...等々おなじみのWordpressテンプレートのphpに対応するページをHTMLでおもむろに生成します。
それすら面倒くさいという方は、html_genereateというHTMLページのたたき台を作るスクリプトが私のリポジトリにありますので、興味があればご使用ください。
ページが出来たら、HTMLのコメント形式でアノテーションを入れるのですが、使用を細かく説明するのが面倒なので、簡単に例を示します。

### HTMLヘッダの例

```html
<!-- %PAGE:
    page_type           = 'archive',
    has_comment         = False,
    has_navigation      = True,
    template            = '_main.jinja',
    content_template    = 'template-parts/content',
    content_type        = 'archive'
-->
```

これはarchive.phpを生成するための雛形archive.htmlに書くべきヘッダの例です。
必ずこの書式で、HTMLファイルの先頭に書いてください。

### タグの置き換え

```html
<!-- %inline: post_thumbnail() -->
　<img style="max-width: 100%" src="img/thumbnail.jpeg">
<!-- %end_inline -->
```

デザインの段階だと、見た目を調整したりいろいろしたいのでダミーの画像などを入れると思います。
そういった部分をphpのコードに置き換えるため、上記のような書式を用いることができます。
上の例だと、%inline～%end_inlineで囲まれた部分が、サムネイルを挿入するphpコードに置き換えられます。
置き換え元のphpコードは、meta_template/\_common.jinjaにjinjaマクロとして定義されています。
いいかえると、post_thumbnail()によって置き換えられるphpコードが気にいらない場合は、
\_common.jinjaのマクロを修正すればよいということです
（ただ、そういう使用法は想定していません、そこまで手間をかけると、自動生成のメリットがないので…）。

なお、これはサムネイルの例ですが、当然サムネイル以外にも、一時的に入れたlorem ipsumを要約に置き換えるなどなど、種々のマクロが定義されています。

```html
<!-- %inline: php.the_except() -->
  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
<!-- %end_inline -->
```

こんな感じです。この場合、<p>タグのローレムイプサムが、記事の要約を挿入するphp呼び出しに置き換えられます。

マクロの定義については、meta_template/\_common.jinjaでまとめて定義しています。
本来一つ一つのマクロについて説明を書くべきなのかもしれませんが、結局、単なる置き換えなので当該ファイルを見た方が早いと思われます。
    
### ファイルの切り出し
    
通常、Wordpressのテンプレートを作る際は、index.htmlなどのファイルを一個作り、切り出してphpファイルにコピペなどの不毛な作業が生じます。
そもそも、このツールはそのコピペ作業が面倒で作ったものなのでした。ということで、下記のような記法を用いることでphpファイルの切り出し範囲を指定できます。
    
```html
<!-- %begin: "index.jinja" -->
                <!-- primary -->
                <div id="primary" class="content-area">					
                    <main id="main" class="site-main">
                        <!-- %block: "main_area" --><!-- %end_block -->
<!-- %begin: "template-parts/content-index.jinja" -->
                        <article id="post-666" class="post post-featured">
                            <header class="entry-header">
                                <!-- %inline: php.entry_title() -->
                                <h1 class="entry-title">Article Title</h1>
                                <!-- %end_inline -->
                            </header>
　　　　　　　　　　　　　...（中略）...
                           
                                    <!-- %inline: php.cat_links() -->
                                    <span class="cat-links"><a href="#" rel="category tag">Categoty</a></span>
                                    <!-- %end_inline -->

                                    <!-- %inline: php.tag_links() -->
                                    <span class="tags-links"><a href="#" rel="tag">Tag1</a>, <a href="#" rel="tag">Tag2</a></span>
                                    <!-- %end_inline -->
                                </div>                                
                            </footer>
                        </article>
<!-- %end:"content-index.jinja" -->
                    </main>
                </div> <!-- #primary -->
<!-- %end: "index.jinja" -->
```
    
コメントとして、%begin、%endなどのディレクティブを指定することで、その範囲をphpファイルとして切り出すことができます。
上記の例ですと、id="primary"のdivタグが、index.phpとして切り出されることになるわけです。
こうすると、HTMLカンプをいちいち切り貼りすることなく、HTMLでデザイン、アノテーション付け、テンプレート生成という一連の作業をスムーズに行うことができるのです！
また、テーマを生成した後で、レイアウトやデザインを修正する場合も、HTMLを直して、phpに反映などの作業は必要なくなります。
大元のHTMLを直して、テーマ全体を再生成してしまえばそれでOKですので、修正箇所が減るわけです。

ちなみに、上記の例ではindex.phpの中に、template-parts/content-index.jinjaが入れ子で入っています。
これは、#primaryの<div>内にある<article>タグの内容がさらに切り出されてtemplate-parts/content-index.phpとして生成されることを意味します。
このように%begin~%endディレクティブは入れ子にすることが可能です。
    
header.php、footer.php、sidebar.phpも同様に生成できますが、こちらに関してはindex.phpに相当するindex.htmlで一度だけアノテーションをつければOKです。

### 実例を見てみる

実際にアノテーションの入ったHTMLテンプレートサンプルがvenom_templateフォルダに入っていますので、そちらの形式に倣って作ればOKです。
なお、このプログラムはコメント部分を識別するため、HTMLをパースしています。
よって、HTMLが不正なフォーマットだと動作しません（例外を吐いて止まります）。
使用するHTMLテンプレートは、オンラインのチェッカーなどを利用し、事前に正しいHTML5形式になっていることを確認してください。

## テンプレートを生成する

maketheme.pyをシェルなどから直接実行します。
ただし、作りかけのため、テンプレート生成用の設定ファイル名がスクリプトにハードコードされたままです。

メイン処理（if __name__ == '__main__'以降）にサンプルのテンプレート名venomが文字列として入っていますので、
その部分をご自分のテンプレート設定ファイル名に置き換えてご使用ください（foo.iniなら、venomをfooに置き換える）。

## ライセンス
    
決めていません。そもそも、テンプレートを生成するツールなので、これ自体を配布する必要性ってない気がします。
よってライセンスどころか、誰かがこれを配布するという事態も想定していません。
もちろん、使うのは自由ですので、改造するなりなんなりして、ご自由にお使いください。
    

