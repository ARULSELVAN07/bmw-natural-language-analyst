from .database_setup import create_database
from .warehouse_setup import create_warehouse
from .schema_setup import create_schema
from .table_setup import create_tables
from .data_setup import load_all_data
from .security_setup import setup_security


def bootstrap():

    print("=" * 60)
    print("BMW NATURAL LANGUAGE ANALYST - BOOTSTRAP")
    print("=" * 60)

    print("\n[1/6] Creating database...")
    create_database()

    print("\n[2/6] Creating warehouse...")
    create_warehouse()

    print("\n[3/6] Creating schema...")
    create_schema()

    print("\n[4/6] Creating tables...")
    create_tables()

    print("\n[5/6] Loading sample data...")
    load_all_data()

    print("\n[6/6] Configuring security...")
    setup_security()

    print("\n" + "=" * 60)
    print("BOOTSTRAP COMPLETED SUCCESSFULLY")
    print("=" * 60)