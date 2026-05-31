# Deploy gratuito: Vercel + Supabase

Este guia coloca o ecommerce online sem cartao, usando Vercel para o Flask e Supabase para PostgreSQL.

## 1. Banco no Supabase

1. No Supabase, abra o projeto.
2. Va em **Connect**.
3. Copie a connection string do **Shared Pooler**.
4. Troque `[YOUR-PASSWORD]` pela senha do banco.

Formato esperado:

```text
postgresql://postgres.PROJECT_REF:SENHA@aws-1-us-east-1.pooler.supabase.com:5432/postgres
```

Se a senha tiver caracteres especiais como `@`, `#`, `%`, `/`, `?` ou `:`, redefina a senha para uma senha forte so com letras e numeros.

## 2. Importar o backup

No PowerShell, dentro da pasta do projeto:

```powershell
pg_restore --clean --if-exists --no-owner --no-acl -d "DATABASE_URL_DO_SUPABASE" backup_render.dump
```

Se `pg_restore` nao estiver instalado, use o SQL Editor do Supabase ou instale o PostgreSQL localmente.

## 3. Subir para o GitHub

Antes do commit, confira que `.env`, backups, logs, comprovantes e fotos privadas nao serao enviados.

```powershell
git status
git add .
git commit -m "Prepare deploy gratuito Vercel Supabase"
git push origin main
```

## 4. Criar o projeto na Vercel

1. Acesse `https://vercel.com`.
2. Entre com GitHub.
3. Clique em **Add New > Project**.
4. Importe o repositorio do ecommerce.
5. Framework Preset: **Other**.
6. Build Command: deixe vazio.
7. Output Directory: deixe vazio.
8. Install Command: `pip install -r requirements.txt`.
9. Clique em **Environment Variables**.

## 5. Variaveis de ambiente

Configure:

```text
APP_ENV=production
DEBUG=False
SECRET_KEY=gere_uma_chave_forte
DATABASE_URL=connection_string_do_supabase
RUN_MIGRATIONS_ON_START=False
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=Lax
MAX_CONTENT_LENGTH=5242880
UPLOAD_FOLDER=/tmp/uploads
DB_POOL_MIN=1
DB_POOL_MAX=1
RATE_LIMIT_DEFAULT=240
RATE_LIMIT_WINDOW_SECONDS=60
```

Para gerar `SECRET_KEY`:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## 6. Deploy

Clique em **Deploy**.

Depois teste:

```text
/
/produtos
/carrinho
/login
/admin
```

## Observacoes importantes

- Vercel serverless nao tem disco persistente. Uploads feitos pelo painel podem funcionar temporariamente, mas podem sumir.
- Imagens publicas versionadas em `static/uploads` sobem junto com o projeto.
- Nao envie `static/uploads/perfis` nem `static/uploads/comprovantes` para o GitHub.
- Para vender de verdade, o proximo passo e mover uploads para Supabase Storage ou Cloudinary.
