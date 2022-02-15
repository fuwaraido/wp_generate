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
<?php

if (! function_exists('venom_theme_setup') ) :

    function venom_theme_setup() {

        /* turn this on if you want to use internationalization features */
        load_theme_textdomain( 'venom', get_template_directory() . './language' );

        /* add RSS feed automatically */
        add_theme_support( 'automatic-feed-links' );

        /* primary menu registration */
        register_nav_menus( array(
            'menu-1' => esc_html__( 'Primary', 'venom' ),
        ) );

        /* support automatic title tags */
        add_theme_support( 'title-tag' );

        /* support thumbnail for each entry */
        add_theme_support( 'post-thumbnails' );

        /* support html5 functions */
        add_theme_support( 'html5', array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
        ) );

        /* background color customization */
        add_theme_support( 'custom-background', apply_filters( 'venom_custom_background_args', 
            array('default-color' => 'ffffff', 'default-image' => '''')) );

        /* selective widget refresh support */
        add_theme_support( 'customize-selective-refresh-widgets' );

        /* custom logo support : NOT IMPLEMENTED ON VIPER THEME YET!!! */
        add_theme_support( 'custom-logo', array('height' => 250, 'width' => 250, 'flex-width' => True, 'flex-height' => True, 'fiex-height' => True) );
    }
endif;

add_action( 'after_setup_theme', 'venom_theme_setup' );

function venom_widgets_init() {
    /* these widget areas are added by the generator */
    register_sidebar( array('id' => 'sidebar-1', 'name' => 'Sidebar', 'description' => 'Add widgets here', 'before_widget' => '<section id="%1$s" class="widget %2$s">', 'after_widget' => '</section>', 'before_title' => '<h2 class="widget-title">', 'after_title' => '</h2>') );
}
add_action( 'widgets_init', 'venom_widgets_init' );

function venom_scripts() {
    /* include theme default css */
    wp_enqueue_style( 'venom-style', get_stylesheet_uri() );

    /* additional styles for venom */ 
    wp_enqueue_style('additional-style', get_template_directory_uri() .  'css/style.css', array(), '1.0', true);wp_enqueue_style('additional-style', get_template_directory_uri() .  'css/style.css', array(), '1.0', true);wp_enqueue_style('additional-style2', get_template_directory_uri() .  'css/style2.css', array(), '1.0', true);wp_enqueue_style('additioanl-script', get_template_directory_uri() .  'js/script.js', array(), '1.0', true);

    /* additional scripts for venom */ 
    wp_enqueue_script('additional-script', get_template_directory_uri() . 'js/script.js', array(), '1.0', true);
}

add_action( 'wp_enqueue_scripts', 'venom_scripts' );

?>
