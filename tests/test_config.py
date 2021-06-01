from io import StringIO

from mailrise.config import ConfigFileError, load_config

import pytest


def test_errors() -> None:
    """Tests for :fun:`load_config`'s failure conditions."""
    with pytest.raises(ConfigFileError):
        f = StringIO("""
            24
            """
        )
        load_config(f)
    with pytest.raises(ConfigFileError):
        f = StringIO("""
            configs: 24
            """
        )
        load_config(f)
    with pytest.raises(ConfigFileError):
        f = StringIO("""
            configs:
              test: 24
            """
        )
        load_config(f)


def test_load() -> None:
    """Tests a successful load with :fun:`load_config`."""
    f = StringIO("""
        configs:
          test:
            urls:
              - json://localhost
        """
    )
    mrise = load_config(f)
    assert len(mrise.configs) == 1
    assert 'test' in mrise.configs

    arise = mrise.configs['test']
    servers = arise.servers()
    assert len(servers) == 1
    assert servers[0].url().startswith('json://localhost/')


def test_multi_load() -> None:
    """Tests a sucessful load with :fun:`load_config` with multiple configs."""
    f = StringIO("""
        configs:
          test1:
            urls:
              - json://localhost
          test2:
            urls:
              - json://localhost
        """
    )
    mrise = load_config(f)
    assert len(mrise.configs) == 2

    for k in ('test1', 'test2'):
        assert k in mrise.configs

        arise = mrise.configs[k]
        servers = arise.servers()
        assert len(servers) == 1
        assert servers[0].url().startswith('json://localhost/')