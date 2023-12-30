plugins {
    id("java")
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    implementation ("org.apache.commons:commons-math3:3.6.1")
    // https://mavenlibs.com/maven/dependency/com.xiantrimble.combinatorics/combinatorics
    implementation("com.xiantrimble.combinatorics:combinatorics:0.2.0")
    implementation("com.google.guava:guava:32.0.0-android")
    // https://mavenlibs.com/maven/dependency/com.googlecode.combinatoricslib/combinatoricslib
    implementation("com.github.dpaukov:combinatoricslib3:3.3.3")
    // https://mavenlibs.com/maven/dependency/com.ibm.icu/icu4j
    implementation("com.ibm.icu:icu4j:73.2")
    // https://mvnrepository.com/artifact/org.apache.commons/commons-collections4
    implementation("org.apache.commons:commons-collections4:4.3")
}

tasks.test {
    useJUnitPlatform()
}