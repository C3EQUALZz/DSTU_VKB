plugins {
    id("java")
    id("application")
    id("org.openjfx.javafxplugin") version "0.1.0"
    id("io.freefair.lombok") version "6.3.0"
}

javafx {
    version = "21.0.2"
    modules("javafx.controls", "javafx.fxml", "javafx.media", "javafx.web", "javafx.media")
}


group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}


dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    implementation("org.apache.commons:commons-math3:3.6.1")
    // https://mavenlibs.com/maven/dependency/com.xiantrimble.combinatorics/combinatorics
    implementation("com.xiantrimble.combinatorics:combinatorics:0.2.0")
    implementation("com.google.guava:guava:32.0.0-android")
    // https://mavenlibs.com/maven/dependency/com.googlecode.combinatoricslib/combinatoricslib
    implementation("com.github.dpaukov:combinatoricslib3:3.3.3")
    // https://mavenlibs.com/maven/dependency/com.ibm.icu/icu4j
    implementation("com.ibm.icu:icu4j:73.2")
    // https://mvnrepository.com/artifact/org.apache.commons/commons-collections4
    implementation("org.apache.commons:commons-collections4:4.3")
    implementation("org.jetbrains:annotations:16.0.2")
    implementation("com.googlecode.json-simple:json-simple:1.1.1")
    implementation("com.github.javafaker:javafaker:1.0.2")
    // https://mvnrepository.com/artifact/com.dlsc/GMapsFX
    implementation("com.sothawo:mapjfx:3.1.0")
    implementation("ch.qos.logback:logback-classic:1.2.3")
    implementation("org.apache.poi:poi-ooxml:5.2.5")
    implementation("org.apache.logging.log4j:log4j-to-slf4j:2.8.2")
    implementation("org.xerial:sqlite-jdbc:3.30.1")
    implementation("de.jensd:fontawesomefx-fontawesome:4.7.0-9.1.2")
    compileOnly("org.projectlombok:lombok:1.18.32")
    annotationProcessor("org.projectlombok:lombok:1.18.32")
    testCompileOnly("org.projectlombok:lombok:1.18.32")
    testAnnotationProcessor("org.projectlombok:lombok:1.18.32")
    implementation("org.controlsfx:controlsfx:11.2.1")
    // https://mvnrepository.com/artifact/javax.xml.bind/jaxb-api
    implementation("jakarta.xml.bind:jakarta.xml.bind-api:4.0.0")
    implementation("org.glassfish.jaxb:jaxb-runtime:4.0.1")
    implementation("javax.xml.bind:jaxb-api:2.3.1")
    implementation("com.sun.xml.bind:jaxb-core:3.0.0")
    implementation("com.sun.xml.bind:jaxb-impl:2.3.3")
    implementation("com.sun.xml.bind:jaxb-core:2.3.0.1")
}

tasks.test {
    useJUnitPlatform()
}

application {
    mainClass = "programmingLanguagesJava.laboratories.GUI.Main"
}