from app.db.base import SessionLocal
from app.models import Company, Corporation, Department, RoleTitle


def start_up_event():
    db = SessionLocal()
    update_increment_key(db=db, table='company')
    update_increment_key(db=db, table='corporation')
    update_increment_key(db=db, table='department')
    update_increment_key(db=db, table='role_title')

    # create default corporation
    pv_vnshop_ka = create_coporation(db, 'PV-Vnshop_KA')

    VNNG = create_coporation(db, 'VNNG')

    # create default company
    PhongVu = create_company(db=db, name='Phong Vũ', corporation=pv_vnshop_ka)
    VnShop = create_company(db=db, name='VnShop', corporation=pv_vnshop_ka)
    Karavan = create_company(db=db, name='Karavan', corporation=pv_vnshop_ka)
    Digilife = create_company(db=db, name='Digilife', corporation=pv_vnshop_ka)
    VNNG_company = create_company(db=db, name='VNNG', corporation=VNNG)

    SaleDepartment = create_company(
        db=db, name='Sale Department', corporation=VNNG)

    # create default department 

    sale_department = create_department(db=db, name="Sale Dapartment", company=VNNG_company)

    # role_title
    sale = create_role_title(db=db, name="Sale", department=sale_department, company=VNNG_company)
    sale_admin = create_role_title(db=db, name="Sale Admin", department=sale_department, company=VNNG_company)
    sale_leader = create_role_title(db=db, name="Sale Leader", department=sale_department, company=VNNG_company)
    sale_manager = create_role_title(db=db, name="Sale Manager", department=sale_department, company=VNNG_company)
    admin = create_role_title(db=db, name="Administrator", department=sale_department, company=VNNG_company)


def update_increment_key(db, table):
    connection = db.connection()
    connection.engine.execute(f"SELECT MAX(id) FROM {table};")
    connection.engine.execute(f"SELECT nextval('{table}_id_seq');")
    connection.engine.execute(
        f"SELECT setval('{table}_id_seq', (SELECT MAX(id) FROM {table})+1);")


def create_coporation(db: SessionLocal, name: str):
    cor = db.query(Corporation).filter(
        Corporation.corporation_name.like(name)).first()
    if cor:
        return cor
    corporation = Corporation(
        corporation_name=name,
        description="mô tả " + name
    )

    db.add(corporation)
    db.commit()

    return corporation


def create_company(db: SessionLocal, name: str, corporation: Corporation):
    company = db.query(Company).filter(
        Company.company_name.like(name)).first()
    if company:
        company.corporation_id = corporation.id
        db.commit()
        return company

    company = Company(
        company_code=name.upper(),
        company_name=name,
        description="Mô tả " + name,
        corporation_id=corporation.id
    )

    db.add(company)
    db.commit()

    return company


def create_department(db: SessionLocal, name: str, company: Company):
    department = db.query(Department).filter(
        Department.department_name.like(name)).first()
    if department:
        return department
    department = Department(
        department_name=name,
        description="Mô tả " + name,
        company_id=company.id,
    )

    db.add(department)
    db.commit()

    return department


def create_role_title(db: SessionLocal, name: str, department: Department, company: Company):
    role_title = db.query(RoleTitle).filter(
        RoleTitle.role_title_name.like(name)).first()
    if role_title:
        return role_title
    role_title = RoleTitle(
        role_title_name=name,
        description="Mô tả " + name,
        company_id=company.id,
        department_id=department.id
    )

    db.add(role_title)
    db.commit()

    return role_title
