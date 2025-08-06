{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (p:
      with p;
      [ fastapi uvicorn pytelegrambotapi sqlalchemy pydantic dynaconf ]
      ++ uvicorn.optional-dependencies.standard
      ++ fastapi.optional-dependencies.standard))
  ];
}
