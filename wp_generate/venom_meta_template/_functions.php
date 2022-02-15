<?php

if (! function_exists('{{ config.theme }}_theme_setup') ) :

    function {{ config.theme }}_theme_setup() {

        {% if config.text_domain_location != None -%}
        /* turn this on if you want to use internationalization features */
        load_theme_textdomain( {{ config.theme | php }}, get_template_directory() . {{ config.text_domain_location | php }} );
        {%- endif %}

        {% if config.automatic_feed_links -%}
        /* add RSS feed automatically */
        add_theme_support( 'automatic-feed-links' );
        {%- endif %}

        {% if config.register_primary_menu != None -%}
        /* primary menu registration */
        register_nav_menus( array(
            'menu-1' => esc_html__( {{ config.register_primary_menu | php }}, {{ config.theme | php }} ),
        ) );
        {%- endif %}

        {% if config.title_tag -%}
        /* support automatic title tags */
        add_theme_support( 'title-tag' );
        {%- endif %}

        {% if config.post_thumbnails -%}
        /* support thumbnail for each entry */
        add_theme_support( 'post-thumbnails' );
        {%- endif %}

        {% if config.html5 -%}
        /* support html5 functions */
        add_theme_support( 'html5', array(
            'search-form',
            'comment-form',
            'comment-list',
            'gallery',
            'caption',
        ) );
        {%- endif %}

        {% if config.custom_background != None -%}
        /* background color customization */
        add_theme_support( 'custom-background', apply_filters( '{{ config.theme }}_custom_background_args', 
            {{ config.custom_background | php }}) );
        {%- endif %}

        {% if config.selective_refresh_widgets -%}
        /* selective widget refresh support */
        add_theme_support( 'customize-selective-refresh-widgets' );
        {%- endif %}

        {% if config.custom_logo != None -%}
        /* custom logo support : NOT IMPLEMENTED ON VIPER THEME YET!!! */
        add_theme_support( 'custom-logo', {{ config.custom_logo | php }} );
        {%- endif %}
    }
endif;

add_action( 'after_setup_theme', '{{ config.theme }}_theme_setup' );

{% if config.sidebar_options != [] -%}
function {{ config.theme }}_widgets_init() {
    /* these widget areas are added by the generator */
    {% for option in config.sidebar_options -%}
    register_sidebar( {{ option | php }} );
    {%- endfor %}
}
add_action( 'widgets_init', '{{ config.theme }}_widgets_init' );
{%- endif %}

function {{ config.theme }}_scripts() {
    /* include theme default css */
    wp_enqueue_style( '{{ config.theme }}-style', get_stylesheet_uri() );

    /* additional styles for {{ config.theme }} */ 
    {% for css in config.styles -%}
    wp_enqueue_style({{ css.name | php }}, get_template_directory_uri() .  {{ css.path | php }}, array(), {{ css.version | php }}, true);
    {%- endfor %}

    /* additional scripts for {{ config.theme }} */ 
    {% for js in config.scripts -%}
    wp_enqueue_script({{ js.name | php }}, get_template_directory_uri() . {{ js.path | php }}, array(), {{ js.version | php }}, true);
    {%- endfor %}
}

add_action( 'wp_enqueue_scripts', '{{ config.theme }}_scripts' );

?>

