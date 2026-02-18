"""CLI 入口"""
import typer
from pathlib import Path
from rich.console import Console
from questfill.parser import parse_questionnaire
from questfill.filler import fill_questionnaire
from questfill.exporter import export_questionnaire

app = typer.Typer(help="自动填写企业安全合规问卷")
console = Console()

@app.command()
def fill(
    input_file: Path = typer.Argument(..., help="问卷文件路径 (PDF/Word/Excel)"),
    template: Path = typer.Option("template.yaml", help="企业信息模板文件"),
    output: Path = typer.Option(None, help="输出文件路径（默认：原文件名_filled）"),
):
    """填写问卷"""
    try:
        # 验证文件存在
        if not input_file.exists():
            console.print(f"[red]错误: 文件不存在 {input_file}[/red]")
            raise typer.Exit(1)
        
        if not template.exists():
            console.print(f"[red]错误: 模板文件不存在 {template}[/red]")
            raise typer.Exit(1)
        
        # 解析问卷
        console.print(f"[cyan]正在解析问卷: {input_file}[/cyan]")
        questions = parse_questionnaire(input_file)
        console.print(f"[green]✓ 发现 {len(questions)} 个问题[/green]")
        
        # 填充答案
        console.print(f"[cyan]正在填充答案...[/cyan]")
        filled_data = fill_questionnaire(questions, template)
        console.print(f"[green]✓ 已填充 {len(filled_data)} 个答案[/green]")
        
        # 导出文件
        if output is None:
            output = input_file.parent / f"{input_file.stem}_filled{input_file.suffix}"
        
        console.print(f"[cyan]正在导出到: {output}[/cyan]")
        export_questionnaire(input_file, filled_data, output)
        console.print(f"[green]✓ 完成！文件已保存到 {output}[/green]")
        
    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def init_template(output: Path = typer.Option("template.yaml", help="模板输出路径")):
    """生成企业信息模板"""
    template_content = """# 企业基本信息
company_name: "示例科技有限公司"
company_address: "北京市朝阳区示例路123号"
company_phone: "+86 10 1234 5678"
company_email: "contact@example.com"
company_website: "https://example.com"
established_date: "2020-01-01"
employee_count: "50-100人"
business_scope: "软件开发与技术服务"

# 安全合规信息
iso_certified: true
iso_cert_number: "ISO27001-2023-001"
data_protection_officer: "张三"
dpo_email: "dpo@example.com"
gdpr_compliant: true
data_retention_policy: "根据法律要求保留3-7年"
encryption_method: "AES-256"
backup_frequency: "每日备份"
incident_response_plan: true
security_training_frequency: "每季度一次"

# 技术架构
cloud_provider: "AWS"
database_type: "PostgreSQL"
authentication_method: "多因素认证(MFA)"
access_control: "基于角色的访问控制(RBAC)"
network_security: "防火墙 + IDS/IPS"
vulnerability_scanning: "每月一次"
penetration_testing: "每年两次"

# 常见问题答案
security_policy_exists: "是"
data_classification_policy: "是"
third_party_audit: "是"
business_continuity_plan: "是"
disaster_recovery_plan: "是"
"""
    
    output.write_text(template_content, encoding="utf-8")
    console.print(f"[green]✓ 模板已生成: {output}[/green]")
    console.print("[yellow]请编辑模板文件填入您的企业信息[/yellow]")

if __name__ == "__main__":
    app()