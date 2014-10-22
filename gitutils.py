import os
import graph
import pygit2 as git

class BrowsedRepo():
    def __init__(self, path):
        path = os.path.abspath(path)
        self.repo = git.Repository(path)

    def branches(self, all = False):
        return self.repo.listall_branches()

    def walk_branch(self, name):
        walker = self.repo.walk(self.repo.lookup_branch(name)
                .get_object().id)

        for commit in walker:
            yield CommitInfo(commit)

    def build_tree(self):
        rt = RepoTree()

        # For each branch, index all the commits in the branch.
        for branch in self.repo.listall_branches():
            walker = self.repo.walk(
                    self.repo.lookup_branch(branch).get_object().id)

            for commit in walker:
                print(commit.parens)
                for parent in commit.parents:
                    rt.index(parent, commit)

                if len(commits.parens) == 0:
                    rt.index(None, commit)


        return rt

class CommitInfo():
    def __init__(self, commit):
        self.commit = commit
        self.children = []

    def to_node(self):
        return graph.Node(str(self.commit.id), str(self))

    def __str__(self):
        return "%s %s (%s)" % (str(self.commit.id)[:7],
                self.commit.message.split('\n')[0],
                self.commit.author.name)

    def __repr__(self):
        return "'CommitInfo<" + str(self.commit.id) + ">'"


class RepoTree():
    """Record commit heritage in a more easily traversible way, similar
    to singly linked list from root to leaves."""

    def __init__(self):
        self.roots = []
        self.commits = {}

    def index(self, commit, child):
        """Record two raw commit objects."""
        # Check if the commit exists.
        id = str(commit.id)
        new = True
        if id in self.commits:
            commitinfo = self.commits[id]
            new = False
        else:
            commitinfo = CommitInfo(commit)
            self.commits[id] = commitinfo

        if child != None:
            childid = str(child.id)
            # Record the child in the commitinfo.
            commitinfo.children.append(childid)

            # If the child was previously a root, replace it with the
            # parent.
            if childid in self.roots:

                # But only replace it if the commit was newly in the
                # tree. Otherwise, delete the other root.
                if new:
                    print("Replacing root %s with %s" % (childid[:8],
                        id[:8]))
                    self.roots[self.roots.index(childid)] = id
                else:
                    print("Removing non-root %s" % childid[:8])
                    del self.roots[self.roots.index(childid)]

        else:
            # If the child was indeed null, record the parent as a new
            # root.
            print("Recording new root %s" % id[:8])
            self.roots.append(id)
