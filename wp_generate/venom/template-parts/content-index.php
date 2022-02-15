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
<article id="post-<?php the_ID(); ?>" class="<?php post_class(); ?>">
	<header class="entry-header">
		<!--  entry title  -->
		<?php if( is_singular() ) : ?>
		<h1 class="entry-title">
			<?php the_title() ?>
		</h1>
		<?php else : ?>
		<h2 class="entry-title">
			<a href="<?php the_permalink() ?>" rel="bookmark">
				<?php the_title() ?>
			</a>
		</h2>
		<?php endif; ?>
	</header>
	<!--  thumbnail  -->
	<a href="<?php the_permalink() ?>" class="post-thumbnail" aria-hidden="true" tabindex="-1">
		<?php the_post_thumbnail(); ?>
	</a>
	<!--  article content  -->
	<div class="entry-content">
		<?php the_excerpt() ?>
	</div>
	<!--  article footer  -->
	<footer class="entry-footer">
		<!--  article meta  -->
		<div class="entry-meta">
			<!--  published/modified date  -->
			<span class="posted-on">
				<a href="<?php the_permalink() ?>" rel="bookmark">
					<?php if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) : ?>
					<time class="entry-date published" datetime="<?php the_date( DATE_W3C ) ?>">
						<?php the_date() ?>
					</time>
					<time class="updated" datetime="<?php the_modified_date( DATE_W3C ) ?>">
						<?php the_modified_date() ?>
					</time>
					<?php else : ?>
					<time class="entry-date published updated" datetime="<?php the_date( DATE_W3C ) ?>">
						<?php the_date() ?>
					</time>
					<?php endif; ?>
				</a>
			</span>
			<!--  byline  -->
			<span class="byline">
				<span class="author vcard">
					<a class="url fn n" href="<?php esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ); ?>">
						<?php echo esc_html(get_the_author()); ?>
					</a>
				</span>
			</span>
			<?php $categories_list = get_the_category_list( esc_html__( ', ', 'underscore' ) );
			if ( $categories_list ) : ?>
			<span class="cat-links">
				<?php echo $categories_list ?>
			</span>
			<?php endif; ?>
			<?php $tags_list = get_the_tag_list('', esc_html_x( ', ', 'list item separator', 'underscore' ) );
			if ( $tags_list ) : ?>
			<span class="tag-links">
				<?php echo $tags_list ?>
			</span>
			<?php endif; ?>
		</div>
	</footer>
</article>
