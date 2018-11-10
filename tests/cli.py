# coding=utf-8

import unittest

from click.testing import CliRunner
from geobuf.scripts.cli import cli

from tests import get_data_path


class CLITests(unittest.TestCase):
    def setUp(self):
        with open(get_data_path("props.json")) as f:
            self.props_json = f.read()

    def test_cli_encode_err(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['encode'], "0")
        assert result.exit_code == 1

    def test_cli_decode_err(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['decode'], "0")
        assert result.exit_code == 1

    def test_cli_roundtrip(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['encode'], self.props_json)
        assert result.exit_code == 0
        pbf = result.output_bytes
        result = runner.invoke(cli, ['decode'], pbf)
        assert result.exit_code == 0
        assert "@context" in result.output
        assert result.output.count("Feature") == 6


if __name__ == "__main__":
    unittest.main()
