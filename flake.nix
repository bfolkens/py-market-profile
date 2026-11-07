{
  description = "Market Profile for Pandas DataFrames";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];

      perSystem =
        { config, pkgs, ... }:
        {
          packages.default = pkgs.callPackage ./nix/package.nix { };
          devShells.default = pkgs.callPackage ./nix/shell.nix {
            market-profile = config.packages.default;
          };
          checks.package = config.packages.default;
        };
    };
}
