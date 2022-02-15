<?php
/**
 *
 * venom theme
 *
 * @link: https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package: venom
*/
get_header();
?>
<div id="primary" class="content-area">
	<main id="main" class="site-main">
		<?php if ( have_posts( ) ) : ?>
		<?php while( have_posts( ) ) : the_post( ) ?>
		<?php get_template_part( 'template-parts/content', get_post_type()); ?>
		<?php if ( comments_open() || get_comments_number() ) : ?>
		<?php comments_template(); ?>
		<?php endif; ?>
		<?php the_post_navigation() ?>
		<?php endwhile; ?>
		<?php else: ?>
		<?php get_template_part( 'template-parts/content', 'none' ); ?>
		<?php endif; ?>
	</main>
</div>
<!--  #primary  -->

<?php
get_sidebar();
get_footer();
?>