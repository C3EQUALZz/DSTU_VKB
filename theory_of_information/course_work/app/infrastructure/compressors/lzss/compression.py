"""
Implementation of the LZSS compression algorithm.
"""

import json

from app.infrastructure.compressors import utils
from app.infrastructure.compressors.lzss.configuration import Configuration


class Compressor:
    """
    The implementation of the compressor.
    """

    configuration = None
    """
    The configuration class to use.

    :type: :class:`class`
    """

    def __init__(self, configuration=Configuration):
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration = configuration

    def compress(self, source):
        """
        Compress the given source buffer using the LZSS algorithm.

        :param source: The source buffer to compress.
        :type source: bytearray

        :return: The compression result.
        :rtype: bytearray
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # Initialize the binary search tree used as the dictionary.
        binary_search_tree = BinarySearchTree(self.configuration)
        binary_search_tree.init_tree()

        # Initialize the buffer for the current code.
        # Each group of 8 bytes forms an output group which gets preceded by a bit mask.
        # We write each group at once, so we are using this code buffer.
        # We need up to 17 bits for it - the first byte is needed for the mask, the
        # remaining 16 bytes are requires for the 8 group items. Each group item can
        # either take 1 or 2 bytes, so we need (in sum) 17 bytes in the "worst case".
        code_buffer = bytearray(17)

        # Reset the first mask/flags.
        # If a bit is `1`, then the corresponding item of the group is an unencoded
        # byte (1 byte). If a bit is `0`, then the corresponding item of the group is
        # a match - which consists of a match position and match length and takes 2
        # bytes.
        code_buffer[0] = 0

        # The current position inside the code buffer. As the mask is at index 0
        # already, we start with `1`.
        code_buffer_position = 1

        # Initialize the mask which encodes the current position to use inside the
        # flags/mask byte of the code buffer/group.
        mask = 1

        # Prepare an empty ring buffer of size `RING_BUFFER_SIZE`, with extra
        # `MATCH_LENGTH_MAX - 1` bytes to facilitate string comparison.
        text_buffer = bytearray(
            self.configuration.RING_BUFFER_SIZE
            + self.configuration.MATCH_LENGTH_MAX
            - 1
        )
        text_buffer_start = 0
        text_buffer_end = (
                self.configuration.RING_BUFFER_SIZE - self.configuration.MATCH_LENGTH_MAX
        )

        # Clear the ring buffer by setting the corresponding entries to a whitespace
        # character. This has to be used in conjunction with the decoding procedure.
        # According to the original author, any character which occurs often is possible
        # here.
        for index in range(text_buffer_start, text_buffer_end):
            text_buffer[index] = ord(" ")

        # Read at most `MATCH_LENGTH_MAX` bytes into the last `MATCH_LENGTH_MAX` bytes
        # of the ring buffer.
        length = 0
        while (
                length < self.configuration.MATCH_LENGTH_MAX
                and source_position < source_length
        ):
            text_buffer[text_buffer_end + length] = source[source_position]
            length += 1
            source_position += 1

        # If the file is empty (length = 0), just return the empty output buffer.
        if length == 0:
            return destination

        # Prepare the binary search tree.
        # Insert the `MATCH_LENGTH_MAX` byte arrays, where each of them is starting
        # with at least one whitespace character.
        # The entries are inserted in reverse order as this should reduce the likelihood
        # of degenerated trees according to the original author.
        for i in range(1, self.configuration.MATCH_LENGTH_MAX + 1):
            binary_search_tree.insert_node(text_buffer, text_buffer_end - i)
        # Insert the whole ring buffer and set the match data.
        match_position, match_length = binary_search_tree.insert_node(
            text_buffer, text_buffer_end
        )

        # Handle the complete input.
        # This slightly differs from the original implementation, as we are using a
        # `while do` loop instead of a `do ... while` loop. This should not be a real
        # problem for regular runs, and as we are stopping if `length == 0` above, so
        # this will always run at least once.
        while length > 0:
            # Make sure that the match length does not exceed the actual input length.
            # According to the original author the match length might be spuriously long
            # near the end of the input.
            match_length = min(match_length, length)

            # Encode the current instruction.
            if match_length <= self.configuration.MATCH_LENGTH_MIN_THRESHOLD:
                # This is a literal instruction.

                # We just send 1 byte holding the current byte, so the match length is
                # 1.
                match_length = 1

                # Set the current flag to 1 to indicate the literal instruction.
                code_buffer[0] |= mask

                # Add the current byte to the output and move to the next output
                # position.
                code_buffer[code_buffer_position] = text_buffer[text_buffer_end]
                code_buffer_position += 1
            else:
                # This is a match instruction.

                # Write the first byte.
                # Send the least significant byte of the match position and move to the
                # next output position.
                # The match position corresponds to the position of the match inside the
                # ring buffer.
                code_buffer[code_buffer_position] = utils.get_last_bytes(
                    match_position, 1
                )
                code_buffer_position += 1

                # Write the second byte.
                # The first part will be the 4 most significant bits of the match
                # position (0xF0 = 11110000_2).
                # The second part will be the match length using 4 bits. We can subtract
                # the threshold from this value as we know that a match needs at least
                # this number of bytes. The additional 1 can be subtracted as a match
                # length of 0 is not possible anyway. With this we can encode a length
                # value of up to 18 using only 4 bits (range [0...15] with
                # 15 = 2^4 - 1).
                # After writing this second byte, move to the next output position.
                to_write = (match_position >> 4) & 0xF0
                to_write |= match_length - (
                        self.configuration.MATCH_LENGTH_MIN_THRESHOLD + 1
                )
                code_buffer[code_buffer_position] = to_write
                code_buffer_position += 1

            # Move to the next group item by moving the mask left by 1 bit.
            mask <<= 1

            # This comparison is slightly different to the original version to avoid
            # always having to cut the leading bits of the `mask` value to only keep the
            # last 8 bits.
            # In fact we are checking the same condition, but in another manner, as
            # (1 << 8) = 2^8 = 256 = 100000000_2.
            if mask == (1 << 8):
                # We have encoded the 8th entry of the current group beforehand.

                # Write the buffered content to the output.
                destination += code_buffer[:code_buffer_position]

                # We have just increased the output size.
                destination_position += code_buffer_position

                # Reset the buffer and mask values as we have to start the next group.
                code_buffer[0] = 0
                code_buffer_position = 1
                mask = 1

            # Save the length of the last match.
            # This is required as the following lines will update the original value.
            last_match_length = match_length

            # Update the tree with the recently compressed data.
            i = 0
            while i < last_match_length and source_position < source_length:
                # Delete the old bytes.
                binary_search_tree.delete_node(text_buffer_start)

                # Read the new byte.
                current_byte = source[source_position]
                source_position += 1
                text_buffer[text_buffer_start] = current_byte

                # If the position is near the end of the buffer, extend the buffer to
                # make comparison easier.
                # The comparison has to be seen in the terms of a ring buffer in this
                # case, as we check whether the start position is before the maximum
                # match length.
                if text_buffer_start < self.configuration.MATCH_LENGTH_MAX - 1:
                    text_buffer[
                        text_buffer_start + self.configuration.RING_BUFFER_SIZE
                        ] = current_byte

                # Move to the next start and end position.
                # As this is a ring buffer, we increment the position modulo N.
                # N - 1 = 4096 - 1 = 4095 is used as 12 bits can represent the range
                # [0...4095] only.
                text_buffer_start = (text_buffer_start + 1) & (
                        self.configuration.RING_BUFFER_SIZE - 1
                )
                text_buffer_end = (text_buffer_end + 1) & (
                        self.configuration.RING_BUFFER_SIZE - 1
                )

                # Add the new entry to the tree.
                match_position, match_length = binary_search_tree.insert_node(
                    text_buffer, text_buffer_end
                )

                # Increment the counter.
                i += 1

            # We might have some data to remove after the end of the text.
            while i < last_match_length:
                # Remove the current node.
                binary_search_tree.delete_node(text_buffer_start)

                # Move to the next start and end position.
                # As this is a ring buffer, we increment the position modulo N.
                # N - 1 = 4096 - 1 = 4095 is used as 12 bits can represent the range
                # [0...4095] only.
                text_buffer_start = (text_buffer_start + 1) & (
                        self.configuration.RING_BUFFER_SIZE - 1
                )
                text_buffer_end = (text_buffer_end + 1) & (
                        self.configuration.RING_BUFFER_SIZE - 1
                )

                # If the input buffer is not empty, add the new entry to the tree.
                if length:
                    match_position, match_length = binary_search_tree.insert_node(
                        text_buffer, text_buffer_end
                    )

                # We have consumed another byte.
                length -= 1

                # Move to the next position.
                i += 1

        # If there is some remaining data to send.
        if code_buffer_position > 1:
            # Write the buffered content to the output.
            destination += code_buffer[:code_buffer_position]

            # Increase the output size.
            destination_position += code_buffer_position

        # Return the destination buffer.
        binary_search_tree.dump_tree(text_buffer)
        return destination


class BinarySearchTree:
    """
    The binary search tree implementation for the compressor.
    """

    configuration = None
    """
    The configuration class to use.

    :type: :class:`class`
    """

    def __init__(self, configuration=Configuration):
        """
        :param configuration: The configuration class to use.
        :type configuration: class
        """
        self.configuration = configuration

        # Initialize the lists used for the tree.
        # For i = 0 to `TREE_ROOT_INDEX - 1`, `_left_children[i]` and
        # `_right_children[i]` will be the left and right children of node `i`.
        # `_parents[i]` is the parent of node `i`.
        # For i = 0 to 255, `_right_children[TREE_ROOT_INDEX + i + 1]` is the root of
        # the tree for strings that begin with the character `i`.
        self._left_children = [0] * (configuration.RING_BUFFER_SIZE + 1)
        self._right_children = [0] * (configuration.RING_BUFFER_SIZE + 257)
        self._parents = [0] * (configuration.RING_BUFFER_SIZE + 1)

        # Save the `NIL` value as we have to use it quite often. `NIL` stands for
        # "not used".
        self._NIL = self.configuration.TREE_ROOT_INDEX

    def init_tree(self):
        """
        Initialize the tree.

        For i = 0 to `TREE_ROOT_INDEX - 1`, `_right_children[i]` and
        `_left_children[i]` will be the right and left children of node `i`. These
        nodes need not be initialized.
        Also, `_parents[i]` is the parent of node `i`. These are initialized to NIL
        (= `TREE_ROOT_INDEX`), which stands for "not used".
        For i = 0 to 255, `_right_children[TREE_ROOT_INDEX + i + 1]` is the root of
        the tree for strings that begin with character `i`. These are initialized to
        NIL. Note there are 256 trees.

        .. note::
           Although this initializes the tree values itself, the :func:`__init__` method
           has to be called nevertheless as it creates the corresponding lists.
        """

        # Initialize the roots of the trees.
        iteration_start = self.configuration.RING_BUFFER_SIZE + 1
        iteration_end = iteration_start + 256
        for i in range(iteration_start, iteration_end):
            self._right_children[i] = self._NIL

        # Initialize the parents.
        for i in range(self.configuration.RING_BUFFER_SIZE + 1):
            self._parents[i] = self._NIL

    def insert_node(self, text_buffer, buffer_position):
        """
        Insert a string of length `MATCH_LENGTH_MAX` - namely
        :code:`text_buffer[buffer_position : buffer_position + MATCH_LENGTH_MAX - 1]` -
        into one of the trees (:code:`text_buffer[buffer_position]`'th tree) and return
        the position and length of the longest match. If the match length equals the
        maximum match length, the old node gets removed in favor of the new one, as the
        old one will be deleted sooner.

        :param text_buffer: The ring buffer to retrieve the text from.
        :type text_buffer: bytearray

        :param buffer_position: The index to start at inside the ring buffer.
        :type buffer_position: int

        :return: The position and length of the longest match.
        :rtype: tuple[int, int]
        """
        # Comparison value for the match indicating the direction of inequality with the
        # current characters.
        # At the start this will always be 1, so we will always start looking at the
        # right branch.
        comparator = 1

        # The text starting at the current position.
        key = text_buffer[buffer_position:]

        # The current position inside the buffer, based upon the first character of the
        # current text.
        p = self.configuration.RING_BUFFER_SIZE + 1 + key[0]

        # Assign a shorter name for the start position inside the ring buffer.
        r = buffer_position

        # Clear the children of the current node.
        self._right_children[r] = self._NIL
        self._left_children[r] = self._NIL

        # Reset the match data.
        match_position = 0
        match_length = 0

        # TODO: Somewhere down here we create loops inside the tree :(
        #       With this, deletion iterates forever, while for some inputs the
        #       insertion loop runs forever as well ...
        #       Currently this infinite iterations are blocked with a counter, but this
        #       is no real solution. Strange enough this problem only seems to show up
        #       for files greater than 4177 bytes for now (which is a little bit more
        #       than the ring buffer size).
        #       The problem seems to arise at different positions for different files.
        #       While the `test.txt` file raises an error within the deletion handling,
        #       `fireworks.jpeg` raises an error within the insertion handling.

        # TODO: Remove the counter if the bug is fixed.
        counter = 0

        # Search the correct node.
        while True:
            # TODO: There seems to be some bug (inside the insertion logic?)
            #       which adds a loop into the tree.
            counter += 1
            if counter >= 1000:
                # Print the last 20 entries to see the loop inside the tree.
                print("Current p is {}.".format(p))
                if counter >= 1020:
                    raise ValueError(
                        "We are probably stuck inside an infinite loop. "
                        + "Current p is {}.".format(p)
                    )

            # Perform the lookup.
            # `comparator` will be 0 for a match, positive if the current byte of the
            # key is greater than the current byte inside the ring buffer and negative
            # if the current byte of the key is less than the current byte inside the
            # ring buffer.
            # At the start this will be 1, so we will always start with looking at the
            # right branch.
            if comparator >= 0:
                # We have to search inside the right branch as the current byte of the
                # key is greater than the current byte of the ring buffer.

                if self._right_children[p] != self._NIL:
                    # We have a right child for the current node, so move to it.
                    p = self._right_children[p]
                else:
                    # We do not have a right child for the current node.

                    # Save the node `r` and set its parent to the current node.
                    self._right_children[p] = r
                    self._parents[r] = p

                    # We have a match in this case.
                    return match_position, match_length
            else:
                # We have to search inside the left branch as the current byte of the
                # key is less than the current byte of the ring buffer.

                if self._left_children[p] != self._NIL:
                    # We have a left child for the current node, so move to it.
                    p = self._left_children[p]
                else:
                    # We do not have a left child for the current node.

                    # Save the node `r` and set its parent to the current node.
                    self._left_children[p] = r
                    self._parents[r] = p

                    # We have a match in this case.
                    return match_position, match_length

            # Check for matches until we have reached the maximum match length.
            length_check = 1
            for i in range(1, self.configuration.MATCH_LENGTH_MAX + 1):
                # Assign the value of `comparator` using the i-th byte of the current
                # key text and the (p + i)-th byte of the ring buffer.
                # This will actually perform the length matching for us, because
                # `comparator` will be 0 if both characters match => increase the match
                # length by 1. If this is not 0, we have a mis-match and have to output
                # the current data.
                comparator = key[i] - text_buffer[p + i]
                if comparator != 0:
                    length_check = i
                    break

            # Check if we can update the match length.
            # `length_check` is the new match length after the previous loop.
            if length_check > match_length:
                # The match starts at the current ring buffer position.
                match_position = p

                # Update the match length.
                match_length = length_check

                # If we have reached the maximum match length, we can stop.
                if match_length >= self.configuration.MATCH_LENGTH_MAX:
                    break

        # If we did not exit early, the node `r` needs to be added to the tree.
        # This should only be reachable if the node can be updated because of a better
        # match length.
        self._parents[r] = self._parents[p]
        self._left_children[r] = self._left_children[p]
        self._right_children[r] = self._right_children[p]

        self._parents[self._left_children[p]] = r
        self._parents[self._right_children[p]] = r

        if self._right_children[self._parents[p]] == p:
            self._right_children[self._parents[p]] = r
        else:
            self._left_children[self._parents[p]] = r

        # Remove `p`.
        self._parents[p] = self._NIL

        # Do not forget to return the match parameters.
        return match_position, match_length

    def delete_node(self, p):
        """
        Delete the given node from the tree.

        :param p: The index of the node to delete.
        :type p: int
        """
        # Abort if the node is not part of the tree.
        if self._parents[p] == self._NIL:
            return

        if self._right_children[p] == self._NIL:
            # If there is a right child, save the left child.
            q = self._left_children[p]
        elif self._left_children[p] == self._NIL:
            # If there is a left child, save the right child.
            q = self._right_children[p]
        else:
            # This nodes has multiple children.

            # Get the left child.
            q = self._left_children[p]
            if self._right_children[q] != self._NIL:
                # The left child has a right child.

                # Get the parent of the node with the largest value.
                # If we would iterate until `q` is `NIL`, we would get the node with the
                # largest value.
                # TODO: Remove the counter if the bug is fixed.
                counter = 0
                while True:
                    # TODO: There seems to be some bug (inside the insertion logic?)
                    #       which adds a loop into the tree.
                    counter += 1
                    if counter >= 1000:
                        # Print the last 20 entries to see the loop inside the tree.
                        print("Current q is {}.".format(q))
                        if counter >= 1020:
                            raise ValueError(
                                "We are probably stuck inside an infinite loop. "
                                + "Current q is {}.".format(q)
                            )
                    q = self._right_children[q]
                    if self._right_children[q] == self._NIL:
                        break

                # The right child of the node to be deleted will be replaced by the
                # left relative of the node with the largest value.
                self._right_children[self._parents[q]] = self._left_children[q]
                self._parents[self._left_children[q]] = self._parents[q]

                # The relative of the node with the largest value will be the left child
                # of the node to delete.
                self._left_children[q] = self._left_children[p]
                self._parents[self._left_children[p]] = q

            # The right child of `q` will be the right child of the node to delete.
            # `_right_children[q]` is the largest value if `_right_children[q]` exists,
            # otherwise it will be the right child of the left child of the node to
            # delete.
            self._right_children[q] = self._right_children[p]
            self._parents[self._right_children[p]] = p

        # Set the new parent.
        self._parents[q] = self._parents[p]

        if self._right_children[self._parents[p]] == p:
            self._right_children[self._parents[p]] = q
        else:
            self._left_children[self._parents[p]] = q

        # Remove the parent of the node to delete.
        self._parents[p] = self._NIL

    def _get_current_text_buffer_part(self, text_buffer, start_index):
        """
        Get the current part of the text buffer. This will retrieve the first
        `MATCH_LENGTH_MAX` bytes from the text buffer in hexadecimal format, starting
        at the given index.

        :param text_buffer: The text buffer to read from.
        :type text_buffer: bytearray

        :param start_index: The index to start at inside the the text buffer.
        :type start_index: int

        :return: The requested bytes from the text buffer, as a string of whitespace
                 separated hexadecimal values.
        :rtype: str
        """
        index = start_index
        output = []
        for _ in range(0, self.configuration.MATCH_LENGTH_MAX):
            output.append(text_buffer[index])
            index += 1
            index &= self.configuration.RING_BUFFER_SIZE - 1
        output = ["0x{:02X}".format(x) for x in output]
        return " ".join(output)

    def dump_tree(self, text_buffer, filename="dump.tree"):
        """
        Dump the given tree in JSON format.

        :param text_buffer: The content of the text buffer which is referenced from the
                            tree nodes.
        :type text_buffer: bytearray

        :param filename: The file to write the dump to.
        :type filename: str
        """
        # Retrieve the regular tree nodes.
        tree_nodes = []
        for i in range(self.configuration.RING_BUFFER_SIZE + 1):
            parent = None if self._parents[i] == self._NIL else self._parents[i]
            left = (
                None if self._left_children[i] == self._NIL else self._left_children[i]
            )
            right = (
                None
                if self._right_children[i] == self._NIL
                else self._right_children[i]
            )
            node = {
                "index": i,
                "parent": parent,
                "left": left,
                "right": right,
                "value": self._get_current_text_buffer_part(text_buffer, i),
            }
            tree_nodes.append(node)

        # Retrieve the root nodes.
        root_nodes = []
        iteration_start = self.configuration.RING_BUFFER_SIZE + 1
        iteration_end = iteration_start + 256
        for i in range(iteration_start, iteration_end):
            node = {"index": i, "character": i - iteration_start}
            root_nodes.append(node)

        # Put everything into a dictionary.
        container = {
            "tree_nodes": tree_nodes,
            "root_nodes": root_nodes,
        }

        # Write to the given file using JSON.
        with open(filename, mode="w", encoding="utf8") as outfile:
            json.dump(container, outfile, indent=4)
