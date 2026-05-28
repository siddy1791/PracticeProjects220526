from sqlalchemy import create_engine, text

def seed_database():
    db_url = "postgresql+psycopg2://admin:postgres123@localhost:5432/project1"
    engine = create_engine(db_url)


    create_table_sql = """
                    CREATE TABLE IF NOT EXISTS orders(
                    order_id varchar(50),
                    customer_id varchar(30),
                    order_date DATE,
                    total_amount NUMERIC(10,2),
                    status VARCHAR(50));
    """
    records = []
    # 1. VALID BASELINE RECORDS (Rows 1 to 60)
    # Standard, clean transactions to build a normal data distribution
    for i in range(1, 61):
        records.append(
            f"('B_{1000+i}', 'C_{i:02d}', '2026-01-01', {50.00 + (i * 2.5):.2f}, 'COMPLETED')" #Valid Baseline
        )

    # 2. NULL TEST CASES (Rows 61 to 70)
    # Missing amounts or missing statuses to test data completeness and imputation
    for i in range(61, 71):
        # Alternating between missing amount and missing status
        if i % 2 == 0:
            records.append(
                f"('N_{1000+i}', 'C_{i:02d}', '2026-01-02', NULL, 'PENDING')"  # NULL Amount Test
            )
        else:
            records.append(
                f"('N_{1000+i}', 'C_{i:02d}', '2026-01-02', {25.00:.2f}, NULL)"  #NULL Status Test
            )

    # 3. NEGATIVE VALUES (Rows 71 to 80)
    # Testing boundary limits and business logic around refunds/chargebacks
    for i in range(71, 81):
        records.append(
            f"('V_{1000+i}', 'C_{i:02d}', '2026-01-03', {-10.00 * (i-70):.2f}, 'REFUNDED')"  #Negative Value Test
        )

    # 4. DUPLICATES (Rows 81 to 90)
    # 5 pairs of exact duplicate rows to test primary key violations or deduplication pipelines
    for i in range(81, 86):
        dup_row = f"('D_{1000+i}', 'C_{i:02d}', '2026-01-04', 199.99, 'COMPLETED')"  #Duplicate Pair
        records.append(dup_row)  # First copy
        records.append(dup_row)  # Second copy

    # 5. STATISTICAL OUTLIERS (Rows 91 to 100)
    # Massive order amounts and extreme date ranges to test anomaly detection or skewness
    for i in range(91, 101):
        if i % 2 == 0:
            records.append(
                f"('O_{1000+i}', 'C_{i:02d}', '2026-01-05', {50000.00 + (i*500):.2f}, 'COMPLETED')"    #Outlier: Extreme Amount
            )
        else:
            # Outlier: Date far into the past/future
            records.append(
                f"('O_{1000+i}', 'C_{i:02d}', '1970-01-01', 45.00, 'COMPLETED')"  #Outlier: Legacy Date
            )

    # Combine everything into the final SQL string
    insert_data_sql = """
    INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
    VALUES 
        {values};""".format(values=",\n        ".join(records))
    print("Connecting to database to seed test data")
    with engine.connect() as conn:
        # clear out old records if run multiple times
        conn.execute(text("DROP TABLE IF EXISTS orders;"))

        # Create table and insert rows
        conn.execute(text(create_table_sql))
        conn.execute(text(insert_data_sql))

        # In SQLAlchemy 2.0, changes must be explicitly committed!
        conn.commit()

    print("Data seeded with intended anamolies")


if __name__=="__main__":
    seed_database()

