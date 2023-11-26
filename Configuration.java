@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    protected SecurityFilterChain config(HttpSecurity http) throws Exception {
        http.oauth2Login()
                .authorizationEndpoint()
                .baseUri("/login");
        return http.build();
    }
}