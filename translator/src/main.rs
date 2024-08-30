// SPDX-License-Identifier: GPL-2.0-or-later

use std::fs;
use std::io::{Read, Write};

use rand::RngCore;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("reading captures...");
    let paths = fs::read_dir("../collector/captures")?;
    let mut rng: rand::rngs::ThreadRng = rand::thread_rng();
    let mut key = [0u8; 32];
    rng.fill_bytes(&mut key);
    for path in paths {
        let p = path?;
        let mut buf = vec![];
        let mut f = fs::File::open(p.path())?;
        f.read_to_end(&mut buf)?;
        // Pure source data, len won't be over 1280
        let res = libacc::encrypt_packet(&buf, &key, 1)?;
        if !std::path::Path::new("./postacc").exists() {
            std::fs::create_dir("./postacc")?;
        }
        let mut c = fs::File::create(format!(
            "./postacc/{}",
            p.file_name().into_string().expect("bad osstring")
        ))?;
        c.write_all(&res)?;
    }
    Ok(())
}
