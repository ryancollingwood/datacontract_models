from pathlib import Path
import ast

from rope.base.project import Project
from rope.base import libutils
from rope.contrib import generate
from rope.contrib import codeassist
from rope.refactor.move import MoveGlobal, create_move
from rope.refactor.importutils import add_import, get_module_imports
from rope.refactor.importutils import ImportTools, importinfo




from ast_selector import AstSelector

from refactoring.ast_node_utils import unparse, dump_node_detail, walk_call_filter, walk_assign_filter
from refactoring.variable_extraction import get_node_start_end

import shutil

def copy_directory(source_dir, destination_dir):
    try:
        # Copy the entire directory and its contents recursively
        shutil.copytree(source_dir, destination_dir)
        print(f"Directory '{source_dir}' successfully copied to '{destination_dir}'.")
    except shutil.Error as e:
        print(f"Error: {e}")
    except OSError as e:
        print(f"Error: {e}")

copy_directory("models/", "output/models/")

PROJECT_BASE = "output"
SOURCE_MODULE = "ecommerce_events"
DESTINATION_PACKAGE = "actors"
DESTINATION_MODULE = "new"
RESOURCE_FILE_PATH = f"{PROJECT_BASE}/{SOURCE_MODULE}.py"
DESTINATION_FILE_PATH = f"{PROJECT_BASE}/{DESTINATION_PACKAGE}/{DESTINATION_MODULE}.py"
REFACTOR_CLASS = "Actor"

def create_or_get_package(project, package_path):
    if not package_path.exists():
        package = generate.create_package(project, DESTINATION_PACKAGE)
    else:
        package = libutils.path_to_resource(project, package_path)
    
    return package

def get_destination_module(project, destination_path, package):
    global DESTINATION_MODULE
    global DESTINATION_FILE_PATH

    if not destination_path.exists():
        destination_module = generate.create_module(project, DESTINATION_MODULE, package)
    else:    
        destination_module = libutils.path_to_resource(
        project, DESTINATION_FILE_PATH
        )
            
    return destination_module

project = Project(PROJECT_BASE)
import_tools = ImportTools(project)

refactor_module = project.get_module(f"{PROJECT_BASE}/{SOURCE_MODULE}")

package_path = Path(f"{PROJECT_BASE}/{DESTINATION_PACKAGE}")
destination_path = package_path / f"{DESTINATION_MODULE}.py"

package = create_or_get_package(project, package_path)

destination_module = get_destination_module(project, destination_path, package)

def move_var_by_class(project, move_class, source_resource, destination_module):
    source_module = libutils.get_string_module(project, source_resource.read())
    tree = source_module.ast_node
    
    variable_declaration = walk_assign_filter(tree, [move_class])
    variable_declaration = variable_declaration[0]

    offset = get_node_start_end(variable_declaration, source_module)
    move_operation = MoveGlobal(project, source_resource, offset[0])
    change = move_operation.get_changes(dest=destination_module)
    project.do(change)

source_imports = get_module_imports(project, refactor_module)
source_import_names = source_imports.imports

source_resource = libutils.path_to_resource(project, f"{PROJECT_BASE}/{SOURCE_MODULE}.py")
move_var_by_class(project, REFACTOR_CLASS, source_resource, destination_module)

exisiting_module = project.get_module("models")
new_module = project.get_module("actors/new")
module_with_imports = import_tools.module_imports(new_module)
# new_import = import_tools.get_from_import(exisiting_module.resource, REFACTOR_CLASS)
# module_with_imports.add_import(new_import)
for source_import in source_import_names:
    module_with_imports.add_import(source_import.import_info)

destination_path.write_text(module_with_imports.get_changed_source())

assert False
# module = .py file
# package = dir with __init__.py

models_resource = project.get_resource("models")
new_import = import_tools.get_from_import(models_resource, "Actor")
new_module = project.get_module("rpg_schema")

destination_module_with_imports = import_tools.module_imports(destination_module)
destination_module_with_imports.add_import(new_import)

assert(False)

module_with_imports = import_tools.module_imports(destination_module)
new_import = import_tools.get_import(self.mod1)
module_with_imports.add_import(new_import)


context = importinfo.ImportContext(project, project.root)
source_imports = get_module_imports(project, source_module)
source_import_names = source_imports.imports

# x = source_import_names[0].import_info.get_imported_names(context)
# x = get_module_imports(project, source_module)

for x in source_import_names:
    add_import(
        project, destination_module, x
    )