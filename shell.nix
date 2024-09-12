{ pkgs ? import <nixpkgs> {} }:

with pkgs; mkShell {
  nativeBuildInputs = [
    gcc14
    libcap
    libpcap
    pkg-config
    gnumake
    jq
    python311
    cargo
    zlib
    which
    libzip
    openssl
    libxml2
    libxslt
    gdb
  ] ++ (with python311Packages; [
    numpy
    scikit-learn
    tensorflow-bin
    (keras.override {
        tensorflow = tensorflow-bin;
    })
  ]);
}
