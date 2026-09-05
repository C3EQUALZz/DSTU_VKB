fn main() -> color_eyre::Result<()> {
    shared::logging::init()?;
    lab_01_progressive_vigenere::presentation::run()
}
