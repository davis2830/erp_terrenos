# ERP Terrenos - Sistema Inmobiliario de Ventas (GCtorque)

Plataforma digital centralizada (Web/Móvil) para el control total del inventario de terrenos en Petén, Guatemala. Gestiona pagos, facturación y reportes estadísticos en tiempo real.

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| **Backend** | Python 3.12 + Django 5.1 + Django REST Framework |
| **Base de datos** | PostgreSQL 16 con PostGIS |
| **Frontend (Admin)** | React 18 + TypeScript + Vite + Tailwind CSS |
| **Cache / Broker** | Redis 7 |
| **Tareas asíncronas** | Celery |
| **Notificaciones** | Twilio (WhatsApp / SMS) |
| **Facturación** | Integración FEL / SAT Guatemala |

## Módulos

1. **Seguridad y Accesos** - Login JWT, roles (Admin, Gerente, Vendedor)
2. **Inventario de Terrenos** - Ficha técnica, estado en tiempo real, multimedia
3. **Mapa Interactivo** - Visualizador SVG con colores por estado
4. **CRM y Ventas** - Directorio de clientes, reservas, WhatsApp
5. **Cartera y Financiamiento** - Planes de pago, amortización, mora
6. **Facturación y Documentos** - FEL/SAT, bóveda legal, contratos
7. **Dashboard y Estadísticas** - Métricas, flujo de caja, KPIs
8. **Notificaciones** - WhatsApp/SMS vía Twilio

## Estructura del Proyecto

```
erp_terrenos/
├── backend/                # Django + DRF
│   ├── config/             # Configuración (settings, urls, wsgi)
│   ├── apps/               # Módulos de la aplicación
│   │   ├── accounts/       # Auth y usuarios
│   │   ├── terrenos/       # Inventario de lotes
│   │   ├── mapa/           # Mapa interactivo SVG
│   │   ├── crm/            # Clientes y reservas
│   │   ├── finanzas/       # Pagos y amortización
│   │   ├── facturacion/    # FEL y documentos
│   │   ├── reportes/       # Dashboard y KPIs
│   │   └── notificaciones/ # WhatsApp/SMS
│   ├── utils/              # Utilidades compartidas
│   └── requirements/       # Dependencias por entorno
├── frontend/               # React + TypeScript + Vite
│   └── src/
│       ├── api/            # Cliente HTTP y endpoints
│       ├── components/     # Componentes (layout, UI, shared)
│       ├── pages/          # Páginas por módulo
│       ├── hooks/          # Custom hooks
│       ├── store/          # Estado global (Zustand)
│       ├── types/          # Interfaces TypeScript
│       └── utils/          # Helpers
├── docs/                   # Documentación y mockups
├── docker-compose.yml      # PostgreSQL + Redis (dev)
└── .env.example            # Variables de entorno
```

## Requisitos Previos

- Python 3.12+
- Node.js 20+
- PostgreSQL 16+ con PostGIS
- Redis 7+
- Docker y Docker Compose (opcional, recomendado)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/davis2830/erp_terrenos.git
cd erp_terrenos
```

### 2. Levantar servicios con Docker

```bash
docker-compose up -d
```

### 3. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
cp ../.env.example .env  # Configurar variables
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 4. Frontend

```bash
cd frontend
npm install
cp .env.example .env  # Configurar API URL
npm run dev
```

## Variables de Entorno

Copiar `.env.example` y configurar las credenciales necesarias. Ver el archivo para la lista completa.

## Fases de Desarrollo

- **Fase 1 (MVP):** Auth + Inventario de Terrenos + Mapa Interactivo
- **Fase 2:** CRM + Ventas + Reservas
- **Fase 3:** Pagos + Financiamiento + Cobranza
- **Fase 4:** FEL + Documentos + Contratos
- **Fase 5:** Dashboard + Estadísticas + Observabilidad

## Licencia

Proyecto privado - GCtorque © 2026
