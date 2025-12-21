# Getting Started

### Reference Documentation

For further reference, please consider the following sections:

* [Official Gradle documentation](https://docs.gradle.org)
* [Spring Boot Gradle Plugin Reference Guide](https://docs.spring.io/spring-boot/4.0.1/gradle-plugin)
* [Create an OCI image](https://docs.spring.io/spring-boot/4.0.1/gradle-plugin/packaging-oci-image.html)
* [Spring Integration AMQP Module Reference Guide](https://docs.spring.io/spring-integration/reference/amqp.html)
* [Spring Integration JDBC Module Reference Guide](https://docs.spring.io/spring-integration/reference/jdbc.html)
* [Spring Integration Test Module Reference Guide](https://docs.spring.io/spring-integration/reference/testing.html)
* [Spring Integration Security Module Reference Guide](https://docs.spring.io/spring-integration/reference/security.html)
* [Spring Integration WebFlux Module Reference Guide](https://docs.spring.io/spring-integration/reference/webflux.html)
* [Spring Boot Testcontainers support](https://docs.spring.io/spring-boot/4.0.1/reference/testing/testcontainers.html#testing.testcontainers)
* [Testcontainers RabbitMQ Module Reference Guide](https://java.testcontainers.org/modules/rabbitmq/)
* [Testcontainers Grafana Module Reference Guide](https://java.testcontainers.org/modules/grafana/)
* [Testcontainers Postgres Module Reference Guide](https://java.testcontainers.org/modules/databases/postgres/)
* [Spring for RabbitMQ](https://docs.spring.io/spring-boot/4.0.1/reference/messaging/amqp.html)
* [Spring for RabbitMQ Streams](https://docs.spring.io/spring-amqp/reference/stream.html)
* [Spring Batch](https://docs.spring.io/spring-boot/4.0.1/how-to/batch.html)
* [Spring Batch JDBC](https://docs.spring.io/spring-boot/4.0.1/how-to/batch.html)
* [Spring Configuration Processor](https://docs.spring.io/spring-boot/4.0.1/specification/configuration-metadata/annotation-processor.html)
* [Spring Data JDBC](https://docs.spring.io/spring-boot/4.0.1/reference/data/sql.html#data.sql.jdbc)
* [Spring Boot DevTools](https://docs.spring.io/spring-boot/4.0.1/reference/using/devtools.html)
* [Flyway Migration](https://docs.spring.io/spring-boot/4.0.1/how-to/data-initialization.html#howto.data-initialization.migration-tool.flyway)
* [Spring Integration](https://docs.spring.io/spring-boot/4.0.1/reference/messaging/spring-integration.html)
* [JDBC API](https://docs.spring.io/spring-boot/4.0.1/reference/data/sql.html)
* [OpenTelemetry](https://docs.spring.io/spring-boot/4.0.1/reference/actuator/observability.html#actuator.observability.opentelemetry)
* [OTLP for metrics](https://docs.spring.io/spring-boot/4.0.1/reference/actuator/metrics.html#actuator.metrics.export.otlp)
* [Prometheus](https://docs.spring.io/spring-boot/4.0.1/reference/actuator/metrics.html#actuator.metrics.export.prometheus)
* [Spring REST Docs](https://docs.spring.io/spring-restdocs/docs/current/reference/htmlsingle/)
* [Spring Security](https://docs.spring.io/spring-boot/4.0.1/reference/web/spring-security.html)
* [Reactive HTTP Client](https://docs.spring.io/spring-boot/4.0.1/reference/io/rest-client.html#io.rest-client.webclient)
* [Testcontainers](https://java.testcontainers.org/)
* [Spring Reactive Web](https://docs.spring.io/spring-boot/4.0.1/reference/web/reactive.html)

### Guides

The following guides illustrate how to use some features concretely:

* [Messaging with RabbitMQ](https://spring.io/guides/gs/messaging-rabbitmq/)
* [Creating a Batch Service](https://spring.io/guides/gs/batch-processing/)
* [Using Spring Data JDBC](https://github.com/spring-projects/spring-data-examples/tree/main/jdbc/basics)
* [Integrating Data](https://spring.io/guides/gs/integration/)
* [Accessing Relational Data using JDBC with Spring](https://spring.io/guides/gs/relational-data-access/)
* [Managing Transactions](https://spring.io/guides/gs/managing-transactions/)
* [Securing a Web Application](https://spring.io/guides/gs/securing-web/)
* [Spring Boot and OAuth2](https://spring.io/guides/tutorials/spring-boot-oauth2/)
* [Authenticating a User with LDAP](https://spring.io/guides/gs/authenticating-ldap/)
* [Building a Reactive RESTful Web Service](https://spring.io/guides/gs/reactive-rest-service/)

### Additional Links

These additional references should also help you:

* [Gradle Build Scans – insights for your project's build](https://scans.gradle.com#gradle)

### Testcontainers support

This project
uses [Testcontainers at development time](https://docs.spring.io/spring-boot/4.0.1/reference/features/dev-services.html#features.dev-services.testcontainers).

Testcontainers has been configured to use the following Docker images:

* [`grafana/otel-lgtm:latest`](https://hub.docker.com/r/grafana/otel-lgtm)
* [`postgres:latest`](https://hub.docker.com/_/postgres)
* [`rabbitmq:latest`](https://hub.docker.com/_/rabbitmq)

Please review the tags of the used images and set them to the same as you're running in production.

