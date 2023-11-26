from __future__ import annotations

import dataclasses
import itertools
import typing

import networkx
import pytest


def sort_items(items: list[pytest.Item]):
    root = build_tree(items)
    items.clear()
    items.extend(node.pytest_node for node in root.sorted_children())  # type: ignore


nodes_by_nodeid: dict[str, Node] = {}


def build_tree(items: list[pytest.Item]):
    global nodes_by_nodeid
    for item in items:
        for predecessor in item.listchain():
            if predecessor.nodeid not in nodes_by_nodeid:
                nodes_by_nodeid[predecessor.nodeid] = Node(pytest_node=predecessor)  # type: ignore
            if predecessor.parent:
                nodes_by_nodeid[predecessor.parent.nodeid].children[
                    predecessor.nodeid
                ] = nodes_by_nodeid[predecessor.nodeid]

    return nodes_by_nodeid[""]


NodeType = typing.Literal["module", "class", "item", "session"]


@dataclasses.dataclass
class Node:
    pytest_node: typing.Union[pytest.Module, pytest.Class, pytest.Item, pytest.Session]
    children: dict[str, Node] = dataclasses.field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Node(pytest_node={self.pytest_node})"

    @property
    def node_type(self) -> NodeType:
        if isinstance(self.pytest_node, pytest.Module):
            return "module"
        elif isinstance(self.pytest_node, pytest.Class):
            return "class"
        elif isinstance(self.pytest_node, pytest.Item):
            return "item"
        return "session"

    @property
    def nodeid(self) -> str:
        return self.pytest_node.nodeid

    def dependencies(self):
        dependencies: list[Dependency] = []
        if isinstance(self.pytest_node, pytest.Item):
            for marker in self.pytest_node.iter_markers(name="dependency"):
                dependencies.extend(create_dependencies(marker, self))
        else:
            for child in self.children.values():
                dependencies.extend(child.dependencies())
        return dependencies

    def build_graph(self):
        graph = networkx.DiGraph()
        for child in self.children.values():
            graph.add_node(child.nodeid)
        for child in self.children.values():
            for dependency in child.dependencies():
                dependency_nodeid = dependency.node_id_with_scope(self.node_type)
                if (
                    graph.has_node(dependency_nodeid)
                    and dependency_nodeid != child.nodeid
                ):
                    graph.add_edge(child.nodeid, dependency_nodeid)
        return graph

    def topological_sort(self):
        graph = self.build_graph()
        visited = set()
        sorted = []

        def dfs(nodeid):
            for neighbor in graph.neighbors(nodeid):
                if neighbor not in visited:
                    dfs(neighbor)
            visited.add(nodeid)
            sorted.append(nodeid)

        for nodeid in graph.nodes:
            if nodeid not in visited:
                dfs(nodeid)

        return sorted

    def sorted_children(self) -> list[Node]:
        if not self.children:
            return [self]
        sorted = self.topological_sort()
        return list(
            itertools.chain.from_iterable(
                [self.children[nodeid].sorted_children() for nodeid in sorted]
            )
        )


Scope = typing.Literal["session", "module", "class"]


def create_dependencies(mark: pytest.Mark, node: Node):
    depends_list: list[str] = mark.kwargs.get("depends", [])
    scope: Scope = mark.kwargs.get("scope", "module")
    dependencies: list[Dependency] = []
    for depends in depends_list:
        node_type_by_scope = {
            "session": pytest.Session,
            "module": pytest.Module,
            "class": pytest.Class,
        }
        scope_node = node.pytest_node.session
        for predecessor in node.pytest_node.listchain():
            if isinstance(predecessor, node_type_by_scope[scope]):
                scope_node = predecessor
        depends_node_id = f"{scope_node.nodeid}::{depends}".strip("::")
        node = nodes_by_nodeid[depends_node_id]
        if not node:
            raise ValueError(f"Unknown node id: {depends_node_id}")
        node_type = node.node_type
        dependencies.append(Dependency.from_node_id(depends_node_id, node_type))
    return dependencies


@dataclasses.dataclass
class Dependency:
    nodeid: str
    module_id: str
    class_id: typing.Optional[str]
    item_id: typing.Optional[str]

    def is_in_scope(self, scope_nodeid: str) -> bool:
        return self.nodeid.startswith(scope_nodeid)

    @classmethod
    def from_node_id(cls, nodeid: str, node_type: NodeType) -> Dependency:
        parts = nodeid.split("::")
        if len(parts) == 1:
            if node_type == "module":
                return cls(
                    module_id=parts[0], class_id=None, item_id=None, nodeid=nodeid
                )
        elif len(parts) == 2:
            if node_type == "class":
                return cls(
                    module_id=parts[0], class_id=parts[1], item_id=None, nodeid=nodeid
                )
            elif node_type == "item":
                return cls(
                    module_id=parts[0], class_id=None, item_id=parts[1], nodeid=nodeid
                )
        elif len(parts) == 3:
            if node_type == "item":
                return cls(
                    module_id=parts[0],
                    class_id=parts[1],
                    item_id=parts[2],
                    nodeid=nodeid,
                )
        raise ValueError(f"Invalid node id: {nodeid}")

    def node_id_with_scope(self, scope_node_type: NodeType) -> str:
        if scope_node_type == "session":
            return f"{self.module_id}"
        elif scope_node_type == "module":
            if self.class_id:
                return f"{self.module_id}::{self.class_id}"
            return f"{self.module_id}::{self.item_id}"
        return self.nodeid
