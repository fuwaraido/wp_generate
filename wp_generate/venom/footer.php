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
</div>
<!--  #content  -->
<!--  site footer  -->
<footer id="colophon" class="site-footer">
	<p class="site-info">
		<span class="copy">
			&copy;
		</span>
		<?php echo date('Y'); ?>
		<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
			<?php bloginfo( 'name' ); ?>
		</a>
		,
		&nbsp;
		All rights reserved. 
	</p>
</footer>
<?php wp_footer(); ?>
</div>
