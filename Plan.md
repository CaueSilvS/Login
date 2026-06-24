# Plan.md — Plano Técnico de Implementação

Este documento registra as decisões de arquitetura tomadas e serve de referência para evoluções futuras.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Django 6.x (Python) |
| Banco de dados | SQLite3 (desenvolvimento) |
| Frontend | HTML5, CSS3, JavaScript puro |
| Autenticação | `django.contrib.auth` (nativo) |
| E-mail (dev) | `console` backend |
| E-mail (prod) | SMTP (a configurar) |

---

## Estrutura de arquivos — estado atual

```
d:\Users\aprendiz.ti\dev\Login\
├── CLAUDE.md
├── PRD.md
├── Plan.md
├── manage.py
├── db.sqlite3
├── raiz/
│   ├── settings.py
│   ├── urls.py          → inclui Login.urls em /
│   ├── wsgi.py
│   └── asgi.py
└── Login/
    ├── apps.py
    ├── forms.py          → CadastroForm
    ├── views.py          → login_view, cadastro_view, logout_view
    ├── urls.py           → 7 rotas
    ├── models.py         → vazio (usa User padrão do Django)
    ├── static/
    │   ├── css/login.css
    │   └── js/login.js
    └── templates/
        ├── base.html
        ├── login.html
        ├── cadastro.html
        ├── logout_confirm.html
        └── registration/
            ├── password_reset_form.html
            ├── password_reset_done.html
            ├── password_reset_confirm.html
            ├── password_reset_complete.html
            ├── password_reset_email.html
            └── password_reset_subject.txt
```

---

## Mapa de URLs

| URL | View | Nome | Método |
|---|---|---|---|
| `/` | `login_view` | `login` | GET, POST |
| `/cadastro/` | `cadastro_view` | `cadastro` | GET, POST |
| `/sair/` | `logout_view` | `logout` | GET (confirmação), POST |
| `/senha/` | `PasswordResetView` | `password_reset` | GET, POST |
| `/senha/enviado/` | `PasswordResetDoneView` | `password_reset_done` | GET |
| `/senha/confirmar/<uidb64>/<token>/` | `PasswordResetConfirmView` | `password_reset_confirm` | GET, POST |
| `/senha/concluido/` | `PasswordResetCompleteView` | `password_reset_complete` | GET |
| `/admin/` | Django Admin | — | — |

---

## Decisões de arquitetura

### Por que não usar `django.contrib.auth.urls`?
As URLs nativas do Django usam slugs em inglês (`/password_reset/`, `/password_reset/done/`, etc.). Optamos por URLs em português (`/senha/`, `/senha/enviado/`) registrando manualmente os CBVs com `template_name` e `success_url` customizados.

### Por que `AuthenticationForm` em vez de form customizado?
`AuthenticationForm(request, data=request.POST)` já chama `authenticate()` internamente, valida credenciais e retorna o usuário via `get_user()`. Não há ganho em reescrever isso.

### Por que `UserCreationForm` e não form do zero?
`UserCreationForm` já implementa: campos `password1`/`password2` com validação de correspondência, todos os `AUTH_PASSWORD_VALIDATORS` do settings, verificação de username único. Só precisamos adicionar o campo `email`.

### Por que `LANGUAGE_CODE = 'pt-br'`?
Ativa as traduções nativas do Django, fazendo com que os labels do `UserCreationForm` e as mensagens de erro dos `AUTH_PASSWORD_VALIDATORS` apareçam em português sem precisar sobrescrever cada label manualmente.

### Por que logout exige POST?
Logout via GET é vulnerável a CSRF passivo (um link externo pode deslogar o usuário). O formulário POST com `{% csrf_token %}` protege contra isso.

### Por que `<div>`/`<p>` em vez de `<ul>`/`<li>` nos erros?
Linters HTML (incluindo o do VS Code) não entendem tags Django `{% for %}` dentro de `<ul>` e geram avisos de "List element has direct children that are not allowed". O comportamento renderizado é idêntico.

### Por que `id="id_password"` e não `id="password"` no input?
Django nomeia inputs como `id_<fieldname>` por convenção. O `login.js` foi corrigido para usar `getElementById('id_password')` — a versão anterior buscava `'password'` e o toggle nunca funcionava.

---

## Configurações-chave em `raiz/settings.py`

```python
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@painel.local'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/admin/'   # trocar quando houver dashboard
```

---

## Herança de templates

```
base.html
├── login.html
├── cadastro.html
├── logout_confirm.html
└── registration/
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    └── password_reset_complete.html
```

`base.html` define três blocos:
- `{% block title %}` — título da aba do navegador
- `{% block body %}` — conteúdo visual da página
- `{% block extra_js %}` — scripts carregados ao final do `<body>`

