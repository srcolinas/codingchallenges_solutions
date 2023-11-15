use clap::Parser;

#[derive(Parser)]
struct Cli {
    #[arg(value_name = "FILE")]
    file: Option<std::path::PathBuf>,

    #[arg(short = 'c', long = "bytes")]
    count_bytes: bool,

    #[arg(short = 'l', long = "lines")]
    count_lines: bool,

    #[arg(short = 'w', long = "words")]
    count_words: bool,

    #[arg(short = 'm', long = "chars")]
    count_chars: bool,
}

fn main() {
    let args = Cli::parse();

    let source: Box<dyn rccwc::LineSource> = match &args.file {
        None => Box::new(rccwc::StdinSource),
        Some(value) => Box::new(rccwc::FileSource {
            path: value.clone(),
        }),
    };

    let lines = source.lines();
    let counts = rccwc::process_lines(lines);
    let result = rccwc::format_counts(
        &counts,
        args.count_chars,
        args.count_lines,
        args.count_words,
        args.count_bytes,
        &source.filename(),
    );
    println!("{}", result);
}
