from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication

class TreeWidgetUpdater:
    def __init__(self, tree_widget):
        self.tree_widget = tree_widget

    def update_items(self, parent_item, data):
        for key, value in data.items():
            existing_items = [parent_item.child(i) for i in range(parent_item.childCount()) if parent_item.child(i).text(0) == key]
            if existing_items:
                existing_item = existing_items[0]
                if isinstance(value, dict):
                    self.update_items(existing_item, value)
                elif isinstance(value, list):
                    existing_item.takeChildren()
                    for idx, item in enumerate(value):
                        if isinstance(item, dict):
                            child_item = QTreeWidgetItem(existing_item, [f'[{idx}]'])
                            self.update_items(child_item, item)
                        else:
                            child_item = QTreeWidgetItem(existing_item, [str(item)])
                else:
                    existing_item.setText(1, str(value))
            else:
                new_item = QTreeWidgetItem(parent_item, [str(key)])
                if isinstance(value, dict):
                    self.update_items(new_item, value)
                elif isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, dict):
                            child_item = QTreeWidgetItem(new_item, [f'[{idx}]'])
                            self.update_items(child_item, item)
                        else:
                            child_item = QTreeWidgetItem(new_item, [str(item)])
                else:
                    value_item = QTreeWidgetItem(new_item, [str(value)])

    def update_tree_widget(self, data):
        self.update_items(self.tree_widget.invisibleRootItem(), data)

# Example usage:
app = QApplication([])

# Existing tree widget
tree_widget = QTreeWidget()
tree_widget.setHeaderLabels(['Key', 'Value'])

# Existing data
existing_data = {
    'key1': 'value1',
    'key2': {
        'subkey1': 'subvalue1',
        'subkey2': 'subvalue2'
    }
}

# Populate the tree widget with existing data
tree_updater = TreeWidgetUpdater(tree_widget)
tree_updater.update_items(tree_widget.invisibleRootItem(), existing_data)

# New data to update the tree widget
new_data = {
    'key1': 'updated_value1',
    'key3': 'value3'
}

# Update the tree widget with new data
tree_updater.update_tree_widget(new_data)

tree_widget.show()

app.exec()
