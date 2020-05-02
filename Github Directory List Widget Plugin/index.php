<?php
/*
Plugin Name: Github Directory List Widget Plugin
Plugin URI: http://wwphp.com/github-directory-list-wordpress-widget-plugin
Description: Github Directory List Widget Plugin.
Version: 1.0
Author: Kerem Bilgehan Gül
Author URI: http://wwphp.com
License: MIT
*/

class wwPHP_Github_Directory_List_Widget_Widget_Plugin extends WP_Widget {

    public function __construct() {

		$options = array(
			'classname' => 'wwPHP_Github_Directory_List_Widget_Widget_Plugin',
			'description' => 'Github Directory List Widget Plugin',
		);

		parent::__construct(
			'wwPHP_Github_Directory_List_Widget_Widget_Plugin', 'Github Directory List Widget Plugin', $options
		);
    }
	
    public function widget( $args, $instance ) {
		
		extract($args);
		$github_user_name   = isset( $instance['github_user_name'] ) ? apply_filters( 'widget_title', $instance['github_user_name'] ) : '';
		$github_repo_name   = isset( $instance['github_repo_name'] ) ? apply_filters( 'widget_title', $instance['github_repo_name'] ) : '';
		$number_of_files    = isset( $instance['number_of_files'] ) ? apply_filters( 'widget_title', $instance['number_of_files'] ) : '';
		$github_api_token   = isset( $instance['github_api_token'] ) ? apply_filters( 'widget_title', $instance['github_api_token'] ) : '';
		$title    			= isset( $instance['title'] ) ? apply_filters( 'widget_title', $instance['title'] ) : '';
		echo $args['before_widget'];
		echo '<div class="widget-text wp_widget_plugin_box">';
		if ($title) {
			echo $before_title . "<i class='fa fa-github'></i>" . $title . $after_title;
		}
			$url 			= 'https://api.github.com/repos/'.$github_user_name.'/'.$github_repo_name.'/contents';
			$request 		= wp_remote_get($url,
             array( 'timeout' => 20,
            'headers' => array( 'user-agent' => 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13',
			'Authorization' => 'token '.$github_api_token
			)));
			$ReturnData 	= json_decode($request["body"], true);
			
			ECHO "<div class='fileslistcontent'><ol>";
			
			foreach($ReturnData as $RData)
			{
				if(strlen($RData["name"]) > 36)
				{
					$LinkTitle = substr($RData["name"], 0, 36)."...";
				}else{
					$LinkTitle = $RData["name"];
				}
				ECHO "<li><i class='fa fa-folder'></i> <a href='".$RData["html_url"]."' target='_blank' rel='nofollow' title='".$RData["name"]."' alt='".$RData["name"]."'>".$LinkTitle."</a></li>";
			}
			ECHO "</ol></div>";
			ECHO "<div class='githubuserrepo'><img src='".plugins_url('', __FILE__)."/img/Github-Icon.png' style='height:24px; position:absolute;'/><a href='https://github.com/".$github_user_name."' target='_blank' rel='nofollow' style='margin-left:30px; margin-right:10px;'>".$github_user_name."</a> / <a href='https://github.com/".$github_user_name."/".$github_repo_name."' target='_blank' rel='nofollow' style='margin-left:10px; '>".$github_repo_name."</a></div>";
		echo '</div>';
		echo $args['after_widget'];
    }
	
	public function form( $instance ) {
		$defaults = array(
			'github_user_name'    => '',
			'github_api_token'    => '',
			'github_repo_name' => '',
			'number_of_files' => '',
			'title' => ''
		);
		extract( wp_parse_args( ( array ) $instance, $defaults ) ); 
		?>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>"><?php _e( 'Widget Title', 'text_domain' ); ?></label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'title' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'title' ) ); ?>" type="text" value="<?php echo esc_attr( $title ); ?>" />
		</p>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'github_user_name' ) ); ?>"><?php _e( 'Github Username', 'text_domain' ); ?></label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'github_user_name' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'github_user_name' ) ); ?>" type="text" value="<?php echo esc_attr( $github_user_name ); ?>" />
		</p>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'github_api_token' ) ); ?>"><?php _e( 'Github API Token', 'text_domain' ); ?></label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'github_api_token' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'github_api_token' ) ); ?>" type="text" value="<?php echo esc_attr( $github_api_token ); ?>" />
		</p>
		<p>
			<label for="<?php echo esc_attr( $this->get_field_id( 'github_repo_name' ) ); ?>"><?php _e( 'Gihub Repo Name', 'text_domain' ); ?></label>
			<input class="widefat" id="<?php echo esc_attr( $this->get_field_id( 'github_repo_name' ) ); ?>" name="<?php echo esc_attr( $this->get_field_name( 'github_repo_name' ) ); ?>" type="text" value="<?php echo esc_attr( $github_repo_name ); ?>" />
		</p>
		<p>
			<label for="<?php echo $this->get_field_id( 'number_of_files' ); ?>"><?php _e( 'Number of Files', 'text_domain' ); ?></label>
			<select name="<?php echo $this->get_field_name( 'number_of_files' ); ?>" id="<?php echo $this->get_field_id( 'number_of_files' ); ?>" class="widefat">
			<?php
			// Your options array
			$options = array(
				''        => __( '5', '5' ),
				'option_1' => __( '10', '10' ),
				'option_2' => __( '15', '15' )
			);

			// Loop through options and add each one to the select dropdown
			foreach ( $options as $key => $name ) {
				echo '<option value="' . esc_attr( $key ) . '" id="' . esc_attr( $key ) . '" '. selected( $number_of_files, $key, false ) . '>'. $name . '</option>';

			} ?>
			</select>
		</p>
	<?php
	}
	
	public function update( $new_instance, $old_instance ) {
		$instance = $old_instance;
		$instance['github_user_name']   = isset( $new_instance['github_user_name'] ) ? wp_strip_all_tags( $new_instance['github_user_name'] ) : '';
		$instance['github_repo_name']   = isset( $new_instance['github_repo_name'] ) ? wp_strip_all_tags( $new_instance['github_repo_name'] ) : '';
		$instance['number_of_files']    = isset( $new_instance['number_of_files'] ) ? wp_strip_all_tags( $new_instance['number_of_files'] ) : '';
		$instance['github_api_token']   = isset( $new_instance['github_api_token'] ) ? wp_strip_all_tags( $new_instance['github_api_token'] ) : '';
		$instance['title']    			= isset( $new_instance['title'] ) ? wp_strip_all_tags( $new_instance['title'] ) : '';
		return $instance;
	}
}

if (!defined('PLUGIN_DIR_GFW')) {
  define('PLUGIN_DIR_GFW',plugins_url('', __FILE__));
}

function load_script_style_wwPHP_GFW() {
      wp_enqueue_style( 'wwphp_gfw_css',PLUGIN_DIR_GFW.'/css/style.css', false, '1.0.0' );
      wp_enqueue_script( 'wwphp_gfw_js',PLUGIN_DIR_GFW.'/js/script.js', false, '1.0.0' );
}

function my_register_wwPHP_Github_Directory_List_Widget_Widget_Plugin() {
    register_widget( 'wwPHP_Github_Directory_List_Widget_Widget_Plugin' );
}
add_action('wp_enqueue_scripts',  'load_script_style_wwPHP_GFW');
add_action( 'widgets_init', 'my_register_wwPHP_Github_Directory_List_Widget_Widget_Plugin' );

?>