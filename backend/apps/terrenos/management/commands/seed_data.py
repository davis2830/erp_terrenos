"""
Management command to seed demo data for the ERP Terrenos system.
Creates sample projects, lots, users, and map data.
"""
import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.mapa.models import CoordenadaLote, MapaProyecto
from apps.terrenos.models import Lote, Proyecto

User = get_user_model()

MANZANAS = {
    "A": [
        ("A-01", Decimal("10.00"), Decimal("20.00")),
        ("A-02", Decimal("10.00"), Decimal("20.00")),
        ("A-03", Decimal("10.00"), Decimal("20.00")),
        ("A-04", Decimal("10.00"), Decimal("20.00")),
        ("A-05", Decimal("12.00"), Decimal("20.00")),
        ("A-06", Decimal("12.00"), Decimal("20.00")),
        ("A-07", Decimal("10.00"), Decimal("25.00")),
        ("A-08", Decimal("10.00"), Decimal("25.00")),
        ("A-09", Decimal("10.00"), Decimal("25.00")),
        ("A-10", Decimal("10.00"), Decimal("25.00")),
        ("A-11", Decimal("12.00"), Decimal("25.00")),
        ("A-12", Decimal("12.00"), Decimal("25.00")),
    ],
    "B": [
        ("B-01", Decimal("10.00"), Decimal("20.00")),
        ("B-02", Decimal("10.00"), Decimal("20.00")),
        ("B-03", Decimal("10.00"), Decimal("20.00")),
        ("B-04", Decimal("10.00"), Decimal("20.00")),
        ("B-05", Decimal("10.00"), Decimal("20.00")),
        ("B-06", Decimal("10.00"), Decimal("20.00")),
        ("B-07", Decimal("12.00"), Decimal("20.00")),
        ("B-08", Decimal("12.00"), Decimal("20.00")),
        ("B-09", Decimal("12.00"), Decimal("20.00")),
        ("B-10", Decimal("12.00"), Decimal("20.00")),
    ],
    "C": [
        ("C-01", Decimal("15.00"), Decimal("25.00")),
        ("C-02", Decimal("15.00"), Decimal("25.00")),
        ("C-03", Decimal("15.00"), Decimal("25.00")),
        ("C-04", Decimal("15.00"), Decimal("25.00")),
        ("C-05", Decimal("15.00"), Decimal("25.00")),
        ("C-06", Decimal("15.00"), Decimal("25.00")),
        ("C-07", Decimal("12.00"), Decimal("30.00")),
        ("C-08", Decimal("12.00"), Decimal("30.00")),
    ],
    "D": [
        ("D-01", Decimal("10.00"), Decimal("20.00")),
        ("D-02", Decimal("10.00"), Decimal("20.00")),
        ("D-03", Decimal("10.00"), Decimal("20.00")),
        ("D-04", Decimal("10.00"), Decimal("20.00")),
        ("D-05", Decimal("10.00"), Decimal("20.00")),
        ("D-06", Decimal("10.00"), Decimal("20.00")),
        ("D-07", Decimal("10.00"), Decimal("20.00")),
        ("D-08", Decimal("10.00"), Decimal("20.00")),
        ("D-09", Decimal("12.00"), Decimal("25.00")),
        ("D-10", Decimal("12.00"), Decimal("25.00")),
    ],
}


def _generate_svg_coords(manzana_key, lot_index, total_in_mz):
    """Generate SVG polygon coordinates for a lot within a manzana grid."""
    mz_offsets = {"A": (50, 50), "B": (420, 50), "C": (50, 350), "D": (420, 350)}
    ox, oy = mz_offsets.get(manzana_key, (50, 50))

    cols = 4 if total_in_mz <= 12 else 5
    row = lot_index // cols
    col = lot_index % cols
    w, h = 80, 55
    gap = 5
    x = ox + col * (w + gap)
    y = oy + row * (h + gap)
    return f"{x},{y} {x + w},{y} {x + w},{y + h} {x},{y + h}"


