fn main() -> color_eyre::Result<()> {
    shared::logging::init()?;
    lab_01_autokey_vigenere::presentation::run()
}
