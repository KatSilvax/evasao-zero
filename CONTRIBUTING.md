# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o EVASÃO-ZERO!

## Como Contribuir

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/evasao-zero.git`
3. **Crie uma branch**: `git checkout -b feature/minha-feature`
4. **Faça suas alterações**
5. **Teste**: `uv run pytest`
6. **Commit**: `git commit -m 'feat: adiciona nova feature'`
7. **Push**: `git push origin feature/minha-feature`
8. **Abra um Pull Request**

## Padrões de Código

- Use **ruff** para formatação: `uv run ruff format .`
- Verifique com linter: `uv run ruff check .`
- Escreva testes para novas features
- Mantenha cobertura de testes > 80%

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `test:` testes
- `refactor:` refatoração

## Dúvidas?

Abra uma [issue](https://github.com/seu-usuario/evasao-zero/issues)!
