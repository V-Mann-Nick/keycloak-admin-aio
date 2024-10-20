{
  pkgs,
  config,
  ...
}: {
  languages.python = {
    enable = true;
    venv.enable = true;
    uv = {
      enable = true;
      sync.enable = true;
      sync.arguments = ["--frozen"];
    };
  };

  env.UV_PYTHON = config.languages.python.package;
  env.VENV_PATH = "${config.env.DEVENV_STATE}/venv";

  enterShell = ''
    python_version="${config.languages.python.package.version}"

    echo "$python_version" > .python-version

    echo
    echo "Python version: $python_version"
    echo "UV version: $(uv version)"
    echo "Virtual environment: $VENV_PATH"
    echo
  '';

  pre-commit.hooks = {
    ruff.enable = true;
    ruff-format.enable = true;
    pyright = {
      enable = true;
      settings.binPath = "${pkgs.pyright}/bin/pyright -v ${config.env.DEVENV_STATE}";
    };
    commitizen.enable = true;
    check-yaml.enable = true;
    end-of-file-fixer.enable = true;
    trim-trailing-whitespace.enable = true;
    check-toml.enable = true;
  };
}
