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
<!doctype html>
<html lang="<?php echo get_bloginfo('language'); ?>">
	<head>
		<meta charset="<?php bloginfo( 'charset' ); ?>">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<?php wp_head(); ?>
	</head>
	<body class="<?php echo esc_attr(join(' ', get_body_class(''))); ?>">
		<div id="page" class="site-container">
			<!--  site header  -->
			<header id="masthead" class="site-header">
				<!--  site logo  -->
				<div class="site-branding">
					<?php if ( has_custom_logo() ) : ?>
					<?php the_custom_logo(); ?>
					<?php elseif( is_front_page() && is_home() ) : ?>
					<h1 class="site-title">
						<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
							<?php bloginfo( 'name' ); ?>
						</a>
					</h1>
					<?php else : ?>
					<p class="site-title">
						<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">
							<?php bloginfo( 'name' ); ?>
						</a>
					</p>
					<?php endif; ?>
					<!--  <p class="site-description">Be happy with Viper!</p>  -->
				</div>
				<!--  navigation menu  -->
				<nav id="site-navigation" class="main-navigation">
					<?php
					wp_nav_menu( array(
					    'theme_location' => 'menu-1',
					    'menu_id'        => 'primary-menu',
					) );
					?>
				</nav>
			</header>
			<!--  content  -->
			<div id="content" class="site-content">
