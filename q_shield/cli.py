import click
import json
from q_shield.parsers.scanner import CryptoScanner
from q_shield.engine.risk_engine import MoscaRiskEngine
from q_shield.engine.reports import ReportGenerator
from q_shield.parsers.refactor import refactor_code

@click.group()
def cli():
    """Q-Shield ECDAT: Enterprise Cryptographic Discovery & Agile Transition Tool"""
    pass

@cli.command()
@click.option('--path', default='.', help='Path to scan for vulnerabilities.')
@click.option('--shelf-life', default=10, help='Shelf life (x)')
@click.option('--migration-time', default=3, help='Migration time (y)')
@click.option('--quantum-horizon', default=7, help='Quantum horizon (z)')
def scan(path, shelf_life, migration_time, quantum_horizon):
    scanner = CryptoScanner()
    findings = scanner.scan_path(path)
    engine = MoscaRiskEngine()
    result = engine.evaluate(findings, x=shelf_life, y=migration_time, z=quantum_horizon)
    click.echo(json.dumps(result, indent=2))

@cli.command()
@click.option('--file', required=True, help='Source file to refactor.')
@click.option('--output', default=None, help='Output file for refactored code.')
def refactor(file, output):
    with open(file, 'r') as f:
        code = f.read()
    updated = refactor_code(code)
    if output:
        with open(output, 'w') as f:
            f.write(updated)
        click.echo(f"Refactored code written to {output}")
    else:
        click.echo(updated)

if __name__ == '__main__':
    cli()
