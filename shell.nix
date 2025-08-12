{
  pkgs ? import <nixpkgs> { },
}:

let
  pyproject = pkgs.lib.importTOML ./bff/pyproject.toml;
  dishka = pkgs.callPackage ./dishka.nix { };
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (
      p:
      with p;
      [
        fastapi
        uvicorn
        pytelegrambotapi
        sqlalchemy
        pydantic
        dynaconf
        dishka
        python-jose
        httplib2
        google-api-python-client
        oauth2client
        (pkgs.python3Packages.mkPythonEditablePackage {
          pname = pyproject.project.name;
          version = pyproject.project.version;

          root = "$PWD/bff";
        })
      ]
      ++ uvicorn.optional-dependencies.standard
      ++ fastapi.optional-dependencies.standard
    ))
  ];
}
