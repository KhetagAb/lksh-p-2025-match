{ pkgs ? import <nixpkgs> { } }:

let pyproject = pkgs.lib.importTOML ./bff/pyproject.toml;
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (p:
      with p;
      [
        fastapi
        uvicorn
        pytelegrambotapi
        sqlalchemy
        pydantic
        dynaconf
        python-jose
        (pkgs.python3Packages.mkPythonEditablePackage {
          pname = pyproject.project.name;
          version = pyproject.project.version;

          root = "$PWD/bff";
        })
      ] ++ uvicorn.optional-dependencies.standard
      ++ fastapi.optional-dependencies.standard))
  ];
}
