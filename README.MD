# 🎬 WatchBook

Catálogo pessoal de filmes e séries assistidos. Gerencie suas obras favoritas, avalie, escreva críticas e compartilhe com amigos.

## 📋 Sobre

Sistema completo para catalogar e acompanhar filmes e séries assistidos, com funcionalidades sociais para conectar-se com amigos e visualizar seus registros.

**Tecnologias:**
- Backend: Django + Django REST Framework
- Frontend Web: Django Templates + Bootstrap
- Mobile: Ionic + Angular + Capacitor

## 🚀 Início Rápido

### Backend (Django)

```bash
# Criar e ativar ambiente virtual
python -m venv virtual
source virtual/bin/activate  # Linux/Mac
# ou
virtual\Scripts\activate  # Windows

# Instalar dependências
cd watchbook
pip install -r requirements.txt

# Configurar banco de dados
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

**Acesse:** `http://127.0.0.1:8000`

### Mobile (Ionic)

```bash
cd watchbook-mobile

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
ionic serve
```

**Acesse:** `http://localhost:8100`

## 📱 Funcionalidades

### Web
- ✅ Autenticação de usuários
- ✅ Catálogo de filmes e séries
- ✅ Busca e filtros por tipo
- ✅ Registrar obras assistidas
- ✅ Sistema de avaliação (estrelas)
- ✅ Críticas pessoais
- ✅ Gestão de amizades
- ✅ Visualizar registros de amigos

### Mobile
- ✅ Login e cadastro
- ✅ Visualizar catálogo
- ✅ Meus registros com filtros
- ✅ Buscar e adicionar amigos
- ✅ Gerenciar convites (aceitar/rejeitar)
- ✅ Ver registros de amigos

## 🔌 API Endpoints

### Autenticação
```
POST /api/auth/login/     - Login
POST /api/auth/logout/    - Logout
```

### Usuários
```
GET    /api/usuarios/              - Listar usuários
POST   /api/usuarios/              - Criar usuário
GET    /api/usuarios/{id}/         - Detalhe do usuário
GET    /api/usuarios/{id}/registros/ - Registros do usuário
```

### Catálogo
```
GET    /api/catalogo/              - Listar obras
GET    /api/catalogo/{id}/         - Detalhe da obra
GET    /api/catalogo/?tipo=filme   - Filtrar por tipo
GET    /api/catalogo/?search=term  - Buscar obras
```

### Registros
```
GET    /api/registros/             - Meus registros
POST   /api/registros/             - Criar registro
PUT    /api/registros/{id}/        - Editar registro
DELETE /api/registros/{id}/        - Deletar registro
```

### Amizades
```
GET    /api/amizades/              - Minhas amizades
POST   /api/amizades/              - Enviar convite
PUT    /api/amizades/{id}/         - Aceitar convite
DELETE /api/amizades/{id}/         - Recusar/Remover
```

## 📂 Estrutura

```
watchbook-project/
├── watchbook/              # Backend Django
│   ├── catalogo/          # App de obras
│   ├── usuarios/          # App de usuários e registros
│   ├── amizade/           # App de amizades
│   ├── templates/         # Templates web
│   └── media/             # Uploads (posters)
│
├── watchbook-mobile/      # App mobile Ionic
│   └── src/
│       └── app/
│           ├── login/
│           ├── cadastro/
│           ├── catalogo/
│           ├── registros/
│           ├── amigos/
│           └── components/
│
└── virtual/               # Ambiente virtual Python
```

## 🛠️ Configuração

### Backend

Edite `watchbook/settings.py` para configurar:
- Banco de dados
- CORS (permitir mobile)
- Media files (posters)

### Mobile

Edite `watchbook-mobile/src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:8000/api'
};
```

## 📦 Dependências Principais

**Backend:**
- Django 5.1.3
- djangorestframework
- django-cors-headers
- Pillow

**Mobile:**
- @ionic/angular
- @capacitor/core
- @ionic/storage-angular
