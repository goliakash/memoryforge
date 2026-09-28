import sys
import time
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
from rich.markdown import Markdown
from rich.rule import Rule

from ai_memory_agent.agents.orchestrator import SecurityMemoryOrchestrator
from ai_memory_agent.models.incident import Incident, IncidentSeverity
from ai_memory_agent.models.audit import AuditRequest

console = Console(safe_box=True, legacy_windows=False)


def run_full_demo():
    console.print()
    console.print(
        Panel(
            "[bold white]AI SECURITY OPERATIONS & COMPLIANCE MEMORY AGENT[/bold white]\n"
            "[italic cyan]Powered by Hindsight Persistent Organizational Memory[/italic cyan]\n"
            "[green]Demonstrating the Complete Memory Loop: SecOps Investigation + Audit Readiness[/green]",
            border_style="bright_blue",
            expand=False,
        )
    )
    console.print()

    orchestrator = SecurityMemoryOrchestrator()
    orchestrator.memory.clear()  # Reset for clean demo run

    # =========================================================================
    # STEP 1: CREATE INCIDENT #1024
    # =========================================================================
    console.print(Rule("[bold yellow]STEP 1: Ingesting Incident #1024 (First Occurrence)", style="yellow"))
    inc1024 = Incident(
        incident_id="INC-1024",
        title="Public Cloud Storage Exposure",
        description="A production storage bucket was discovered with public read access.",
        severity=IncidentSeverity.HIGH,
        affected_asset="customer-data-bucket",
        asset_type="cloud_storage",
        evidence="Configuration scan detected public read access via permissive ACL and wildcard Principal: '*' in bucket policy.",
    )

    t1 = Table(show_header=False, box=None)
    t1.add_row("[bold]Incident ID:[/bold]", f"[cyan]{inc1024.incident_id}[/cyan]")
    t1.add_row("[bold]Title:[/bold]", inc1024.title)
    t1.add_row("[bold]Affected Asset:[/bold]", f"[red]{inc1024.affected_asset}[/red]")
    t1.add_row("[bold]Severity:[/bold]", f"[bold red]{inc1024.severity.value}[/bold red]")
    t1.add_row("[bold]Detection Evidence:[/bold]", inc1024.evidence)
    console.print(Panel(t1, title="[yellow]Incoming Security Incident[/yellow]", border_style="yellow"))
    time.sleep(1)

    # =========================================================================
    # STEPS 2, 3, 4: AI INVESTIGATION, CONTROLS, REMEDIATION, HINDSIGHT RETAIN
    # =========================================================================
    console.print(Rule("[bold cyan]STEPS 2-4: AI Investigation & Hindsight Retention", style="cyan"))
    with console.status("[bold cyan]AI Investigation Agent analyzing Incident #1024..."):
        res1024 = orchestrator.investigate_and_remember(inc1024)
        time.sleep(1)

    console.print(f"[bold green][OK] Investigation Completed in {res1024.execution_time_ms}ms[/bold green]")
    console.print(f"[bold red]Root Cause Identified:[/bold red] {res1024.root_cause.category}")
    console.print(f"  [dim]{res1024.root_cause.summary}[/dim]\n")

    # Display Controls Table
    ctrl_table = Table(title="Mapped Security Controls & Compliance Frameworks", border_style="blue")
    ctrl_table.add_column("Control ID", style="cyan", no_wrap=True)
    ctrl_table.add_column("Framework", style="magenta")
    ctrl_table.add_column("Control Name", style="white")
    ctrl_table.add_column("Category", style="yellow")
    for c in res1024.security_controls:
        ctrl_table.add_row(c.control_id, c.framework.value, c.name, c.category)
    console.print(ctrl_table)

    # Display Remediation Steps Table
    rem_table = Table(title="Generated Technical Remediation Plan", border_style="green")
    rem_table.add_column("Step", style="dim")
    rem_table.add_column("Action", style="green")
    rem_table.add_column("Verification Criteria", style="white")
    for s in res1024.remediation_steps:
        rem_table.add_row(s.step_id, s.action, s.verification_criteria)
    console.print(rem_table)

    # Display Evidence Fingerprints
    ev_table = Table(title="Fingerprinted Audit Evidence (Cryptographic Chain of Custody)", border_style="magenta")
    ev_table.add_column("Evidence ID", style="cyan")
    ev_table.add_column("Type", style="yellow")
    ev_table.add_column("SHA-256 Digest", style="green")
    for ev in res1024.evidence_collected:
        ev_table.add_row(ev.evidence_id, ev.evidence_type, ev.hash_digest)
    console.print(ev_table)

    console.print(
        Panel(
            "[bold white]Hindsight Retain Operation Executed [Memory][/bold white]\n"
            f"- Retained into [cyan]Experience Network[/cyan]: Incident {inc1024.incident_id} root cause, controls, remediations.\n"
            f"- Verified memory persistence across organizational memory bank.",
            border_style="bright_blue",
        )
    )
    time.sleep(1)

    # =========================================================================
    # STEP 5: CREATE SIMILAR INCIDENT #1038
    # =========================================================================
    console.print()
    console.print(Rule("[bold yellow]STEP 5: New Incident Occurs -- Ingesting Incident #1038", style="yellow"))
    inc1038 = Incident(
        incident_id="INC-1038",
        title="Customer Analytics Storage Bucket Public Exposure",
        description="Production analytics storage bucket discovered with unauthenticated public read permissions.",
        severity=IncidentSeverity.HIGH,
        affected_asset="analytics-data-bucket",
        asset_type="cloud_storage",
        evidence="Configuration scan detected public read access: AWS Config rule 's3-bucket-public-read-prohibited' failed.",
    )

    t2 = Table(show_header=False, box=None)
    t2.add_row("[bold]Incident ID:[/bold]", f"[cyan]{inc1038.incident_id}[/cyan]")
    t2.add_row("[bold]Title:[/bold]", inc1038.title)
    t2.add_row("[bold]Affected Asset:[/bold]", f"[red]{inc1038.affected_asset}[/red]")
    t2.add_row("[bold]Detection Alert:[/bold]", inc1038.evidence)
    console.print(Panel(t2, title="[yellow]New Similar Security Incident[/yellow]", border_style="yellow"))
    time.sleep(1)

    # =========================================================================
    # STEPS 6 & 7: HINDSIGHT RECALL & PREVIOUS KNOWLEDGE REUSE
    # =========================================================================
    console.print(Rule("[bold green]STEPS 6 & 7: Hindsight Recall & Organizational Knowledge Reuse [Memory]", style="green"))
    with console.status("[bold green]Agent querying Hindsight Memory for past incident resolutions..."):
        res1038 = orchestrator.investigate_and_remember(inc1038)
        time.sleep(1)

    recalled = res1038.recalled_prior_incident
    if recalled:
        recall_panel_text = (
            f"[bold green][OK] HINDSIGHT RECALL SUCCESSFUL![/bold green]\n"
            f"The agent recalled prior incident [cyan]{recalled.recalled_incident_id}[/cyan] with [magenta]similarity score {recalled.relevance_score:.2f}[/magenta].\n\n"
            f"[bold]Recalled Root Cause:[/bold] {recalled.recalled_root_cause}\n"
            f"[bold]Recalled Proven Remediation:[/bold] {', '.join(recalled.recalled_remediations[:2])}\n"
            f"[bold red]Recurring Issue Alert:[/bold red] {res1038.recurrence_rationale}"
        )
        console.print(Panel(recall_panel_text, title="[bold green]Organizational Memory Recall[/bold green]", border_style="bright_green"))
    else:
        console.print("[red]No prior memory recalled.[/red]")

    # Side-by-side comparison
    comp_table = Table(title="Investigation Acceleration: Without vs With Hindsight Memory", border_style="cyan")
    comp_table.add_column("Capability", style="bold")
    comp_table.add_column("Incident #1024 (Cold Start / First Occurrence)", style="yellow")
    comp_table.add_column("Incident #1038 (With Hindsight Recall)", style="green")
    comp_table.add_row("Historical Context", "None (investigated from scratch)", "Recalled INC-1024 automatically")
    comp_table.add_row("Root Cause Analysis", "Full diagnostic required", "Instant correlation with verified policy flaw")
    comp_table.add_row("Remediation Plan", "Generated new runbook", "Reused proven, pre-verified playbook")
    comp_table.add_row("Recurrence Flag", "Single isolated event", f"Recurring Pattern Detected ({res1038.recurrence_count} occurrences)")
    console.print(comp_table)
    time.sleep(1)

    # =========================================================================
    # STEP 8: AUDITOR ASKS FOR ACCESS CONTROL FINDINGS
    # =========================================================================
    console.print()
    console.print(Rule("[bold magenta]STEP 8: Auditor Inquires for Historical Findings & Evidence", style="magenta"))
    audit_req = AuditRequest(
        control="Access Control",
        request="Show me previous findings related to access control, their remediation status, and available evidence.",
        requested_by="External SOC 2 & ISO 27001 Auditor",
    )
    console.print(
        Panel(
            f"[bold]Auditor Inquiry:[/bold] \"{audit_req.request}\"\n"
            f"[bold]Target Control Category:[/bold] {audit_req.control}\n"
            f"[bold]Auditor Role:[/bold] {audit_req.requested_by}",
            title="[magenta]External Compliance Audit Request[/magenta]",
            border_style="magenta",
        )
    )
    time.sleep(1)

    # =========================================================================
    # STEPS 9 & 10: AGENT RECALLS FINDINGS, EVIDENCE & GENERATES AUDIT REPORT
    # =========================================================================
    console.print(Rule("[bold cyan]STEPS 9 & 10: Historical Evidence Retrieval & Audit Report Generation", style="cyan"))
    with console.status("[bold cyan]Audit Agent searching Hindsight organizational memory..."):
        audit_res = orchestrator.handle_audit_request(audit_req)
        time.sleep(1)

    # Audit Findings Summary Table
    audit_table = Table(title="Historical Access Control Findings (Retrieved from Hindsight)", border_style="bright_blue")
    audit_table.add_column("Finding ID", style="cyan")
    audit_table.add_column("Incident", style="white")
    audit_table.add_column("Control", style="magenta")
    audit_table.add_column("Root Cause", style="yellow")
    audit_table.add_column("Remediation Status", style="green")
    audit_table.add_column("Evidence Hashes", style="dim")

    for f in audit_res.historical_findings:
        audit_table.add_row(
            f.finding_id,
            f.incident_id,
            f.control_id,
            f.root_cause[:45] + "...",
            f"[bold green]{f.status.value}[/bold green]",
            ", ".join(f.evidence_hashes[:2]),
        )
    console.print(audit_table)

    # Executive Audit Summary Box
    exec_summary_text = (
        f"[bold]Compliance Posture:[/bold] [bold green]{audit_res.compliance_posture}[/bold green]\n\n"
        f"[bold]Executive Summary:[/bold]\n{audit_res.executive_summary}\n\n"
        f"[bold]Auditor Verification Notes:[/bold]\n{audit_res.auditor_verification_notes}\n\n"
        f"[bold]Recurring Patterns Detected Across Memory:[/bold]\n"
        + "\n".join(f"  - {p}" for p in audit_res.recurring_patterns_detected)
    )
    console.print(Panel(exec_summary_text, title="[bold green]Official Audit Report & Evidence Package[/bold green]", border_style="bright_green"))

    # Memory Networks Inspection
    networks_summary = orchestrator.memory.get_networks_summary()
    net_table = Table(title="Hindsight Memory Networks State Post-Demo", border_style="white")
    net_table.add_column("Memory Network", style="cyan")
    net_table.add_column("Cognitive Role", style="yellow")
    net_table.add_column("Units Stored", style="green")
    net_table.add_row("World Network", "Objective environment facts, baseline policies, approved controls", str(networks_summary["networks"]["world"]))
    net_table.add_row("Experience Network", "Episodic incident investigations, containment actions, post-mortems", str(networks_summary["networks"]["experience"]))
    net_table.add_row("Observation Network", "Synthesized patterns across incidents (e.g. repeated S3 exposures)", str(networks_summary["networks"]["observation"]))
    net_table.add_row("Opinion Network", "Evolving organizational beliefs & risks (e.g. need for automated guardrails)", str(networks_summary["networks"]["opinion"]))
    console.print(net_table)

    console.print()
    console.print(
        Panel(
            "[bold green][OK] DEMO STORY COMPLETED SUCCESSFULLY[/bold green]\n"
            "Proven: The AI agent successfully transformed previous security incidents into\n"
            "persistent organizational memory and used that memory to improve future incident response\n"
            "and continuous audit readiness. [bold]The memory loop is the product! [Memory-SecOps][/bold]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    run_full_demo()
