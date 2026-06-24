# PRD — Product Requirements Document
## Sistema de Autenticação — Painel

---

## Visão do produto

Um sistema web de autenticação completo onde o usuário pode se cadastrar, fazer login e recuperar a senha caso a esqueça. Interface em português brasileiro, tema visual escuro com acento vermelho, sem dependências externas além do Django.

---

## Usuários-alvo

Qualquer pessoa com acesso ao link do sistema. Não há distinção de papéis por enquanto (admin e usuário comum compartilham o mesmo fluxo de entrada).

---

## Funcionalidades entregues

### 1. Login (`/`)
- Campos: Usuário e Senha
- Toggle de visibilidade da senha (ícone olho)
- Mensagem de erro inline quando credenciais são inválidas
- Link "Esqueceu a senha?" → redireciona para recuperação
- Link "Não tem conta? Cadastre-se" → redireciona para cadastro
- Após login bem-sucedido: redireciona para `/admin/` (ou `?next=` se presente)
- Usuário já autenticado é redirecionado automaticamente sem mostrar o formulário

### 2. Cadastro (`/cadastro/`)
- Campos: Usuário, E-mail, Senha, Confirmar Senha
- Validação completa via Django (`UserCreationForm`): senha fraca, senhas divergentes, usuário duplicado
- E-mail obrigatório (necessário para recuperação de senha)
- Erros exibidos inline por campo
- Auto-login após cadastro bem-sucedido
- Link "Já tem conta? Entrar" → redireciona para login

### 3. Logout (`/sair/`)
- Exige confirmação via formulário POST (proteção CSRF)
- Página de confirmação antes de efetuar logout
- Redireciona para login após logout

### 4. Recuperação de senha — 4 etapas

| Etapa | URL | Descrição |
|---|---|---|
| Solicitar | `/senha/` | Usuário informa o e-mail cadastrado |
| Confirmação de envio | `/senha/enviado/` | Mensagem neutra (não revela se e-mail existe) |
| Nova senha | `/senha/confirmar/<uid>/<token>/` | Usuário define nova senha via link do e-mail |
| Conclusão | `/senha/concluido/` | Confirmação + link para login |

- Link de reset expira em 24 horas
- Token inválido/expirado exibe mensagem específica na tela de nova senha
- Em desenvolvimento: e-mail impresso no terminal (backend `console`)
- Em produção: trocar para backend SMTP (ver CLAUDE.md)

---

## Requisitos não-funcionais

- **Idioma**: Português brasileiro em toda a interface e e-mails
- **Segurança**: CSRF em todos os formulários POST; senha nunca trafega em texto puro; campo de senha começa como `type="password"`
- **Responsividade**: Layout adapta-se a telas menores que 600px via media query
- **Sem dependências externas**: apenas Django e sua biblioteca padrão
- **Sem JavaScript frameworks**: JS puro para o toggle de senha

---

## Funcionalidades fora do escopo atual

- Dashboard pós-login (atualmente redireciona para `/admin/`)
- Autenticação social (Google, GitHub, etc.)
- Autenticação por e-mail (sem username)
- Perfil de usuário (alterar nome, foto, e-mail)
- Verificação de e-mail no cadastro
- Rate limiting em tentativas de login
- 2FA (autenticação de dois fatores)

---

## Fluxo completo do usuário

```
Acessa /
    │
    ├─ [Tem conta] Preenche usuário + senha
    │     ├─ Válido   → /admin/
    │     └─ Inválido → mensagem de erro na mesma tela
    │
    ├─ [Sem conta] Clica "Cadastre-se" → /cadastro/
    │     ├─ Formulário válido → auto-login → /admin/
    │     └─ Erro (usuário já existe, senhas divergem, senha fraca)
    │           └─ Erros exibidos por campo, formulário mantém valores
    │
    └─ [Esqueceu a senha] Clica "Esqueceu a senha?" → /senha/
          └─ Informa e-mail → /senha/enviado/
                └─ Abre link do e-mail → /senha/confirmar/<uid>/<token>/
                      ├─ Token válido  → digita nova senha → /senha/concluido/
                      │     └─ Link "Ir para o login" → /
                      └─ Token inválido → "Link expirado" + link para nova solicitação
```
