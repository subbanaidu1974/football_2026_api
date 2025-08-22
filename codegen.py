import re, os
from jinja2 import Template

# === Templates ===
model_tpl = Template("""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.db import Base
from app.enums import *

class {{ class_name }}(Base):
    __tablename__ = "{{ table_name }}"

    id = Column(Integer, primary_key=True, index=True)
    {%- for f in fields %}
    {{ f }}
    {%- endfor %}

    {%- for rel in relationships %}
    {{ rel }}
    {%- endfor %}
""")

schema_tpl = Template("""
from pydantic import BaseModel
from typing import Optional
from app.enums import *

class {{ class_name }}Base(BaseModel):
    {%- for f in fields %}
    {{ f }}
    {%- endfor %}

class {{ class_name }}Create({{ class_name }}Base):
    pass

class {{ class_name }}Update({{ class_name }}Base):
    pass

class {{ class_name }}Out({{ class_name }}Base):
    id: int
    class Config:
        orm_mode = True
""")

crud_tpl = Template("""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.{{ module }} import {{ class_name }}
from app.schemas.{{ module }} import {{ class_name }}Create, {{ class_name }}Update

async def get_all(db: AsyncSession):
    result = await db.execute(select({{ class_name }}))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, item_id: int):
    return await db.get({{ class_name }}, item_id)

async def create(db: AsyncSession, obj_in: {{ class_name }}Create):
    db_obj = {{ class_name }}(**obj_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, db_obj: {{ class_name }}, obj_in: {{ class_name }}Update):
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def delete(db: AsyncSession, db_obj: {{ class_name }}):
    await db.delete(db_obj)
    await db.commit()
""")

router_tpl = Template("""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.schemas.{{ module }} import {{ class_name }}Out, {{ class_name }}Create, {{ class_name }}Update
from app.crud import {{ module }} as crud_{{ module }}
from app.models.{{ module }} import {{ class_name }}

router = APIRouter(prefix="/{{ table_name }}", tags=["{{ class_name }}"])

@router.get("/", response_model=list[{{ class_name }}Out])
async def list_items(db: AsyncSession = Depends(get_db)):
    return await crud_{{ module }}.get_all(db)

@router.get("/{item_id}", response_model={{ class_name }}Out)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    obj = await crud_{{ module }}.get_by_id(db, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="{{ class_name }} not found")
    return obj

@router.post("/", response_model={{ class_name }}Out)
async def create_item(item: {{ class_name }}Create, db: AsyncSession = Depends(get_db)):
    return await crud_{{ module }}.create(db, item)

@router.put("/{item_id}", response_model={{ class_name }}Out)
async def update_item(item_id: int, item: {{ class_name }}Update, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_{{ module }}.get_by_id(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="{{ class_name }} not found")
    return await crud_{{ module }}.update(db, db_obj, item)

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_obj = await crud_{{ module }}.get_by_id(db, item_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="{{ class_name }} not found")
    await crud_{{ module }}.delete(db, db_obj)
    return {"ok": True}
""")


enum_tpl = Template("""
import enum

{% for name, values in enums.items() %}
class {{ name }}(str, enum.Enum):
    {% for v in values %}
    {{ v }} = "{{ v }}"
    {% endfor %}

{% endfor %}
""")

# === Read JDL ===
with open("sports_adda_jdl.txt") as f:
    jdl = f.read()

# --- Enums ---
enums = {}
for match in re.findall(r"enum\s+(\w+)\s*\{([^}]*)\}", jdl, re.DOTALL):
    name, body = match
    values = [v.strip() for v in body.split(",") if v.strip()]
    enums[name] = values

print("📦 Enums found:", enums)

os.makedirs("app", exist_ok=True)
with open("app/enums.py", "w") as f:
    f.write(enum_tpl.render(enums=enums))
print("✅ Wrote app/enums.py")

# --- Entities ---
entities = re.findall(r"entity\s+(\w+)\s*\{([^}]*)\}", jdl, re.DOTALL)
print("📦 Entities found:", [e[0] for e in entities])

# --- Relationships ---
rels = re.findall(r"relationship\s+ManyToOne\s*\{([^}]*)\}", jdl, re.DOTALL)
rel_map = []
for r in rels:
    parts = r.split(" to ")
    if len(parts) != 2:
        continue
    left, right = parts[0].strip(), parts[1].strip()
    entity = left.split("{")[0].strip()
    field = left.split("{")[1].split("}")[0].split("(")[0].strip()
    rel_map.append((entity, field, right))

print("📦 Relationships found:", rel_map)

# --- Ensure dirs ---
for d in ["app/models", "app/schemas", "app/crud", "app/routers"]:
    os.makedirs(d, exist_ok=True)

# --- Generate code ---
for name, body in entities:
    fields, schema_fields, relationships = [], [], []

    for line in body.strip().splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        fname, ftype = parts[0], parts[1]

        if ftype == "String":
            fields.append(f"{fname} = Column(String, nullable=True)")
            schema_fields.append(f"{fname}: Optional[str] = None")
        elif ftype == "Integer":
            fields.append(f"{fname} = Column(Integer, nullable=True)")
            schema_fields.append(f"{fname}: Optional[int] = None")
        elif ftype == "Double":
            fields.append(f"{fname} = Column(Float, nullable=True)")
            schema_fields.append(f"{fname}: Optional[float] = None")
        elif ftype == "Boolean":
            fields.append(f"{fname} = Column(Boolean, nullable=True)")
            schema_fields.append(f"{fname}: Optional[bool] = None")
        elif ftype == "Instant":
            fields.append(f"{fname} = Column(DateTime, nullable=True)")
            schema_fields.append(f"{fname}: Optional[str] = None")
        elif ftype in enums:
            fields.append(f"{fname} = Column(Enum({ftype}, name='{ftype.lower()}_enum'), nullable=False)")
            schema_fields.append(f"{fname}: {ftype}")
        else:
            fields.append(f"{fname} = Column(String, nullable=True)")
            schema_fields.append(f"{fname}: Optional[str] = None")

    for ent, field, target in rel_map:
        if ent == name:
            fk_col = f"{field}_id"
            fields.append(f"{fk_col} = Column(Integer, ForeignKey('{target.lower()}s.id'))")
            relationships.append(f"{field} = relationship('{target}')")
            schema_fields.append(f"{fk_col}: Optional[int] = None")

    ctx = {
        "class_name": name,
        "module": name.lower(),
        "table_name": name.lower() + "s",
        "fields": fields,
        "relationships": relationships,
    }

    # write files
    with open(f"app/models/{name.lower()}.py", "w") as f:
        f.write(model_tpl.render(**ctx))
    print("✅ Wrote model:", f"app/models/{name.lower()}.py")

    ctx["fields"] = schema_fields
    with open(f"app/schemas/{name.lower()}.py", "w") as f:
        f.write(schema_tpl.render(**ctx))
    print("✅ Wrote schema:", f"app/schemas/{name.lower()}.py")

    with open(f"app/crud/{name.lower()}.py", "w") as f:
        f.write(crud_tpl.render(**ctx))
    print("✅ Wrote crud:", f"app/crud/{name.lower()}.py")

    with open(f"app/routers/{name.lower()}.py", "w") as f:
        f.write(router_tpl.render(**ctx))
    print("✅ Wrote router:", f"app/routers/{name.lower()}.py")

print("\n🎉 Codegen complete with relationships + enums!")


