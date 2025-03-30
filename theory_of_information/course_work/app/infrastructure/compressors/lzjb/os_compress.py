#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =====================================================================================
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License, Version 1.0 only
# (the "License").  You may not use this file except in compliance
# with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
# =====================================================================================

# These are the original copyright lines:
# =====================================================================================
# Copyright (c) 1998 by Sun Microsystems, Inc.
# All rights reserved.
# =====================================================================================

# Some changes are based upon the work by Evan Nemerson:
# =====================================================================================
# Copyright (c) 2013-2016, Evan Nemerson (nemequ). All rights reserved.
# =====================================================================================

# Some additional changes, the code documentation and the Python port are my own work:
# =====================================================================================
# Copyright (c) 2020, Stefan65. All rights reserved.
# =====================================================================================

"""
Implementation of the LZJB algorithm as available in `os/compress.c`.

This uses a hash table with 2^8 = 256 entries and returns the original data (plus one
byte to indicate whether the data has been compressed or not) if the compressed data
would be bigger than the source data. In the original version the hash table will be
uninitialized and therefore the results will be non-deterministic, which we cannot
reproduce in Python (as we do not have the C pointer model) and therefore will be using
a regular hash table with all entries initialized to zero.
"""

from lz77_variants.common import utils
from lz77_variants.common.error import BadData