class Command(BaseCommand):
    help = "Seed demo data: users, projects, lots, and map coordinates."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing data before seeding.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing data...")
            CoordenadaLote.objects.all().delete()
            MapaProyecto.objects.all().delete()
            Lote.objects.all().delete()
            Proyecto.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self._create_users()
        proyecto = self._create_proyecto()
        lotes = self._create_lotes(proyecto)
        self._create_mapa(proyecto, lotes)

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))

    def _create_users(self):
        if not User.objects.filter(email="admin@gctorque.com").exists():
            User.objects.create_superuser(
                email="admin@gctorque.com",
                username="admin",
                password="Admin123!",
                first_name="Carlos",
                last_name="López",
                role="admin",
                phone="502 5555-0001",
            )
            self.stdout.write("  Created admin user: admin@gctorque.com / Admin123!")

        users_data = [
            {
                "email": "gerente@gctorque.com",
                "username": "gerente",
                "first_name": "María",
                "last_name": "García",
                "role": "gerente",
                "phone": "502 5555-0002",
            },
            {
                "email": "vendedor1@gctorque.com",
                "username": "vendedor1",
                "first_name": "Juan",
                "last_name": "Pérez",
                "role": "vendedor",
                "phone": "502 5555-0003",
            },
            {
                "email": "vendedor2@gctorque.com",
                "username": "vendedor2",
                "first_name": "Ana",
                "last_name": "Martínez",
                "role": "vendedor",
                "phone": "502 5555-0004",
            },
        ]

        for data in users_data:
            if not User.objects.filter(email=data["email"]).exists():
                user = User(**data)
                user.set_password("Demo123!")
                user.save()
                self.stdout.write(f"  Created user: {data['email']} / Demo123!")

    def _create_proyecto(self):
        proyecto, created = Proyecto.objects.get_or_create(
            nombre="Residencial Las Flores",
            defaults={
                "ubicacion": "Km 485, carretera a Flores, Petén",
                "departamento": "Petén",
                "municipio": "Flores",
                "descripcion": (
                    "Proyecto residencial con 40 lotes distribuidos en 4 manzanas. "
                    "Acceso pavimentado, agua potable, drenaje y energía eléctrica. "
                    "A 10 minutos del centro de Flores."
                ),
                "coordenadas_lat": Decimal("16.9306300"),
                "coordenadas_lng": Decimal("-89.8924900"),
                "area_total": Decimal("12500.00"),
            },
        )
        if created:
            self.stdout.write("  Created project: Residencial Las Flores")
        return proyecto

    def _create_lotes(self, proyecto):
        all_lotes = []
        estados = [Lote.Estado.DISPONIBLE, Lote.Estado.RESERVADO, Lote.Estado.VENDIDO]
        pesos = [0.50, 0.20, 0.30]

        for mz_key, lotes_data in MANZANAS.items():
            for numero, frente, fondo in lotes_data:
                area = frente * fondo
                precio = area * Decimal("850.00")

                lote, created = Lote.objects.get_or_create(
                    proyecto=proyecto,
                    manzana=mz_key,
                    numero=numero,
                    defaults={
                        "medida_frente": frente,
                        "medida_fondo": fondo,
                        "area_total": area,
                        "precio_base": precio,
                        "estado": random.choices(estados, weights=pesos, k=1)[0],
                        "num_finca": f"F-{random.randint(1000, 9999)}",
                        "folio": f"{random.randint(100, 999)}",
                        "libro": f"L-{random.randint(1, 50)}",
                    },
                )
                all_lotes.append(lote)

        self.stdout.write(f"  Created/loaded {len(all_lotes)} lots")
        return all_lotes

    def _create_mapa(self, proyecto, lotes):
        mapa, _ = MapaProyecto.objects.get_or_create(
            proyecto=proyecto,
            defaults={
                "svg_data": "",
                "configuracion_colores": {
                    "disponible": "#22c55e",
                    "reservado": "#f59e0b",
                    "vendido": "#ef4444",
                },
                "ancho": 800,
                "alto": 600,
            },
        )

        lotes_by_mz = {}
        for lote in lotes:
            lotes_by_mz.setdefault(lote.manzana, []).append(lote)

        created_count = 0
        for mz_key, mz_lotes in lotes_by_mz.items():
            for idx, lote in enumerate(mz_lotes):
                _, was_created = CoordenadaLote.objects.get_or_create(
                    mapa=mapa,
                    lote=lote,
                    defaults={
                        "svg_path": _generate_svg_coords(
                            mz_key, idx, len(mz_lotes)
                        ),
                    },
                )
                if was_created:
                    created_count += 1

        self.stdout.write(f"  Created map with {created_count} lot coordinates")
