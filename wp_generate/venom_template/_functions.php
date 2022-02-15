<?php

{% block theme_setup %}

if (! function_exists('viper_theme_setup') ) :

    function viper_theme_setup() {

        {% block text_domain_support %}
        /* turn this on if you want to use internationalization features */
        load_theme_textdomain( 'viper', get_template_directory() . '/languages' );
        {% endblock %}

        {% block automatic_feed_link_support %}
        /* add RSS feed automatically */
        add_theme_support( 'automatic-feed-links' );
        {% endblock %}

        {% block register_primary_menu %}
        /* primary menu registration */
        register_nav_menus( array(
            'menu-1' => esc_html__( 'Primary', 'viper' ),
        ) );
        {% endblock %}

        {% block title_tag_support %}
        /* support automatic title tags */
        add_theme_support( 'title-tag' );
        {% endblock %}

        {% block post_thumbnail_support %}
        /* support thumbnail for each entry */
        add_theme_support( 'post-thumbnails' );
        {% endblock %}

        {% block html5_support %}
        /* support html5 functions */
        add_theme_support( 'html5', array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
        ) );
        {% endblock %}

        {% block custom_background %}
        /* background color customization */
        add_theme_support( 'custom-background', apply_filters( 'viper_custom_background_args', array(
            'default-color' => 'ffffff',
            'default-image' => '',
        ) ) );
        {% endblock %}

        {% block selective_refresh_widget_support %}
        /* selective widget refresh support */
        add_theme_support( 'customize-selective-refresh-widgets' );
        {% endblock %}

        {% block custom_logo_support %}
        /* custom logo support : NOT IMPLEMENTED ON VIPER THEME YET!!! */
        add_theme_support( 'custom-logo', array(
            'height'      => 250,
            'width'       => 250,
            'flex-width'  => true,
            'flex-height' => true,
        ) );
        {% endblock %}
    }
endif;

add_action( 'after_setup_theme', 'viper_theme_setup' );

{% endblock %}


{% block register_wiget_areas %}

/* TODO: allow multiple widget area from generator! */
function viper_widgets_init() {
	register_sidebar( array(
		'name'          => esc_html__( 'Sidebar', 'viper' ),
		'id'            => 'sidebar-1',
		'description'   => esc_html__( 'Add widgets here.', 'viper' ),
		'before_widget' => '<section id="%1$s" class="widget %2$s">',
		'after_widget'  => '</section>',
		'before_title'  => '<h2 class="widget-title">',
		'after_title'   => '</h2>',
	) );
}
add_action( 'widgets_init', 'viper_widgets_init' );

{% endblock %}

{% block register_scripts %}

function viper_scripts() {
    wp_enqueue_style( 'viper-style', get_stylesheet_uri() );

    {% if 'styles' in page %}
        {% for css in page.styles %}
        wp_enqueue_style({{ css.name | quote }}, get_template_directory_uri() .  {{ css.path | quote }}, array(), css.version, true);
        {% endfor %}
    {% endif %}

    {% if 'scripts' in page %}
        {% for js in page.scripts %}
        wp_enqueue_script({{ js.name | quote }}, get_template_directory_uri() . {{ js.path | quote }}, array(), js.version, true);
        {% endfor %}
    {% endif %}

}
add_action( 'wp_enqueue_scripts', 'viper_scripts' );

{% endblock %}

?>