class Configuration:
    """
    The configuration values for executing the algorithm, as they are defined inside
    the original file.
    """

    NBBY = 8
    """
    The number of bits per byte.

    In fact this value has not been defined inside the compression code file directly,
    but by the OpenSolaris system. FreeBSD has the same definition, see
    https://github.com/freebsd/freebsd/blob/ebc1f2ee78a0e997c7b205f69a2eb80c8464bc6f/sys/sys/param.h#L230.

    :type: :class:`int`
    """

    MATCH_BITS = 6
    """
    The number of bits to encode the match length.

    :type: :class:`int`
    """

    MATCH_MIN = 3
    """
    The minimum match length.

    :type: :class:`int`
    """

    MATCH_MAX = (1 << MATCH_BITS) + (MATCH_MIN - 1)
    """
    The maximum match length we can encode.

    The first part is 2^6 = 64 by default, so we can have a value in the range [0, 63].
    But as the minimum match length is 3, we get 3 more bits and therefore [0, 66].

    :type: :class:`int`
    """

    OFFSET_MASK = (1 << (16 - MATCH_BITS)) - 1
    """
    The offset mask - also known as the maximum offset allowed.

    Each match instruction takes 2 bytes = 16 bits, so we have 16 - 6 = 10 bits for the
    offset. We therefore have 2^10 = 1024 possible values in the range [0, 1023].

    :type: :class:`int`
    """

    LEMPEL_SIZE = 256
    """
    The size of the search buffer (hash table/dictionary).

    This corresponds to 2^8. Due to this, there will be 256 hash table entries.

    This value is actually 1/4 as small as for the `zfs.lzjb` version.

    :type: :class:`int`
    """


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
        Compress the given source buffer using the `os.compress` variant of the LZJB
        algorithm.

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

        # The position of the 8-bit bitmap that precedes each 8 items of output and
        # indicates if the N-th bit is a copy item. It precedes the instruction group
        # itself and therefore points to the start of the corresponding group.
        copy_map_position = -1

        # Indicator of the current position inside the mask.
        # This will be 00000010_2 if we are handling the second bit of the output for
        # example.
        # We initialize this to 01000000_2 as the next shift will reset it.
        copy_mask = 1 << (self.configuration.NBBY - 1)

        # The hash table itself.
        # This gets initialized by zero for all entries, unlike in the C implementation.
        # Otherwise it would not work in Python (or we would have to switch to a
        # dictionary-based approach)
        hash_table = [0] * self.configuration.LEMPEL_SIZE

        # Reserve first byte to indicate whether this is compressed or not.
        # The `1` indicates compressed output.
        destination.append(1)
        destination_position += 1

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # Shift the copy mask by one position (move to the next position).
            copy_mask <<= 1

            if copy_mask == (1 << self.configuration.NBBY):
                # If we have reached the last element of the bit mask, save the bit mask
                # and reset it.

                # Special to this version: Just write the source bytes if the length of
                # the output would be greater than the length of the input.
                if (
                    destination_position
                    >= source_length - 1 - 2 * self.configuration.NBBY
                ):
                    # Byte to indicate that this is uncompressed.
                    destination = bytearray()
                    destination.append(0)

                    # Copy all the bytes from the source to the destination buffer.
                    destination += source

                    # Return the destination buffer.
                    return destination

                # Reset the copy mask.
                copy_mask = 1
                # Set the position of the copy map inside the output to the current
                # output position.
                copy_map_position = destination_position

                # Initialize the value at the current position (where the copy map will
                # be) with 0, then move to the next position for being able to save the
                # instructions itself.
                destination.append(0)
                destination_position += 1

            # The current position is less than `MATCH_MAX` bytes from the end of the
            # input, so we are just copying the current byte to the output.
            # This actually seems to be a bit weird, as we might have matches in there
            # as well, but perfectly makes sense if the input is less than `MATCH_MAX`
            # bytes long at all.
            # This will set the current copy map value to 0.
            if source_position > source_length - self.configuration.MATCH_MAX:
                destination.append(source[source_position])
                source_position += 1
                destination_position += 1
                continue

            # Determine the current hash of the first 3 bytes of the current buffer.
            # (This differs from the hashing in `os.compress`).
            hash_value = self._hash(source, source_position)
            # Get the position saved inside the hash table for the current buffer start.
            hash_position = hash_table[hash_value]

            # Determine the offset and ensure that it stays in the desired range.
            # With this and the if condition we do not have to clear our hash table
            # manually when it contains outdated (= not reachable in the sense of too
            # far away) entries.
            offset = (source_position - hash_position) & self.configuration.OFFSET_MASK

            # Save the current position for the current buffer start inside the hash
            # table.
            hash_table[hash_value] = source_position

            # Determine the position at which we have to start copying.
            copy_start_position = source_position - offset

            # Perform the encoding itself.
            # Conditions explained:
            #   1. copy_start_position >= 0 should always be true.
            #   2. If both positions are the same, we did not find a match in the search
            #      buffer and therefore have to use a literal instruction.
            #   3. The match length has to be at least 3.
            if (
                copy_start_position >= 0
                and copy_start_position != source_position
                and utils.compare_first_bytes(
                    source, source_position, copy_start_position, 3
                )
            ):
                # Use a match instruction.

                # Set the current bit inside the copy map to 1 to indicate a match
                # instruction.
                destination[copy_map_position] |= copy_mask

                # Find the current match length inside the given bounds.
                # We start with `MATCH_MIN` as we have already checked above that this
                # applies.
                match_length = self.configuration.MATCH_MIN
                for length in range(
                    self.configuration.MATCH_MIN, self.configuration.MATCH_MAX
                ):
                    if (
                        source[source_position + length]
                        != source[copy_start_position + length]
                    ):
                        break
                    match_length += 1

                # Save the offset and the length of the match using a total of 2 bytes.

                # First byte.
                # `match_length - MATCH_MIN` lets the length value start at zero.
                # `NBBY - MATCH_BITS` moves the length value to the left to let it
                # occupy the first `MATCH_BITS` of the first byte only.
                # `offset >> NBBY` only keeps the first `NBBY - MATCH_BITS` bits from
                # the offset.
                # `|` to combine the values which leads to the match length having
                # `MATCH_BITS` with the first bits of the offset using the remaining
                # bits of this byte.
                match_length_write = match_length - self.configuration.MATCH_MIN
                to_write = match_length_write << (
                    self.configuration.NBBY - self.configuration.MATCH_BITS
                )
                to_write |= offset >> self.configuration.NBBY
                destination.append(to_write)
                destination_position += 1

                # Second byte.
                # Keep only the last byte of the offset.
                destination.append(utils.get_last_bytes(offset, 1))
                destination_position += 1

                # Move the source forward by the match length.
                source_position += match_length
            else:
                # Use a literal instruction.
                # This will keep the current bit inside the copy map at 0 to indicate a
                # literal instruction.

                # Copy the current byte and move the buffers forward.
                destination.append(source[source_position])
                source_position += 1
                destination_position += 1

        # Return the destination buffer.
        return destination

    def _hash(self, buffer, start_position):
        """
        Hash the given buffer, starting at the given position. This will only look at
        the first 3 bytes of the buffer.

        :param buffer: The buffer to work on.
        :type buffer: bytearray

        :param start_position: The position (index) to start at.
        :type start_position: int

        :return: The hash value determined for the first three bytes of the buffer
                 while starting at the given position.
        :rtype: int
        """
        # Get the first 3 bytes from the buffer.
        source = buffer[start_position : start_position + 3]

        # Use some offset value and XOR the bytes.
        hash_value = (source[0] + 13) ^ (source[1] - 13) ^ source[2]

        # AND-ing with `LEMPEL_SIZE - 1` only keeps the last `log2(LEMPEL_SIZE - 1)`
        # bits of the hash and ensures that the hash value is in the correct range.
        # This is a faster(?) version of the modulo operation
        # `hash_value % LEMPEL_SIZE`.
        hash_value = hash_value & (self.configuration.LEMPEL_SIZE - 1)

        # Return the calculated hash value.
        return hash_value


