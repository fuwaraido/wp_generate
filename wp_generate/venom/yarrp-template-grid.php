<?php
/**
 *
 * venom theme
 *
 * @link: https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package: venom
*/
?>
<h2 class="primary-headings">
	Related Posts
</h2>
<div class="row clearfix">
	<!--  article example  -->
	<article id="post-<?php the_ID(); ?>" class="<?php post_class(); ?>">
		<!--  thumbnail  -->
		<div class="post-thumbnail">
			<img style="max-width: 100%" src="img/thumbnail.jpeg">
			</div>
			<!--  article content  -->
			<div class="entry-content">
				<h2>
					<a href="<?php the_permalink() ?>" rel="bookmark">
						<?php the_title() ?>
					</a>
				</h2>
				<p>
					Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
				</p>
			</div>
			<!--  article footer  -->
			<footer class="entry-footer">
				<span class="cat-links">
					<a href="#" rel="category tag">
						Categoty
					</a>
				</span>
				<span class="tags-links">
					<a href="#" rel="tag">
						Tag1
					</a>
					, 
					<a href="#" rel="tag">
						Tag2
					</a>
				</span>
			</footer>
		</article>
		<!--  article example  -->
		<article id="post-<?php the_ID(); ?>" class="<?php post_class(); ?>">
			<!--  thumbnail  -->
			<div class="post-thumbnail">
				<img style="max-width: 100%" src="img/island.jpg">
				</div>
				<!--  article content  -->
				<div class="entry-content">
					<h2>
						Headings H2
					</h2>
					<p>
						Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
					</p>
				</div>
				<!--  article footer  -->
				<footer class="entry-footer">
					<span class="cat-links">
						<a href="#" rel="category tag">
							Categoty
						</a>
					</span>
					<span class="tags-links">
						<a href="#" rel="tag">
							Tag1
						</a>
						, 
						<a href="#" rel="tag">
							Tag2
						</a>
					</span>
				</footer>
			</article>
			<!--  article example  -->
			<article id="post-<?php the_ID(); ?>" class="<?php post_class(); ?>">
				<!--  thumbnail  -->
				<div class="post-thumbnail">
					<img style="max-width: 100%" src="img/japan.jpg">
					</div>
					<!--  article content  -->
					<div class="entry-content">
						<h2>
							Headings H2
						</h2>
						<p>
							Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
						</p>
					</div>
					<!--  article footer  -->
					<footer class="entry-footer">
						<span class="cat-links">
							<a href="#" rel="category tag">
								Categoty
							</a>
						</span>
						<span class="tags-links">
							<a href="#" rel="tag">
								Tag1
							</a>
							, 
							<a href="#" rel="tag">
								Tag2
							</a>
						</span>
					</footer>
				</article>
			</div>
