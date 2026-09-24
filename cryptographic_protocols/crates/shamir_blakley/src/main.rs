use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    shamir_blakley::presentation::cli::run()
}
