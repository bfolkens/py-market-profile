{
  mkShellNoCC,
  python3,
  market-profile,
}:

mkShellNoCC {
  packages = [ (python3.withPackages (ps: market-profile.dependencies ++ [ ps.pytest ])) ];

  shellHook = ''
    export PYTHONPATH="$PWD/src''${PYTHONPATH:+:$PYTHONPATH}"
  '';
}