---

## Arquitetura CSS

Um único arquivo `login.css` com dois sistemas visuais coexistentes:

### Sistema 1 — Card branco (tela de login `/`)

| Classe | Papel |
|---|---|
| `.login-page` | Wrapper fullscreen, fundo `#3d3d3d`, flex column centralizado |
| `.brand` | Nome do sistema acima do card |
| `.login-card` | Card branco, `box-shadow`, `border-radius: 6px`, `width: 420px` |
| `.card-title` | Título "Acesse sua conta" dentro do card |
| `.input-icon-wrapper` | Flex row com ícone SVG à esquerda + input + toggle à direita |
| `.input-icon` | Ícone posicionado absoluto, `left: 12px` |
| `.form-row` | Flex row com `justify-content: space-between` — checkbox + botão |
| `.remember-label` | Label clicável do checkbox "Lembrar Senha" |
| `.card-links` | Área de links abaixo do formulário |
| `.card-link` | Link individual (cinza → vermelho `#911919` no hover) |
| `.page-footer` | Rodapé abaixo do card, texto branco semitransparente |

### Sistema 2 — Caixa vermelha (demais páginas)

| Classe | Papel |
|---|---|
| `.login` | Wrapper fullscreen, fundo `rgb(0,0,0)`, flex centralizado |
| `.login-background` | Caixa `rgba(145,25,25,0.85)`, `border-radius: 10px`, `450×550px` |
| `.form-group` | Grupo label + input, `margin-bottom: 20px` |
| `.password-wrapper` | Wrapper relativo para toggle de senha |
| `.toggle-password` | Botão SVG posicionado absoluto, `right: 12px` |
| `.forgot-password` | Link "Esqueceu a senha?" — branco semitransparente |
| `.auth-link` | Link secundário genérico |
| `.cadastro-box` | Modificador de `.login-background` — `height: auto` |
| `.form-errors` | Erros por campo — `#ff6b6b` |
| `.non-field-errors` | Erros gerais do formulário — `#ff6b6b` |
| `.message-box` | Caixa de mensagem informativa (reset enviado, concluído) |

### Paleta de cores

| Elemento | Cor |
|---|---|
| Fundo Sistema 1 | `#3d3d3d` — cinza escuro |
| Fundo Sistema 2 | `rgb(0, 0, 0)` — preto |
| Caixa Sistema 2 | `rgba(145, 25, 25, 0.85)` — baseado em `#911919` |
| Botão | `#C77C48` — laranja-terra |
| Botão hover | `#a8622d` |
| Focus ring inputs | `rgba(199, 124, 72, 0.4)` — baseado em `#C77C48` |
| Link hover / erros no card | `#911919` — vermelho escuro |
| Erros nas caixas vermelhas | `#ff6b6b` — vermelho claro |

### Fonte

`'Calibri', sans-serif` em todo o arquivo.

### Seções do arquivo `login.css`

1. **Reset global** — `* { margin: 0; padding: 0; box-sizing: border-box }`
2. **Sistema 2 — Layout** — `.login`, `.login-background`
3. **Sistema 2 — Formulário** — `.form-group`, `label`, `input`, `button`
4. **Toggle de senha (Sistema 2)** — `.password-wrapper`, `.toggle-password`
5. **Links (Sistema 2)** — `.forgot-password`, `.auth-link`
6. **Modificadores (Sistema 2)** — `.cadastro-box`
7. **Feedback** — `.form-errors`, `.non-field-errors`, `.message-box`
8. **Responsivo (Sistema 2)** — `@media (max-width: 600px)`
9. **Sistema 1 — Card de login** — `.login-page`, `.brand`, `.login-card`, `.form-row`, etc.
10. **Responsivo (Sistema 1)** — `@media (max-width: 500px)`

---

## Próximo passo sugerido: Dashboard

O redirect pós-login aponta para `/admin/` como placeholder. Para criar um dashboard real:

1. Criar `dashboard_view` em `Login/views.py` com `@login_required`
2. Adicionar rota `/dashboard/` em `Login/urls.py`
3. Criar `Login/templates/dashboard.html` estendendo `base.html`
4. Atualizar `LOGIN_REDIRECT_URL = '/dashboard/'` em `settings.py`
5. Atualizar os `redirect('/admin/')` em `views.py` para `redirect('dashboard')`

---

## Como configurar e-mail SMTP para produção

Substituir em `raiz/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.seudominio.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seuemail@dominio.com'
EMAIL_HOST_PASSWORD = 'suasenha'          # usar variável de ambiente
DEFAULT_FROM_EMAIL = 'seuemail@dominio.com'
```

Nunca commitar `EMAIL_HOST_PASSWORD` diretamente — usar `python-decouple` ou variáveis de ambiente do servidor.
