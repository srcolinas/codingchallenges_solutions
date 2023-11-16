use assert_cmd::Command;
use predicates::prelude::*;
use assert_fs::prelude::*;


#[test]
fn file_doesnt_exist() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("rccwc")?;
    cmd.arg("test/file/doesnt/exist");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("file doesn't exist:"));

    Ok(())
}

#[test]
fn file_exists() -> Result<(), Box<dyn std::error::Error>> {
    let file = assert_fs::NamedTempFile::new("sample.txt")?;
    file.write_str("A\nsample\nfile\nwith\neverything\n\x01\x02\n桜の花")?;

    let result = String::from("\t7 7 36 ") + file.to_str().unwrap();
    let mut cmd = Command::cargo_bin("rccwc")?;
    cmd.arg(file.path());
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(result)?);

    Ok(())
}

#[test]
fn from_stdin() -> Result<(), Box<dyn std::error::Error>> {
    let result = String::from("\t7 7 36 ");
    let mut cmd = Command::cargo_bin("rccwc")?;
    cmd.write_stdin("A\nsample\nfile\nwith\neverything\n\x01\x02\n桜の花");
    cmd.assert()
        .success()
        .stdout(predicate::str::is_match(result)?);

    Ok(())
}