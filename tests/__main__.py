
import click

from .id import tests as id_tests

@click.command()
def cli():
    id_tests()

cli()


