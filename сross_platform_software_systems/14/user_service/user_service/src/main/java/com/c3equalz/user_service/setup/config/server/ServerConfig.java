package com.c3equalz.user_service.setup.config.server;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

import java.util.ArrayList;
import java.util.List;

/**
 * Configuration container for additional server settings.
 * <p>
 * Configures CORS and debug settings for the web server.
 * <p>
 * Note: Host and port are configured using standard Spring Boot properties:
 * - server.address (default: 0.0.0.0)
 * - server.port (default: 8080)
 */
@Getter
@Setter
@Validated
@ConfigurationProperties(prefix = "app.server")
public class ServerConfig {

    /**
     * Enable debug output.
     * Default: true
     */
    private boolean debug = true;

    /**
     * Enable CORS credentials.
     * Default: false
     */
    private boolean allowCredentials = false;

    /**
     * Allowed HTTP methods for CORS.
     * Default: GET, POST, PUT, PATCH, DELETE
     */
    private List<String> allowMethods = new ArrayList<>(List.of(
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE"
    ));

    /**
     * Allowed headers for CORS.
     * Default: Authorization, Content-Type, Cache-Control, Set-Cookie, etc.
     */
    private List<String> allowHeaders = new ArrayList<>(List.of(
            "Authorization",
            "Content-Type",
            "Cache-Control",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin"
    ));
}

