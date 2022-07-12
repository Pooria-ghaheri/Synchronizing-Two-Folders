import shutil
import filecmp
import os


# Synchronization Object
class Dispatch:

    def __init__(self, name=''):
        self.name = name
        self.node_list = []
        self.file_copied_count = 0
        self.folder_copied_count = 0

    def add_node(self, node):
        self.node_list.append(node)

        # Take Nodes and Compare

    def compare_nodes(self):
        nodeListLength = len(self.node_list)

        # Now For each node
        for node in self.node_list:
            # If list has another Item , Compare it
            if self.node_list.index(node) < len(self.node_list) - 1:
                Replica = self.node_list[self.node_list.index(node) + 1]
                print('\nComparing Node ' + str(self.node_list.index(node)) +
                ' and Node ' + str(self.node_list.index(node) + 1) + ':')
                # Passes the two root directories of the nodes
                self._compare_directories(node.root_path, Replica.root_path)

    # Comparing Directories
    def _compare_directories(self, left, right):

        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for d in comparison.common_dirs:
                self._compare_directories(os.path.join(left, d), os.path.join(right, d))
        if comparison.left_only:
            self._copy(comparison.left_only, left, right)
        if comparison.right_only:
            self._copy(comparison.right_only, right, left)
        left_newer = []
        right_newer = []
        if comparison.diff_files:
            for d in comparison.diff_files:
                l_modified = os.stat(os.path.join(left, d)).st_mtime
                r_modified = os.stat(os.path.join(right, d)).st_mtime
                if l_modified > r_modified:
                    left_newer.append(d)
                else:
                    right_newer.append(d)
        self._copy(left_newer, left, right)
        self._copy(right_newer, right, left)

        # Copying files from Original to Replica

    def _copy(self, file_list, src, dest):
        for f in file_list:
            source_path = os.path.join(src, os.path.basename(f))
            if os.path.isdir(source_path):
                shutil.copytree(source_path, os.path.join(dest, os.path.basename(f)))
                self.folder_copied_count = self.folder_copied_count + 1
                print('Copied directory \"' + os.path.basename(source_path) + 
                '\" from \"' + os.path.dirname(source_path) + '\" to \"' + dest + '\"')
            else:
                shutil.copy2(source_path, dest)
                self.file_copied_count = self.file_copied_count + 1
                print('Copied \"' + os.path.basename(source_path) + '\" from \"' + os.path.dirname(
                    source_path) + '\" to \"' + dest + '\"')

    # a node in Synchronization
class Node:

    def __init__(self, path, name=''):
        self.name = name
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)


if __name__ == "__main__":
    my_dispatch = Dispatch('aaron')
    Original = Node('E:\gest2', 'Original')
    Replica = Node('E:\gest2-rep', 'Replica')
    my_dispatch.add_node(Original)
    my_dispatch.add_node(Replica)
    my_dispatch.compare_nodes()
    print('Total files copied ' + str(my_dispatch.file_copied_count))
    print('Total folders copied ' + str(my_dispatch.folder_copied_count))
