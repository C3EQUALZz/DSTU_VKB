package programmingLanguagesJava.laboratories.GUI.config;

import javafx.scene.media.AudioClip;

import java.util.Objects;

/**
 * Перечисление, которое содержит все звуки для приложения.
 */
public enum SOUND {
    ;
    public final static AudioClip HOVER = new AudioClip(Objects.requireNonNull(SOUND.class.getResource("/music/hover.mp3")).toExternalForm());
    public final static AudioClip CLICK = new AudioClip(Objects.requireNonNull(SOUND.class.getResource("/music/click.mp3")).toExternalForm());
    public final static AudioClip NOTIFICATION = new AudioClip(Objects.requireNonNull(SOUND.class.getResource("/music/notification.mp3")).toExternalForm());

}
