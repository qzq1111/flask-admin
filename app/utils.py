import hashlib


def get_md5(string):
    """获取md5码"""
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


class BuildMenuTree(object):

    def __init__(self, menus):
        self.menus = menus

    @staticmethod
    def __generate_node(menu) -> dict:

        node = {
            "id": menu.menu_id,
            "name": menu.menu_name,
            "path": menu.path,
            "component": menu.component,
            "hidden": menu.visible == 0,
            "meta": {
                "icon": menu.icon,
                "title": menu.menu_title,
            },
            "children": [],
        }
        return node

    def sidebar_tree(self):
        """生成侧边栏"""
        data = list()
        for menu in self.menus:
            if menu.parent_id != 0 or menu.status == 0:
                continue
            node = self.__generate_node(menu)
            node["alwaysShow"] = True
            node["redirect"] = "noRedirect"
            menus = self.__build_sidebar_tree(node)
            data.append(menus)
        return data

    def __build_sidebar_tree(self, child):
        data = list()

        for menu in self.menus:
            if menu.parent_id != child["id"] or menu.status == 0:
                continue
            node = self.__generate_node(menu)
            if menu.menu_type != "F":
                child_menu = self.__build_sidebar_tree(node)
                data.append(child_menu)
        child["children"] = data
        return child

    def label_tree(self) -> list:
        """生成label树"""
        data = list()

        for menu in self.menus:
            if menu.parent_id != 0 or menu.status == 0:
                continue
            node = dict(id=menu.menu_id, label=menu.menu_title, children=[])
            menus = self.__build_label_tree(node)
            data.append(menus)
        return data

    def __build_label_tree(self, child: dict) -> dict:
        data = list()

        for menu in self.menus:
            if menu.parent_id != child["id"] or menu.status == 0:
                continue
            node = dict(id=menu.menu_id, label=menu.menu_title, children=[])
            child_menu = self.__build_label_tree(node)
            data.append(child_menu)
        child["children"] = data
        return child
