plugins {
    id("java")
    id("application")
    id("org.openjfx.javafxplugin") version "0.1.0"
}

javafx {
    version = "21.0.2"
    modules("javafx.controls", "javafx.fxml", "javafx.media", "javafx.web")
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
}

tasks.test {
    useJUnitPlatform()
}

application {
    mainClass = "programmingLanguagesJava.laboratories.GUI.Main"
}