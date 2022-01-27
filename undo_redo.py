from game_objects import Box
from gamefield import get_object_in_set, find_player


class UndoRedo:
    def __init__(self):
        self._history = [((), ())]  # A default setting of empty gamefield
        self._history_position = 0  # The position that is used for UNDO/REDO

    @property
    def history(self):
        """Return all records in the History list"""
        return self._history

    def undo(self):
        """Undo a command if there is a command that can be undone.
        Update the history psoition so that further UNDOs or REDOs
        point to the correct index"""
        if self._history_position > 0:
            self._history_position -= 1
            self._steps[
                self._history[self._history_position][1]
            ].execute(self._history[self._history_position][2])
        else:
            print("nothing to undo")

    def add_to_history(self, cells):
        boxes = []
        for cell in cells:
            box = get_object_in_set(Box, cells.get(cell))
            if box:
                boxes.append((box.row, box.column))
        player = find_player(cells)
        # TODO: чистим конец истории
        self._history.append(((player.row, player.column), boxes))
        self._history_position += 1

    def clear_history(self):
        self._history = [((), ())]
        self._history_position = 0

    def show_history(self):
        for step in self._history:
            print(step)
