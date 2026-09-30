# Stage 4 Lab - Part E review evidence (reads the code; runs no behaviour tests)
import ast
from pathlib import Path
 
source_path = Path(__file__).with_name("smartcare_v04.py")
source = source_path.read_text(encoding="utf-8")
tree = ast.parse(source)
 
imports = sorted({(n.module if isinstance(n, ast.ImportFrom) else a.name)
                  for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
                  for a in (n.names if isinstance(n, ast.Import) else [None])})
print("Imports:", imports)
print("Standard library only:", set(imports) <= {"__future__", "datetime", "enum", "typing"})
 
classes = {c.name: c for c in ast.walk(tree) if isinstance(c, ast.ClassDef)}
for name in ("Patient", "Practitioner", "Appointment"):
    print(f"{name} base classes:", [ast.unparse(b) for b in classes[name].bases] or "none")
 
for name in ("Patient", "Practitioner", "Appointment"):
    props = {f.name for f in classes[name].body if isinstance(f, ast.FunctionDef)
             and any(ast.unparse(d) == "property" for d in f.decorator_list)}
    setters = [f.name for f in classes[name].body if isinstance(f, ast.FunctionDef)
               and any(ast.unparse(d).endswith(".setter") for d in f.decorator_list)]
    print(f"{name} read-only properties:", sorted(props), "| setters:", setters or "none")