class Decompressor:
    """
    The implementation of the decompressor.
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

    def decompress(self, source):
        """
        Decompress the given buffer compressed using the `os.compres` variant of the
        LZJB algorithm.

        :param source: The source buffer to decompress.
        :type source: bytearray

        :return: The uncompressed data.
        :rtype: bytearray

        :raises BadData: The source buffer content is malformed.
        """
        # The source parameters: the current position inside the source buffer and the
        # overall length of the source buffer.
        source_position = 0
        source_length = len(source)

        # The destination buffer and the current position inside it (which corresponds
        # to the output length).
        destination = bytearray()
        destination_position = 0

        # The 8-bit bitmap that precedes each 8 items of output and indicates if the
        # N-th bit is a copy item.
        copy_map = -1

        # Indicator of the current position inside the mask.
        # This will be 00000010_2 if we are handling the second bit of the output for
        # example.
        # We initialize this to 01000000_2 as the next shift will reset it.
        copy_mask = 1 << (self.configuration.NBBY - 1)

        # Ignore check if destination buffer is smaller than destination buffer as it
        # does not matter in Python.

        # Check whether we have uncompressed data using the indicator byte.
        first_byte = source[0]
        source_position += 1
        if first_byte == 0:
            # This is uncompressed data, so just copy the content of the source buffer.
            # We skip the first byte as this is the indicator.
            destination = source[1:]
            return destination
        elif first_byte != 1:
            # The first byte is neither 0 (=> uncompressed, see above) nor 1
            # (=> compressed), so this is an error for our own block format.
            raise BadData("Indicator byte has unknown value {}.".format(first_byte))

        # Iterate until the end of the input has been reached.
        while source_position < source_length:
            # Shift the copy mask by one position (move to the next position).
            copy_mask <<= 1

            if copy_mask == (1 << self.configuration.NBBY):
                # If we have reached the last element of the bit mask, save the bit mask
                # and reset it.

                # Reset the copy mask.
                copy_mask = 1

                # Get the copy map value and move the next source byte.
                copy_map = source[source_position]
                source_position += 1

            # Perform the decoding itself.
            # `copy_mask` is 0 for all bits except the current bit position.
            # `copy_map` is 1 if the corresponding instruction is a match instruction
            # and 0 otherwise.
            # By AND-ing them, we will check if the current entry of the `copy_map` is
            # 1. If it is 1, we have this match instruction, otherwise a literal
            # instruction.
            if copy_map & copy_mask:
                # This is a match instruction.

                # Retrieve the two bytes indicating the instruction.
                instruction_bytes = source[source_position : source_position + 2]

                # Retrieve the match length.
                # This are the first `MATCH_BITS` bits from the first byte of the source
                # buffer. To get the real length value, we have to add the minimum match
                # length `MATCH_MIN`.
                match_length = instruction_bytes[0] >> (
                    self.configuration.NBBY - self.configuration.MATCH_BITS
                )
                match_length += self.configuration.MATCH_MIN

                # Retrieve the offset value.
                # This are the last `NBBY - MATCH_BITS` from the first byte of the
                # source buffer, concatenated with the second byte of the source buffer.
                # In this case, we are using a slightly different approach: We get the
                # full first byte, move it one byte to make space for another empty byte
                # afterwards and save the second full byte there. By using the offset
                # mask, we only keep the last `OFFSET_MASK` bits of the offset.
                offset = instruction_bytes[0] << self.configuration.NBBY
                offset |= instruction_bytes[1]
                offset &= self.configuration.OFFSET_MASK

                # A match instruction uses 2 bytes, so move 2 bytes forward.
                source_position += 2

                # Determine the position at which we have to start copying.
                copy_position = destination_position - offset

                # Detect invalid inputs.
                if copy_position < 0:
                    raise BadData("Offset {} is too large.".format(offset))

                # Copy the data byte by byte.
                # Please note that we cannot really improve this as we might have
                # overlaps. Therefore we just use the version of the original
                # implementation here.
                for _ in range(match_length):
                    destination.append(destination[copy_position])
                    destination_position += 1
                    copy_position += 1
            else:
                # This is a literal instruction.

                # Copy the current byte and move the buffers forward.
                destination.append(source[source_position])
                destination_position += 1
                source_position += 1

        # Return the destination buffer.
        return destination
