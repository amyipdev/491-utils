{ pkgs ? import <nixpkgs> {} }:

let
    pygad = pkgs.python311Packages.buildPythonPackage rec {
        pname = "pygad";
        version = "3.3.1";
        propagatedBuildInputs = with pkgs.python311Packages; [
            cloudpickle
            pip
            numpy
            matplotlib
            torch
            keras
        ];
        src = pkgs.fetchFromGitHub {
            owner = "amyipdev";
            repo = "GeneticAlgorithmPython";
            rev = "8ee60fce58788f97d9b318b202467846e9f7f1ed";
            hash = "sha256-+rLvmgar5cwy6t1sk8YVljP9CAqdZwnnDcKSfUboMrA=";
        };
        pythonImportsCheck = [ "pygad" ];
        catchConflicts = false;
    };
in
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
    pygad
    scikit-learn
    tensorflow-bin
    (keras.override {
        tensorflow = tensorflow-bin;
    })
  ]);
}
