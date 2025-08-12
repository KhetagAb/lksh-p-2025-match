{
  lib,
  pkgs,
  ...
}:

pkgs.python3Packages.buildPythonPackage rec {
  pname = "dishka";
  version = "1.6.0";
  pyproject = true;

  disabled = pkgs.python3Packages.pythonOlder "3.10";

  src = pkgs.fetchFromGitHub {
    owner = "reagento";
    repo = "dishka";
    tag = "${version}";
    hash = "sha256-N3c1kTAnMoRgJL8ti6YYlpI6b5D2dRnrGUAmBaeWM0s=";
  };

  dependencies = [
    pkgs.python3Packages.exceptiongroup
  ];

  build-system = [ pkgs.python3Packages.setuptools ];

  pythonImportsCheck = [ "dishka" ];

  meta = {
    description = "Cute DI framework with scopes and agreeable API";
    homepage = "https://github.com/reagento/dishka";
    changelog = "https://github.com/reagento/dishka/releases/tag/${src.tag}";
    license = lib.licenses.asl20;
  };
}
