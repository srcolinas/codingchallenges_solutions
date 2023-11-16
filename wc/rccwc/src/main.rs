use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::io::BufReader;


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

    let source: Box<dyn LineSource> = match &args.file {
        None => Box::new(StdinSource),
        Some(value) => Box::new(FileSource {
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


trait LineSource {
    fn lines(&self) -> Box<dyn Iterator<Item = Result<String, io::Error>>>;
    fn filename(&self) -> String;
}

struct StdinSource;

impl LineSource for StdinSource {
    fn lines(&self) -> Box<dyn Iterator<Item = Result<String, io::Error>>> {
        Box::new(BufReader::new(io::stdin()).lines())
    }

    fn filename(&self) -> String {
        String::from("Standard Input (stdin)")
    }
}

pub struct FileSource {
    pub path: std::path::PathBuf,
}

impl LineSource for FileSource {
    fn lines(&self) -> Box<dyn Iterator<Item = Result<String, io::Error>>> {
        match File::open(&self.path) {
            Ok(file) => Box::new(BufReader::new(file).lines()),
            Err(e) => {
                eprintln!("file doesn't exist: {}", e);
                std::process::exit(1);
            }
        }
    }

    fn filename(&self) -> String {
        self.path.to_string_lossy().to_string()
    }
}
