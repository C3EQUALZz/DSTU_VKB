package com.c3equalz.user_service.setup.config.server;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration class that enables server configuration properties.
 */
@Configuration
@EnableConfigurationProperties(ServerConfig.class)
public class ServerConfiguration {
}

