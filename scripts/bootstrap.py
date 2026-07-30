"""Script de inicialização para novos projetos de dados.

Limpa os arquivos explicativos/educacionais e personaliza
os metadados do projeto para início imediato (ready-to-go).
"""

import re
import shutil
from pathlib import Path


def main() -> None:
    """Orquestra o processo de bootstrap do projeto de dados."""
    print("==================================================")
    print("   Inicialização do Novo Projeto de Dados         ")
    print("==================================================")

    # Prompt user
    project_name = input("Nome do projeto (kebab-case, ex: meu-projeto): ").strip()
    if not project_name:
        project_name = "meu-projeto-de-dados"

    project_description = input("Descrição do projeto: ").strip()
    if not project_description:
        project_description = "Pipeline de dados estruturado."

    author_name = input("Autor (Nome <email>): ").strip()
    if not author_name:
        author_name = "Desenvolvedor"

    repo_url = input("URL do repositório (opcional): ").strip()
    if not repo_url:
        repo_url = "https://github.com/usuario/meu-projeto"

    project_name_title = project_name.replace("-", " ").title()

    print("\n[1/5] Personalizando metadados...")

    # 1. Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        content = pyproject_path.read_text(encoding="utf-8")

        # Replace project name
        content = re.sub(
            r"name\s*=\s*\"[^\"]+\"", f'name = "{project_name}"', content, count=1
        )
        # Replace description
        content = re.sub(
            r"description\s*=\s*\"[^\"]+\"",
            f'description = "{project_description}"',
            content,
            count=1,
        )

        # Remove init task from taskipy
        content = re.sub(r"\n\s*init\s*=\s*\"[^\"]+\"", "", content)

        pyproject_path.write_text(content, encoding="utf-8")
        print("  - pyproject.toml atualizado.")

    # 2. Update mkdocs.yml
    mkdocs_path = Path("mkdocs.yml")
    if mkdocs_path.exists():
        content = mkdocs_path.read_text(encoding="utf-8")

        content = re.sub(
            r"site_name:\s*.*", f"site_name: {project_name_title}", content
        )
        content = re.sub(
            r"site_description:\s*.*",
            f"site_description: {project_description}",
            content,
        )
        content = re.sub(r"repo_name:\s*.*", f"repo_name: {project_name}", content)
        content = re.sub(r"repo_url:\s*.*", f"repo_url: {repo_url}", content)

        # Clean up navigation
        nav_pattern = re.compile(r"nav:\s*\n(\s*-.*\n)+", re.MULTILINE)
        clean_nav = (
            "nav:\n"
            "  - Introdução: index.md\n"
            "  - Estrutura do projeto: estrutura.md\n"
            "  - Pipeline: pipeline.md\n"
        )
        content = nav_pattern.sub(clean_nav, content)

        mkdocs_path.write_text(content, encoding="utf-8")
        print("  - mkdocs.yml atualizado.")

    print("\n[2/5] Recriando arquivos de documentação...")

    # 3. Recreate docs/index.md
    docs_dir = Path("docs")
    if docs_dir.exists():
        index_path = docs_dir / "index.md"
        index_content = (
            f"# {project_name_title}\n\n"
            f"{project_description}\n\n"
            "## Estrutura do Projeto\n\n"
            "O projeto segue a estrutura padrão de engenharia de dados:\n"
            "- `app/` - Código-fonte do pipeline (extract, transform, load).\n"
            "- `tests/` - Testes automatizados (pytest).\n"
            "- `docs/` - Documentação do projeto (MkDocs).\n\n"
            "Para mais detalhes sobre as pastas, veja a página de "
            "[Estrutura do projeto](estrutura.md).\n"
        )
        index_path.write_text(index_content, encoding="utf-8")
        print("  - docs/index.md recriado.")

    # 4. Recreate README.md
    readme_path = Path("README.md")
    readme_content = f"""# {project_name_title}

{project_description}

## Como Rodar o Projeto

1. Instale as dependências com o `uv`:
   ```bash
   uv sync
   uv run pre-commit install
   ```

2. Implemente as etapas de extração, transformação e carga em `app/pipeline/`.

3. Execute o pipeline:
   ```bash
   uv run python app/main.py
   ```

## Comandos Úteis

- `uv run task format` - Formata o código com o Ruff.
- `uv run task lint` - Valida o estilo com o Ruff.
- `uv run task test` - Executa a suíte de testes (pytest).
- `uv run task docs` - Executa o servidor de documentação local (MkDocs).
"""
    readme_path.write_text(readme_content, encoding="utf-8")
    print("  - README.md recriado.")

    print("\n[3/5] Removendo arquivos de guia e explicações...")

    # Files and folders to delete
    to_delete = [
        docs_dir / "guia",
        docs_dir / "ia-como-acelerador.md",
        docs_dir / "sdd.md",
        docs_dir / "prd-template.md",
    ]

    for item in to_delete:
        if item.exists():
            if item.is_dir():
                shutil.rmtree(item)
                print(f"  - Pasta removida: {item.relative_to(Path('.'))}")
            else:
                item.unlink()
                print(f"  - Arquivo removido: {item.relative_to(Path('.'))}")

    print("\n[4/5] Limpando ambiente virtual e site antigo...")
    site_dir = Path("site")
    if site_dir.exists():
        shutil.rmtree(site_dir)
        print("  - Pasta site/ removida.")

    print("\n[5/5] Finalizando...")

    # Delete script self
    script_path = Path(__file__)
    rel_script = script_path.relative_to(Path("."))
    print(f"  - Removendo o script de inicialização: {rel_script}")

    # Windows sometimes locks running files, but
    # python can unlink __file__ on modern OS.
    try:
        script_path.unlink()
    except OSError:
        print(
            "  - Não foi possível deletar o script automaticamente. "
            "Por favor, delete manualmente a pasta scripts/."
        )

    print("\n==================================================")
    print("   Projeto inicializado com sucesso! Pronto para ir.  ")
    print("==================================================")


if __name__ == "__main__":
    main()
