package com.c3equalz.user_service.setup.config.security;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration class that enables security configuration properties.
 */
@Configuration
@EnableConfigurationProperties(SecurityConfig.class)
public class SecurityConfiguration {
}
