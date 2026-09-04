with open("q_shield/cli.py", "r") as f:
    content = f.read()

old_scan_def = """@cli.command()
@click.option('--path', default='.', help='Path to scan for vulnerabilities.')
@click.option('--shelf-life', default=10, help='Shelf life (x)')
@click.option('--migration-time', default=3, help='Migration time (y)')
@click.option('--quantum-horizon', default=7, help='Quantum horizon (z)')
def scan(path, shelf_life, migration_time, quantum_horizon):
    scanner = CryptoScanner()
    findings = scanner.scan_path(path)
    engine = MoscaRiskEngine()
    result = engine.evaluate(findings, x=shelf_life, y=migration_time, z=quantum_horizon)
    click.echo(json.dumps(result, indent=2))"""

new_scan_def = """@cli.command()
@click.option('--path', default='.', help='Path to scan for vulnerabilities.')
@click.option('--shelf-life', default=10, help='Shelf life (x)')
@click.option('--migration-time', default=3, help='Migration time (y)')
@click.option('--quantum-horizon', default=7, help='Quantum horizon (z)')
@click.option('--format', default='json', type=click.Choice(['json', 'cbom', 'sarif']), help='Report export format.')
@click.option('--output', default=None, help='File path to write the report.')
def scan(path, shelf_life, migration_time, quantum_horizon, format, output):
    scanner = CryptoScanner()
    findings = scanner.scan_path(path)
    engine = MoscaRiskEngine()
    result = engine.evaluate(findings, x=shelf_life, y=migration_time, z=quantum_horizon)
    
    if format == 'cbom':
        output_data = ReportGenerator.generate_cbom(findings)
    elif format == 'sarif':
        output_data = ReportGenerator.generate_sarif(findings)
    else:
        output_data = result

    output_str = json.dumps(output_data, indent=2)
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(output_str)
        click.echo(f"Report successfully written to {output}")
    else:
        click.echo(output_str)"""

if old_scan_def in content:
    content = content.replace(old_scan_def, new_scan_def)
    with open("q_shield/cli.py", "w") as f:
        f.write(content)
    print("CLI updated with format and output options.")
else:
    print("Could not match scan definition exactly, please inspect cli.py.")
