# CLAUDE.md — Guia para o Assistente

Este arquivo instrui o Claude sobre como trabalhar neste projeto. Leia antes de qualquer tarefa.

---

## Projeto

Sistema de autenticação web construído com Django 6.x (backend) e HTML/CSS/JS puro (frontend). O projeto chama-se `raiz` internamente e contém um único app Django chamado `Login`.

---

## Como rodar

```bash
# Ativar o ambiente virtual (Windows)
.\venv\Scripts\activate

# Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse em `http://127.0.0.1:8000/`

---

## Estrutura do projeto

```
Login/                        # App Django principal
├── forms.py                  # CadastroForm (UserCreationForm + email)
├── views.py                  # login_view, cadastro_view, logout_view
├── urls.py                   # 7 rotas — ver PRD.md
├── static/
│   ├── css/login.css         # Único arquivo CSS — tema escuro, vermelho
│   └── js/login.js           # Toggle de visibilidade de senha
└── templates/
    ├── base.html             # Layout compartilhado (head, blocks)
    ├── login.html
    ├── cadastro.html
    ├── logout_confirm.html
    └── registration/         # Templates de reset de senha do Django
        ├── password_reset_form.html
        ├── password_reset_done.html
        ├── password_reset_confirm.html
        ├── password_reset_complete.html
        ├── password_reset_email.html   # Corpo do e-mail (texto puro)
        └── password_reset_subject.txt  # Assunto do e-mail

raiz/
├── settings.py               # Configurações principais
└── urls.py                   # Inclui Login.urls na raiz /
```

---

## Convenções do projeto

### Backend
- Usar `django.contrib.auth` nativo — não instalar pacotes externos de autenticação.
- Views como funções (FBV), não class-based, exceto os CBVs de reset de senha que vêm do Django.
- Formulários em `Login/forms.py`; nunca misturar lógica de formulário dentro das views.
- Redirecionamento após login aponta para `/admin/` — esse é o placeholder atual até existir um dashboard.

### Frontend
- **Um único arquivo CSS**: `login.css`. Adicionar novos estilos ao final, nunca criar arquivos CSS extras.
- Todas as páginas estendem `base.html` via `{% extends 'base.html' %}`.
- Carregar JS no bloco `{% block extra_js %}` ao final do `<body>`, nunca no `<head>`.
- Erros de formulário: usar `<div class="form-errors">` (não `<ul>`) para compatibilidade com linters HTML que não entendem tags Django dentro de listas.
- Classes CSS existentes a reutilizar: `.login`, `.login-background`, `.form-group`, `.password-wrapper`, `.toggle-password`, `.forgot-password`, `.auth-link`, `.form-errors`, `.non-field-errors`, `.message-box`, `.cadastro-box`.

### Tema visual
- Fundo: `rgb(0, 0, 0)` (preto)
- Caixa do formulário: `rgba(187, 0, 0, 0.473)` (vermelho semitransparente)
- Texto: branco
- Erros: `#ff6b6b` (vermelho claro)
- Fonte: Arial, sans-serif
- Manter esse tema em qualquer nova tela.

---

## Settings relevantes

| Chave | Valor atual | Observação |
|---|---|---|
| `LANGUAGE_CODE` | `pt-br` | Traduz labels do Django automaticamente |
| `TIME_ZONE` | `America/Sao_Paulo` | — |
| `EMAIL_BACKEND` | `console` | E-mails aparecem no terminal do `runserver` |
| `LOGIN_URL` | `/` | Redireciona usuários não autenticados para o login |
| `LOGIN_REDIRECT_URL` | `/admin/` | Placeholder — trocar quando houver dashboard |

---

## O que NÃO fazer

- Não instalar pacotes de autenticação de terceiros (django-allauth, rest-framework-simplejwt, etc.) — o projeto usa apenas `django.contrib.auth`.
- Não criar arquivos CSS separados por página — tudo vai em `login.css`.
- Não substituir o `login.css` inteiro — apenas appends ao final.
- Não usar `<ul>`/`<li>` dentro de blocos `{% for %}` em templates — usar `<div>`/`<p>`.
- Não colocar `<script>` no `<head>` sem `defer`.
- Não criar um modelo de usuário customizado sem discutir com o usuário primeiro — o projeto usa o `User` padrão do Django.
- Não usar `DEBUG=False` nem `ALLOWED_HOSTS` restrito sem discutir com o usuário.

---

## Próximos passos conhecidos (ver PRD.md)

- Criar um dashboard básico para substituir o redirect para `/admin/`
- Configurar SMTP real para envio de e-mails em produção
- Adicionar `DEFAULT_AUTO_FIELD` ao settings para suprimir aviso do Django
