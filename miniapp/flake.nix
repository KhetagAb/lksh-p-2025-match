{
  description = "Angular Telegram Mini App Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        nodejs = pkgs.nodejs_20;

        angularApp = pkgs.stdenv.mkDerivation rec {
          pname = "telegram-mini-app";
          version = "1.0.0";

          src = ./.;

          nativeBuildInputs = with pkgs; [
            nodejs
            nodePackages.npm
          ];

          buildPhase = ''
            export HOME=$TMPDIR
            npm ci --legacy-peer-deps
            npm run build -- --configuration production
          '';

          installPhase = ''
            mkdir -p $out
            cp -r dist/telegram-mini-app/* $out/
          '';
        };

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs
            nodePackages.npm
            nodePackages.pnpm
            nodePackages.yarn

            nodePackages."@angular/cli"

            git
            curl
            jq

            openssl
            mkcert

            docker
            docker-compose
          ];

          shellHook = ''
            echo "🚀 Angular Telegram Mini App Development Environment"
            echo ""
            echo "Available commands:"
            echo "  ng new <app-name>    - Create new Angular app"
            echo "  ng serve --ssl        - Run dev server with HTTPS"
            echo "  npm run build         - Build production app"
            echo "  mkcert -install       - Install local CA for HTTPS"
            echo ""
            echo "Node version: $(node --version)"
            echo "NPM version: $(npm --version)"
            echo "Angular CLI: $(ng --version 2>/dev/null | head -n 1 || echo 'Run npm install -g @angular/cli')"
            if [[ $- == *i* && -z "$NO_FISH" && "$SHELL" != *"fish"* ]]; then
              exec ${pkgs.fish}/bin/fish -C "
                set SHELL '${pkgs.fish}/bin/fish'
              "
            fi
          '';
        };

        packages = {
          default = angularApp;
        };

        apps.default = flake-utils.lib.mkApp {
          drv = pkgs.writeShellScriptBin "serve" ''
            ${nodejs}/bin/npx http-server ${angularApp} -p 8080 --ssl --cert cert.pem --key key.pem
          '';
        };
      });
}
