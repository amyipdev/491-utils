{ pkgs ? import <nixpkgs> {} }:

with pkgs; mkShell {
  nativeBuildInputs = [
    gcc14
    libcap
    libpcap
    pkg-config
    gnumake
    jq
  ];
}
