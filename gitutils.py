import os
import time
import graph
import pygit2 as git

class BrowsedRepo():
    def __init__(self, path):
        path = os.path.abspath(path)
        self.repo = git.Repository(path)
        self.tree = None

    def branches(self, all = False):
        return self.repo.listall_branches()

    def walk_branch(self, name):
        walker = self.repo.walk(self.repo.lookup_branch(name)
                .get_object().id)

        for commit in walker:
            yield CommitInfo(commit)

    def branch_contains(self, branch, commitid):
        # Get the commit ID only.
        if type(commitid) != str:
            commitid = str(commitid.id)

        walker = self.repo.walk(self.repo.lookup_branch(branch)
                .get_object().id)

        # Compare each commit in the tree, starting from the tip of the
        # branch.
        for commit in walker:
            if commitid == str(commit.id):
                return True

        # If nothing matched, return False.
        return False

    def build_tree(self):
        self.tree = RepoTree()

        # For each branch, index all the commits in the branch.
        for branch in self.repo.listall_branches():
            walker = self.repo.walk(
                    self.repo.lookup_branch(branch).get_object().id)

            # We will walk from the top of the branch (the latest
            # commit) back to the root. So each commit we index will
            # have children to have come before it, except the first
            # one.

            for commit in walker:
                self.tree.index(commit, commit.parents)

        return self.tree

    def balance_tree_on(self, branch):
        print("Balancing tree")
        self.tree.balance_on(self.branch_contains, *self.branches())

class CommitInfo():
    def __init__(self, commit):
        self.commit = commit
        self.id = str(commit.id)
        self.sid = self.id[:7]
        self.children = []

    def to_node(self):
        return graph.Node(self.id,
                str(self),
                x = self.center_shift,
                y = self.time_in_the_past(),
                *self.children
                )

    def time_in_the_past(self):
        unixauthor = self.commit.author.time
        unixnow = int(time.time())
        return (unixnow - unixauthor)/3600

    def __str__(self):
        return "%s %s (%s)" % (self.sid,
                self.commit.message.split('\n')[0],
                self.commit.author.name)

    def __repr__(self):
        return "'CommitInfo<" + str(self.commit.id) + ">'"


class RepoTree():
    """Record commit heritage in a more easily traversible way, similar
    to singly linked list from root to leaves."""

    class MissingCommitError(Exception): pass

    def __init__(self):
        self.roots = []
        self.commits = {}

    def index(self, commit, parents):
        """Record two raw or info-wrapped commit objects."""
        # Check if the commit was given.
        if commit == None:
            raise MissingCommitError("Commit not given")

        # Typeconvert real quick
        if type(commit) != CommitInfo:
            commit = CommitInfo(commit)

        # Check if the commit is in the database already. If so, skip
        # re-indexing it.
        if commit.id in self.commits:
            return

        # Record the commit in the tree.
        self.commits[commit.id] = commit

        # Perform a similar type conversion for each of the parents,
        # looking each of them up first. In each one, record the child
        # commit.
        for index, parent in enumerate(parents):
            if parent.id in self.commits:
                parents[index] = self.commits[parent.id]
            else:
                # Typeconvert real quick, if necessary.
                if type(parent) != CommitInfo:
                    parent = CommitInfo(parent)
                    parents[index] = parent

            print("Recording %s as a child of %s" % (commit.sid,
                    parent.sid))
            parents[index].children.append(commit.id)


        # If there are no parents, then the commit is a root.
        if len(parents) == 0:
            print("Recording new root %s" % commit.sid)
            self.roots.append(commit.id)
            return

    def balance_on(self, membership_function, *center_priorities):
        # For every commit,
        for commit in self.commits.values():
            # First, unset x.
            commit.center_shift = None

            # Try to match it to the centermost category. For example,
            # by branch - commits in 'master' will be centered, others
            # will be offset.
            for index, center_val in enumerate(center_priorities):
                # If it matches, set its center_shift to its category's
                # position in the list.
                if membership_function(center_val, commit):
                    commit.center_shift = index
                    continue


            # If there are no matches, move it all the way out.
            commit.center_shift = len(center_priorities)
            self.commits[commit.id] = commit

    def to_graph(self):
        g = graph.Graph()
        for commit in self.commits.values():
            g.add(commit.to_node())

        return g
