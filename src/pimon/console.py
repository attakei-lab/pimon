"""Console output wrapper.

This module for print to terminal with colors.
You should be call ``from pimon.app import console`` and ``console.info``.
"""
import click


def echo(msg: str, nl: bool = True):  # noqa: D103
    click.echo(msg, nl=nl)


def _out(text: str, fg: str, nl: bool = True):  # noqa: D103
    click.echo(click.style(text, fg=fg), nl=nl)


def info(msg: str, nl: bool = True):  # noqa: D103
    _out(msg, "green", nl=nl)


def warning(msg: str, nl: bool = True):  # noqa: D103
    _out(msg, "yellow", nl=nl)


def error(msg: str, nl: bool = True):  # noqa: D103
    _out(msg, "red", nl=nl)
