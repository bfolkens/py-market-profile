{ lib, python3Packages }:

python3Packages.buildPythonPackage {
  pname = "market-profile";
  version = lib.strings.trim (builtins.readFile ../VERSION);
  src = lib.cleanSource ../.;
  pyproject = true;

  # Nix runs pytest directly, so setuptools does not need to fetch pytest-runner.
  postPatch = ''
    substituteInPlace setup.py --replace-fail "    setup_requires=['pytest-runner']," ""
  '';

  build-system = [ python3Packages.setuptools ];
  dependencies = with python3Packages; [
    numpy
    pandas
    scipy
  ];

  nativeCheckInputs = [ python3Packages.pytestCheckHook ];
  pythonImportsCheck = [ "market_profile" ];

  meta = {
    description = "Calculate market profiles from Pandas DataFrames";
    homepage = "https://github.com/bfolkens/py-market-profile";
    license = lib.licenses.bsd2;
  };
}
