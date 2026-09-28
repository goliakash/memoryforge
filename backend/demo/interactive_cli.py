import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from ai_memory_agent.agents.orchestrator import SecurityMemoryOrchestrator
from ai_memory_agent.models.incident import Incident, IncidentSeverity
from ai_memory_agent.models.audit import AuditRequest
from demo.demo_story import run_full_demo

console = Console(safe_box=True, legacy_windows=False)
orchestrator = SecurityMemoryOrchestrator()


def display_menu():
    console.print()
    console.print(
        Panel(
            "[bold white]AI Security Operations & Compliance Memory Agent[/bold white]\n"
            "[italic cyan]Powered by Hindsight Persistent Memory[/italic cyan]\n\n"
            "1. Run 10-Step Automated Demo Story (INC-1024 -> INC-1038 -> Audit)\n"
            "2. Ingest & Investigate New Incident (Interactive)\n"
            "3. Submit Auditor Inquiry (Access Control, Evidence, Remediation)\n"
            "4. Search Hindsight Memory Directly (Semantic Recall)\n"
            "5. Reflect on Memory Bank (Cross-Incident Pattern Synthesis)\n"
            "6. View Hindsight Memory Networks Status\n"
            "7. View Memory Timeline Stream\n"
            "8. Exit",
            title="[bold bright_blue]Main Menu[/bold bright_blue]",
            border_style="bright_blue",
        )
    )


def handle_new_incident():
    console.print("\n[bold yellow]-- Ingest New Security Incident --[/bold yellow]")
    inc_id = Prompt.ask("Incident ID", default="INC-2048")
    title = Prompt.ask("Incident Title", default="Unauthorized IAM Administrator Role Assumption")
    desc = Prompt.ask("Description", default="A deployment service account assumed an IAM role with AdministratorAccess wildcard policy.")
    severity_str = Prompt.ask("Severity (LOW/MEDIUM/HIGH/CRITICAL)", default="HIGH").upper()
    asset = Prompt.ask("Affected Asset", default="deploy-service-role")
    asset_type = Prompt.ask("Asset Type (cloud_storage/iam_role/compute)", default="iam_role")
    evidence = Prompt.ask("Detection Alert / Evidence", default="CloudTrail logged sts:AssumeRole for role 'deploy-service-role' from anomalous IP.")

    incident = Incident(
        incident_id=inc_id,
        title=title,
        description=desc,
        severity=IncidentSeverity[severity_str] if severity_str in IncidentSeverity.__members__ else IncidentSeverity.HIGH,
        affected_asset=asset,
        asset_type=asset_type,
        evidence=evidence,
    )

    with console.status("[cyan]Investigating and consulting Hindsight memory..."):
        result = orchestrator.investigate_and_remember(incident)

    console.print(f"\n[bold green][OK] Investigation completed for {inc_id}![/bold green]")
    if result.recalled_prior_incident:
        console.print(f"[bold cyan]Recalled Memory:[/bold cyan] {result.recalled_prior_incident.recalled_incident_id} (Score: {result.recalled_prior_incident.relevance_score:.2f})")
    if result.is_recurring_issue:
        console.print(f"[bold red]Recurring Alert:[/bold red] {result.recurrence_rationale}")

    console.print(f"[bold]Root Cause:[/bold] {result.root_cause.summary}")
    console.print(f"[bold]Remediation Steps:[/bold] {len(result.remediation_steps)} actions generated")
    console.print(f"[bold]Evidence Fingerprints:[/bold] {len(result.evidence_collected)} SHA-256 hashes retained into Hindsight.")


def handle_audit_query():
    console.print("\n[bold magenta]-- Submit Compliance Audit Inquiry --[/bold magenta]")
    control = Prompt.ask("Control Category", default="Access Control")
    query = Prompt.ask("Audit Inquiry", default="Show me previous findings related to access control, their remediation status, and available evidence.")

    req = AuditRequest(
        control=control,
        request=query,
        requested_by="External Auditor",
    )

    with console.status("[magenta]Searching Hindsight organizational memory..."):
        res = orchestrator.handle_audit_request(req)

    console.print(f"\n[bold green]Compliance Posture:[/bold green] {res.compliance_posture}")
    console.print(f"[bold]Historical Findings Retrived:[/bold] {len(res.historical_findings)}")
    console.print(f"[bold]Evidence Artifacts Retrived:[/bold] {len(res.evidence_items)}")
    console.print(f"\n[italic]{res.executive_summary}[/italic]")


def handle_memory_recall():
    console.print("\n[bold cyan]-- Hindsight Memory Semantic Recall --[/bold cyan]")
    q = Prompt.ask("Search Query", default="storage bucket public access")
    recalled = orchestrator.memory.recall(query=q, limit=5)

    table = Table(title=f"Hindsight Recall Results for: '{q}'", border_style="cyan")
    table.add_column("Network", style="yellow")
    table.add_column("Score", style="green")
    table.add_column("Content Snippet", style="white")
    for item in recalled:
        table.add_row(item.memory_unit.network_type.value.upper(), f"{item.score:.2f}", item.memory_unit.content[:70] + "...")
    console.print(table)


def handle_memory_reflect():
    console.print("\n[bold green]-- Hindsight Memory Reflection --[/bold green]")
    topic = Prompt.ask("Topic to Reflect Upon", default="Access Control")
    reflection = orchestrator.memory.reflect(topic=topic)
    console.print(Panel(reflection.synthesis, title=f"Hindsight Reflection: {topic}", border_style="green"))
    if reflection.recurring_patterns:
        console.print("[bold red]Recurring Patterns:[/bold red]")
        for p in reflection.recurring_patterns:
            console.print(f"  - {p}")
    if reflection.recommended_policy_changes:
        console.print("[bold yellow]Recommended Policy Enhancements:[/bold yellow]")
        for r in reflection.recommended_policy_changes:
            console.print(f"  - {r}")


def handle_networks_status():
    summary = orchestrator.memory.get_networks_summary()
    table = Table(title="Hindsight Memory Networks", border_style="blue")
    table.add_column("Network", style="cyan")
    table.add_column("Units Count", style="green")
    for net, count in summary["networks"].items():
        table.add_row(net.upper(), str(count))
    console.print(table)
    console.print(f"[bold]Active Engine:[/bold] {summary['engine_mode']}")
    console.print(f"[bold]Total Retained Units:[/bold] {summary['total_memories']}")


def handle_timeline():
    timeline = orchestrator.memory.get_timeline()
    table = Table(title="Hindsight Memory Timeline Stream", border_style="magenta")
    table.add_column("Timestamp (UTC)", style="dim")
    table.add_column("Network", style="yellow")
    table.add_column("Entities", style="cyan")
    table.add_column("Content", style="white")
    for item in timeline[-10:]:
        table.add_row(
            item["timestamp"][:19],
            item["network"].upper(),
            ", ".join(item["entities"][:2]),
            item["content"][:65] + "...",
        )
    console.print(table)


def main():
    while True:
        display_menu()
        choice = Prompt.ask("Select an option (1-8)", default="1")
        if choice == "1":
            run_full_demo()
        elif choice == "2":
            handle_new_incident()
        elif choice == "3":
            handle_audit_query()
        elif choice == "4":
            handle_memory_recall()
        elif choice == "5":
            handle_memory_reflect()
        elif choice == "6":
            handle_networks_status()
        elif choice == "7":
            handle_timeline()
        elif choice == "8":
            console.print("[cyan]Exiting Security Memory Agent. Goodbye![/cyan]")
            break
        else:
            console.print("[red]Invalid selection. Try again.[/red]")


if __name__ == "__main__":
    main()
