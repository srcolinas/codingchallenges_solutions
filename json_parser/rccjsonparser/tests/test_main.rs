use assert_cmd::Command;


#[test]
fn file_doesnt_exist() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("rccjsonparser")?;
    cmd.arg("test/file/doesnt/exist");
    cmd.assert().failure().code(1);
    Ok(())
}

#[test]
fn valid_files() -> Result<(), Box<dyn std::error::Error>> {
    let files = vec!["../tests/step1/valid.json"];
    for file in files.iter(){
        let mut cmd = Command::cargo_bin("rccjsonparser")?;
        cmd.arg(file);
        cmd.assert().success().code(0);
    }
    Ok(())
}


#[test]
fn invalid_files() -> Result<(), Box<dyn std::error::Error>> {
    let files = vec!["../tests/step1/invalid.json"];
    for file in files.iter(){
        let mut cmd = Command::cargo_bin("rccjsonparser")?;
        cmd.arg(file);
        cmd.assert().failure().code(2);
    }
    Ok(())
}
